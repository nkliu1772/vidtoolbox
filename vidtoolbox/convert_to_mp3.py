import os
import argparse
import subprocess
from pathlib import Path
from collections import defaultdict

def get_audio_files(directory, pattern="*.mp4"):
    """
    獲取目錄中的音訊檔案
    
    Args:
        directory (str): 目錄路徑
        pattern (str): 檔案匹配模式
    
    Returns:
        list: 音訊檔案列表
    """
    video_dir = Path(directory)
    audio_files = list(video_dir.glob(pattern))
    
    if not audio_files:
        raise FileNotFoundError(f"在目錄 {directory} 中找不到符合 {pattern} 的檔案")
    
    return sorted(audio_files)

def convert_video_to_mp3(input_file, output_file=None, quality="2", overwrite=False):
    """
    將單個影片檔案轉換為 MP3
    
    Args:
        input_file (str): 輸入影片檔案路徑
        output_file (str): 輸出 MP3 檔案路徑（可選）
        quality (str): MP3 品質設定 (0-9，0=最高品質)
        overwrite (bool): 是否覆蓋現有檔案
    
    Returns:
        bool: 轉換是否成功
    """
    input_path = Path(input_file)
    
    # 如果沒有指定輸出檔案，使用相同檔名但副檔名為 .mp3
    if output_file is None:
        output_path = input_path.with_suffix('.mp3')
    else:
        output_path = Path(output_file)
    
    # 檢查輸出檔案是否已存在
    if output_path.exists() and not overwrite:
        print(f"⚠️  檔案已存在，跳過: {output_path.name}")
        return True
    
    # 建立 ffmpeg 命令
    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-vn",  # 不包含影片
        "-acodec", "libmp3lame",
        "-q:a", quality,
        "-y" if overwrite else "-n",  # -y 覆蓋，-n 不覆蓋
        str(output_path)
    ]
    
    try:
        print(f"🔄 轉換: {input_path.name} → {output_path.name}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 完成: {output_path.name}")
            return True
        else:
            print(f"❌ 轉換失敗: {input_path.name}")
            if result.stderr:
                print(f"錯誤: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 轉換錯誤: {e}")
        return False

def batch_convert_to_mp3(directory, pattern="*.mp4", quality="2", overwrite=False, 
                        output_directory=None, recursive=False):
    """
    批次轉換目錄中的影片檔案為 MP3
    
    Args:
        directory (str): 目錄路徑
        pattern (str): 檔案匹配模式
        quality (str): MP3 品質設定
        overwrite (bool): 是否覆蓋現有檔案
        output_directory (str): 輸出目錄（可選）
        recursive (bool): 是否遞迴搜尋子目錄
    
    Returns:
        dict: 轉換結果統計
    """
    print(f"🎵 開始批次轉換 MP3...")
    print(f"📁 目錄: {directory}")
    print(f"🔍 模式: {pattern}")
    print(f"🎨 品質: {quality}")
    print(f"🔄 遞迴: {'是' if recursive else '否'}")
    
    # 統計結果
    stats = {
        'total': 0,
        'success': 0,
        'failed': 0,
        'skipped': 0
    }
    
    try:
        # 獲取檔案列表
        if recursive:
            # 遞迴搜尋
            video_dir = Path(directory)
            audio_files = []
            for pattern_item in pattern.split(','):
                audio_files.extend(video_dir.rglob(pattern_item.strip()))
            audio_files = sorted(audio_files)
        else:
            # 只搜尋當前目錄
            audio_files = get_audio_files(directory, pattern)
        
        if not audio_files:
            print(f"❌ 找不到符合 {pattern} 的檔案")
            return stats
        
        print(f"\n📄 找到 {len(audio_files)} 個檔案:")
        for i, file_path in enumerate(audio_files, 1):
            print(f"  {i}. {file_path.name}")
        
        # 確認轉換
        confirm = input(f"\n✅ 確認轉換 {len(audio_files)} 個檔案？(Y/N): ").strip().lower()
        if confirm != "y":
            print("❌ 轉換已取消")
            return stats
        
        # 開始轉換
        print(f"\n🚀 開始轉換...")
        
        for file_path in audio_files:
            stats['total'] += 1
            
            # 決定輸出路徑
            if output_directory:
                output_dir = Path(output_directory)
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / file_path.with_suffix('.mp3').name
            else:
                output_file = file_path.with_suffix('.mp3')
            
            # 檢查是否已存在
            if output_file.exists() and not overwrite:
                print(f"⏭️  跳過已存在的檔案: {output_file.name}")
                stats['skipped'] += 1
                continue
            
            # 轉換檔案
            success = convert_video_to_mp3(
                str(file_path), 
                str(output_file), 
                quality, 
                overwrite
            )
            
            if success:
                stats['success'] += 1
            else:
                stats['failed'] += 1
        
        # 顯示結果
        print(f"\n📊 轉換完成！")
        print(f"  總計: {stats['total']}")
        print(f"  成功: {stats['success']}")
        print(f"  失敗: {stats['failed']}")
        print(f"  跳過: {stats['skipped']}")
        
        return stats
        
    except Exception as e:
        print(f"❌ 批次轉換失敗: {e}")
        return stats

def get_quality_presets():
    """
    獲取 MP3 品質預設值說明
    
    Returns:
        dict: 品質預設值說明
    """
    return {
        "0": "最高品質 (320kbps)",
        "2": "高品質 (192kbps) - 推薦",
        "4": "中等品質 (128kbps)",
        "6": "較低品質 (96kbps)",
        "8": "低品質 (64kbps)",
        "9": "最低品質 (32kbps)"
    }

def main():
    parser = argparse.ArgumentParser(description="將影片檔案轉換為 MP3 音訊檔案")
    parser.add_argument("directory", help="包含影片檔案的目錄路徑")
    parser.add_argument("-p", "--pattern", default="*.mp4", 
                        help="檔案匹配模式 (預設: *.mp4)")
    parser.add_argument("-q", "--quality", default="2", 
                        help="MP3 品質 (0-9，預設: 2)")
    parser.add_argument("-o", "--output", help="輸出目錄 (預設: 與原檔案相同目錄)")
    parser.add_argument("-r", "--recursive", action="store_true", 
                        help="遞迴搜尋子目錄")
    parser.add_argument("--overwrite", action="store_true", 
                        help="覆蓋現有檔案")
    parser.add_argument("--show-quality", action="store_true", 
                        help="顯示品質預設值說明")
    
    args = parser.parse_args()
    
    # 顯示品質預設值說明
    if args.show_quality:
        print("🎨 MP3 品質預設值:")
        presets = get_quality_presets()
        for quality, description in presets.items():
            print(f"  {quality}: {description}")
        return
    
    try:
        # 執行批次轉換
        stats = batch_convert_to_mp3(
            args.directory,
            args.pattern,
            args.quality,
            args.overwrite,
            args.output,
            args.recursive
        )
        
        if stats['success'] > 0:
            print(f"\n🎉 成功轉換 {stats['success']} 個檔案！")
        else:
            print(f"\n💥 沒有成功轉換任何檔案")
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    main() 