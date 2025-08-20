#!/bin/bash

# YouTube Video Downloader with Embedded Chapters
# Simple bash script version

set -e  # Exit on error

# Default values
OUTPUT_DIR="downloads"
FORMAT="bestvideo+bestaudio/best"
EMBED_CHAPTERS=true

# Help function
show_help() {
    echo "Usage: $0 [OPTIONS] URL"
    echo ""
    echo "Download YouTube videos in highest quality with embedded chapters"
    echo ""
    echo "OPTIONS:"
    echo "  -o, --output DIR     Output directory (default: downloads)"
    echo "  -f, --format FORMAT  Video format (default: bestvideo+bestaudio/best)"
    echo "  -n, --no-chapters    Don't embed chapters"
    echo "  -l, --list-formats   List available formats"
    echo "  -h, --help          Show this help"
    echo ""
    echo "EXAMPLES:"
    echo "  $0 'https://www.youtube.com/watch?v=VIDEO_ID'"
    echo "  $0 -o my_videos 'https://www.youtube.com/watch?v=VIDEO_ID'"
    echo "  $0 -f 'best[height<=720]' 'https://www.youtube.com/watch?v=VIDEO_ID'"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        -n|--no-chapters)
            EMBED_CHAPTERS=false
            shift
            ;;
        -l|--list-formats)
            if [[ -z "$2" ]]; then
                echo "Error: URL required for --list-formats"
                exit 1
            fi
            yt-dlp --list-formats "$2"
            exit 0
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "Unknown option $1"
            show_help
            exit 1
            ;;
        *)
            URL="$1"
            shift
            ;;
    esac
done

# Check if URL is provided
if [[ -z "$URL" ]]; then
    echo "Error: YouTube URL is required"
    show_help
    exit 1
fi

# Check if yt-dlp is installed
if ! command -v yt-dlp &> /dev/null; then
    echo "Error: yt-dlp is not installed"
    echo "Install it with: pip3 install yt-dlp"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Build yt-dlp command
CMD=(
    "yt-dlp"
    "--format" "$FORMAT"
    "--output" "$OUTPUT_DIR/%(title)s.%(ext)s"
    "--write-info-json"
    "--write-description"
    "--write-thumbnail"
    "--write-auto-subs"
    "--write-subs"
    "--sub-langs" "en"
    "--convert-subs" "srt"
    "--embed-metadata"
)

if [[ "$EMBED_CHAPTERS" == true ]]; then
    CMD+=("--embed-chapters")
fi

CMD+=("$URL")

# Print command for debugging
echo "Downloading: $URL"
echo "Output directory: $OUTPUT_DIR"
echo "Format: $FORMAT"
echo "Embed chapters: $EMBED_CHAPTERS"
echo "Command: ${CMD[*]}"
echo "$(printf '%0.s-' {1..50})"

# Execute the command
"${CMD[@]}"

# Check if download was successful
if [[ $? -eq 0 ]]; then
    echo ""
    echo "✅ Download completed successfully!"
    echo "📁 Files saved to: $(realpath "$OUTPUT_DIR")"
    
    # List downloaded files
    echo ""
    echo "📄 Downloaded files:"
    find "$OUTPUT_DIR" -type f -newer . 2>/dev/null | sort | while read -r file; do
        size=$(du -h "$file" | cut -f1)
        echo "  - $(basename "$file") ($size)"
    done
else
    echo ""
    echo "❌ Download failed!"
    exit 1
fi
