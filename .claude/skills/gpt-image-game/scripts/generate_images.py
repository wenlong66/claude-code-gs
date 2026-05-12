#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).parent
CWD = Path.cwd()
OUTPUT_BASE_DIR = "outputs"
DEFAULT_ASPECT_BY_GAME_TYPE = {
    "character": "9:16",
    "ui": "16:9",
}
ASPECT_RATIO_VALUES = {
    "16:9": 16 / 9,
    "9:16": 9 / 16,
    "1:1": 1.0,
}
SIZE_PATTERN = re.compile(r"^(\d+)x(\d+)$")
HEX_COLOR_PATTERN = re.compile(r"^#?[0-9A-Fa-f]{6}$")


def configure_console_encoding() -> None:
    if os.name == "nt":
        try:
            import ctypes

            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
        except Exception:
            pass

    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def find_and_load_env() -> bool:
    env_locations = []
    explicit = os.getenv("GPT_IMAGE2_IMAGE_ENV")
    if explicit:
        env_locations.append(Path(explicit))
    env_locations.extend(
        [
            SCRIPT_DIR.parent / ".env",
            Path.home() / ".claude" / "skills" / "gpt-image-game" / ".env",
            Path.home() / "skills" / "gpt-image-game" / ".env",
        ]
    )

    for env_path in env_locations:
        if env_path.exists():
            load_dotenv(env_path, override=True)
            print(f"Loaded environment from: {env_path}")
            return True

    print("Warning: No .env file found in scoped locations; using process env vars only.")
    return False


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate game images with gpt-image-2")
    parser.add_argument("--prompt", help="Prompt text")
    parser.add_argument("--prompt-file", help="Path to a UTF-8 text file containing the prompt")
    parser.add_argument("--game-type", choices=["character", "ui"], required=True)
    parser.add_argument("--design-size", help="Game design size, for example 1920x1080")
    parser.add_argument("--size", help="Deprecated alias of --design-size")
    parser.add_argument("--aspect", choices=["1:1", "16:9", "9:16"], help="Override the generation aspect ratio")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--output-dir", help="Output directory path")
    parser.add_argument("--base-name", default="image")
    parser.add_argument("--quality", choices=["low", "medium", "high", "auto"])
    parser.add_argument("--slice-mode", choices=["none", "chroma-key-components"], default="none")
    parser.add_argument("--slice-alpha-threshold", type=int, default=8)
    parser.add_argument("--slice-min-width", type=int, default=16)
    parser.add_argument("--slice-min-height", type=int, default=16)
    parser.add_argument("--slice-min-area", type=int, default=256)
    parser.add_argument("--slice-padding", type=int, default=2)
    parser.add_argument("--slice-output-dir", help="Base output directory for sliced sprites")
    parser.add_argument("--slice-prefix", default="sprite")
    parser.add_argument("--key-color", default="#00FF00", help="Chroma key background color, for example #00FF00")
    parser.add_argument("--key-threshold", type=int, default=48, help="Chroma key color distance threshold")
    parser.add_argument("--edge-softness", type=int, default=12, help="Soft transition range above key threshold")
    parser.add_argument("--despill-strength", type=float, default=1.2, help="Edge de-spill strength for transparent slices")
    return parser


def load_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    raise ValueError("Either --prompt or --prompt-file is required")


def build_output_dir(output_dir: str | None) -> Path:
    if output_dir:
        path = Path(output_dir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = CWD / OUTPUT_BASE_DIR / timestamp
    path.mkdir(parents=True, exist_ok=True)
    return path


def normalize_design_size(size_text: str | None, option_name: str) -> str | None:
    if not size_text:
        return None
    match = SIZE_PATTERN.fullmatch(size_text.strip())
    if not match:
        raise ValueError(f"{option_name} must use WIDTHxHEIGHT format, for example 1920x1080")
    width = int(match.group(1))
    height = int(match.group(2))
    if width <= 0 or height <= 0:
        raise ValueError(f"{option_name} width and height must be positive integers")
    return f"{width}x{height}"


def normalize_key_color(color_text: str) -> str:
    raw = color_text.strip()
    if not HEX_COLOR_PATTERN.fullmatch(raw):
        raise ValueError("--key-color must be a 6-digit hex color like #00FF00")
    return raw if raw.startswith("#") else f"#{raw}"


def resolve_design_size(args: argparse.Namespace) -> str | None:
    design_size = normalize_design_size(args.design_size, "--design-size")
    legacy_size = normalize_design_size(args.size, "--size")
    if design_size and legacy_size and design_size != legacy_size:
        raise ValueError("--design-size and --size must match when both are provided")
    if legacy_size and not design_size:
        print("Warning: --size is deprecated; use --design-size instead.", file=sys.stderr)
    return design_size or legacy_size


def determine_generation_aspect(design_size: str | None, explicit_aspect: str | None, game_type: str) -> str:
    if explicit_aspect:
        return explicit_aspect
    if design_size:
        width_text, height_text = design_size.split("x", 1)
        ratio = int(width_text) / int(height_text)
        return min(ASPECT_RATIO_VALUES, key=lambda key: abs(ASPECT_RATIO_VALUES[key] - ratio))
    return DEFAULT_ASPECT_BY_GAME_TYPE[game_type]


def build_prompt(
    user_prompt: str,
    game_type: str,
    design_size: str | None,
    slice_mode: str,
    key_color: str,
) -> str:
    sections = [
        "请生成一张用于游戏项目的图片素材。",
        "主体或组件必须清晰、完整，便于后续放入游戏画面或游戏 UI。",
    ]

    chroma_key_mode = slice_mode == "chroma-key-components"

    if game_type == "character":
        sections.extend(
            [
                "这是游戏角色素材，主体必须完整、识别度高、轮廓清晰。",
                "适合作为立绘、卡面、头像裁切或场景叠加素材。",
                "除非用户明确要求，不要让复杂环境背景抢走主体。",
            ]
        )
    else:
        sections.extend(
            [
                "这是游戏 UI / HUD 素材。",
                "强调可读性、层级关系、边缘清晰度和可叠加性。",
                "适合作为按钮、图标、面板、状态条、弹窗等独立组件。",
            ]
        )

    sections.extend(
        [
            f"请使用统一、纯净、饱和的绿色背景，背景主色为 {key_color}。",
            "背景尽量保持纯色，不要渐变、纹理、投影或额外装饰。",
            "前景主体或组件与背景之间保持高对比度。",
            "不要生成白底、黑底、摄影棚底或复杂场景背景。",
        ]
    )

    if chroma_key_mode:
        sections.extend(
            [
                "元素之间不要粘连、覆盖或明显重叠，尽量留出绿底间隔。",
                "这张图是为了后续自动抠绿底并拆成散图，不是海报。",
            ]
        )

    if design_size:
        sections.extend(
            [
                f"游戏目标画面设计尺寸为 {design_size}。",
                "请按这个游戏画面尺寸设计布局、元素比例与安全区域。",
                f"这是设计语义要求，不是要求最终输出像素必须等于 {design_size}。",
            ]
        )

    sections.extend(
        [
            "不要输出解释，只生成最终图片。",
            "具体需求如下：",
            user_prompt.strip(),
        ]
    )
    return "\n".join(sections)


def build_slice_config(args: argparse.Namespace, output_dir: Path) -> dict[str, Any]:
    enabled = args.slice_mode != "none"
    slice_output_dir = Path(args.slice_output_dir) if args.slice_output_dir else output_dir / "slices"
    config = {
        "enabled": enabled,
        "mode": args.slice_mode,
        "alpha_threshold": args.slice_alpha_threshold,
        "min_width": args.slice_min_width,
        "min_height": args.slice_min_height,
        "min_area": args.slice_min_area,
        "padding": args.slice_padding,
        "output_dir": str(slice_output_dir),
        "prefix": args.slice_prefix,
        "key_color": normalize_key_color(args.key_color),
        "key_threshold": args.key_threshold,
        "edge_softness": args.edge_softness,
        "despill_strength": args.despill_strength,
    }
    if enabled:
        if not 0 <= args.slice_alpha_threshold <= 255:
            raise ValueError("--slice-alpha-threshold must be between 0 and 255")
        if args.slice_min_width < 1 or args.slice_min_height < 1:
            raise ValueError("--slice-min-width and --slice-min-height must be at least 1")
        if args.slice_min_area < 1:
            raise ValueError("--slice-min-area must be at least 1")
        if args.slice_padding < 0:
            raise ValueError("--slice-padding must be 0 or greater")
        if args.key_threshold < 0:
            raise ValueError("--key-threshold must be 0 or greater")
        if args.edge_softness < 0:
            raise ValueError("--edge-softness must be 0 or greater")
        if args.despill_strength < 0:
            raise ValueError("--despill-strength must be 0 or greater")
    return config


def main() -> None:
    configure_console_encoding()
    find_and_load_env()

    parser = create_parser()
    args = parser.parse_args()

    if args.count < 1:
        parser.error("--count must be at least 1")

    try:
        design_size = resolve_design_size(args)
        prompt = load_prompt(args)
        output_dir = build_output_dir(args.output_dir)
        slice_config = build_slice_config(args, output_dir)
    except ValueError as error:
        parser.error(str(error))
        return

    final_prompt = build_prompt(
        prompt,
        args.game_type,
        design_size,
        args.slice_mode,
        slice_config["key_color"],
    )
    generation_aspect = determine_generation_aspect(design_size, args.aspect, args.game_type)

    from image_generator import ASPECT_TO_SIZE, GptImage2Generator
    from sprite_slicer import slice_image_by_chroma_key

    generation_size = ASPECT_TO_SIZE[generation_aspect]
    generator = GptImage2Generator(aspect_ratio=generation_aspect)
    if args.quality:
        generator.quality = args.quality

    background_mode_hint = "green-screen"

    manifest: dict[str, Any] = {
        "model": generator.model_name,
        "game_type": args.game_type,
        "background_mode": None,
        "design_size": design_size,
        "requested_size": design_size,
        "generation_aspect": generation_aspect,
        "resolved_aspect": generation_aspect,
        "generation_size": generation_size,
        "resolved_size": generation_size,
        "count": args.count,
        "quality": generator.quality,
        "output_dir": str(output_dir),
        "prompt": final_prompt,
        "slice": slice_config,
        "images": [],
    }

    for index in range(1, args.count + 1):
        output_path = output_dir / f"{args.base_name}-{index:02d}.png"
        scene_data = {
            "index": index,
            "image_prompt": final_prompt,
        }
        result = generator.generate_scene_image(
            scene_data=scene_data,
            output_path=str(output_path),
            request_size=generation_size,
            design_size=design_size,
            background_mode_hint=background_mode_hint,
        )

        image_entry: dict[str, Any] = {
            "index": index,
            "output_path": result["output_path"],
            "generated_image_size": result["generated_image_size"],
            "background_mode": result["background_mode"],
            "slices": [],
            "slice_error": None,
        }

        manifest["background_mode"] = result["background_mode"]

        if slice_config["enabled"]:
            per_image_slice_output_dir = Path(slice_config["output_dir"]) / output_path.stem
            try:
                slice_result = slice_image_by_chroma_key(
                    input_path=result["output_path"],
                    output_dir=str(per_image_slice_output_dir),
                    prefix=args.slice_prefix,
                    key_color=slice_config["key_color"],
                    key_threshold=slice_config["key_threshold"],
                    edge_softness=slice_config["edge_softness"],
                    despill_strength=slice_config["despill_strength"],
                    alpha_threshold=slice_config["alpha_threshold"],
                    min_width=slice_config["min_width"],
                    min_height=slice_config["min_height"],
                    min_area=slice_config["min_area"],
                    padding=slice_config["padding"],
                )
                image_entry["slices"] = slice_result["slices"]
                image_entry["slice_summary"] = slice_result.get("summary")
            except Exception as error:
                image_entry["slice_error"] = str(error)
                print(f"[slice] {output_path.name}: {error}")

        manifest["images"].append(image_entry)

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    total_slices = sum(len(image_entry["slices"]) for image_entry in manifest["images"])
    print("=" * 60)
    print("Game image generation complete")
    print("=" * 60)
    print(f"Output directory: {output_dir}")
    print(f"Design size: {manifest['design_size']}")
    print(f"Generation aspect: {manifest['generation_aspect']}")
    print(f"Generation size: {manifest['generation_size']}")
    print(f"Background mode: {manifest['background_mode']}")
    print(f"Slice mode: {manifest['slice']['mode']}")
    print(f"Total slices: {total_slices}")
    for image_entry in manifest["images"]:
        print(f"Image: {image_entry['output_path']}")
        if image_entry["slice_error"]:
            print(f"Slice error: {image_entry['slice_error']}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
