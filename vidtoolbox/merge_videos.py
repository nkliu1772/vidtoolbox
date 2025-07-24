import os
import argparse
import subprocess
from typing import Tuple

from vidtoolbox.generate_timestamps import (
    generate_timestamps,
    create_file_list,
    display_timestamps,
)
from vidtoolbox.video_info import get_video_info
import shutil


def check_consistent_resolution(video_directory: str) -> Tuple[bool, str]:
    """Check if all videos share the same resolution and display info.

    Parameters
    ----------
    video_directory: str
        Directory containing ``.mp4`` files.

    Returns
    -------
    tuple
        ``(True, "")`` if all files have the same resolution. ``(False, details)``
        when a mismatch is found where ``details`` describes the offending
        files and their resolutions.
    """

    # Display basic video information for the user
    get_video_info(video_directory)

    files = [f for f in os.listdir(video_directory) if f.endswith(".mp4")]
    base_resolution = None
    mismatches = []

    for file in files:
        file_path = os.path.join(video_directory, file)
        cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "csv=p=0",
            file_path,
        ]
        output = subprocess.check_output(cmd).decode().strip()
        width, height = map(int, output.split(","))
        if base_resolution is None:
            base_resolution = (width, height)
        elif (width, height) != base_resolution:
            mismatches.append(f"{file}: {width}x{height}")

    if mismatches:
        details = "\n".join(mismatches)
        return False, details

    return True, ""


def ensure_uniform_format_resolution(video_directory: str) -> Tuple[str, str]:
    """Ensure all videos are MP4 and share the same resolution.

    If a mismatch is found, videos are converted to match the resolution of the
    first video and stored in a temporary ``converted`` directory. The path to
    the directory used for merging and the temporary directory (if any) are
    returned.
    """

    video_exts = (".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm")
    files = [f for f in os.listdir(video_directory) if f.lower().endswith(video_exts)]
    if not files:
        return video_directory, ""

    first_path = os.path.join(video_directory, files[0])
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height",
        "-of",
        "csv=p=0",
        first_path,
    ]
    output = subprocess.check_output(cmd).decode().strip()
    base_width, base_height = map(int, output.split(","))

    need_conversion = False
    for file in files:
        file_path = os.path.join(video_directory, file)
        cmd[10] = file_path  # update path in ffprobe command
        info = subprocess.check_output(cmd).decode().strip()
        width, height = map(int, info.split(","))
        if os.path.splitext(file)[1].lower() != ".mp4" or (width, height) != (
            base_width,
            base_height,
        ):
            need_conversion = True
            break

    if not need_conversion:
        return video_directory, ""

    converted_dir = os.path.join(video_directory, "converted")
    os.makedirs(converted_dir, exist_ok=True)
    print("\n⚙️ Converting videos to a uniform format and resolution...")

    for file in files:
        src = os.path.join(video_directory, file)
        dst = os.path.join(converted_dir, os.path.splitext(file)[0] + ".mp4")

        cmd = ["ffmpeg", "-i", src]
        cmd += ["-vf", f"scale={base_width}:{base_height}"]
        cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "18"]
        cmd += ["-c:a", "aac", "-b:a", "192k", dst]

        subprocess.run(cmd, check=True)

    print("✅ Conversion completed.")

    return converted_dir, converted_dir


def merge_videos(video_directory, output_file=None, keep_filelist=False, reencode=False):
    """Merge videos after ensuring consistent format and resolution."""
    folder_name = os.path.basename(os.path.normpath(video_directory))
    timestamps_path = os.path.join(video_directory, f"{folder_name}.txt")

    if os.path.exists(timestamps_path):
        print(f"\n🛑 Detected an existing `{folder_name}.txt`, regenerating...")
        os.remove(timestamps_path)

    work_dir, temp_dir = ensure_uniform_format_resolution(video_directory)

    generate_timestamps(work_dir)

    if not display_timestamps(work_dir):
        return

    # Confirm if the timestamps are correct
    confirm = input("\n✅ Confirm that the timestamps are correct? (Y/N): ").strip().lower()
    if confirm != "y":
        print("❌ Merge canceled!")
        return

    files = create_file_list(work_dir)
    if files is None:
        return

    consistent, _ = check_consistent_resolution(work_dir)
    if not consistent:
        reencode = True

    if not output_file:
        output_file = os.path.join(video_directory, f"{folder_name}.mp4")
    else:
        output_file = os.path.join(video_directory, output_file)

    # Generate file_list.txt
    file_list_path = os.path.join(work_dir, "file_list.txt")
    with open(file_list_path, "w") as f:
        for file in files:
            # Use the correct absolute path to avoid multi-directory issues
            file_path = os.path.abspath(os.path.join(work_dir, file))
            f.write(f"file '{file_path}'\n")

    print(f"\n🚀 **Starting video merge, output file:** {output_file}\n")

    if reencode:
        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", file_list_path,
            "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", output_file
        ]
    else:
        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", file_list_path, "-c", "copy", output_file
        ]
    
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"❌ Video merge failed with return code {result.returncode}")
        return

    print(f"✅ Video merge completed! Output file: {output_file}")

    if not keep_filelist:
        os.remove(file_list_path)
        print("🧹 `file_list.txt` deleted")

    if temp_dir:
        shutil.rmtree(temp_dir)

def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple videos and ensure timestamps.txt is confirmed first"
    )
    parser.add_argument("video_directory", help="Directory containing video files")
    parser.add_argument("-o", "--output", help="Output video filename (default is the folder name)")
    parser.add_argument("--keep-filelist", action="store_true", help="Keep file_list.txt")
    parser.add_argument("--reencode", action="store_true", help="Re-encode videos before merging")

    args = parser.parse_args()
    merge_videos(args.video_directory, args.output, args.keep_filelist, args.reencode)

if __name__ == "__main__":
    main()
