from ..classes import FolderAndFilePatterns
from ..custom_objects import MediaFile


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

    unformatted_media_files = []  # A list to hold the media files that need to be updated.
    media_files_to_be_updated = []  # each element will be a tuple and each tuple will have the following format: (old file name, new file name)

    # take the first element from the media file list, determine what folder the file(s) are in.
    # once determined, update the media file(s) accordingly.
    first_file_in_list = class_based_video_file_list[0]
    if folder_and_files_patterns.tv_show_season_folder_check(
        first_file_in_list.folder_file_is_in()
    ):
        # print("tv show") # for debugging

        # First step is to determine if there is are media file(s) in the folder with the correct format. if so,
        # grab the highest episode number in the group of correctly formated media file(s) while placing unformatted
        # media files into a list
        highest_episode_number = 0
        for file in class_based_video_file_list:
            if folder_and_files_patterns.tv_show_episode_pattern_check(
                file.file_name()
            ):
                # a TV show episode may be multiple episode, which is why we need to check/grab both numbers
                first_episode_number = folder_and_files_patterns.tv_episode_file_format_regex_pattern.match(
                    file.file_name()
                ).group("first_ep")
                second_episode_number = folder_and_files_patterns.tv_episode_file_format_regex_pattern.match(
                    file.file_name()
                ).group("second_ep")
                if second_episode_number is not None:
                    if int(second_episode_number) > highest_episode_number:
                        highest_episode_number = int(second_episode_number)
                else:
                    if int(first_episode_number) > highest_episode_number:
                        highest_episode_number = int(first_episode_number)

            else:
                unformatted_media_files.append(file)

        # now having the highest episode number, the next step is to generate the correct file format name for each video file
        # that need to be updated. The directory is included to make it easer when using Python library os
        #
        # The correct file format for a tv show video file is the follow:
        # show_name - sxxeyy.extension
        #
        # xx - the season number, found by looking at the folder it is in. for Specials folder, the season number is 00.
        # yy - episode number.
        #
        tv_show_name = first_file_in_list.split("/")[-3]
        season_folder = first_file_in_list.folder_file_is_in()

        # If the season folder is "Specials" then the season number is 00.
        # else, grab the season number from the folder name
        if season_folder.lower() == "specials":
            season_number = "00"
        elif int(season_folder.split(" ")[1]) > 9:
            season_number = season_folder.split(" ")[1]
        else:
            season_number = "0" + season_folder.split(" ")[1]

        for file in unformatted_media_files:
            highest_episode_number += 1
            episode_number_string = (
                str(highest_episode_number)
                if highest_episode_number > 9
                else ("0" + str(highest_episode_number))
            )

            # A '.' is not needed for the extension for .file_extension() returns the dot with the extension
            new_file_name = f"{file.directory_path()}/{tv_show_name} - s{season_number}e{episode_number_string}{file.file_extension()}"

            # The str() is needed to revert the MediaFile class to a string, or it will cause errors for certain situations.
            # like using os.rename.
            media_files_to_be_updated.append((str(file), new_file_name))

        # create a string message to user so they know what folder has files to be updated
        status_message = f"\t-- Folder: {tv_show_name}/{season_folder} -> # of Update Files: {len(media_files_to_be_updated)}"

    elif folder_and_files_patterns.extra_folder_check(
        first_file_in_list.folder_file_is_in()
    ):
        # print("extra folder") # for debugging

        # get the name of the extra folder for checking if the files are formatted correctly
        # The removing the 's' from the folder name because the file name are singular.
        if first_file_in_list.folder_file_is_in().endswith("s"):
            modified_folder_name = first_file_in_list.folder_file_is_in()[:-1]
        else:
            modified_folder_name = first_file_in_list.folder_file_is_in()

        # First step is to determine if there is a media file(s) in the folder with the correct format. if so, grab
        # the highest number in the group of correctly formated media file(s) while placing unformatted media files into
        # a list
        highest_file_number = 0
        for file in class_based_video_file_list:
            if folder_and_files_patterns.extra_media_file_check(
                file.file_name(), file.folder_file_is_in()
            ):
                file_number = (
                    folder_and_files_patterns.extra_file_format_regex_pattern.match(
                        file.file_name()
                    ).group("number")
                )
                if int(file_number) > highest_file_number:
                    highest_file_number = int(file_number)
            else:
                unformatted_media_files.append(file)

        # Now having the highest number, the next step is to create the correct file format name for each media files
        # that need to be updated. The directory is included to make it easer when using Python library os
        #
        # the correct file format for a media file in an extra folder is it has the folder name followed by
        # a number that increments up by one.
        for file in unformatted_media_files:
            highest_file_number += 1
            # A '.' is not needed for the extension for .file_extension() returns the dot with the extension
            new_file_name = f"{file.directory_path()}/{modified_folder_name} {highest_file_number}{file.file_extension()}"
            # The str() is needed to revert the MediaFile class to a string, or it will cause errors for certain situations.
            # like using os.rename.
            media_files_to_be_updated.append((str(file), new_file_name))

        # create a string message to user so they know what folder has files to be updated
        show_name = first_file_in_list.split("/")[-3]
        status_message = f"\t-- Folder: {show_name}/{modified_folder_name}s -> # of Update Files: {len(media_files_to_be_updated)}"

    else:  # movie folder
        # print('movie update') # for debugging

        # given there is only one media file in a movie media folder, there is no need
        # to loop through the list_of_media_files.
        old_movie_file_format = first_file_in_list

        # the correct file format for a movie media file is it's matches the folder name it is in.
        # hence why the 'new file name' is the name of the folder the file is in.
        # A '.' is not needed for the extension for .file_extension() returns the dot with the extension
        new_file_name = f"{old_movie_file_format.directory_path()}/{old_movie_file_format.folder_file_is_in()}{old_movie_file_format.file_extension()}"
        # The str() is needed to revert the MediaFile class to a string, or it will cause errors for certain situations.
        # like using os.rename.
        media_files_to_be_updated.append((str(old_movie_file_format), new_file_name))

        # create a string message to user so they know what folder has files to be updated
        status_message = f"\t-- Folder: {old_movie_file_format.folder_file_is_in()} -> # of Update Files: {len(media_files_to_be_updated)}"

    return media_files_to_be_updated, status_message
