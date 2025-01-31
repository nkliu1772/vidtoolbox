import os
import argparse
import subprocess

def format_duration(seconds):
    """將秒數轉換為 HH:MM:SS 格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def create_file_list(video_directory):
    """ 取得影片檔案並顯示順序，讓使用者確認 """
    files = sorted([f for f in os.listdir(video_directory) if f.endswith('.mp4')])

    print("\n📌 時間軸將使用以下影片順序:")
    for index, file in enumerate(files, start=1):
        print(f"  {index}. {file}")

    confirm = input("\n✅ 是否確認順序？ (Y/N): ").strip().lower()
    if confirm != "y":
        print("❌ 已取消時間軸生成！")
        return None
    return files

def generate_timestamps(video_directory):
    """ 根據影片時長生成 YouTube 章節時間戳記 """
    files = create_file_list(video_directory)
    if files is None:
        return

    timestamps = []
    total_time = 0  # 累計時間

    for file in files:
        file_path = os.path.join(video_directory, file)

        # 取得影片時長
        cmd_duration = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'format=duration', '-of', 'csv=p=0',
            file_path
        ]
        duration = float(subprocess.check_output(cmd_duration).decode().strip())

        # 格式化時間
        timestamp = format_duration(total_time)
        chapter_name = os.path.splitext(file)[0]  # 去掉 .mp4 副檔名
        timestamps.append(f"{timestamp} - {chapter_name}")

        # 更新累計時間
        total_time += duration

    # 預設名稱為資料夾名稱
    folder_name = os.path.basename(os.path.normpath(video_directory))
    output_timestamps = os.path.join(video_directory, f"{folder_name}.txt")

    # 寫入 `timestamps.txt`
    with open(output_timestamps, "w", encoding="utf-8") as f:
        f.write("\n".join(timestamps))

    print(f"\n✅ YouTube 章節時間戳記已生成: {output_timestamps}")

def display_timestamps(video_directory):
    """ 讀取並顯示 timestamps.txt 的內容 """
    folder_name = os.path.basename(os.path.normpath(video_directory))
    timestamps_path = os.path.join(video_directory, f"{folder_name}.txt")

    if not os.path.exists(timestamps_path):
        print("\n❌ 找不到 `timestamps.txt`，請確認是否已經生成。")
        return False

    print("\n📌 以下是時間軸內容:")
    with open(timestamps_path, "r", encoding="utf-8") as f:
        print(f.read())  # 直接顯示內容

    return True

def main():
    parser = argparse.ArgumentParser(description="單獨產生 YouTube 章節時間戳記")
    parser.add_argument("video_directory", help="影片所在的資料夾")
    
    args = parser.parse_args()
    generate_timestamps(args.video_directory)

if __name__ == "__main__":
    main()
