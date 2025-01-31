import os
import argparse
import subprocess
from nk_video_toolbox.generate_timestamps import generate_timestamps, create_file_list, display_timestamps

def merge_videos(video_directory, output_file=None, keep_filelist=False):
    """ 先產生 timestamps.txt，確認後再合併影片 """
    # 確保 timestamps.txt 是最新的
    folder_name = os.path.basename(os.path.normpath(video_directory))
    timestamps_path = os.path.join(video_directory, f"{folder_name}.txt")

    if os.path.exists(timestamps_path):
        print(f"\n🛑 偵測到已存在的 `{folder_name}.txt`，將重新生成...")
        os.remove(timestamps_path)

    generate_timestamps(video_directory)  # 先生成 timestamps.txt

    # 讀取並顯示 `timestamps.txt`
    if not display_timestamps(video_directory):
        return

    # 確認時間軸是否正確
    confirm = input("\n✅ 是否確認時間軸無誤？ (Y/N): ").strip().lower()
    if confirm != "y":
        print("❌ 已取消合併！")
        return

    # 確保合併時不包含已存在的合併影片
    files = create_file_list(video_directory)
    if files is None:
        return

    # 預設影片名稱為資料夾名稱
    if not output_file:
        output_file = os.path.join(video_directory, f"{folder_name}.mp4")
    else:
        output_file = os.path.join(video_directory, output_file)

    # 產生 file_list.txt
    file_list_path = os.path.join(video_directory, "file_list.txt")
    with open(file_list_path, "w") as f:
        for file in files:
            # 使用正確的絕對路徑，避免多重資料夾錯誤
            file_path = os.path.abspath(os.path.join(video_directory, file))
            f.write(f"file '{file_path}'\n")


    print(f"\n🚀 **開始合併影片，輸出檔案:** {output_file}\n")

    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", file_list_path, "-c", "copy", output_file
    ]
    
    subprocess.run(cmd)
    print(f"✅ 影片合併完成！輸出檔案: {output_file}")

    # **自動刪除 file_list.txt**
    if not keep_filelist:
        os.remove(file_list_path)
        print("🧹 已刪除 `file_list.txt`")

def main():
    parser = argparse.ArgumentParser(description="合併多個 .mp4 影片，並確保 timestamps.txt 先被確認")
    parser.add_argument("video_directory", help="影片所在的資料夾")
    parser.add_argument("-o", "--output", help="輸出的影片檔名 (預設為資料夾名稱)")
    parser.add_argument("--keep-filelist", action="store_true", help="保留 file_list.txt")

    args = parser.parse_args()
    merge_videos(args.video_directory, args.output, args.keep_filelist)

if __name__ == "__main__":
    main()
