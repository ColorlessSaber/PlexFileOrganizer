"""
Contains functions to test if a folder or a set of folders meets the conditions.
"""
from ..classes import FolderAndFilePatterns

def default_folder_condition(_):
    """
    Allow any folder to be scanned.
    """
    return True


def skip_extra_folders(folder_name):
    """
    Skips any extra folders.

    :param folder_name: The folder to check.
    """
    folder_and_file_patterns = FolderAndFilePatterns()

    if folder_and_file_patterns.extra_folder_check(folder_name):
        return False # False for we want to skip the extra folder
    else:
        return True # True for we want to the program to proceed with the folder and its contents