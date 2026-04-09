from ..classes import FolderAndFilePatterns
from ..custom_objects import MediaFile
from .media_file_format_funcs import (
    tv_show_file_format,
    extra_file_format,
    movie_file_format
)


def generate_correct_video_file_format(
    list_of_video_files: tuple[str],
) -> tuple[list[tuple[str, str]], str]:
    """
    Takes the list of video files in a directory and automatically generates the correct file format for each file
    that isn't formatted correctly.
    This program also handles numbering tv shows in a season folder that already has formated files--IE, it will
    figure out the next number(s) to give to the unformatted tv show episodes.

    :param list_of_video_files: A tuple list of video files in a directory
    :return: A list with each element a tuple with the following format: (old file name, new file name); and a status message of
    how many files will be updated in the directory
    """
    folder_and_files_patterns = FolderAndFilePatterns()

    # convert all strings in list to a custom object--MediaFile
    class_based_video_file_list = [MediaFile(file) for file in list_of_video_files]

    # take the first element from the media file list, determine what folder the file(s) are in.
    # once determined, update the media file(s) accordingly.
    first_file_in_list = class_based_video_file_list[0]
    if folder_and_files_patterns.tv_show_season_folder_check(
        first_file_in_list.folder_file_is_in()
    ):
        # print("tv show") # for debugging
        media_files_to_be_updated, status_message = tv_show_file_format(class_based_video_file_list)

    elif folder_and_files_patterns.extra_folder_check(
        first_file_in_list.folder_file_is_in()
    ):
        # print("extra folder") # for debugging
        media_files_to_be_updated, status_message = extra_file_format(class_based_video_file_list)

    else:  # movie folder
        # print('movie update') # for debugging

        media_files_to_be_updated, status_message = movie_file_format(class_based_video_file_list)

    return media_files_to_be_updated, status_message
