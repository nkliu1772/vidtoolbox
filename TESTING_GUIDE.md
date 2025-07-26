# 🧪 VidToolbox 本地測試指南

這個指南幫助您快速設置本地開發環境並測試 VidToolbox 功能。

---

## 📋 快速測試步驟

### 1️⃣ **移除現有的 vidtoolbox**
```bash
# 移除已安裝的 vidtoolbox
pipx uninstall vidtoolbox

# 確認已移除
pipx list | grep vidtoolbox
```

### 2️⃣ **安裝本地版本**
```bash
# 在專案目錄中安裝本地版本
pipx install -e .

# 確認安裝成功
pipx list | grep vidtoolbox
```

### 3️⃣ **測試命令是否可用**
```bash
# 測試所有命令
vid-info --help
vid-merge --help
vid-timestamps --help
vid-filelist --help
vid-quick-merge --help
vid-mp3 --help
```

---

## 🚀 功能測試

### **基本功能測試**
```bash
# 1. 影片資訊檢索
vid-info /path/to/video_folder

# 2. 生成時間戳記
vid-timestamps /path/to/video_folder

# 3. 合併影片
vid-merge /path/to/video_folder

# 4. 生成檔案列表
vid-filelist /path/to/video_folder

# 5. 快速合併
vid-quick-merge /path/to/video_folder

# 6. MP3 轉換
vid-mp3 /path/to/video_folder
```

### **MP3 轉換測試**
```bash
# 顯示品質預設值
vid-mp3 --show-quality

# 高品質轉換
vid-mp3 /path/to/video_folder -q 0

# 指定輸出目錄
vid-mp3 /path/to/video_folder -o /path/to/output

# 遞迴搜尋
vid-mp3 /path/to/video_folder -r

# 覆蓋現有檔案
vid-mp3 /path/to/video_folder --overwrite
```

### **檔案列表生成測試**
```bash
# 基本生成
vid-filelist /path/to/video_folder

# 指定輸出檔案
vid-filelist /path/to/video_folder -o my_list.txt

# 指定檔案模式
vid-filelist /path/to/video_folder -p "*.mp4"

# 不排序
vid-filelist /path/to/video_folder --no-sort

# 顯示合併命令
vid-filelist /path/to/video_folder --show-merge-cmd
```

---

## 🧪 自動化測試

### **快速測試腳本**
```bash
# 一鍵執行所有測試步驟 (推薦)
python simple_test_runner.py

# 或使用完整版本 (可能會有 Unicode 問題)
python quick_test.py
```

### **個別測試腳本**
```bash
# 測試 MP3 轉換功能
python test_mp3_conversion.py

# 測試多語言文檔
python test_multilingual_docs.py

# 測試檔案列表生成
python test_file_list_auto.py

# 測試編碼修復
python test_encoding_fix.py
```

---

## 🔧 開發模式

### **重新安裝開發版本**
```bash
# 每次修改程式碼後重新安裝
pipx uninstall vidtoolbox
pipx install -e .
```

### **檢查版本**
```bash
# 確認安裝的是本地版本
pipx list | grep vidtoolbox
```

---

## 📝 常用命令速查

| 命令 | 功能 | 常用選項 |
|------|------|----------|
| `vid-info` | 檢索影片資訊 | `-o output.txt` |
| `vid-timestamps` | 生成時間戳記 | `-o timestamps.txt` |
| `vid-merge` | 合併影片 | `-o output.mp4` |
| `vid-filelist` | 生成檔案列表 | `-o file_list.txt`, `-p "*.mp4"` |
| `vid-quick-merge` | 快速合併 | `-o output.mp4`, `--keep-filelist` |
| `vid-mp3` | MP3 轉換 | `-q 0`, `-o /path`, `-r`, `--overwrite` |

---

## 🐛 故障排除

### **命令找不到**
```bash
# 重新安裝
pipx uninstall vidtoolbox
pipx install -e .

# 檢查 PATH
echo $PATH
which vid-info
```

### **權限問題**
```bash
# Windows PowerShell (以管理員身份運行)
# macOS/Linux
sudo pipx install -e .
```

### **版本衝突**
```bash
# 完全清理
pipx uninstall vidtoolbox
pipx uninstall --all
pipx install -e .
```

---

## 📚 相關檔案

- `README.md` - 英文說明文檔
- `README_ZH.md` - 繁體中文說明文檔
- `CHANGELOG_EN.md` - 英文更新日誌
- `CHANGELOG_ZH.md` - 繁體中文更新日誌
- `test_*.py` - 各種測試腳本

---

## 💡 提示

1. **每次修改程式碼後**都要重新安裝：`pipx uninstall vidtoolbox && pipx install -e .`
2. **測試前確認**命令可用：`vid-info --help`
3. **使用 `-e` 參數**安裝開發版本，這樣修改程式碼後會自動生效
4. **備份測試資料**，避免測試時覆蓋重要檔案 