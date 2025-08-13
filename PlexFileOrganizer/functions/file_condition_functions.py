def video_file_condition(file_path):
    """
    The condition that validates that the file found is a video file.

    :param file_path: The directory location of the file
    :return:
    """
    if any(file_path.endswith(file_extension) for file_extension in ['.mkv', '.mp4', '.avi']):
        return True
    else:
        return False
