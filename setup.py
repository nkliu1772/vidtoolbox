from setuptools import setup, find_packages

setup(
    name="vidtoolbox",
    version="0.1",
    packages=find_packages(),
    install_requires=["ffmpeg-python"],  # 必要依賴
    entry_points={
        "console_scripts": [
            "vid-info=vidtoolbox.video_info:main",
            "vid-merge=vidtoolbox.merge_videos:main",
            "vid-timestamps=vidtoolbox.generate_timestamps:main",
        ],
    },
)
