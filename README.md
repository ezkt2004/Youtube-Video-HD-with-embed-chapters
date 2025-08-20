# YouTube Video HD Downloader with Embedded Chapters

Download YouTube videos in the highest quality possible with embedded chapters using yt-dlp.

## Features

- 🎥 Download videos in the highest available quality
- 📚 Embed chapters directly into video files
- 📝 Download subtitles and metadata
- 🖼️ Download thumbnails
- 📊 Progress tracking and error handling
- 🔧 Customizable format selection

## Requirements

- Python 3.6+
- yt-dlp
- ffmpeg (for video processing)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ezkt2004/Youtube-Video-HD-with-embed-chapters.git
cd Youtube-Video-HD-with-embed-chapters
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Make sure ffmpeg is installed:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/
```

## Usage

### Basic Usage

Download a video with embedded chapters:
```bash
python3 download_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Advanced Options

```bash
# Custom output directory
python3 download_youtube.py "URL" -o "my_videos"

# Custom format (highest quality video + audio)
python3 download_youtube.py "URL" -f "bestvideo+bestaudio/best"

# Download without chapters
python3 download_youtube.py "URL" --no-chapters

# List available formats first
python3 download_youtube.py "URL" --list-formats
```

### Command Line Options

- `-o, --output`: Output directory (default: downloads)
- `-f, --format`: Video format selector (default: bestvideo+bestaudio/best)
- `--no-chapters`: Don't embed chapters
- `--list-formats`: List available formats and exit

## Examples

### Download in highest quality with chapters:
```bash
python3 download_youtube.py "https://www.youtube.com/watch?v=cheIaehqwyM"
```

### Download specific quality:
```bash
python3 download_youtube.py "https://www.youtube.com/watch?v=cheIaehqwyM" -f "best[height<=720]"
```

## Output Files

The script downloads:
- Video file with embedded chapters (MP4/MKV)
- Video information (JSON)
- Thumbnail image
- Subtitles (SRT format)
- Video description

## Supported Formats

yt-dlp supports many formats. Common format selectors:
- `best`: Best overall quality
- `bestvideo+bestaudio/best`: Best video + best audio (recommended)
- `worst`: Lowest quality
- `best[height<=720]`: Best quality up to 720p
- `best[filesize<100M]`: Best quality under 100MB

## Troubleshooting

### yt-dlp not found
```bash
pip3 install --upgrade yt-dlp
```

### ffmpeg not found
Install ffmpeg using your system's package manager.

### Permission errors
Make sure you have write permissions to the output directory.

## License

This project is licensed under the MIT License.