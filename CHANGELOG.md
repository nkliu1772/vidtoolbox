# **Version Changelog - 2025**

## **2025/2/2**
### **v0.1.4**
- 🚀 **Added optional re-encoding in vid-merge** using the `--reencode` flag.
- 🛠 **Videos with different resolutions now trigger a prompt before merging.**

## **2025/2/3**
### **v0.1.5**
- 🚀 **Automatically converts videos with differing formats or resolutions before merging.**
- 🛠 **`--reencode` now applies only to the final output.**

## **2025/2/1**
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
