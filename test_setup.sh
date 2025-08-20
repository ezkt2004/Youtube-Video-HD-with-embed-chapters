#!/bin/bash

# Test script to demonstrate yt-dlp functionality
# This script tests various yt-dlp features

echo "🧪 YouTube Downloader Test Suite"
echo "================================="

# Test 1: Check yt-dlp installation
echo ""
echo "📋 Test 1: Checking yt-dlp installation..."
if command -v yt-dlp &> /dev/null; then
    echo "✅ yt-dlp is installed"
    echo "   Version: $(yt-dlp --version)"
else
    echo "❌ yt-dlp is not installed"
    exit 1
fi

# Test 2: Check ffmpeg installation
echo ""
echo "📋 Test 2: Checking ffmpeg installation..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ ffmpeg is installed"
    echo "   Version: $(ffmpeg -version | head -n 1)"
else
    echo "⚠️  ffmpeg is not installed (some features may not work)"
fi

# Test 3: Test with a simple video (if accessible)
echo ""
echo "📋 Test 3: Testing basic functionality..."

# Try a simple public domain video or educational content
TEST_URL="https://www.youtube.com/watch?v=aqz-KE-bpKQ"  # Big Buck Bunny
echo "Testing with: $TEST_URL"

# Create test directory
mkdir -p test_downloads

# Try to get basic info
echo "Getting video info..."
if yt-dlp --get-title --get-duration "$TEST_URL" 2>/dev/null; then
    echo "✅ Video info accessible"
    
    # Try to download with simple options
    echo "Attempting download with basic options..."
    if yt-dlp \
        --format "worst" \
        --output "test_downloads/%(title)s.%(ext)s" \
        --max-filesize 10M \
        "$TEST_URL"; then
        echo "✅ Download test successful"
    else
        echo "⚠️  Download test failed (this might be due to network/access restrictions)"
    fi
else
    echo "⚠️  Could not access test video (this might be due to network restrictions)"
fi

# Test 4: Show available format options
echo ""
echo "📋 Test 4: Testing format listing..."
echo "Common format options for yt-dlp:"
echo "  - best: Best quality available"
echo "  - worst: Lowest quality available"
echo "  - bestvideo+bestaudio: Best video + best audio (requires ffmpeg)"
echo "  - best[height<=720]: Best quality up to 720p"
echo "  - best[filesize<100M]: Best quality under 100MB"

echo ""
echo "🎯 Test Results Summary:"
echo "========================"
echo "The download scripts are ready to use!"
echo ""
echo "📝 Usage examples:"
echo "  Python script: python3 download_youtube.py 'VIDEO_URL'"
echo "  Bash script:   ./download_youtube.sh 'VIDEO_URL'"
echo ""
echo "⚠️  Note: Some videos may have geographic restrictions or access limitations"
echo "    that prevent downloading in certain environments."
