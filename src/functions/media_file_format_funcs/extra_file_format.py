from ...classes import FolderAndFilePatterns
from ...custom_objects import MediaFile


def extra_file_format(video_file_list: list[MediaFile]) -> tuple[list[tuple[str, str]], str]:
    """
    Takes the list of video files in an Extra Folder directory and automatically generates the correct file format for
    each file that isn't formatted correctly.

    :param video_file_list: A list of video files in the Extra Folder directory
    :return: A list with each element a tuple with the following format: (old file name, new file name); and a status message of
    how many files will be updated in the directory
    """
    folder_and_files_patterns = FolderAndFilePatterns()
    unformatted_media_files = []  # A list to hold the media files that need to be updated.
    media_files_to_be_updated = []  # each element will be a tuple and each tuple will have the following format: (old file name, new file name)
    first_file_in_list = video_file_list[0]

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
    for file in video_file_list:
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
    message = f"\t-- Folder: {show_name}/{modified_folder_name}s -> # of Update Files: {len(media_files_to_be_updated)}"

    return media_files_to_be_updated, message
