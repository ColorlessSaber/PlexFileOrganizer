"""
Contains functions to test if a folder or a set of folders meets the conditions.
"""

from ..classes import FolderAndFilePatterns


def default_folder_condition(_) -> bool:
    """
    Allow any folder to be scanned.

    :param _: Accepts a variable but does not use it.
    :return: Always returns True. IE, scan all folders!
    """
    return True


def skip_extra_folders(folder_name: str) -> bool:
    """
    Skip extra folders from being scanned.

    :param folder_name: The name of the folder to be checked.
    :return: A boolean indicating if the folder needs to be scanned.
    False -- skip the extra folder, True -- scan the extra folder
    """
    folder_and_file_patterns = FolderAndFilePatterns()

    if folder_and_file_patterns.extra_folder_check(folder_name):
        return False  # False for we want to skip the extra folder
    else:
        return True  # True for we want to scan the folder
