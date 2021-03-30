"""API for flattening folder structures"""

import os
import shutil


__all__ = [
    "flatten_tree"
]


def flatten_tree(root_dir):
    """Recursively pull all files in the root_dir out of subdirectries
    and into the root_dir.py

    Args:
        root_dir (str): Valid Directory

    Returns:
        None

    Raises:
        ValueError: If root_dir is not a valid directory.

    """
    if not os.path.isdir(root_dir):
        raise ValueError("root_dir must be a valid directory, got: {}".format(root_dir))

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            source_file = os.path.join(dirpath, filename)
            dest_file = os.path.join(root_dir, filename)
            # Move any file to the root_dir
            shutil.move(source_file, dest_file)
        if not os.listdir(dirpath):
            # if the folder is empty, delete it
            os.rmdir(dirpath)
