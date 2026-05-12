#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import base64
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

import requests

ASPECT_TO_SIZE = {
    "16:9": "1536x1024",
    "9:16": "1024x1536",
    "1:1": "1024x1024",
}

REQUEST_TIMEOUT_SECS = 600
MAX_RETRIES = 3
RETRY_DELAY_SECS = 5
MAX_ASPECT_RETRIES = 2
ASPECT_TOLERANCE = 0.15


def parse_size_ratio(size: str) -> float | None:
    try:
        width_text, height_text = size.split("x", 1)
        width = int(width_text)
        height = int(height_text)
    except (AttributeError, TypeError, ValueError):
        return None
    if width <= 0 or height <= 0:
        return None
    return width / height


def read_png_dimensions(path: str) -> tuple[int, int]:
    import struct

    try:
        with open(path, "rb") as file:
            head = file.read(24)
        if head[:8] != b"\x89PNG\r\n\x1a\n":
            return 0, 0
        width, height = struct.unpack(">II", head[16:24])
        return width, height
    except Exception:
        return 0, 0


def aspect_acceptable(width: int, height: int, expected_ratio: float | None, tolerance: float = ASPECT_TOLERANCE) -> bool:
    if not (width and height):
        return True
    if expected_ratio is None:
        return True
    actual = width / height
    deviation = abs(actual - expected_ratio) / expected_ratio
    return deviation <= tolerance


class GptImage2Generator:
    def __init__(self, aspect_ratio: str = "1:1") -> None:
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com").rstrip("/")
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model_name = os.getenv("GPT_IMAGE_MODEL_NAME", "gpt-image-2")
        self.quality = os.getenv("GPT_IMAGE_QUALITY", "high")
        self.endpoint = os.getenv("GPT_IMAGE_ENDPOINT", "auto").lower()

        if not self.api_key:
            raise ValueError("缺少 OPENAI_API_KEY，请在 .env 中配置")

        self.aspect_ratio = aspect_ratio
        self.default_size = ASPECT_TO_SIZE.get(aspect_ratio, "1024x1024")
        self.last_background_mode = "default"

        print(
            f"[init] 初始化 gpt-image-2 生成器 "
            f"(model={self.model_name}, size={self.default_size}, "
            f"quality={self.quality}, endpoint={self.endpoint})"
        )

    def _save_b64(self, b64: str, output_path: str) -> None:
        if "," in b64 and b64.startswith("data:"):
            b64 = b64.split(",", 1)[1]
        with open(output_path, "wb") as file:
            file.write(base64.b64decode(b64))

    def _download_url(self, url: str, output_path: str) -> None:
        from urllib.parse import urlparse

        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"拒绝下载非 http(s) 协议的 URL: {parsed.scheme}")
        print(f"[download] 下载图片 host={parsed.netloc} path={parsed.path[:80]}")
        response = requests.get(url, stream=True, timeout=REQUEST_TIMEOUT_SECS)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "")
        if content_type and not content_type.startswith("image/"):
            print(f"(!) 非 image Content-Type: {content_type}（仍尝试写盘，请人工核对）")
        max_bytes = 50 * 1024 * 1024
        written = 0
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                written += len(chunk)
                if written > max_bytes:
                    file.close()
                    os.remove(output_path)
                    raise ValueError(f"下载超过 {max_bytes} 字节上限，已丢弃 {url[:80]}")
                file.write(chunk)

    def _save_payload(self, payload: str, output_path: str) -> None:
        if payload.startswith("data:image/") or (len(payload) > 200 and "/" not in payload[:200]):
            self._save_b64(payload, output_path)
        elif payload.startswith("http"):
            self._download_url(payload, output_path)
        else:
            self._save_b64(payload, output_path)

    def _extract_from_text(self, text: str) -> Optional[str]:
        match = re.search(r"data:image/[\w]+;base64,[A-Za-z0-9+/=]+", text)
        if match:
            return match.group(0)
        match = re.search(r"!\[.*?\]\((https?://[^\)\s]+)\)", text)
        if match:
            return match.group(1)
        match = re.search(r"(https?://[^\s\)]+\.(?:png|jpg|jpeg|webp|gif))", text, re.IGNORECASE)
        if match:
            return match.group(1)
        match = re.search(r"(https?://[^\s\)]+)", text)
        if match:
            return match.group(1)
        return None

    def _request_via_chat(self, prompt: str, size: str, reference_image_path: Optional[str] = None) -> str:
        url = f"{self.base_url}/v1/chat/completions"

        if self.aspect_ratio == "9:16":
            aspect_hint = (
                "\n\n【画面比例——强制】严格按 9:16 竖版生成 "
                "(portrait, vertical 9:16, height much taller than width)。"
                "绝对不要方图。"
            )
        elif self.aspect_ratio == "1:1":
            aspect_hint = "\n\n【画面比例——强制】1:1 方图。"
        else:
            aspect_hint = (
                "\n\n【画面比例——强制】生成图片必须是 16:9 横版宽屏 "
                "(landscape orientation, widescreen 16:9 aspect ratio). "
                "宽度必须明显大于高度。绝对不要生成方图或竖图。"
            )

        full_prompt = f"{prompt}{aspect_hint}"
        if reference_image_path and os.path.exists(reference_image_path):
            with open(reference_image_path, "rb") as file:
                ref_b64 = base64.b64encode(file.read()).decode("ascii")
            ref_data_url = f"data:image/png;base64,{ref_b64}"
            user_content: Any = [
                {"type": "image_url", "image_url": {"url": ref_data_url}},
                {
                    "type": "text",
                    "text": (
                        "请以上面这张图作为视觉风格参考（配色、材质、氛围、构图），"
                        "按下方要求生成一张全新的图片，不要复制原图文字或细节。\n\n"
                        + full_prompt
                    ),
                },
            ]
        else:
            user_content = full_prompt

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": user_content}],
            "stream": True,
            "temperature": 0.7,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        }

        print(f"[request] POST {url} size={size} stream=True")
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            stream=True,
            timeout=REQUEST_TIMEOUT_SECS,
        )
        print(f"[download] status={response.status_code}")
        if response.status_code != 200:
            raise RuntimeError(f"chat 调用失败 (status={response.status_code}): {response.text[:500]}")

        full_text: list[str] = []
        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data:"):
                continue
            data_str = line[5:].strip()
            if data_str == "[DONE]":
                break
            try:
                import json as json_module

                chunk = json_module.loads(data_str)
            except Exception:
                continue
            choices = chunk.get("choices") or []
            if not choices:
                continue
            delta = choices[0].get("delta") or {}
            content = delta.get("content")
            if content:
                full_text.append(content)
                snippet = content.replace("\n", " ").strip()
                if snippet:
                    print(f"  -> {snippet[:80]}")

        merged = "".join(full_text)
        found = self._extract_from_text(merged)
        if not found:
            raise RuntimeError(f"流式响应里没找到图片 URL/base64。完整文本：{merged[:500]}")
        return found

    def _request_via_images(self, prompt: str, size: str, background_mode_hint: str) -> str:
        url = f"{self.base_url}/v1/images/generations"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "n": 1,
            "size": size,
            "quality": self.quality,
        }
        background_mode = background_mode_hint
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        print(f"[request] POST {url} size={size} quality={self.quality} background_mode={background_mode}")
        response = requests.post(url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT_SECS)
        print(f"[download] status={response.status_code}")

        if response.status_code != 200:
            raise RuntimeError(f"images 调用失败 (status={response.status_code}): {response.text[:500]}")

        self.last_background_mode = background_mode
        result = response.json()
        data = result.get("data") or []
        if not data:
            raise RuntimeError(f"响应没有 data: {str(result)[:300]}")
        first = data[0]
        b64 = first.get("b64_json")
        url_field = first.get("url")
        if b64:
            return f"data:image/png;base64,{b64}"
        if url_field:
            return url_field
        raise RuntimeError(f"data[0] 既没 b64_json 也没 url: {str(first)[:300]}")

    def generate_scene_image(
        self,
        scene_data: Dict[str, Any],
        output_path: str,
        request_size: str | None = None,
        design_size: str | None = None,
        reference_image_path: Optional[str] = None,
        background_mode_hint: str = "green-screen",
    ) -> Dict[str, Any]:
        scene_index = scene_data.get("index", 0)
        prompt = scene_data.get("image_prompt", "")
        if not prompt:
            raise ValueError(f"场景 {scene_index} 缺少 image_prompt")

        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        generation_size = request_size or self.default_size
        expected_ratio = parse_size_ratio(generation_size)
        print(
            f"[prompt] prompt[:100]: {prompt[:100].replace(chr(10), ' ')}"
            f"{'...' if len(prompt) > 100 else ''}"
        )
        print(
            f"[target] design_size={design_size or 'auto'} "
            f"generation_aspect={self.aspect_ratio} generation_size={generation_size}"
        )

        import time as time_module

        for ratio_attempt in range(MAX_ASPECT_RETRIES + 1):
            last_err = None
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    if self.endpoint == "images":
                        if reference_image_path:
                            raise RuntimeError("images endpoint 当前不支持 reference_image_path，请改用 chat 或实现 edits 路径")
                        payload = self._request_via_images(prompt, generation_size, background_mode_hint)
                    elif self.endpoint == "chat":
                        self.last_background_mode = background_mode_hint
                        payload = self._request_via_chat(prompt, generation_size, reference_image_path)
                    else:
                        if reference_image_path:
                            self.last_background_mode = background_mode_hint
                            payload = self._request_via_chat(prompt, generation_size, reference_image_path)
                        else:
                            payload = self._request_via_images(prompt, generation_size, background_mode_hint)

                    self._save_payload(payload, output_path)
                    break
                except Exception as error:
                    last_err = error
                    message = str(error)[:200]
                    transient = any(
                        marker in message
                        for marker in (
                            "524",
                            "502",
                            "503",
                            "504",
                            "timeout",
                            "Read timed out",
                            "Connection aborted",
                            "RemoteDisconnected",
                        )
                    )
                    if attempt < MAX_RETRIES and transient:
                        print(f"(!) [scene {scene_index}] 第 {attempt} 次失败({message})，{RETRY_DELAY_SECS}s 后重试")
                        time_module.sleep(RETRY_DELAY_SECS)
                        continue
                    raise
            else:
                raise RuntimeError(f"重试 {MAX_RETRIES} 次仍失败: {last_err}")

            width, height = read_png_dimensions(output_path)
            generated_image_size = f"{width}x{height}" if width and height else None
            if aspect_acceptable(width, height, expected_ratio):
                print(
                    f"[OK] 已保存: {output_path} ({generated_image_size or 'unknown'}, "
                    f"design_size {design_size or 'auto'}，实际请求 {generation_size})"
                )
                return {
                    "output_path": output_path,
                    "design_size": design_size,
                    "generation_aspect": self.aspect_ratio,
                    "generation_size": generation_size,
                    "generated_image_size": generated_image_size,
                    "background_mode": self.last_background_mode,
                }

            actual_ratio = width / height if height else 0
            expected = expected_ratio or parse_size_ratio(self.default_size) or 1.0
            deviation_pct = abs(actual_ratio - expected) / expected * 100 if expected else 0
            if ratio_attempt < MAX_ASPECT_RETRIES:
                print(
                    f"[aspect] [scene {scene_index}] 尺寸 {width}x{height} (比例 {actual_ratio:.3f}) "
                    f"偏离目标 {self.aspect_ratio} {deviation_pct:.0f}%，重生 ({ratio_attempt + 1}/{MAX_ASPECT_RETRIES})"
                )
                try:
                    os.remove(output_path)
                except OSError:
                    pass
                continue

            print(f"(!) [scene {scene_index}] 尺寸 {width}x{height} 仍偏离 {deviation_pct:.0f}%，已达上限，保留")
            return {
                "output_path": output_path,
                "design_size": design_size,
                "generation_aspect": self.aspect_ratio,
                "generation_size": generation_size,
                "generated_image_size": generated_image_size,
                "background_mode": self.last_background_mode,
            }

        return {
            "output_path": output_path,
            "design_size": design_size,
            "generation_aspect": self.aspect_ratio,
            "generation_size": generation_size,
            "generated_image_size": None,
            "background_mode": self.last_background_mode,
        }


if __name__ == "__main__":
    generator = GptImage2Generator(aspect_ratio="16:9")
    generator.generate_scene_image(
        {"index": 0, "image_prompt": "A clean sci-fi UI kit on a pure green chroma key background"},
        "test_output.png",
        request_size="1536x1024",
        design_size="1920x1080",
        background_mode_hint="green-screen",
    )
    print(f"自检完成: {Path('test_output.png').resolve()}")
