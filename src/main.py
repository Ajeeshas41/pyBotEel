import sys
from pathlib import Path
sys.path.append(Path.joinpath(Path(__file__).resolve().parent, "boteel"))

from boteel.core.boteel import init


if __name__ == '__main__':
    init()
