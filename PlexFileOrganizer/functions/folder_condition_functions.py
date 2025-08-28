"""
Contains functions to test if a folder or a set of folders meets the conditions.
"""
from ..classes import FolderAndFilePatterns

def default_folder_condition(_):
    """
    Allow any folder to be scanned.

    :param _: Accepts a variable but does not use it.
    """
    return True

def season_and_extra_folders(folder_name):
    """
    Allow only season and extra folders to be scanned.

    :param folder_name: The folder to check.
    """
    folder_and_file_patterns = FolderAndFilePatterns()

    if folder_and_file_patterns.tv_show_season_folder_check(folder_name):
        return True
    elif folder_and_file_patterns.extra_folder_check(folder_name):
        return True
    else:
        return False

def season_and_skip_extra_folders(folder_name):
    """
    Allow only season folders to be scanned, skips extra folders.

    :param folder_name: The folder to check.
    """
    folder_and_file_patterns = FolderAndFilePatterns()

    if folder_and_file_patterns.tv_show_season_folder_check(folder_name):
        return True
    elif folder_and_file_patterns.extra_folder_check(folder_name):
        return False # False for we want to skip the extra folder
    else:
        return False