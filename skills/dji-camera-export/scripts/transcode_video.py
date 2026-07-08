#!/usr/bin/env python3
"""
Transcode a video to H.264 with appropriate scaling for playback compatibility.

Usage:
    python transcode_video.py <input_path> <output_path>

Scales to fit within 1920px on the long side, keeps aspect ratio.
Auto-selects best available H.264 encoder (qsv -> amf -> nvenc -> mf -> libx264).
"""

import subprocess
import json
import sys
import os


def get_video_info(path):
    """Get video stream info using ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    for stream in data.get("streams", []):
        if stream.get("codec_type") == "video":
            num, den = [int(x) for x in stream["r_frame_rate"].split("/")]
            fps = num / den if den > 0 else 0
            return {
                "width": stream["width"],
                "height": stream["height"],
                "codec": stream.get("codec_name", ""),
                "profile": stream.get("profile", ""),
                "bit_rate": int(stream.get("bit_rate", 0)),
                "fps": round(fps, 1),
                "pix_fmt": stream.get("pix_fmt", ""),
            }
    return None


def needs_transcoding(info):
    """Determine if a video is likely to cause playback issues. Returns list of reasons."""
    reasons = []
    pixels = info["width"] * info["height"]
    threshold_mp = 1920 * 1080

    if pixels > threshold_mp:
        reasons.append(f"分辨率 {info['width']}x{info['height']}（超过 1080p 标准）")

    is_10bit = "10" in info.get("profile", "") or "10" in info.get("pix_fmt", "")
    if info["codec"] == "hevc" and is_10bit:
        reasons.append("10-bit HEVC 编码，多数播放器和显卡不支持硬件解码")
    elif info["codec"] == "hevc" and pixels > threshold_mp:
        reasons.append("HEVC 编码在高分辨率下软件解码负担重")

    if info["bit_rate"] > 50000000:
        reasons.append(f"码率 {info['bit_rate'] / 1e6:.0f} Mbps（超过 50 Mbps）")

    if info["fps"] > 50:
        reasons.append(f"帧率 {info['fps']:.0f} fps（每秒处理量大）")

    return reasons


def determine_target_size(width, height):
    """Scale down to fit within 1920 on the long side, keeping aspect ratio."""
    max_dim = 1920

    if width <= max_dim and height <= max_dim:
        if height > 1440:
            scale = 1440 / height
            tw = int(width * scale) // 2 * 2
            th = 1440
            return tw, th
        return width, height

    if width >= height:
        target_width = max_dim
        target_height = int(max_dim * height / width) // 2 * 2
    else:
        target_height = max_dim
        target_width = int(max_dim * width / height) // 2 * 2

    return target_width, target_height


def find_best_encoder():
    """Find the best available H.264 encoder by priority."""
    cmd = ["ffmpeg", "-encoders"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    encoders = result.stdout + result.stderr

    for enc in ["h264_qsv", "h264_amf", "h264_nvenc", "h264_mf", "libx264"]:
        if enc in encoders:
            return enc
    return "libx264"


def transcode(input_path, output_path, target_w, target_h, encoder):
    """Transcode video with ffmpeg."""
    vf = f"scale={target_w}:{target_h}"

    if encoder == "libx264":
        cmd = [
            "ffmpeg", "-i", input_path,
            "-vf", vf,
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "copy",
            "-y", output_path
        ]
    else:
        cmd = [
            "ffmpeg", "-i", input_path,
            "-vf", vf,
            "-c:v", encoder, "-global_quality", "22",
            "-c:a", "copy",
            "-y", output_path
        ]

    process = subprocess.run(cmd, capture_output=True, text=True)
    return process.returncode == 0


def main():
    if len(sys.argv) != 3:
        print("Usage: python transcode_video.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"错误: 输入文件不存在 '{input_path}'")
        sys.exit(1)

    print(f"分析视频: {os.path.basename(input_path)}")
    info = get_video_info(input_path)
    if not info:
        print("错误: 无法读取视频信息")
        sys.exit(1)

    reasons = needs_transcoding(info)
    if not reasons:
        print("该视频规格较低，无需转码")
        return

    print(f"  分辨率: {info['width']}x{info['height']}")
    print(f"  编码:   {info['codec']} {info.get('profile', '')}")
    print(f"  码率:   {info['bit_rate'] / 1e6:.1f} Mbps")
    print(f"  帧率:   {info['fps']:.0f} fps")

    tw, th = determine_target_size(info["width"], info["height"])
    print(f"  目标:   {tw}x{th} H.264")

    encoder = find_best_encoder()
    print(f"  编码器: {encoder}")

    print(f"\n转码中...")
    success = transcode(input_path, output_path, tw, th, encoder)

    if success:
        out_size_mb = os.path.getsize(output_path) / 1e6
        print(f"转码完成: {os.path.basename(output_path)} ({out_size_mb:.0f} MB)")
    else:
        print("转码失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
