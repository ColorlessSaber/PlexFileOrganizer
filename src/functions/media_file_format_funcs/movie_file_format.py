from ...custom_objects import MediaFile


def movie_file_format(video_file_list: list[MediaFile]) -> tuple[list[tuple[str, str]], str]:
    """
    Takes the list of video files in a Movie Folder directory and automatically generates the correct file format for
    each file that isn't formatted correctly.

    :param video_file_list: A list of video files in the Movie Folder directory
    :return: A list with each element a tuple with the following format: (old file name, new file name); and a status message of
    how many files will be updated in the directory
    """

    # given there is only one media file in a movie media folder, there is no need
    # to loop through the list_of_media_files.
    old_movie_file_format = video_file_list[0]

    # the correct file format for a movie media file is it's matches the folder name it is in.
    # hence why the 'new file name' is the name of the folder the file is in.
    # A '.' is not needed for the extension for .file_extension() returns the dot with the extension
    new_file_name = f"{old_movie_file_format.directory_path()}/{old_movie_file_format.folder_file_is_in()}{old_movie_file_format.file_extension()}"
    # The str() is needed to revert the MediaFile class to a string, or it will cause errors for certain situations.
    # like using os.rename.
    media_files_to_be_updated = [(str(old_movie_file_format), new_file_name)]

    # create a string message to user so they know what folder has files to be updated
    message = f"\t-- Folder: {old_movie_file_format.folder_file_is_in()} -> # of Update Files: {len(media_files_to_be_updated)}"

    return media_files_to_be_updated, message
