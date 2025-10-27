# Word Clipper

A cross-platform tool to extract video clips based on words found in subtitle files.

## Features

- 🔍 Search for words in subtitle files (SRT format)
- 🎬 Automatically create video clips for each occurrence
- 🎵 **Audio track selector** - Choose specific audio tracks (languages, commentary, etc.)
- ⏱️ Adjustable time buffers before/after each word
- 👁️ Preview found instances before creating clips
- 📊 Real-time progress feedback
- 🔗 Optional merging of all clips into one video
- 📝 Smart filenames with timestamps
- 📁 Automatic folder organization

---

## Quick Start

### macOS

**First time setup:**
```bash
./setup_mac.sh
```

**Run the tool:**
Double-click `content_clipper.command` in Finder, or:
```bash
./content_clipper.sh
```

### Windows

**First time setup:**
1. Install [ffmpeg](https://ffmpeg.org/download.html)
2. Run: `pip install -r requirements.txt`

**Run the tool:**
Double-click `content clipper.bat`

---

## Installation

### macOS Setup

**Easy Method - Automated:**
```bash
cd word-clipper
./setup_mac.sh
```

**Manual Method:**

1. Install Homebrew (if needed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install dependencies:
```bash
brew install ffmpeg python-tk
```
⚠️ **Important:** `python-tk` is required for the GUI to work on Mac!

3. Install Python packages:
```bash
/opt/homebrew/bin/python3 -m pip install --user --break-system-packages -r requirements.txt
```

### Windows Setup

1. Install [ffmpeg](https://ffmpeg.org/download.html)
2. Install Python packages:
```bash
pip install -r requirements.txt
```

---

## How to Use

1. **Select video file** - Browse for your video (MP4, MKV, AVI, etc.)
2. **Choose audio track** (optional) - Select a specific language or commentary track
3. **Select subtitle file** - Browse for your .srt subtitle file
4. **Enter search word** - Type the word or phrase you want to find
5. **Adjust output folder** (optional) - Default: `~/WordClipperOutput`
6. **Set time buffers** (optional) - Default: 1 second before/after
7. **Enable merge** (optional) - Combine all clips into one video
8. **Preview** (optional) - Click "Preview Instances" to see what you'll get
9. **Create Clips** - Click to start processing!

### Output Structure

Your clips are automatically organized:
```
~/WordClipperOutput/
└── clips_yourword/
    ├── clip_001_00-02-15.mp4  (word at 2:15)
    ├── clip_002_00-05-32.mp4  (word at 5:32)
    ├── clip_003_00-08-47.mp4  (word at 8:47)
    └── merged_yourword.mp4    (optional combined video)
```

---

## Audio Track Selection

### What Is This?

Many videos have multiple audio tracks:
- 🌍 Different languages (English, Spanish, Japanese, etc.)
- 🎙️ Commentary tracks (director's commentary, cast commentary)
- 🎵 Different audio mixes (5.1 surround, stereo)

The tool lets you choose which audio track to include in your clips!

### How It Works

1. When you select a video, tracks are automatically detected
2. A dropdown shows all available tracks:
   ```
   Track 1: eng (English) - aac 6ch
   Track 2: spa (Spanish) - aac 2ch
   Track 3: eng (Commentary) - aac 2ch
   ```
3. Choose "All audio tracks" (default) or select a specific track
4. Your clips will include only the selected audio

### Use Cases

- **Language learning**: Select only Japanese audio from a dual-language video
- **Remove commentary**: Choose main audio without director's commentary
- **Reduce file size**: Select one track instead of keeping all
- **Specific language**: Extract clips with only your target language

---

## Troubleshooting

### macOS Issues

**"macOS 26 required" or "Abort trap: 6" error**
- This is a tkinter compatibility issue
- **Fix:** Run `brew install python-tk`
- The launcher will automatically use the correct Python after installation

**"Module not found" (pysrt, ffmpeg-python)**
- **Fix:** `/opt/homebrew/bin/python3 -m pip install --user --break-system-packages -r requirements.txt`

**"ffmpeg not found"**
- **Fix:** `brew install ffmpeg`

**Permissions error on .command file**
- **Fix:** `chmod +x content_clipper.command`

### Windows Issues

**"ffmpeg not found"**
- Install ffmpeg from https://ffmpeg.org/download.html
- Make sure it's in your system PATH

**"Module not found"**
- **Fix:** `pip install -r requirements.txt`

### General Issues

**No audio tracks detected?**
- Make sure your video file has audio
- Click the "Refresh" button to rescan
- Check if the video file is corrupted

**Subtitle encoding errors**
- The tool tries UTF-8 and Latin-1 automatically
- If issues persist, convert your subtitle file to UTF-8

**Wrong audio track in clips?**
- Verify you selected the correct track before creating clips
- Use "Preview Instances" to check before processing

---

## Requirements

- **Python 3.x**
- **FFmpeg**
- **Python packages:** pysrt, ffmpeg-python (installed via requirements.txt)

---

## File Structure

```
word-clipper/
├── content_finder.py           # Main application
├── content_clipper.command     # Mac launcher (double-click)
├── content_clipper.sh          # Mac shell script
├── content clipper.bat         # Windows launcher
├── setup_mac.sh                # Mac automated setup
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── CHANGELOG.md                # Version history
└── .gitignore                  # Git ignore rules
```

---

## Tips & Tricks

💡 **Finding Rare Words**: Use preview to see how many instances exist before processing

💡 **Language Learning**: Combine word search with specific audio track selection for targeted study clips

💡 **File Size**: Select a single audio track to reduce clip file sizes by 30-50%

💡 **Batch Processing**: Search for multiple words separately - each gets its own organized folder

💡 **Time Buffers**: Increase "seconds before/after" for more context in your clips

---

## Version

Current version: **2.1**

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

---

## Support

Having issues? Check the Troubleshooting section above.

For bugs or feature requests, check the repository issues page.

---

**Enjoy creating your clips!** 🎬
