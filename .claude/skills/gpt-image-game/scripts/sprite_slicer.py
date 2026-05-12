#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path
from typing import Any

from PIL import Image, ImageFilter


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Slice UI components from transparent or chroma key images")
    parser.add_argument("--input", required=True, help="Input PNG path")
    parser.add_argument("--output-dir", required=True, help="Output directory for sliced images")
    parser.add_argument("--mode", choices=["alpha-components", "chroma-key-components"], default="alpha-components")
    parser.add_argument("--prefix", default="sprite")
    parser.add_argument("--alpha-threshold", type=int, default=8)
    parser.add_argument("--min-width", type=int, default=16)
    parser.add_argument("--min-height", type=int, default=16)
    parser.add_argument("--min-area", type=int, default=256)
    parser.add_argument("--padding", type=int, default=4)
    parser.add_argument("--key-color", default="#00FF00")
    parser.add_argument("--key-threshold", type=int, default=48)
    parser.add_argument("--edge-softness", type=int, default=12)
    parser.add_argument("--despill-strength", type=float, default=1.2)
    return parser


def parse_hex_color(color_text: str) -> tuple[int, int, int]:
    raw = color_text.strip()
    if raw.startswith("#"):
        raw = raw[1:]
    if len(raw) != 6:
        raise ValueError("key color must be a 6-digit hex color like #00FF00")
    return tuple(int(raw[index : index + 2], 16) for index in (0, 2, 4))


def clamp_box(box: tuple[int, int, int, int], width: int, height: int, padding: int) -> tuple[int, int, int, int]:
    left, top, right, bottom = box
    return (
        max(0, left - padding),
        max(0, top - padding),
        min(width, right + padding),
        min(height, bottom + padding),
    )


def sort_boxes(boxes: list[tuple[int, int, int, int]]) -> list[tuple[int, int, int, int]]:
    return sorted(boxes, key=lambda box: (box[1], box[0], box[3] - box[1], box[2] - box[0]))


def find_component_boxes(mask: Image.Image, threshold: int) -> list[tuple[int, int, int, int]]:
    width, height = mask.size
    pixels = mask.load()
    visited = bytearray(width * height)
    boxes: list[tuple[int, int, int, int]] = []

    def index(x: int, y: int) -> int:
        return y * width + x

    for start_y in range(height):
        for start_x in range(width):
            flat_index = index(start_x, start_y)
            if visited[flat_index]:
                continue
            visited[flat_index] = 1
            if pixels[start_x, start_y] <= threshold:
                continue

            queue: deque[tuple[int, int]] = deque([(start_x, start_y)])
            min_x = max_x = start_x
            min_y = max_y = start_y

            while queue:
                x, y = queue.popleft()
                for delta_y in (-1, 0, 1):
                    for delta_x in (-1, 0, 1):
                        if delta_x == 0 and delta_y == 0:
                            continue
                        next_x = x + delta_x
                        next_y = y + delta_y
                        if next_x < 0 or next_y < 0 or next_x >= width or next_y >= height:
                            continue
                        neighbor_index = index(next_x, next_y)
                        if visited[neighbor_index]:
                            continue
                        visited[neighbor_index] = 1
                        if pixels[next_x, next_y] <= threshold:
                            continue
                        queue.append((next_x, next_y))
                        min_x = min(min_x, next_x)
                        min_y = min(min_y, next_y)
                        max_x = max(max_x, next_x)
                        max_y = max(max_y, next_y)

            boxes.append((min_x, min_y, max_x + 1, max_y + 1))

    return sort_boxes(boxes)


def validate_mask_channel(mask: Image.Image, threshold: int) -> None:
    min_value, max_value = mask.getextrema()
    if max_value <= threshold:
        raise ValueError("mask contains no visible components above the configured threshold")
    if min_value > threshold:
        raise ValueError("mask has no background separation; all pixels are above the threshold")


def validate_alpha_channel(image: Image.Image, threshold: int) -> Image.Image:
    if "A" not in image.getbands():
        raise ValueError("image has no alpha channel; transparent component slicing requires PNG alpha")
    alpha = image.getchannel("A")
    validate_mask_channel(alpha, threshold)
    return alpha


def build_mask_from_chroma_key(image: Image.Image, key_color: tuple[int, int, int], key_threshold: int, edge_softness: int) -> Image.Image:
    width, height = image.size
    mask = Image.new("L", (width, height), 0)
    source_pixels = image.load()
    mask_pixels = mask.load()
    max_distance = key_threshold + edge_softness

    for y in range(height):
        for x in range(width):
            red, green, blue, _ = source_pixels[x, y]
            distance = ((red - key_color[0]) ** 2 + (green - key_color[1]) ** 2 + (blue - key_color[2]) ** 2) ** 0.5
            if distance <= key_threshold:
                alpha_value = 0
            elif edge_softness > 0 and distance < max_distance:
                alpha_value = int((distance - key_threshold) / edge_softness * 255)
            else:
                alpha_value = 255
            mask_pixels[x, y] = max(0, min(255, alpha_value))

    if edge_softness > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(radius=max(1, edge_softness / 6)))
    return mask


def apply_mask_as_alpha(image: Image.Image, mask: Image.Image, key_color: tuple[int, int, int], despill_strength: float) -> Image.Image:
    masked_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    masked_image.paste(image, (0, 0), mask)
    masked_image.putalpha(mask)
    if despill_strength <= 0:
        return masked_image

    dominant_channel_index = max(range(3), key=lambda index: key_color[index])
    pixels = masked_image.load()
    width, height = masked_image.size

    for y in range(height):
        for x in range(width):
            red, green, blue, alpha = pixels[x, y]
            if not 0 < alpha < 255:
                continue

            channels = [red, green, blue]
            dominant_value = channels[dominant_channel_index]
            support_value = max(value for index, value in enumerate(channels) if index != dominant_channel_index)
            if dominant_value <= support_value:
                continue

            edge_factor = 1 - alpha / 255
            blend_strength = min(1.0, despill_strength * (0.35 + edge_factor * 0.65))
            channels[dominant_channel_index] = int(round(dominant_value + (support_value - dominant_value) * blend_strength))
            pixels[x, y] = (channels[0], channels[1], channels[2], alpha)

    return masked_image


def export_slices(
    image: Image.Image,
    mask: Image.Image,
    output_dir: str,
    prefix: str,
    alpha_threshold: int,
    min_width: int,
    min_height: int,
    min_area: int,
    padding: int,
) -> list[dict[str, Any]]:
    validate_mask_channel(mask, alpha_threshold)
    destination_dir = Path(output_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    boxes = find_component_boxes(mask, alpha_threshold)
    width, height = image.size
    slices: list[dict[str, Any]] = []

    for box in boxes:
        padded_box = clamp_box(box, width, height, padding)
        left, top, right, bottom = padded_box
        component_width = right - left
        component_height = bottom - top
        component_area = component_width * component_height

        if component_width < min_width or component_height < min_height or component_area < min_area:
            continue

        slice_index = len(slices) + 1
        output_file = destination_dir / f"{prefix}-{slice_index:02d}.png"
        image.crop(padded_box).save(output_file)
        slices.append(
            {
                "index": slice_index,
                "box": [left, top, right, bottom],
                "width": component_width,
                "height": component_height,
                "output_path": str(output_file),
            }
        )

    if not slices:
        raise ValueError("no sliceable components found after applying the current filters")
    return slices


def slice_image_components(
    input_path: str,
    output_dir: str,
    prefix: str = "sprite",
    alpha_threshold: int = 8,
    min_width: int = 16,
    min_height: int = 16,
    min_area: int = 256,
    padding: int = 4,
) -> dict[str, Any]:
    if not 0 <= alpha_threshold <= 255:
        raise ValueError("alpha_threshold must be between 0 and 255")
    if min_width < 1 or min_height < 1:
        raise ValueError("min_width and min_height must be at least 1")
    if min_area < 1:
        raise ValueError("min_area must be at least 1")
    if padding < 0:
        raise ValueError("padding must be 0 or greater")

    input_file = Path(input_path)
    with Image.open(input_file) as source:
        image = source.convert("RGBA")
        alpha = validate_alpha_channel(image, alpha_threshold)
        slices = export_slices(
            image=image,
            mask=alpha,
            output_dir=output_dir,
            prefix=prefix,
            alpha_threshold=alpha_threshold,
            min_width=min_width,
            min_height=min_height,
            min_area=min_area,
            padding=padding,
        )

    return {
        "input_path": str(input_file),
        "output_dir": str(Path(output_dir)),
        "summary": {
            "mode": "alpha-components",
            "detected_components": len(slices),
        },
        "slices": slices,
    }


def slice_image_by_chroma_key(
    input_path: str,
    output_dir: str,
    prefix: str = "sprite",
    key_color: str = "#00FF00",
    key_threshold: int = 48,
    edge_softness: int = 12,
    despill_strength: float = 1.2,
    alpha_threshold: int = 8,
    min_width: int = 16,
    min_height: int = 16,
    min_area: int = 256,
    padding: int = 4,
) -> dict[str, Any]:
    if key_threshold < 0:
        raise ValueError("key_threshold must be 0 or greater")
    if edge_softness < 0:
        raise ValueError("edge_softness must be 0 or greater")
    if despill_strength < 0:
        raise ValueError("despill_strength must be 0 or greater")

    input_file = Path(input_path)
    parsed_key_color = parse_hex_color(key_color)
    with Image.open(input_file) as source:
        image = source.convert("RGBA")
        mask = build_mask_from_chroma_key(image, parsed_key_color, key_threshold, edge_softness)
        transparent_image = apply_mask_as_alpha(image, mask, parsed_key_color, despill_strength)
        slices = export_slices(
            image=transparent_image,
            mask=mask,
            output_dir=output_dir,
            prefix=prefix,
            alpha_threshold=alpha_threshold,
            min_width=min_width,
            min_height=min_height,
            min_area=min_area,
            padding=padding,
        )
        histogram = mask.histogram()
        foreground_pixels = sum(count for alpha_value, count in enumerate(histogram) if alpha_value > alpha_threshold)
        total_pixels = image.size[0] * image.size[1]

    return {
        "input_path": str(input_file),
        "output_dir": str(Path(output_dir)),
        "summary": {
            "mode": "chroma-key-components",
            "key_color": key_color,
            "key_threshold": key_threshold,
            "edge_softness": edge_softness,
            "despill_strength": despill_strength,
            "detected_components": len(slices),
            "foreground_ratio": round(foreground_pixels / total_pixels, 4) if total_pixels else 0,
        },
        "slices": slices,
    }


def main() -> None:
    args = create_parser().parse_args()
    if args.mode == "alpha-components":
        result = slice_image_components(
            input_path=args.input,
            output_dir=args.output_dir,
            prefix=args.prefix,
            alpha_threshold=args.alpha_threshold,
            min_width=args.min_width,
            min_height=args.min_height,
            min_area=args.min_area,
            padding=args.padding,
        )
    else:
        result = slice_image_by_chroma_key(
            input_path=args.input,
            output_dir=args.output_dir,
            prefix=args.prefix,
            key_color=args.key_color,
            key_threshold=args.key_threshold,
            edge_softness=args.edge_softness,
            despill_strength=args.despill_strength,
            alpha_threshold=args.alpha_threshold,
            min_width=args.min_width,
            min_height=args.min_height,
            min_area=args.min_area,
            padding=args.padding,
        )

    print(f"Sliced {len(result['slices'])} components into: {result['output_dir']}")
    print(result.get("summary"))
    for item in result["slices"]:
        print(f"Slice: {item['output_path']} {item['box']}")


if __name__ == "__main__":
    main()
