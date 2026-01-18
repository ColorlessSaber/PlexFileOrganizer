import os
from ..functions import video_file_condition
from ..classes import MediaFolderData, correct_media_file_format, MediaCategory


def scan_media_folder(media_folder_path: str) -> tuple[MediaFolderData, bool]:
    """
    Scans the media folder directory and figures out if it's a TV show or movie folder, and if there are any
    extra folders. The function also validates the given directory is a media folder.

    :param media_folder_path: the folder location of the media folder to scan.
    :return: A media folder object and bool value if folder is a media folder (True if it is a media folder)
    """
    folder_and_file_patterns = correct_media_file_format.FolderAndFilePatterns()
    media_folder_information = MediaFolderData()

    media_folder_information.media_title = media_folder_path.split('/')[-1]
    media_folder_information.directory = media_folder_path

    with os.scandir(media_folder_information.directory) as directory_to_scan:
        for entry in directory_to_scan:
            if entry.name.startswith('.'): # Assuming all files starting with dot should not be checked.
                continue

            if entry.is_file() and video_file_condition(entry.path):
                media_folder_information.media_type = MediaCategory.MOVIE
            elif entry.is_dir():
                if folder_and_file_patterns.extra_folder_check(entry.name):
                    media_folder_information.extra_folders[entry.name.lower()] = True
                elif folder_and_file_patterns.tv_show_season_folder_check(entry.name):
                    # don't want to count the 'Special' season folder
                    if not entry.name.lower() == 'special':
                        media_folder_information.number_of_seasons += 1
                else:
                    pass
            else:
                pass

    # Situation when media folder is not a media folder
    if media_folder_information.media_type is MediaCategory.UNCATEGORIZED and media_folder_information.number_of_seasons == 0:
        return media_folder_information, False

    if media_folder_information.media_type is MediaCategory.UNCATEGORIZED and media_folder_information.number_of_seasons > 0:
        media_folder_information.media_type = MediaCategory.TV

    return media_folder_information, True
