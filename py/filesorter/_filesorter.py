"""API for sorting files in a directory into logical subfolders by date"""

from datetime import datetime
import enum
import errno
import logging
import os
import shutil
import sys


class DATE_ENUM(enum.Enum):
    HOUR = 1
    DAY = 2
    MONTH = 3
    YEAR = 4


def collect_file_info(root_dir, recursive=False, _file_dict=None):
    """Collect data on each file in the supplied root_dir

    Args:
        root_dir (str): valid directory path
        recursive (bool, optional): If true will traverse the tree from the
            supplied root_dir in

    Returns:
        dict: dictionary with sub-dictionaries for each file in the root_dir

    Raises:
        ValueError: If supplied root_dir is not a valid directroy

    """
    if not os.path.isdir(root_dir):
        raise ValueError("root_dir must be a valid directory")
    
    if _file_dict is None:
        _file_dict = {}

    for filename in os.listdir(root_dir):
        if not os.path.isdir(os.path.join(root_dir, filename)):
            sub_dict = {}
            sub_dict['filename'] = filename
            sub_dict['filepath'] = root_dir
            full_filepath = os.path.join(root_dir, filename)
            date_time = datetime.fromtimestamp(os.path.getmtime(full_filepath))
            sub_dict['datetime'] = date_time
            _file_dict[filename] = sub_dict
        else:
            if recursive:
                sub_root = os.path.join(root_dir, filename)
                collect_file_info(sub_root, recursive=recursive, _file_dict=_file_dict)
    return _file_dict


def _get_file_sort_folder_name(file_info_dict, sort_by):
    """Logic for concatenating a folder named according to a supplied DATE_ENUM."""
    file_datetime = file_info_dict.get('datetime')
    assert file_datetime, "No 'datetime' entry in supplied file_info_dict"

    if sort_by == DATE_ENUM.HOUR:
        return "{}-{}".format(file_datetime.date(), file_datetime.hour)
    elif sort_by == DATE_ENUM.DAY:
        return str(file_datetime.date())
    elif sort_by == DATE_ENUM.MONTH:
        return "{}-{}".format(file_datetime.year, file_datetime.month)
    elif sort_by == DATE_ENUM.YEAR:
        return str(file_datetime.year)


def organize_files_by_creation_date(file_info_dict, sort_by=DATE_ENUM.MONTH):
    """Sort all files in the provided info_dict according to the supplied sort_by enum

    Args:
        file_info_dict (dict): Dict with file info. See collect_file_info.
        sort_by (Enum, optional): See DATE_ENUM. Defaults to DATE_ENUM.MONTH.

    Returns:
        None

    Raises:
        ValueError: If supplied value for sort_by is not a DATE_ENUM.

    See Also:
        collect_file_info

    """
    if not isinstance(sort_by, DATE_ENUM):
        raise ValueError("Value for sort_by must be a DATE_ENUM")

    for _, file_info in file_info_dict.items():
        print("file_info: {}".format(file_info))
        print("type: {}".format(type(file_info)))
        sort_folder_name = _get_file_sort_folder_name(file_info, sort_by)
        sort_folder = os.path.join(file_info.get('filepath'), sort_folder_name)
        ensure_path(sort_folder)
        source_file = os.path.join(file_info.get('filepath'), file_info.get('filename'))
        dest_file = os.path.join(sort_folder, file_info.get('filename'))
        shutil.move(source_file, dest_file)


def ensure_path(directory):
    """Function to ensure a directory exists without raising an exception.

    Args:
        directory (str): directory path to create

    Returns:
        bool: True if successful

    Raises:
        OSError

    """
    try:
        os.makedirs(directory)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise OSError(exc)
    return True
    