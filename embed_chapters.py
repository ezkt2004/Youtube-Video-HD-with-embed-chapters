#!/usr/bin/env python3
"""
Embed chapters from yt-dlp info.json into a video file using ffmpeg.
"""
import json
import sys
import os
from pathlib import Path
import subprocess

def extract_ffmetadata(info_json_path, ffmetadata_path):
    with open(info_json_path, "r") as f:
        info = json.load(f)
    chapters = info.get("chapters", [])
    if not chapters:
        print("No chapters found in info.json.")
        return False
    lines = [";FFMETADATA1"]
    for c in chapters:
        lines.append("[CHAPTER]")
        lines.append("TIMEBASE=1/1")
        lines.append(f"START={int(c['start_time'])}")
        lines.append(f"END={int(c['end_time'])}")
        lines.append(f"title={c['title']}")
    with open(ffmetadata_path, "w") as out:
        out.write("\n".join(lines))
    print(f"Chapters metadata written to {ffmetadata_path}")
    return True

def embed_chapters(video_path, ffmetadata_path, output_path):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", ffmetadata_path,
        "-map_metadata", "1",
        "-codec", "copy",
        output_path
    ]
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"✅ Chapters embedded: {output_path}")
        return True
    else:
        print(f"❌ ffmpeg failed.")
        return False

def main():
    if len(sys.argv) < 3:
        print("Usage: embed_chapters.py <video_file> <info_json>")
        sys.exit(1)
    video_file = sys.argv[1]
    info_json = sys.argv[2]
    ffmetadata = "chapters.ffmetadata"
    output_file = f"{Path(video_file).stem}_with_chapters{Path(video_file).suffix}"
    if not extract_ffmetadata(info_json, ffmetadata):
        sys.exit(1)
    if not embed_chapters(video_file, ffmetadata, output_file):
        sys.exit(1)
    print(f"Output: {output_file}")

if __name__ == "__main__":
    main()
