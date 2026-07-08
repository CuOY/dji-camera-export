---
name: dji-camera-export
description: Export photos and videos from a camera USB drive to a local folder with automatic organization and compatibility transcoding. Use when the user asks to: export/copy media from a camera, import files from a USB drive or SD card, organize camera footage into categorized folders, transcode high-resolution or high-bitrate videos to a playable format, or any combination of these tasks. Works with any camera that presents as a mass storage device with DCIM structure.
---

# Camera Media Export

## Overview

Organize camera media into categorized folders, detect high-spec videos that may cause playback stuttering, and transcode them to a compatible H.264 format.

**Script: `scripts/transcode_video.py`** — Transcodes a video to H.264 with auto-scaled resolution and best-available hardware encoder.

## Workflow

### Step 1 — Ask user for settings

Ask the user for:

1. **Source drive** — The camera USB drive letter (e.g. G:)
2. **Destination drive** — Where to save the exported files (e.g. F:\)
3. **Parent folder name** — The top-level folder under destination. Default: the source drive's volume label.

Get the volume label with:
```
(Get-Volume -DriveLetter X).FileSystemLabel
```

### Step 2 — Scan source for media files

Find video and photo files on the source drive under DCIM:
```
Get-ChildItem -Path "${src}:\DCIM" -Include "*.MP4","*.MOV","*.WAV","*.JPG","*.DNG" -Recurse
```

File types to handle:
- **.MP4, .MOV** — video files
- **.WAV** — standalone audio tracks (DJI, some action cams)
- **.JPG, .DNG** — photos / raw images
- **Skip .LRF** — low-resolution preview files (action cams)

### Step 3 — Create directory structure and copy files

```
$baseDest = "D:\parentFolderName"
New-Item -ItemType Directory -Path "$baseDest\原视频及音轨" -Force | Out-Null
New-Item -ItemType Directory -Path "$baseDest\原图片" -Force | Out-Null
New-Item -ItemType Directory -Path "$baseDest\预览视频" -Force | Out-Null
```

Copy files (bit-perfect, no quality loss):
- Photos (.JPG, .DNG) -> 原图片\
- Videos (.MP4, .MOV) + audio (.WAV) -> 原视频及音轨\

Use `Copy-Item -LiteralPath` for individual copies. Skip `.LRF` files.

### Step 4 — Analyze each video for transcoding needs

For each MP4/MOV file, run ffprobe:
```
ffprobe -v quiet -print_format json -show_streams "path\to\video.mp4"
```

Extract from JSON: `width`, `height`, `codec_name`, `profile`, `pix_fmt`, `bit_rate`, `r_frame_rate`.

**Transcoding thresholds** — flag a video if ANY apply:
- Resolution > 1920x1080 (more than 2.1 megapixels)
- HEVC (H.265) + 10-bit profile or pixel format
- Bitrate > 50 Mbps
- Frame rate > 50 fps

For each flagged video, note the details to explain the reasons to the user.

### Step 5 — Present findings and get consent

Show a summary like:

```
检测到以下视频可能需要转码：
  xxxx_D.MP4 - 3840x2880 HEVC Main 10 60fps 80 Mbps
    - 分辨率过高 (3840x2880)
    - 10-bit HEVC 编码兼容性差
    - 码率过高 (80 Mbps)
    - 高帧率 (60 fps)

原因：[通俗解释，如"这台电脑的显卡不支持 10-bit HEVC 硬解，
纯 CPU 解 4K 60fps 会导致卡顿和音画不同步"]
```

Ask: "是否对这些视频进行转码？转码后的 H.264 版可以流畅播放。"
- If yes -> Step 6
- If no -> Done. Report summary.

### Step 6 — Transcode flagged videos

For each flagged video:
```
python <skill_path>\scripts\transcode_video.py "原视频及音轨\video.mp4" "预览视频\video.mp4"
```

The script:
- Reads video specs via ffprobe
- Scales to <= 1920px on long side, keeps aspect ratio
- Selects best H.264 encoder (qsv -> amf -> nvenc -> mf -> libx264)
- Copies audio stream without re-encoding

### Step 7 — Report completion

Show the final folder structure with file sizes using:
```
Get-ChildItem $baseDest -Recurse | Where-Object { -not $_.PSIsContainer } | Select-Object Directory, Name, Length
```
