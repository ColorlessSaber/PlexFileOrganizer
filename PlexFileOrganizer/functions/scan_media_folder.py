import os
from ..functions import video_file_condition
from ..classes import ModifiedMediaFolder, correct_media_file_format


def scan_media_folder(media_folder_path: str) -> tuple[ModifiedMediaFolder, str]:
    """
    Scans the media folder directory and figures out if it's a TV show or movie folder, and if there are any
    extra folders. The function also validates the given directory is a media folder.

    :param media_folder_path: the folder location of the media folder to scan.
    :return: A tuple of the media folder object and an error message, if any were found.
    """
    folder_and_file_patterns = correct_media_file_format.FolderAndFilePatterns()
    media_folder_information = ModifiedMediaFolder()

    media_folder_information.directory = media_folder_path

    with os.scandir(media_folder_information.directory) as directory_to_scan:
        for entry in directory_to_scan:
            if entry.is_file() and video_file_condition(entry.path) and not entry.name.startswith('.'):
                media_folder_information.movie_or_tv = 'movie'
            elif entry.is_dir():
                if folder_and_file_patterns.extra_folder_check(entry.name):
                    media_folder_information.extra_folders[entry.name.lower()] = True
                elif folder_and_file_patterns.tv_show_season_folder_check(entry.name):
                    media_folder_information.number_of_seasons += 1
                else:
                    pass
            else:
                pass

    if media_folder_information.movie_or_tv is None and media_folder_information.number_of_seasons > 0:
        media_folder_information.movie_or_tv = 'tv'

    if media_folder_information.movie_or_tv is None and media_folder_information.number_of_seasons == 0:
        return media_folder_information, "not media folder"

    return media_folder_information, "no error"
