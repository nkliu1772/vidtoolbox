# **VidToolbox**

[English](README.md) | [繁體中文](README_ZH.md)

📋 **Changelog**: [English](CHANGELOG_EN.md) | [繁體中文](CHANGELOG_ZH.md)

🧪 **Testing Guide**: [English](TESTING_GUIDE_EN.md) | [繁體中文](TESTING_GUIDE.md)

## 📌 Introduction
**VidToolbox** is a video processing tool that supports:
- 🔍 **Retrieving video information** (resolution, duration, file size)
- 📝 **Generating YouTube chapter timestamps** (`timestamps.txt`)
- 🎬 **Merging multiple video files**
- 📄 **Automatically generating `file_list.txt` for ffmpeg concat**
- 🔍 **Video compatibility checking and smart merging**
- 🎵 **Converting videos to MP3 audio files**
- 🏷️ **Automatically naming output files based on the folder name**

This tool works on **Windows**, **macOS** and **Linux**, utilizing `ffmpeg` for video processing.

---

## ⚡ Installation

### 1️⃣ **Install `ffmpeg`** (if not installed)
```bash
brew install ffmpeg  # macOS (Homebrew)
sudo apt install ffmpeg  # Ubuntu / Debian
```

### 2️⃣ **Install VidToolbox using `pipx` (Recommended)**
```bash
pipx install --force git+https://github.com/nkliu1772/vidtoolbox.git
```

If `pipx` is not installed, run:

```bash
# For macOS (using Homebrew)
brew install pipx
pipx ensurepath

# For other systems
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

---

## 🚀 Usage

### **1️⃣ Get Video Information**
```bash
vid-info /path/to/video_folder
```
🔹 Displays resolution, duration, and file size.

### **2️⃣ Generate YouTube Chapter Timestamps**
```bash
vid-timestamps /path/to/video_folder
```
🔹 Creates `timestamps.txt` and prompts user for confirmation.

### **3️⃣ Merge Videos**
```bash
vid-merge /path/to/video_folder
```
🔹 Confirms timestamps before merging videos.

🔹 **Smart merging**: Automatically checks video compatibility and offers re-encoding options if needed.

🔹 The default output file name is **the folder name**, but you can specify an output file with `-o`:
```bash
vid-merge /path/to/video_folder -o output.mp4
```

### **4️⃣ Generate File List for FFmpeg Concat**
```bash
vid-filelist /path/to/video_folder
```
🔹 Automatically generates `file_list.txt` for ffmpeg concat operations.

🔹 Options:
```bash
# 指定輸出檔案名稱
vid-filelist /path/to/video_folder -o my_list.txt

# 指定檔案模式
vid-filelist /path/to/video_folder -p "*.mp4"

# 不按檔案名稱排序
vid-filelist /path/to/video_folder --no-sort

# 顯示合併命令
vid-filelist /path/to/video_folder --show-merge-cmd
```

### **5️⃣ Quick Merge Videos**
```bash
vid-quick-merge /path/to/video_folder
```
🔹 Automatically generates `file_list.txt` and merges videos in one step.

🔹 Options:
```bash
# 指定輸出檔案名稱
vid-quick-merge /path/to/video_folder -o merged_video.mp4

# 保留 file_list.txt
vid-quick-merge /path/to/video_folder --keep-filelist

# 使用現有的 file_list.txt
vid-quick-merge /path/to/video_folder --use-existing-list
```

### **6️⃣ Convert Videos to MP3**
```bash
vid-mp3 /path/to/video_folder
```
🔹 Converts video files to MP3 audio files for transcription or audio processing.

🔹 Options:
```bash
# 基本轉換
vid-mp3 /path/to/video_folder

# 指定品質 (0=最高品質, 9=最低品質)
vid-mp3 /path/to/video_folder -q 0

# 指定輸出目錄
vid-mp3 /path/to/video_folder -o /path/to/output

# 遞迴搜尋子目錄
vid-mp3 /path/to/video_folder -r

# 覆蓋現有檔案
vid-mp3 /path/to/video_folder --overwrite

# 顯示品質預設值說明
vid-mp3 --show-quality
```

🔹 **Quality Presets**:
- `0`: 最高品質 (320kbps)
- `2`: 高品質 (192kbps) - 推薦
- `4`: 中等品質 (128kbps)
- `6`: 較低品質 (96kbps)
- `8`: 低品質 (64kbps)
- `9`: 最低品質 (32kbps)

### **7️⃣ Merge Subtitle Files**
```bash
vid-subtitles /path/to/video_folder
```
🔹 Merges multiple `.srt` subtitle files in order, with automatic time shifting and re-indexing.

🔹 Options:
```bash
# 基本合併
vid-subtitles /path/to/video_folder

# 指定輸出檔案
vid-subtitles /path/to/video_folder -o merged_subtitles.srt

# 指定字幕檔案模式
vid-subtitles /path/to/video_folder -p "*.srt"

# 指定影片檔案模式 (用於計算時間偏移)
vid-subtitles /path/to/video_folder -v "*.mp4"

# 不確認檔案順序
vid-subtitles /path/to/video_folder --no-confirm
```

🔹 **Features**:
- Automatically sorts subtitle files by name
- Shifts timing based on corresponding video durations
- Re-indexes subtitle entries sequentially
- Supports UTF-8 encoding for international characters

---

## 📌 TODO
- [ ] Add `--output` parameter to allow specifying the output directory
- [ ] Add an option to merge videos in all subdirectories automatically.
- [ ] Add `bumpversion` for automatic versioning and changelog management
- [ ] Add en/zh language setting
- [ ] Add `.srt` merge support (auto shift)
- [ ] Add Windows support
- [ ] Improve CLI usability
- [ ] Add GUI for better user experience

---

## 🛠️ License
This project is licensed under the MIT License.