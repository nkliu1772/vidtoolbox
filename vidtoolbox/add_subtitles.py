import os
import argparse
import subprocess
import re
from pathlib import Path
import srt
from datetime import timedelta

def get_subtitle_files(directory, pattern="*.srt"):
    subtitle_dir = Path(directory)
    subtitle_files = list(subtitle_dir.glob(pattern))
    if not subtitle_files:
        raise FileNotFoundError(f"在目錄 {directory} 中找不到符合 {pattern} 的檔案")
    return sorted(subtitle_files)

def parse_srt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return list(srt.parse(content))
    except Exception as e:
        print(f"解析字幕檔案失敗 {file_path}: {e}")
        return []

def get_subtitle_duration(subtitle_list):
    """從字幕列表計算總時長"""
    if not subtitle_list:
        return 0.0
    # 取最後一個字幕的結束時間
    last_subtitle = subtitle_list[-1]
    return last_subtitle.end.total_seconds()

def parse_timestamps_file(timestamps_file):
    """解析時間軸檔案，返回時間點列表"""
    try:
        with open(timestamps_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正則表達式匹配時間格式 HH:MM:SS
        time_pattern = r'(\d{2}:\d{2}:\d{2})'
        times = re.findall(time_pattern, content)
        
        # 轉換為秒數
        time_seconds = []
        for time_str in times:
            h, m, s = map(int, time_str.split(':'))
            total_seconds = h * 3600 + m * 60 + s
            time_seconds.append(total_seconds)
        
        return time_seconds
    except Exception as e:
        print(f"解析時間軸檔案失敗 {timestamps_file}: {e}")
        return []

def get_duration_from_timestamps(timestamps, index):
    """從時間軸計算指定索引的累積開始時間"""
    if not timestamps or index >= len(timestamps):
        return 0.0
    
    # 直接返回該索引對應的時間點（累積開始時間）
    return timestamps[index]

def get_video_duration(file_path):
    try:
        cmd = [
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'csv=p=0', str(file_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return float(result.stdout.strip())
        else:
            print(f"無法獲取影片時長 {file_path}")
            return 0.0
    except Exception as e:
        print(f"獲取影片時長失敗 {file_path}: {e}")
        return 0.0

def merge_subtitles(subtitle_files, video_files=None, timestamps_file=None, output_file=None, use_subtitle_duration=True):
    print(f"開始合併字幕檔案...")
    if not subtitle_files:
        print("沒有字幕檔案可合併")
        return False
    if output_file is None:
        first_file = Path(subtitle_files[0])
        output_file = first_file.parent / f"{first_file.parent.name}_merged.srt"
    
    # 解析時間軸檔案
    timestamps = None
    if timestamps_file and timestamps_file.exists():
        timestamps = parse_timestamps_file(timestamps_file)
        if timestamps:
            print(f"✅ 找到時間軸檔案，包含 {len(timestamps)} 個時間點")
            print(f"時間點: {[f'{t//60:.0f}:{t%60:02.0f}' for t in timestamps]}")
    
    merged_subtitles = []
    current_index = 1
    
    for i, subtitle_file in enumerate(subtitle_files):
        subtitle_list = parse_srt_file(subtitle_file)
        if not subtitle_list:
            print(f"跳過空字幕檔案: {subtitle_file.name}")
            continue
        
        # 計算時間偏移
        time_offset = timedelta(seconds=0)
        if timestamps and i < len(timestamps):
            # 使用時間軸檔案：直接使用對應的開始時間
            time_offset = timedelta(seconds=timestamps[i])
            print(f"✅ 字幕檔案 {i+1} ({subtitle_file.name}) 偏移到: {timestamps[i]//60:.0f}:{timestamps[i]%60:02.0f}")
        elif video_files and i < len(video_files):
            # 使用影片時長：累積偏移
            for j in range(i):
                video_duration = get_video_duration(video_files[j])
                if video_duration > 0:
                    time_offset += timedelta(seconds=video_duration)
            print(f"✅ 使用影片時長計算偏移: {time_offset.total_seconds():.2f} 秒")
        elif use_subtitle_duration and i > 0:
            # 使用字幕時長：累積偏移
            for j in range(i):
                prev_subtitle_list = parse_srt_file(subtitle_files[j])
                prev_subtitle_duration = get_subtitle_duration(prev_subtitle_list)
                time_offset += timedelta(seconds=prev_subtitle_duration)
            print(f"⚠️  使用字幕時長計算偏移: {time_offset.total_seconds():.2f} 秒")
        
        # 處理字幕
        for subtitle in subtitle_list:
            subtitle.start += time_offset
            subtitle.end += time_offset
            subtitle.index = current_index
            current_index += 1
            merged_subtitles.append(subtitle)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(srt.compose(merged_subtitles))
        print(f"字幕合併完成: {output_file}")
        print(f"總字幕條目數: {len(merged_subtitles)}")
        return True
    except Exception as e:
        print(f"寫入字幕檔案失敗: {e}")
        return False

def batch_merge_subtitles(directory, pattern="*.srt", video_pattern="*.mp4", timestamps_pattern="*.txt", output_file=None, confirm_order=True):
    print(f"開始批次合併字幕...")
    try:
        subtitle_files = get_subtitle_files(directory, pattern)
        video_files = None
        timestamps_file = None
        
        # 尋找時間軸檔案
        try:
            timestamps_files = get_subtitle_files(directory, timestamps_pattern)
            if timestamps_files:
                timestamps_file = timestamps_files[0]  # 使用第一個找到的時間軸檔案
                print(f"✅ 找到時間軸檔案: {timestamps_file.name} (最準確的時間計算)")
        except FileNotFoundError:
            pass
        
        # 尋找影片檔案
        try:
            video_files = get_subtitle_files(directory, video_pattern)
            if timestamps_file:
                print(f"找到 {len(video_files)} 個影片檔案 (備用)")
            else:
                print(f"找到 {len(video_files)} 個影片檔案，將使用影片時長計算時間偏移（推薦）")
        except FileNotFoundError:
            if not timestamps_file:
                print("⚠️  找不到影片檔案，將使用字幕檔案時長計算時間偏移")
                print("   注意：如果影片中有無聲片段（無字幕），可能會導致時間重疊")
                print("   建議：將對應的影片檔案或時間軸檔案放在同一目錄中以獲得準確的時間偏移")
        
        if not subtitle_files:
            print(f"找不到符合 {pattern} 的字幕檔案")
            return False
        
        print(f"\n找到 {len(subtitle_files)} 個字幕檔案:")
        for i, file_path in enumerate(subtitle_files, 1):
            print(f"  {i}. {file_path.name}")
        
        if video_files:
            print(f"\n找到 {len(video_files)} 個影片檔案:")
            for i, file_path in enumerate(video_files, 1):
                print(f"  {i}. {file_path.name}")
        
        if timestamps_file:
            print(f"\n找到時間軸檔案: {timestamps_file.name}")
        
        if confirm_order:
            confirm = input(f"\n確認合併 {len(subtitle_files)} 個字幕檔案？(Y/N): ").strip().lower()
            if confirm != "y":
                print("合併已取消")
                return False
        
        success = merge_subtitles(subtitle_files, video_files, timestamps_file, output_file)
        if success:
            print(f"\n成功合併 {len(subtitle_files)} 個字幕檔案！")
        else:
            print(f"\n字幕合併失敗")
        return success
    except Exception as e:
        print(f"批次合併失敗: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="合併 .srt 字幕檔案")
    parser.add_argument("directory", help="包含字幕檔案的目錄路徑")
    parser.add_argument("-p", "--pattern", default="*.srt", help="字幕檔案匹配模式 (預設: *.srt)")
    parser.add_argument("-v", "--video-pattern", default="*.mp4", help="影片檔案匹配模式 (預設: *.mp4)")
    parser.add_argument("-o", "--output", help="輸出檔案路徑 (預設: 目錄名_merged.srt)")
    parser.add_argument("--no-confirm", action="store_true", help="不確認檔案順序")
    args = parser.parse_args()
    try:
        success = batch_merge_subtitles(
            args.directory,
            args.pattern,
            args.video_pattern,
            "*.txt",  # timestamps_pattern
            args.output,
            not args.no_confirm
        )
        if success:
            print(f"\n字幕合併完成！")
        else:
            print(f"\n字幕合併失敗")
    except Exception as e:
        print(f"錯誤: {e}")

if __name__ == "__main__":
    main()
