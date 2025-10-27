# Changelog

## v2.1 - Audio Track Selection (Oct 27, 2025)

### New Features
- **Audio Track Selector**: Choose specific audio tracks from multi-audio videos
  - Auto-detects all available audio tracks (languages, commentary, etc.)
  - Shows detailed track info (language, codec, channels)
  - Option to use all tracks or select a specific one

### Improvements
- Better audio handling with proper stream mapping
- Refresh button to reload audio tracks
- Clear track information display

---

## v2.0 - Mac Support + Major Improvements (Oct 27, 2025)

### Platform Support
- macOS support with `.command` and `.sh` launcher files
- Automated setup script for Mac (`setup_mac.sh`)
- Cross-platform compatibility (Windows + Mac)
- Added `requirements.txt` for easy dependency management

### New Features
- **Preview Mode**: View all found instances with timestamps before creating clips
- **Progress Feedback**: Real-time progress bar during clip creation
- **Merge Clips**: Option to combine all clips into a single video
- **Smart Filenames**: Clips named with timestamps (e.g., `clip_001_00-02-15.mp4`)
- **Word-Specific Folders**: Auto-organized output in `clips_yourword/` folders
- **Default Output Folder**: Pre-filled with `~/WordClipperOutput`

### Improvements
- Comprehensive error handling for missing files, FFmpeg errors, encoding issues
- Input validation before processing
- Auto-create output directories
- Better subtitle encoding support (UTF-8 and Latin-1 fallback)
- Threading for responsive UI during processing
- Better default values (1 second pre/post time)
- Improved GUI layout and alignment

### Technical
- Added docstrings for all functions
- Better separation of concerns
- Progress callback system
- Robust FFmpeg error handling with stderr capture

---

## v1.0 - Initial Windows Release

### Features
- Basic word search in SRT subtitle files
- Video clip extraction
- Adjustable pre/post buffer time
- Simple GUI interface
- Windows batch file launcher
