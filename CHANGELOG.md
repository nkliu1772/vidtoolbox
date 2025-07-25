# **Version Changelog - 2025**

## **2025/2/1**
### **v0.1.6**
- 🐛 **修復中文路徑編碼問題**：
  - 修復 `file_list.txt` 中中文路徑顯示亂碼的問題
  - 添加 `encoding="utf-8"` 到檔案寫入操作
  - 標準化路徑分隔符，確保 ffmpeg 相容性
  - 改善錯誤訊息顯示，提供更詳細的除錯資訊
- 🔧 **改進路徑處理**：統一處理 Windows 和 Unix 路徑格式

### **v0.1.5**
- 🆕 **新增影片規格檢查和智慧合併功能**：
  - 新增 `video_specs.py` 模組，自動檢查影片編碼、解析度、音訊規格
  - 智慧合併：相同規格使用快速合併，不同規格提供重新編碼選項
  - 可調整畫質設定：CRF 值和音訊位元率
  - 改善錯誤處理和使用者體驗
- 🔧 **改進合併流程**：自動檢測相容性並提供最佳合併方案
- 📝 **更新文檔**：加入智慧合併功能說明

### **v0.1.4**
- 🆕 **新增跨平台 file_list.txt 生成功能**：
  - 新增 `vid-filelist` 命令，自動生成 ffmpeg concat 所需的 file_list.txt
  - 新增 `vid-quick-merge` 命令，一步完成檔案列表生成和影片合併
  - 支援 Windows、macOS 和 Linux 跨平台使用
  - 自動處理路徑格式，確保 ffmpeg 相容性
- 🔧 **改進路徑處理**：使用 pathlib 處理跨平台路徑問題
- 📝 **更新文檔**：加入新功能的使用說明和範例

### **v0.1.3**
- 🔧 **Updated version to v0.1.3** to allow new release on PyPI.
- 🛠 **Fixed PyPI upload issue** by ensuring version number increments with each release.
- 🏷 **Added better version management workflow** to avoid duplicate uploads.

## **2025/1/31**
### **v0.1.2**
- 🎨 **Improved CLI interaction**: Now displays the merge order before confirmation.
- 🐛 **Fixed incorrect `timestamps.txt` filename**.
- 🛠 **Fixed issue with `vid-merge` when using relative paths**.

### **v0.1.1**
- 🐛 **Bug Fixes**:
  - Fixed an issue where `timestamps.txt` had incorrect filenames.
  - Fixed an issue where `vid-merge` failed to run in relative paths.

### **v0.1.0 - Initial Release**
- 🎉 **First official release**
  - `vid-info`: Retrieve video information (resolution, duration, file size).
  - `vid-timestamps`: Generate YouTube chapter timestamps.
  - `vid-merge`: Merge multiple video files.
  - 🏷 **Auto-naming for output videos**: Uses the folder name by default.
