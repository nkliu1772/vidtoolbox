import os
import argparse
import subprocess
from .generate_file_list import generate_file_list, quick_merge_command

def quick_merge_videos(video_directory, output_file="output.mp4", pattern="*.mp4", 
                      sort_by_name=True, keep_filelist=False, auto_generate_list=True):
    """
    快速合併影片檔案
    
    Args:
        video_directory (str): 包含影片檔案的目錄路徑
        output_file (str): 輸出檔案名稱
        pattern (str): 檔案匹配模式
        sort_by_name (bool): 是否按檔案名稱排序
        keep_filelist (bool): 是否保留 file_list.txt
        auto_generate_list (bool): 是否自動生成 file_list.txt
    
    Returns:
        bool: 合併是否成功
    """
    try:
        # 如果指定自動生成 file_list.txt
        if auto_generate_list:
            file_list_path = generate_file_list(
                video_directory, 
                "file_list.txt", 
                pattern, 
                sort_by_name
            )
            if not file_list_path:
                print("❌ 無法生成 file_list.txt，合併取消")
                return False
        else:
            # 使用現有的 file_list.txt
            file_list_path = os.path.join(video_directory, "file_list.txt")
            if not os.path.exists(file_list_path):
                print(f"❌ 找不到 {file_list_path}")
                return False
        
        # 確保輸出檔案路徑
        if not os.path.isabs(output_file):
            output_file = os.path.join(video_directory, output_file)
        
        print(f"\n🚀 開始合併影片，輸出檔案: {output_file}")
        
        # 執行 ffmpeg 合併命令
        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0",
            "-i", file_list_path,
            "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            output_file
        ]
        
        print(f"執行命令: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 影片合併完成！輸出檔案: {output_file}")
            
            # 清理 file_list.txt（如果不需要保留）
            if not keep_filelist and auto_generate_list:
                os.remove(file_list_path)
                print("🧹 file_list.txt 已刪除")
            
            return True
        else:
            print(f"❌ 合併失敗！錯誤訊息:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 合併過程中發生錯誤: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="快速合併影片檔案")
    parser.add_argument("video_directory", help="包含影片檔案的目錄路徑")
    parser.add_argument("-o", "--output", default="output.mp4", help="輸出檔案名稱 (預設: output.mp4)")
    parser.add_argument("-p", "--pattern", default="*.mp4", help="檔案匹配模式 (預設: *.mp4)")
    parser.add_argument("--no-sort", action="store_true", help="不按檔案名稱排序")
    parser.add_argument("--keep-filelist", action="store_true", help="保留 file_list.txt")
    parser.add_argument("--use-existing-list", action="store_true", help="使用現有的 file_list.txt")
    
    args = parser.parse_args()
    
    success = quick_merge_videos(
        args.video_directory,
        args.output,
        args.pattern,
        not args.no_sort,
        args.keep_filelist,
        not args.use_existing_list
    )
    
    if success:
        print("\n🎉 所有操作完成！")
    else:
        print("\n💥 操作失敗！")

if __name__ == "__main__":
    main() 