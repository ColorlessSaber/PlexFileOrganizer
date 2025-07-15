import re
from PlexFileOrganizer.functions import MediaFile, FolderAndFilePatterns

def automatic_media_file_update(list_of_media_files):
    """
    Takes the list of media files in a media folder and automatically updates them based on the folder they are in.
    This program also handles numbering tv shows in a season folder that already has formated files--IE, it will
    figure out the next number(s) to give to the unformatted tv show episodes.

    :param list_of_media_files: The list of media files, each one is a DirEntry object.
    :return: N/A
    """
    def convert_elements_to_media_file_class(file_list):
        """
        Converts the DirEntry to MediaFile class object
        :param file_list: The list to convert.
        :return: A new list where each element is a MediaFile class.
        """
        new_list = [MediaFile(i.path) for i in file_list]
        return new_list

    folder_and_files_patterns = FolderAndFilePatterns()

    unformatted_media_files = []  # A list to hold the media files that need to be updated.
    # for the variable below, each element will be a tuple and each tuple will have the
    # following format: (MediaFile, new file name)
    media_files_to_be_updated = []

    # take the first element from the media file list, determine what folder the file(s) are in.
    # once determined, update the media file(s) accordingly.
    first_file_in_list = list_of_media_files[0]
    if folder_and_files_patterns.tv_show_season_folder_check(first_file_in_list.path):
        print("tv show") # for debugging

        media_files_in_season_folder = convert_elements_to_media_file_class(list_of_media_files)

        # The correct file format for a media file in a tv show season folder is the follow:
        # show_name - sxxeyy.extension
        # xx - the season number, found by looking at the folder it is in. for Specials folder, the season number is 00.
        # yy - episode number, starting from 01 and up.
        #
        #
        # First step is to determine if there is an media file(s) in the folder with the correct format. if so,
        # grab the highest episode number in the group of correctly formated media file(s) while placing unformatted
        # media files into a list
        highest_episode_number = 0
        for file in media_files_in_season_folder:
            if folder_and_files_patterns.tv_show_episode_pattern_check(file.file_name()):
                continue
            else:
                unformatted_media_files.append(file)

        print(unformatted_media_files)

    elif folder_and_files_patterns.extra_folder_check(first_file_in_list.path):
        # print("extra folder") # for debugging

        media_files_in_extra_folder = convert_elements_to_media_file_class(list_of_media_files)

        # get the name of the extra folder for checking if the files are formatted correctly
        # The removing the 's' from the folder name make the file name singular instead of plural.
        correct_file_format = media_files_in_extra_folder[0].folder_file_is_in().strip('s')

        # the correct file format for a media file in an extra folder is it matches the folder name and then
        # has an incremented number appended to the end of it.
        #
        # First step is to determine if there is a media file(s) in the folder with the correct format. if so, grab
        # the highest number in the group of correctly formated media file(s) while placing unformatted media files into
        # a list
        highest_file_number = 0
        for file in media_files_in_extra_folder:
            if correct_file_format in file.file_name():
                file_number = folder_and_files_patterns.extra_media_file_format.match(file.file_name(with_extension=False)).group('number')
                if int(file_number) > highest_file_number:
                    highest_file_number = int(file_number)
            else:
                unformatted_media_files.append(file)

        # Now having the highest number, create the correct file format name for each media files that need to be updated, and
        # include the directory they are located in.
        for file in unformatted_media_files:
            highest_file_number += 1
            new_file_name = file.directory_path() + '/' + correct_file_format + ' ' + str(highest_file_number) + file.file_extension()
            media_files_to_be_updated.append((file, new_file_name))

    else: # movie folder
        # print('movie update') # for debugging

        # given there is only one media file in a movie media folder, there is no need
        # to loop through the list_of_media_files.
        old_movie_file_format = MediaFile(list_of_media_files[0].path)

        # the correct file format for a movie media file is it's matches the folder name it is in.
        # hence why the 'new file name' is the name of the folder the file is in.
        media_files_to_be_updated.append((old_movie_file_format, old_movie_file_format.folder_file_is_in()))

    # TODO add code to loop though the media_files_to_be_update and update the files
    print(media_files_to_be_updated) # for debugging

    # TODO have the function return a message of what it accomplished. Maybe also format it pretty, IE show the files updated--before / after