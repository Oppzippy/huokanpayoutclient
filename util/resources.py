import sys
import os


def get_resource_path(path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        # pylint: disable=no-member,protected-access
        return os.path.join(sys._MEIPASS, path)
    return path
