"""
Contains functions to test if a file meets the conditions
"""

def video_file_condition(file):
    """
    The condition that validates that the file found is a video file.

    :param file: The file to check
    :return:
    """
    if any(file.endswith(file_extension) for file_extension in ['.mkv', '.mp4', '.avi']):
        return True
    else:
        return False
