import shutil
import os


def copy_files(src: str, dst: str):
    if os.path.exists(src):
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(src=src, dst=dst)
