#!/usr/bin/env python3
"""
YouTube Video Downloader with Embedded Chapters
Download YouTube videos in the highest quality with embedded chapters
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def create_downloads_directory():
    """Create downloads directory if it doesn't exist"""
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)
    return downloads_dir

def download_video(url, output_dir="downloads", format_selector="best", embed_chapters=True, use_fallback=True):
    """
    Download YouTube video with the specified parameters
    
    Args:
        url (str): YouTube video URL
        output_dir (str): Output directory for downloads
        format_selector (str): Quality format selector
        embed_chapters (bool): Whether to embed chapters
        use_fallback (bool): Use fallback options for restricted videos
    """
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Build yt-dlp command
    cmd = [
        "yt-dlp",
        "--format", format_selector,
        "--output", f"{output_dir}/%(title)s.%(ext)s",
        "--write-info-json",
        "--write-description",
        "--write-thumbnail",
        "--write-auto-subs",
        "--write-subs",
        "--sub-langs", "en",
        "--convert-subs", "srt",
    ]
    
    # Add fallback options for restricted videos
    if use_fallback:
        cmd.extend([
            "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "--extractor-args", "youtube:player_client=web",
            "--ignore-errors"
        ])
    
    if embed_chapters:
        cmd.extend([
            "--embed-chapters",
            "--embed-metadata"
        ])
    
    # Add URL
    cmd.append(url)
    
    print(f"Downloading: {url}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        # Run the command
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ Download completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Download failed with error code: {e.returncode}")
        
        # Try with simplified options if first attempt failed
        if use_fallback:
            print("🔄 Trying with simplified options...")
            simplified_cmd = [
                "yt-dlp",
                "--format", "best",
                "--output", f"{output_dir}/%(title)s.%(ext)s",
                "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                url
            ]
            
            try:
                result = subprocess.run(simplified_cmd, check=True, capture_output=False)
                print(f"\n✅ Download completed with simplified options!")
                return True
            except subprocess.CalledProcessError:
                print(f"\n❌ Both attempts failed. The video might be restricted or unavailable.")
                return False
        
        return False
    except FileNotFoundError:
        print("❌ yt-dlp not found. Please install it first.")
        return False

def list_available_formats(url):
    """List available video formats for the given URL"""
    cmd = ["yt-dlp", "--list-formats", url]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Failed to list formats")
    except FileNotFoundError:
        print("yt-dlp not found")

def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos with embedded chapters")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", default="downloads", help="Output directory")
    parser.add_argument("-f", "--format", default="bestvideo+bestaudio/best", 
                       help="Video format selector (default: bestvideo+bestaudio/best)")
    parser.add_argument("--no-chapters", action="store_true", 
                       help="Don't embed chapters")
    parser.add_argument("--list-formats", action="store_true", 
                       help="List available formats and exit")
    
    args = parser.parse_args()
    
    if args.list_formats:
        list_available_formats(args.url)
        return
    
    # Download the video
    success = download_video(
        url=args.url,
        output_dir=args.output,
        format_selector=args.format,
        embed_chapters=not args.no_chapters
    )
    
    if success:
        print(f"\n📁 Files saved to: {os.path.abspath(args.output)}")
        # List downloaded files
        output_path = Path(args.output)
        if output_path.exists():
            print("\n📄 Downloaded files:")
            for file in sorted(output_path.iterdir()):
                if file.is_file():
                    size = file.stat().st_size / (1024 * 1024)  # MB
                    print(f"  - {file.name} ({size:.1f} MB)")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
