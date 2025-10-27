# Changelog

## v2.1 - Audio Track Selection (Oct 27, 2025)

### New Features
- **Audio Track Selector**: Choose specific audio tracks from videos with multiple audio streams
  - Automatically detects all available audio tracks (languages, commentary, etc.)
  - Shows track information (language, codec, channels)
  - Option to include all tracks or select a specific one
  - Useful for videos with multiple language tracks or commentary

### Improvements
- Better audio handling with stream mapping
- Refresh button to reload audio tracks if needed
- Clear track information display

## v2.0 - Mac Support + Major Improvements (Oct 27, 2025)

### Platform Support
- ✅ Added macOS support with `.command` and `.sh` launcher files
- ✅ Cross-platform compatibility maintained (Windows + Mac)
- ✅ Added `requirements.txt` for easy dependency management
- ✅ Added `.gitignore` for cleaner repository

### New Features
- **Preview Mode**: View all found instances with timestamps and subtitle context before creating clips
- **Progress Feedback**: Real-time progress bar showing clip creation status
- **Merge Clips**: Option to combine all clips into a single video file
- **Smart Filenames**: Clips now include timestamps in filename (e.g., `clip_001_00-02-15.mp4`)
- **Word-Specific Folders**: Clips organized in folders named after the search word
- **Default Output Folder**: Automatically set to `~/WordClipperOutput`
- **Better UI Layout**: Improved alignment and visual hierarchy

### Improvements
- **Error Handling**: Comprehensive error handling for:
  - Missing files
  - FFmpeg errors
  - Subtitle encoding issues (UTF-8 and Latin-1 fallback)
  - Invalid inputs
- **Input Validation**: Validates file existence before processing
- **Auto-Create Folders**: Automatically creates output directories if they don't exist
- **Better Defaults**: Pre/post time sliders default to 1 second
- **Threading**: Clip creation runs in background thread to keep UI responsive
- **Encoding Support**: Better subtitle file encoding detection
- **Better Feedback**: Clear success and error messages with details

### Technical Improvements
- Added docstrings for all functions
- Separated concerns (validation, processing, UI updates)
- Progress callback system for real-time updates
- More robust FFmpeg error handling with stderr capture
- Cleaner code structure and maintainability

### Files Structure
```
word-clipper/
├── content_finder.py           # Main Python script (improved)
├── content_clipper.command     # macOS launcher (NEW)
├── content_clipper.sh          # macOS shell script (NEW)
├── content clipper.bat         # Windows launcher (original)
├── requirements.txt            # Python dependencies (NEW)
├── README.md                   # Documentation (NEW)
├── CHANGELOG.md               # This file (NEW)
└── .gitignore                 # Git ignore file (NEW)
```

## v1.0 - Initial Windows Release

### Features
- Basic word search in SRT subtitle files
- Video clip extraction
- Adjustable pre/post buffer time
- Simple GUI interface

