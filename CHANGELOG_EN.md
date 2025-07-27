# Changelog

All notable changes to this project will be documented in this file.

---

## **2025/2/1**
### **v0.1.8**
- 🆕 **New Subtitle Merge Feature**:
  - Added `vid-subtitles` command to merge multiple `.srt` subtitle files
  - Automatic time shifting based on corresponding video durations
  - Sequential re-indexing of subtitle entries
  - Support for UTF-8 encoding and international characters
  - Cross-platform compatibility (Windows, macOS, Linux)
  - Interactive file order confirmation
- 🎬 **Subtitle Processing**: Uses Python `srt` package for subtitle manipulation
- 📝 **Documentation**: Added subtitle merge feature description and usage examples

### **v0.1.7**
- 🆕 **New MP3 Conversion Feature**:
  - Added `vid-mp3` command to convert video files to MP3 audio files
  - Support batch conversion of all video files in a directory
  - Adjustable MP3 quality (0-9, 0=highest quality)
  - Support recursive subdirectory search
  - Specify output directory
  - Cross-platform support (Windows, macOS, Linux)
  - Suitable for Whisper speech-to-text processing
- 🎵 **Audio Processing**: Uses ffmpeg libmp3lame encoder
- 📝 **Documentation**: Added MP3 conversion feature description and quality presets

### **v0.1.6**
- 🐛 **Fixed Chinese Path Encoding Issues**:
  - Fixed garbled characters in `file_list.txt` for Chinese paths
  - Added `encoding="utf-8"` to file write operations
  - Normalized path separators for ffmpeg compatibility
  - Improved error message display with detailed debugging information
- 🔧 **Path Handling Improvements**: Unified handling of Windows and Unix path formats

### **v0.1.5**
- 🆕 **Enhanced Video Compatibility Checking**:
  - Added automatic video specification checking before merging
  - Smart merging with re-encoding options when specifications differ
  - Quality adjustment options (CRF, audio bitrate)
  - Force merge option for incompatible videos
  - Improved error handling and user feedback
- 🔍 **Video Analysis**: Added `video_specs.py` module for detailed video analysis
- 🎬 **Smart Merging**: Automatic detection of video compatibility issues

### **v0.1.4**
- 🆕 **Cross-platform File List Generation**:
  - Added `vid-filelist` command for automatic `file_list.txt` generation
  - Added `vid-quick-merge` command for one-step video merging
  - Cross-platform path handling (Windows, macOS, Linux)
  - Support for various video file patterns
  - Interactive file selection and confirmation
- 📄 **File Management**: Automatic file list generation for ffmpeg concat operations
- 🚀 **Quick Operations**: Streamlined workflow for video merging

### **v0.1.3**
- 🐛 **Bug Fixes**:
  - Fixed file path handling issues
  - Improved error messages
  - Enhanced cross-platform compatibility

### **v0.1.2**
- 🔧 **Improvements**:
  - Better command-line interface
  - Enhanced file processing
  - Updated documentation

### **v0.1.1**
- 🆕 **Initial Features**:
  - Video information retrieval
  - YouTube chapter timestamp generation
  - Basic video merging functionality
  - Cross-platform support

### **v0.1.0**
- 🎉 **Initial Release**:
  - Basic video processing tools
  - Command-line interface
  - Documentation and examples 