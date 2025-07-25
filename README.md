# **VidToolbox**

## 📌 Introduction
**VidToolbox** is a video processing tool that supports:
- 🔍 **Retrieving video information** (resolution, duration, file size)
- 📝 **Generating YouTube chapter timestamps** (`timestamps.txt`)
- 🎬 **Merging multiple video files**
- 📄 **Automatically generating `file_list.txt` for ffmpeg concat**
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