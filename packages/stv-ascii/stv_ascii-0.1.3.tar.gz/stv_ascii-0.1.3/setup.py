from setuptools import setup
from pathlib import Path

# 读取README内容作为长描述
current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="stv_ascii",
    version="0.1.3",  # 保持与当前版本一致
    py_modules=["stv_ascii"],
    description="CLI tool for generating ASCII art from images/videos with GPU acceleration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="星灿长风v(StarWindv)",
    author_email="starwindv.stv@gmail.com",  # 替换为你的邮箱
    url="https://github.com/StarWindv/STv_ASCII_ART/",  # 替换为项目地址
    license="MIT",
    install_requires=[
        "tqdm",
        "pillow",
        "opencv-python",
        "numpy",
        "torch==2.5.1+cu121",  
        "torchvision==0.20.1+cu121",
    ],
    entry_points={
        "console_scripts": ["stv_ascii = stv_ascii:main"]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)
