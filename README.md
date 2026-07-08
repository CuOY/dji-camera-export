# Camera Media Export Skill (dji-camera-export)

[![Install with npx skills](https://img.shields.io/badge/Install%20with-npx%20skills-blue)](https://skills.sh/)

---

[🇬🇧 English](#english) &nbsp;|&nbsp; [🇨🇳 中文](#chinese) &nbsp;|&nbsp; [🇯🇵 日本語](#japanese) &nbsp;|&nbsp; [🇰🇷 한국어](#korean)

---

## English

<a id="english"></a>

A Codex skill that exports photos and videos from a camera USB drive, organizes them into categorized folders, detects high-spec videos that may cause playback stuttering, and optionally transcodes them to a compatible H.264 format.

### Description

This skill automates the workflow of copying media from a camera connected via USB to your computer.

1. **Organizes** — Sorts photos, original videos, and preview/transcoded versions into separate folders
2. **Analyzes** — Reads video encoding parameters (resolution, codec, bitrate, frame rate) to detect files that may cause playback issues
3. **Explains** — Tells you exactly why certain videos might stutter
4. **Transcodes** — Converts problematic videos to H.264 with appropriate scaling, using the best available hardware encoder (Intel QSV, AMD AMF, NVIDIA NVENC, or software libx264)

Designed for action cameras (DJI, GoPro), mirrorless cameras, or any device that presents as a USB mass storage with a DCIM folder structure.

### Prerequisites

- **Windows** (the skill uses PowerShell commands)
- **[ffmpeg](https://ffmpeg.org/)** in PATH
- **Python 3** in PATH
- **Codex** (OpenAI Codex CLI or Desktop) with skill support

### Installation

```bash
npx skills add <your-github-username>/dji-camera-export -g -y
```

Or clone manually to `~/.codex/skills/dji-camera-export`. After installation, restart Codex.

### Usage

Tell Codex: *"帮我从相机导出视频和照片"* or *"I want to export media from my camera"*

The skill walks through: source drive → destination → folder naming → scan and copy → video analysis → transcode consent → completion report.

**Output structure:**

```
F:\CameraName\
+-- 原图片\           # Original photos (.JPG, .DNG)
+-- 原视频及音轨\     # Original videos (.MP4, .MOV) + audio (.WAV)
+-- 预览视频\         # Transcoded H.264 versions
```

**Transcoding thresholds:** Resolution > 1920x1080, HEVC 10-bit, Bitrate > 50 Mbps, Frame rate > 50 fps.

### File Structure

```
dji-camera-export/
+-- README.md
+-- LICENSE (MIT)
+-- .gitignore
+-- SKILL.md
+-- agents/openai.yaml
+-- scripts/transcode_video.py
```

---

## 中文

<a id="chinese"></a>

一款 Codex skill，从相机 U 盘导出照片和视频，自动分类存放，检测高规格视频的播放兼容性问题，并可选转码为 H.264 格式。

### 功能简介

1. **自动分类** — 照片、原始视频、转码预览版分别存入独立文件夹
2. **规格检测** — 逐视频读取分辨率、编码、码率、帧率，识别可能卡顿的文件
3. **原因说明** — 用通俗语言解释为什么某些视频会卡（如"4K 10-bit HEVC @ 60fps，你的显卡不支持硬件解码"）
4. **智能转码** — 转码为 H.264，自动缩放到长边 ≤1920px，自动选用最佳硬件编码器

适用于大疆、GoPro 等运动相机、微单相机，以及任何以 U 盘模式连接、带 DCIM 文件夹的设备。

### 环境要求

- **Windows**（使用 PowerShell 命令）
- **[ffmpeg](https://ffmpeg.org/)** 已安装并在 PATH 中
- **Python 3** 已安装并在 PATH 中
- **Codex**（OpenAI Codex CLI 或桌面版）

### 安装方法

```bash
npx skills add <你的GitHub用户名>/dji-camera-export -g -y
```

或手动克隆到 `~/.codex/skills/dji-camera-export`，然后重启 Codex。

### 使用方法

直接告诉 Codex：*"帮我从相机导出视频和照片"*

流程：选择来源盘符 → 选择目标路径 → 设置文件夹名称 → 扫描并复制 → 视频分析 → 确认转码 → 完成报告。

**输出目录结构：**

```
F:\相机名\
+-- 原图片\           # 原始照片
+-- 原视频及音轨\     # 原始视频 + 独立音轨
+-- 预览视频\         # 转码后的流畅播放版
```

**转码触发条件（满足任意一条即标记）：** 分辨率 > 1920x1080、HEVC 10-bit 编码、码率 > 50 Mbps、帧率 > 50 fps。

### 文件结构

```
dji-camera-export/
+-- README.md
+-- LICENSE (MIT)
+-- .gitignore
+-- SKILL.md          # Codex 工作流指令
+-- agents/openai.yaml
+-- scripts/transcode_video.py    # 独立转码脚本
```

---

## 日本語

<a id="japanese"></a>

カメラのUSBドライブから写真と動画を書き出し、自動的にフォルダ分類し、再生互換性の問題がある高スペック動画を検出し、必要に応じてH.264形式にトランスコードするCodexスキルです。

### 機能概要

1. **自動分類** — 写真、オリジナル動画、トランスコード済みプレビュー版をそれぞれ別フォルダに整理
2. **スペック検出** — 各動画の解像度、コーデック、ビットレート、フレームレートを解析し、再生時に問題が発生する可能性があるファイルを特定
3. **理由の説明** — なぜ特定の動画がカクつくのかを平易な言葉で説明（例：「4K 10-bit HEVC @ 60fps、お使いのGPUはハードウェアデコードに対応していません」）
4. **スマートトランスコード** — H.264に変換し、長辺を1920px以下に自動スケーリング、最適なハードウェアエンコーダーを自動選択

DJI、GoProなどのアクションカメラ、ミラーレスカメラ、USBマスストレージとして接続されDCIMフォルダ構造を持つあらゆるデバイスに対応。

### 前提条件

- **Windows**（PowerShellコマンドを使用）
- **[ffmpeg](https://ffmpeg.org/)** がインストールされPATHに含まれていること
- **Python 3** がインストールされPATHに含まれていること
- **Codex**（OpenAI Codex CLI または デスクトップ版）

### インストール方法

```bash
npx skills add <あなたのGitHubユーザー名>/dji-camera-export -g -y
```

または手動で `~/.codex/skills/dji-camera-export` にクローンし、Codexを再起動してください。

### 使い方

Codexに次のように伝えてください：*"カメラから動画と写真をエクスポートして"*

フロー：ソースドライブの選択 → 保存先の選択 → フォルダ名の設定 → スキャンとコピー → 動画分析 → トランスコードの確認 → 完了レポート。

**出力ディレクトリ構成：**

```
F:\カメラ名\
+-- 原图片\           # オリジナル写真
+-- 原视频及音轨\     # オリジナル動画 + 音声ファイル
+-- 预览视频\         # トランスコード版（スムーズ再生用）
```

**トランスコード条件（いずれかに該当）：** 解像度 > 1920x1080、HEVC 10-bit、ビットレート > 50 Mbps、フレームレート > 50 fps。

### ファイル構成

```
dji-camera-export/
+-- README.md
+-- LICENSE (MIT)
+-- .gitignore
+-- SKILL.md
+-- agents/openai.yaml
+-- scripts/transcode_video.py
```

---

## 한국어

<a id="korean"></a>

카메라 USB 드라이브에서 사진과 비디오를 내보내고, 자동으로 폴더를 분류하며, 재생 호환성 문제가 있는 고사양 비디오를 감지하고, 필요에 따라 H.264 형식으로 트랜스코딩하는 Codex 스킬입니다.

### 기능 설명

1. **자동 분류** — 사진, 원본 비디오, 트랜스코딩된 미리보기 버전을 각각 별도 폴더로 정리
2. **스펙 감지** — 각 비디오의 해상도, 코덱, 비트레이트, 프레임레이트를 분석하여 재생 문제가 발생할 수 있는 파일 식별
3. **이유 설명** — 특정 비디오가 끊기는 이유를 알기 쉬운 언어로 설명 (예: "4K 10-bit HEVC @ 60fps, 사용 중인 GPU가 하드웨어 디코딩을 지원하지 않습니다")
4. **스마트 트랜스코딩** — H.264로 변환, 긴 쪽을 1920px 이하로 자동 스케일링, 최적의 하드웨어 인코더 자동 선택

DJI, GoPro 등의 액션 카메라, 미러리스 카메라, USB 매스 스토리지로 연결되며 DCIM 폴더 구조를 가진 모든 장치에서 사용 가능.

### 사전 요구사항

- **Windows** (PowerShell 명령어 사용)
- **[ffmpeg](https://ffmpeg.org/)** 설치 및 PATH 등록
- **Python 3** 설치 및 PATH 등록
- **Codex** (OpenAI Codex CLI 또는 데스크톱 앱)

### 설치 방법

```bash
npx skills add <GitHub사용자명>/dji-camera-export -g -y
```

또는 수동으로 `~/.codex/skills/dji-camera-export`에 클론한 후 Codex를 재시작하세요.

### 사용 방법

Codex에 다음과 같이 말하세요: *"카메라에서 사진과 비디오를 내보내줘"*

플로우: 소스 드라이브 선택 → 저장 위치 선택 → 폴더명 설정 → 스캔 및 복사 → 비디오 분석 → 트랜스코딩 확인 → 완료 보고.

**출력 디렉토리 구조:**

```
F:\카메라명\
+-- 原图片\           # 원본 사진
+-- 原视频及音轨\     # 원본 비디오 + 오디오 파일
+-- 预览视频\         # 트랜스코딩 버전 (부드러운 재생용)
```

**트랜스코딩 조건 (하나라도 해당 시 플래그):** 해상도 > 1920x1080, HEVC 10-bit, 비트레이트 > 50 Mbps, 프레임레이트 > 50 fps.

### 파일 구조

```
dji-camera-export/
+-- README.md
+-- LICENSE (MIT)
+-- .gitignore
+-- SKILL.md
+-- agents/openai.yaml
+-- scripts/transcode_video.py
```

---

## License / 许可协议 / ライセンス / 라이선스

MIT
