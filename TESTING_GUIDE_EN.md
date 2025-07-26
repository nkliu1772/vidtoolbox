# 🧪 VidToolbox Local Testing Guide

This guide helps you quickly set up a local development environment and test VidToolbox features.

---

## 📋 Quick Testing Steps

### 1️⃣ **Remove existing vidtoolbox**
```bash
# Remove installed vidtoolbox
pipx uninstall vidtoolbox

# Confirm removal
pipx list | grep vidtoolbox
```

### 2️⃣ **Install local version**
```bash
# Install local version in project directory
pipx install -e .

# Confirm successful installation
pipx list | grep vidtoolbox
```

### 3️⃣ **Test if commands are available**
```bash
# Test all commands
vid-info --help
vid-merge --help
vid-timestamps --help
vid-filelist --help
vid-quick-merge --help
vid-mp3 --help
```

---

## 🚀 Feature Testing

### **Basic Feature Testing**
```bash
# 1. Video information retrieval
vid-info /path/to/video_folder

# 2. Generate timestamps
vid-timestamps /path/to/video_folder

# 3. Merge videos
vid-merge /path/to/video_folder

# 4. Generate file list
vid-filelist /path/to/video_folder

# 5. Quick merge
vid-quick-merge /path/to/video_folder

# 6. MP3 conversion
vid-mp3 /path/to/video_folder
```

### **MP3 Conversion Testing**
```bash
# Show quality presets
vid-mp3 --show-quality

# High quality conversion
vid-mp3 /path/to/video_folder -q 0

# Specify output directory
vid-mp3 /path/to/video_folder -o /path/to/output

# Recursive search
vid-mp3 /path/to/video_folder -r

# Overwrite existing files
vid-mp3 /path/to/video_folder --overwrite
```

### **File List Generation Testing**
```bash
# Basic generation
vid-filelist /path/to/video_folder

# Specify output file
vid-filelist /path/to/video_folder -o my_list.txt

# Specify file pattern
vid-filelist /path/to/video_folder -p "*.mp4"

# No sorting
vid-filelist /path/to/video_folder --no-sort

# Show merge command
vid-filelist /path/to/video_folder --show-merge-cmd
```

---

## 🧪 Automated Testing

### **Quick Test Script**
```bash
# One-click execution of all test steps (Recommended)
python simple_test_runner.py

# Or use full version (may have Unicode issues)
python quick_test.py
```

### **Individual Test Scripts**
```bash
# Test MP3 conversion functionality
python test_mp3_conversion.py

# Test multilingual documentation
python test_multilingual_docs.py

# Test file list generation
python test_file_list_auto.py

# Test encoding fixes
python test_encoding_fix.py
```

---

## 🔧 Development Mode

### **Reinstall Development Version**
```bash
# Reinstall after each code modification
pipx uninstall vidtoolbox
pipx install -e .
```

### **Check Version**
```bash
# Confirm local version is installed
pipx list | grep vidtoolbox
```

---

## 📝 Command Quick Reference

| Command | Function | Common Options |
|---------|----------|----------------|
| `vid-info` | Retrieve video information | `-o output.txt` |
| `vid-timestamps` | Generate timestamps | `-o timestamps.txt` |
| `vid-merge` | Merge videos | `-o output.mp4` |
| `vid-filelist` | Generate file list | `-o file_list.txt`, `-p "*.mp4"` |
| `vid-quick-merge` | Quick merge | `-o output.mp4`, `--keep-filelist` |
| `vid-mp3` | MP3 conversion | `-q 0`, `-o /path`, `-r`, `--overwrite` |

---

## 🐛 Troubleshooting

### **Command Not Found**
```bash
# Reinstall
pipx uninstall vidtoolbox
pipx install -e .

# Check PATH
echo $PATH
which vid-info
```

### **Permission Issues**
```bash
# Windows PowerShell (Run as Administrator)
# macOS/Linux
sudo pipx install -e .
```

### **Version Conflicts**
```bash
# Complete cleanup
pipx uninstall vidtoolbox
pipx uninstall --all
pipx install -e .
```

---

## 📚 Related Files

- `README.md` - English documentation
- `README_ZH.md` - Traditional Chinese documentation
- `CHANGELOG_EN.md` - English changelog
- `CHANGELOG_ZH.md` - Traditional Chinese changelog
- `test_*.py` - Various test scripts

---

## 💡 Tips

1. **Reinstall after each code modification**: `pipx uninstall vidtoolbox && pipx install -e .`
2. **Confirm commands are available before testing**: `vid-info --help`
3. **Use `-e` parameter** to install development version, so code changes take effect automatically
4. **Backup test data** to avoid overwriting important files during testing 