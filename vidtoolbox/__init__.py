"""
vidtoolbox - A simple video processing toolbox for merging, timestamping, and analyzing videos.
"""

__version__ = "0.1.7" 

# Core modules
from .video_info import get_video_info
from .generate_timestamps import generate_timestamps
from .merge_videos import merge_videos
from .generate_file_list import generate_file_list, quick_merge_command
from .quick_merge import quick_merge_videos
from .video_specs import check_video_compatibility, get_video_specs
from .convert_to_mp3 import convert_video_to_mp3, batch_convert_to_mp3, get_quality_presets
