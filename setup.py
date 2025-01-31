from setuptools import setup, find_packages

setup(
    name="vidtoolbox",
    version="0.1",
    packages=find_packages(),
    install_requires=["ffmpeg-python"],  # 需要的依賴
    entry_points={
        "console_scripts": [
            "nk-video=nk_video_toolbox.video_info:main",
            "nk-video-merge=nk_video_toolbox.merge_videos:main",
            "nk-video-timestamps=nk_video_toolbox.generate_timestamps:main",
        ],
    },
)
