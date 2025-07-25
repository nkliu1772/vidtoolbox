# 🆕 VidToolbox 新功能：跨平台 file_list.txt 生成

## 📋 功能概述

VidToolbox 現在支援自動生成 `file_list.txt` 檔案，讓您可以在 Windows、macOS 和 Linux 上輕鬆使用 ffmpeg 進行影片合併。

## 🚀 新功能

### 1. `vid-filelist` - 生成檔案列表
自動掃描目錄中的影片檔案並生成 ffmpeg concat 所需的 `file_list.txt`。

```bash
# 基本用法
vid-filelist /path/to/video_folder

# 指定輸出檔案名稱
vid-filelist /path/to/video_folder -o my_list.txt

# 指定檔案模式
vid-filelist /path/to/video_folder -p "*.mp4"

# 不按檔案名稱排序
vid-filelist /path/to/video_folder --no-sort

# 顯示合併命令
vid-filelist /path/to/video_folder --show-merge-cmd
```

### 2. `vid-quick-merge` - 快速合併
一步完成檔案列表生成和影片合併。

```bash
# 基本用法
vid-quick-merge /path/to/video_folder

# 指定輸出檔案名稱
vid-quick-merge /path/to/video_folder -o merged_video.mp4

# 保留 file_list.txt
vid-quick-merge /path/to/video_folder --keep-filelist

# 使用現有的 file_list.txt
vid-quick-merge /path/to/video_folder --use-existing-list
```

## 🔧 跨平台支援

### Windows 範例
```powershell
# PowerShell 中的舊方式
Get-ChildItem -Filter *.mp4 | Sort-Object Name | ForEach-Object { "file '$($_.Name)'" } > file_list.txt

# 新的跨平台方式
vid-filelist C:\Users\User\Videos\MyVideos
```

### macOS/Linux 範例
```bash
# 舊的 shell 方式
ls *.mp4 | sort | sed 's/^/file '\''/;s/$/'\''/' > file_list.txt

# 新的跨平台方式
vid-filelist /home/user/videos/my_videos
```

## 📄 生成的 file_list.txt 格式

生成的檔案會自動處理路徑格式，確保 ffmpeg 相容性：

```
file 'C:/Users/User/Videos/video_001.mp4'
file 'C:/Users/User/Videos/video_002.mp4'
file 'C:/Users/User/Videos/video_003.mp4'
```

## 🎯 使用場景

### 場景 1：快速生成檔案列表
```bash
# 進入影片目錄
cd /path/to/videos

# 生成檔案列表
vid-filelist . --show-merge-cmd

# 複製顯示的 ffmpeg 命令並執行
```

### 場景 2：一鍵合併影片
```bash
# 直接合併目錄中的所有影片
vid-quick-merge /path/to/videos -o final_video.mp4
```

### 場景 3：批次處理多個目錄
```bash
# 為多個目錄生成檔案列表
for dir in */; do
    vid-filelist "$dir" -o "${dir%/}_list.txt"
done
```

## 🔍 與現有功能的比較

| 功能 | 傳統方式 | 新功能 |
|------|----------|--------|
| 生成檔案列表 | 手動編寫腳本 | `vid-filelist` |
| 影片合併 | 需要 timestamps.txt | `vid-quick-merge` |
| 跨平台支援 | 需要不同腳本 | 統一命令 |
| 路徑處理 | 手動處理 | 自動處理 |

## 🛠️ 技術特點

- **跨平台路徑處理**：自動將 Windows 反斜線轉換為正斜線
- **絕對路徑支援**：確保 ffmpeg 可以正確找到檔案
- **檔案排序**：按檔案名稱自動排序
- **錯誤處理**：完善的錯誤檢查和提示
- **使用者確認**：顯示檔案列表供確認

## 📝 注意事項

1. 確保目錄中有 `.mp4` 檔案（或指定的檔案模式）
2. 生成的 `file_list.txt` 預設會在合併後自動刪除
3. 使用 `--keep-filelist` 選項可以保留檔案列表
4. 支援相對路徑和絕對路徑

## 🔄 升級指南

如果您之前使用手動方式生成 `file_list.txt`，現在可以：

1. 安裝最新版本的 VidToolbox
2. 將手動腳本替換為 `vid-filelist` 命令
3. 享受跨平台的一致體驗

## 📚 相關文檔

- [README.md](README.md) - 完整使用說明
- [example_usage.py](example_usage.py) - 程式碼使用範例
- [test_file_list_auto.py](test_file_list_auto.py) - 功能測試 