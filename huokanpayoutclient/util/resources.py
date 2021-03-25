import sys
import os


ROOT_PATH = os.path.dirname(os.path.dirname(__file__))


def get_resource_path(path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        # pylint: disable=no-member,protected-access
        return os.path.join(sys._MEIPASS, path)
    return os.path.join(ROOT_PATH, path)
