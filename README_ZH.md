# **VidToolbox**

[English](README.md) | [繁體中文](README_ZH.md)

📋 **更新日誌**: [English](CHANGELOG_EN.md) | [繁體中文](CHANGELOG_ZH.md)

🧪 **測試指南**: [English](TESTING_GUIDE_EN.md) | [繁體中文](TESTING_GUIDE.md)

## 📌 簡介
**VidToolbox** 是一個影片處理工具，支援：
- 🔍 **檢索影片資訊** (解析度、時長、檔案大小)
- 📝 **生成 YouTube 章節時間戳記** (`timestamps.txt`)
- 🎬 **合併多個影片檔案**
- 📄 **自動生成 `file_list.txt` 用於 ffmpeg 串接**
- 🔍 **影片相容性檢查和智慧合併**
- 🎵 **將影片轉換為 MP3 音訊檔案**
- 🏷️ **根據資料夾名稱自動命名輸出檔案**

此工具可在 **Windows**、**macOS** 和 **Linux** 上運行，使用 `ffmpeg` 進行影片處理。

---

## ⚡ 安裝

### 1️⃣ **安裝 `ffmpeg`** (如果尚未安裝)
```bash
brew install ffmpeg  # macOS (Homebrew)
sudo apt install ffmpeg  # Ubuntu / Debian
```

### 2️⃣ **使用 `pipx` 安裝 VidToolbox (推薦)**
```bash
pipx install --force git+https://github.com/nkliu1772/vidtoolbox.git
```

如果尚未安裝 `pipx`，請執行：

```bash
# macOS (使用 Homebrew)
brew install pipx
pipx ensurepath

# 其他系統
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

---

## 🚀 使用方法

### **1️⃣ 取得影片資訊**
```bash
vid-info /path/to/video_folder
```
🔹 顯示解析度、時長和檔案大小。

### **2️⃣ 生成 YouTube 章節時間戳記**
```bash
vid-timestamps /path/to/video_folder
```
🔹 建立 `timestamps.txt` 並提示使用者確認。

### **3️⃣ 合併影片**
```bash
vid-merge /path/to/video_folder
```
🔹 在合併影片前確認時間戳記。

🔹 **智慧合併**：自動檢查影片相容性，如有需要會提供重新編碼選項。

🔹 預設輸出檔案名稱是**資料夾名稱**，但您可以使用 `-o` 指定輸出檔案：
```bash
vid-merge /path/to/video_folder -o output.mp4
```

### **4️⃣ 為 FFmpeg 串接生成檔案列表**
```bash
vid-filelist /path/to/video_folder
```
🔹 自動生成 ffmpeg 串接操作所需的 `file_list.txt`。

🔹 選項：
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

### **5️⃣ 快速合併影片**
```bash
vid-quick-merge /path/to/video_folder
```
🔹 自動生成 `file_list.txt` 並一步完成影片合併。

🔹 選項：
```bash
# 指定輸出檔案名稱
vid-quick-merge /path/to/video_folder -o merged_video.mp4

# 保留 file_list.txt
vid-quick-merge /path/to/video_folder --keep-filelist

# 使用現有的 file_list.txt
vid-quick-merge /path/to/video_folder --use-existing-list
```

### **6️⃣ 將影片轉換為 MP3**
```bash
vid-mp3 /path/to/video_folder
```
🔹 將影片檔案轉換為 MP3 音訊檔案，適用於轉錄或音訊處理。

🔹 選項：
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

🔹 **品質預設值**：
- `0`: 最高品質 (320kbps)
- `2`: 高品質 (192kbps) - 推薦
- `4`: 中等品質 (128kbps)
- `6`: 較低品質 (96kbps)
- `8`: 低品質 (64kbps)
- `9`: 最低品質 (32kbps)

---

## 📌 待辦事項
- [ ] 添加 `--output` 參數以允許指定輸出目錄
- [ ] 添加自動合併所有子目錄中影片的選項
- [ ] 添加 `bumpversion` 用於自動版本控制和更新日誌管理
- [ ] 添加中英文語言設定
- [ ] 添加 `.srt` 合併支援 (自動位移)
- [ ] 添加 Windows 支援
- [ ] 改善命令列介面易用性
- [ ] 添加圖形使用者介面以提供更好的使用者體驗

---

## 🛠️ 授權
本專案採用 MIT 授權條款。 