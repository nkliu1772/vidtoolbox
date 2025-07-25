import os
import subprocess
from collections import defaultdict

def get_video_specs(file_path):
    """
    獲取影片的詳細規格資訊
    
    Args:
        file_path (str): 影片檔案路徑
    
    Returns:
        dict: 包含影片規格的字典
    """
    try:
        # 獲取影片編碼資訊
        cmd_codec = [
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=codec_name,width,height,pix_fmt,bit_rate', 
            '-of', 'csv=p=0', file_path
        ]
        video_info = subprocess.check_output(cmd_codec).decode().strip().split(',')
        
        # 獲取音訊編碼資訊
        cmd_audio = [
            'ffprobe', '-v', 'error', '-select_streams', 'a:0',
            '-show_entries', 'stream=codec_name,sample_rate,channels', 
            '-of', 'csv=p=0', file_path
        ]
        audio_info = subprocess.check_output(cmd_audio).decode().strip().split(',')
        
        # 解析資訊
        if len(video_info) >= 4:
            video_codec = video_info[0] or 'unknown'
            width = video_info[1] or 'unknown'
            height = video_info[2] or 'unknown'
            pix_fmt = video_info[3] or 'unknown'
            video_bitrate = video_info[4] if len(video_info) > 4 else 'unknown'
        else:
            video_codec = width = height = pix_fmt = video_bitrate = 'unknown'
        
        if len(audio_info) >= 3:
            audio_codec = audio_info[0] or 'unknown'
            sample_rate = audio_info[1] or 'unknown'
            channels = audio_info[2] or 'unknown'
        else:
            audio_codec = sample_rate = channels = 'unknown'
        
        return {
            'video_codec': video_codec,
            'width': width,
            'height': height,
            'pix_fmt': pix_fmt,
            'video_bitrate': video_bitrate,
            'audio_codec': audio_codec,
            'sample_rate': sample_rate,
            'channels': channels,
            'resolution': f"{width}x{height}" if width != 'unknown' and height != 'unknown' else 'unknown'
        }
        
    except Exception as e:
        print(f"❌ 無法獲取影片規格: {e}")
        return None

def check_video_compatibility(video_files, video_directory):
    """
    檢查影片檔案的相容性
    
    Args:
        video_files (list): 影片檔案列表
        video_directory (str): 影片目錄路徑
    
    Returns:
        dict: 相容性檢查結果
    """
    specs_list = []
    specs_groups = defaultdict(list)
    
    print("\n🔍 檢查影片規格相容性...")
    
    for i, file in enumerate(video_files, 1):
        file_path = os.path.join(video_directory, file)
        specs = get_video_specs(file_path)
        
        if specs:
            specs_list.append((file, specs))
            
            # 創建規格組合的鍵值
            spec_key = (
                specs['video_codec'],
                specs['resolution'],
                specs['pix_fmt'],
                specs['audio_codec'],
                specs['sample_rate']
            )
            specs_groups[spec_key].append(file)
            
            print(f"  {i}. {file}")
            print(f"     影片編碼: {specs['video_codec']}, 解析度: {specs['resolution']}")
            print(f"     像素格式: {specs['pix_fmt']}, 音訊: {specs['audio_codec']} {specs['sample_rate']}Hz")
        else:
            print(f"  {i}. {file} - ❌ 無法讀取規格")
    
    # 分析相容性
    if len(specs_groups) == 1:
        # 所有影片規格相同
        return {
            'compatible': True,
            'message': '✅ 所有影片規格相同，可以使用快速合併',
            'specs': specs_list[0][1] if specs_list else None
        }
    else:
        # 影片規格不同
        print(f"\n⚠️  發現 {len(specs_groups)} 種不同的影片規格:")
        for i, (spec_key, files) in enumerate(specs_groups.items(), 1):
            print(f"  規格 {i}: {len(files)} 個檔案")
            for file in files:
                print(f"    - {file}")
        
        return {
            'compatible': False,
            'message': f'❌ 發現 {len(specs_groups)} 種不同的影片規格，需要重新編碼',
            'specs_groups': specs_groups,
            'specs_list': specs_list
        }

def get_merge_options():
    """
    獲取合併選項
    
    Returns:
        str: 使用者選擇的選項
    """
    print("\n🎯 請選擇合併方式:")
    print("  1. 重新編碼合併 (推薦，可調整畫質)")
    print("  2. 強制合併 (嘗試直接合併，可能失敗)")
    print("  3. 取消合併")
    
    while True:
        choice = input("\n請輸入選項 (1/2/3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("❌ 無效選項，請輸入 1、2 或 3")

def get_quality_settings():
    """
    獲取畫質設定
    
    Returns:
        dict: 畫質設定
    """
    print("\n🎨 畫質設定:")
    
    # CRF 值設定
    print("CRF 值 (0-51，越低畫質越好，檔案越大):")
    print("  18-23: 高畫質 (推薦)")
    print("  23-28: 中等畫質")
    print("  28-35: 較低畫質")
    
    while True:
        try:
            crf = input("請輸入 CRF 值 (預設: 18): ").strip()
            if crf == "":
                crf = 18
            else:
                crf = int(crf)
                if 0 <= crf <= 51:
                    break
                else:
                    print("❌ CRF 值必須在 0-51 之間")
        except ValueError:
            print("❌ 請輸入有效的數字")
    
    # 音訊位元率設定
    print("\n音訊位元率設定:")
    print("  128k: 較低音質")
    print("  192k: 中等音質 (推薦)")
    print("  256k: 高音質")
    print("  320k: 最高音質")
    
    while True:
        audio_bitrate = input("請輸入音訊位元率 (預設: 192k): ").strip()
        if audio_bitrate == "":
            audio_bitrate = "192k"
        if audio_bitrate.endswith('k') and audio_bitrate[:-1].isdigit():
            break
        else:
            print("❌ 請輸入有效的位元率 (例如: 192k)")
    
    return {
        'crf': crf,
        'audio_bitrate': audio_bitrate
    }

def build_ffmpeg_command(file_list_path, output_file, quality_settings):
    """
    建立 ffmpeg 命令
    
    Args:
        file_list_path (str): file_list.txt 路徑
        output_file (str): 輸出檔案路徑
        quality_settings (dict): 畫質設定
    
    Returns:
        list: ffmpeg 命令參數列表
    """
    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", file_list_path,
        "-c:v", "libx264", "-preset", "slow", 
        "-crf", str(quality_settings['crf']),
        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # 確保解析度為偶數
        "-c:a", "aac", "-b:a", quality_settings['audio_bitrate'],
        "-y",  # 覆蓋輸出檔案
        output_file
    ]
    
    return cmd

def build_force_merge_command(file_list_path, output_file):
    """
    建立強制合併的 ffmpeg 命令（使用 copy 模式）
    
    Args:
        file_list_path (str): file_list.txt 路徑
        output_file (str): 輸出檔案路徑
    
    Returns:
        list: ffmpeg 命令參數列表
    """
    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", file_list_path,
        "-c", "copy",  # 使用 copy 模式
        "-y",  # 覆蓋輸出檔案
        output_file
    ]
    
    return cmd 