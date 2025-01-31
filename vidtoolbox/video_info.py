import os
import subprocess
import argparse

def format_duration(seconds):
    """將秒數轉換為 HH:MM:SS 格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def get_file_size(file_path):
    """取得檔案大小 (MB)"""
    size_in_bytes = os.path.getsize(file_path)
    size_in_mb = size_in_bytes / (1024 * 1024)
    return size_in_mb

def get_video_info(video_directory, sort_by="name"):
    """ 獲取指定目錄內所有影片的解析度、時間長度和大小，並可排序 """
    files = [f for f in os.listdir(video_directory) if f.endswith('.mp4')]

    video_data = []
    for file in files:
        file_path = os.path.join(video_directory, file)

        # 獲取影片尺寸
        cmd_size = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height', '-of', 'csv=p=0',
            file_path
        ]
        width_height = subprocess.check_output(cmd_size).decode().strip()

        # 獲取影片時長
        cmd_duration = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'format=duration', '-of', 'csv=p=0',
            file_path
        ]
        duration = float(subprocess.check_output(cmd_duration).decode().strip())
        formatted_duration = format_duration(duration)

        # 獲取檔案大小
        file_size = get_file_size(file_path)

        video_data.append((file, width_height, formatted_duration, file_size, duration))

    # **根據使用者選擇的排序方式排列**
    if sort_by == "name":
        video_data.sort(key=lambda x: x[0])  # 按照檔名排序
    elif sort_by == "size":
        video_data.sort(key=lambda x: x[3], reverse=True)  # 按照檔案大小排序（大 → 小）
    elif sort_by == "duration":
        video_data.sort(key=lambda x: x[4], reverse=True)  # 按照影片時長排序（長 → 短）

    # **輸出結果**
    print("\n📌 影片資訊:")
    for file, width_height, formatted_duration, file_size, _ in video_data:
        print(f"影片: {file}, 尺寸: {width_height}, 時間長度: {formatted_duration}, 檔案大小: {file_size:.2f} MB")

def main():
    parser = argparse.ArgumentParser(description="獲取影片尺寸、時間長度、檔案大小，並可排序")
    parser.add_argument("video_directory", help="影片所在資料夾")
    parser.add_argument("--sort", choices=["name", "size", "duration"], default="name",
                        help="選擇排序方式: name（檔名, 預設）, size（檔案大小）, duration（影片時長）")
    
    args = parser.parse_args()
    get_video_info(args.video_directory, args.sort)

if __name__ == "__main__":
    main()
