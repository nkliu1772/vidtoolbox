import os
import argparse
import glob
from pathlib import Path

def generate_file_list(video_directory, output_file="file_list.txt", pattern="*.mp4", sort_by_name=True):
    """
    自動生成 file_list.txt 檔案，用於 ffmpeg concat 功能
    
    Args:
        video_directory (str): 包含影片檔案的目錄路徑
        output_file (str): 輸出的檔案名稱，預設為 "file_list.txt"
        pattern (str): 檔案匹配模式，預設為 "*.mp4"
        sort_by_name (bool): 是否按檔案名稱排序，預設為 True
    
    Returns:
        str: 生成的 file_list.txt 檔案路徑
    """
    # 確保目錄存在
    if not os.path.exists(video_directory):
        raise FileNotFoundError(f"目錄不存在: {video_directory}")
    
    # 使用 pathlib 來處理跨平台路徑
    video_dir = Path(video_directory)
    
    # 搜尋符合模式的影片檔案
    video_files = list(video_dir.glob(pattern))
    
    if not video_files:
        raise FileNotFoundError(f"在目錄 {video_directory} 中找不到符合 {pattern} 的檔案")
    
    # 按檔案名稱排序（如果需要）
    if sort_by_name:
        video_files.sort(key=lambda x: x.name)
    
    # 顯示找到的檔案
    print(f"\n📁 在目錄中找到 {len(video_files)} 個影片檔案:")
    for i, file_path in enumerate(video_files, 1):
        print(f"  {i}. {file_path.name}")
    
    # 確認檔案順序
    confirm = input(f"\n✅ 確認檔案順序並生成 {output_file}？(Y/N): ").strip().lower()
    if confirm != "y":
        print("❌ 取消生成 file_list.txt")
        return None
    
    # 生成 file_list.txt 的路徑
    file_list_path = video_dir / output_file
    
    # 寫入 file_list.txt
    with open(file_list_path, "w", encoding="utf-8") as f:
        for file_path in video_files:
            # 使用絕對路徑，確保 ffmpeg 可以正確找到檔案
            absolute_path = file_path.resolve()
            # 在 Windows 上，將反斜線轉換為正斜線，確保 ffmpeg 相容性
            normalized_path = str(absolute_path).replace("\\", "/")
            f.write(f"file '{normalized_path}'\n")
    
    print(f"\n✅ 成功生成 {file_list_path}")
    print(f"📄 檔案內容預覽:")
    
    # 顯示生成的內容
    with open(file_list_path, "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
    
    return str(file_list_path)

def quick_merge_command(file_list_path, output_name="output.mp4"):
    """
    生成快速合併的 ffmpeg 命令
    
    Args:
        file_list_path (str): file_list.txt 的檔案路徑
        output_name (str): 輸出檔案名稱
    
    Returns:
        str: ffmpeg 命令字串
    """
    cmd = f'ffmpeg -f concat -safe 0 -i "{file_list_path}" -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 192k "{output_name}"'
    return cmd

def main():
    parser = argparse.ArgumentParser(description="自動生成 file_list.txt 檔案，用於 ffmpeg 影片合併")
    parser.add_argument("video_directory", help="包含影片檔案的目錄路徑")
    parser.add_argument("-o", "--output", default="file_list.txt", help="輸出的檔案名稱 (預設: file_list.txt)")
    parser.add_argument("-p", "--pattern", default="*.mp4", help="檔案匹配模式 (預設: *.mp4)")
    parser.add_argument("--no-sort", action="store_true", help="不按檔案名稱排序")
    parser.add_argument("--show-merge-cmd", action="store_true", help="顯示合併命令")
    
    args = parser.parse_args()
    
    try:
        file_list_path = generate_file_list(
            args.video_directory,
            args.output,
            args.pattern,
            not args.no_sort
        )
        
        if file_list_path and args.show_merge_cmd:
            print(f"\n🚀 合併命令:")
            merge_cmd = quick_merge_command(file_list_path)
            print(merge_cmd)
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    main() 