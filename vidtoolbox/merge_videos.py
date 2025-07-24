import os
import argparse
import subprocess
from typing import Tuple

from vidtoolbox.generate_timestamps import generate_timestamps, create_file_list, display_timestamps
from vidtoolbox.video_info import get_video_info


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


def check_consistent_resolution(video_directory):
    """Return True if all mp4 files share the same resolution."""
    files = [f for f in os.listdir(video_directory) if f.endswith(".mp4")]
    resolution = None
    for file in files:
        file_path = os.path.join(video_directory, file)
        cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "csv=p=0",
            file_path,
        ]
        output = subprocess.check_output(cmd).decode().strip()
        if resolution is None:
            resolution = output
        elif output != resolution:
            return False
    return True

def merge_videos(video_directory, output_file=None, keep_filelist=False, reencode=False):
    """Generate timestamps.txt first, confirm, and then merge videos."""
    # Ensure timestamps.txt is up-to-date
    folder_name = os.path.basename(os.path.normpath(video_directory))
    timestamps_path = os.path.join(video_directory, f"{folder_name}.txt")

    if os.path.exists(timestamps_path):
        print(f"\n🛑 Detected an existing `{folder_name}.txt`, regenerating...")
        os.remove(timestamps_path)

    generate_timestamps(video_directory)  # Generate timestamps.txt first

    # Read and display `timestamps.txt`
    if not display_timestamps(video_directory):
        return

    # Confirm if the timestamps are correct
    confirm = input("\n✅ Confirm that the timestamps are correct? (Y/N): ").strip().lower()
    if confirm != "y":
        print("❌ Merge canceled!")
        return

    # Ensure that the merged video does not include an existing merged file
    files = create_file_list(video_directory)
    if files is None:
        return

    # Check video resolutions
    consistent = check_consistent_resolution(video_directory)
    if not consistent:
        print("\n⚠️ Videos have different resolutions.")
        if not reencode:
            proceed = input("Re-encode videos before merging? (Y/N): ").strip().lower()
            if proceed != "y":
                print("❌ Merge canceled!")
                return
        reencode = True

    # Default video name is the folder name
    if not output_file:
        output_file = os.path.join(video_directory, f"{folder_name}.mp4")
    else:
        output_file = os.path.join(video_directory, output_file)

    # Generate file_list.txt
    file_list_path = os.path.join(video_directory, "file_list.txt")
    with open(file_list_path, "w") as f:
        for file in files:
            # Use the correct absolute path to avoid multi-directory issues
            file_path = os.path.abspath(os.path.join(video_directory, file))
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

    # **Automatically delete file_list.txt**
    if not keep_filelist:
        os.remove(file_list_path)
        print("🧹 `file_list.txt` deleted")

def main():
    parser = argparse.ArgumentParser(description="Merge multiple .mp4 videos and ensure timestamps.txt is confirmed first")
    parser.add_argument("video_directory", help="Directory containing video files")
    parser.add_argument("-o", "--output", help="Output video filename (default is the folder name)")
    parser.add_argument("--keep-filelist", action="store_true", help="Keep file_list.txt")
    parser.add_argument("--reencode", action="store_true", help="Re-encode videos before merging")

    args = parser.parse_args()
    merge_videos(args.video_directory, args.output, args.keep_filelist, args.reencode)

if __name__ == "__main__":
    main()
