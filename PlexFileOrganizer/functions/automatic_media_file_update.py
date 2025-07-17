from PlexFileOrganizer.functions import MediaFile, FolderAndFilePatterns, update_file_name

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

    status_message = '' # To hold the message to print to the user. Letting them how many files where affected.
    unformatted_media_files = []  # A list to hold the media files that need to be updated.
    # for the variable below, each element will be a tuple and each tuple will have the
    # following format: (MediaFile, new file name)
    media_files_to_be_updated = []

    # take the first element from the media file list, determine what folder the file(s) are in.
    # once determined, update the media file(s) accordingly.
    first_file_in_list = list_of_media_files[0]
    if folder_and_files_patterns.tv_show_season_folder_check(first_file_in_list.path):
        #print("tv show") # for debugging

        media_files_in_season_folder = convert_elements_to_media_file_class(list_of_media_files)

        # First step is to determine if there is an media file(s) in the folder with the correct format. if so,
        # grab the highest episode number in the group of correctly formated media file(s) while placing unformatted
        # media files into a list
        highest_episode_number = 0
        for file in media_files_in_season_folder:
            if folder_and_files_patterns.tv_show_episode_pattern_check(file.file_name()):

                # a tv show episode may be multiple episode, which is why we need to check/grab both numbers
                first_episode_number = folder_and_files_patterns.tv_episode_file_format.match(file.file_name()).group('first_ep')
                second_episode_number = folder_and_files_patterns.tv_episode_file_format.match(file.file_name()).group('second_ep')
                if second_episode_number is not None:
                    if int(second_episode_number) > highest_episode_number:
                        highest_episode_number = int(highest_episode_number)
                else:
                    if int(first_episode_number) > highest_episode_number:
                        highest_episode_number = int(first_episode_number)

            else:
                unformatted_media_files.append(file)

        # now having the highest episode number, the next step is to create the correct file format name for each media files
        # that need to be updated. The directory is included to make it easer when using library os
        #
        # The correct file format for a media file in a tv show season folder is the follow:
        # show_name - sxxeyy.extension
        # xx - the season number, found by looking at the folder it is in. for Specials folder, the season number is 00.
        # yy - episode number.
        tv_show_name = first_file_in_list.path.split('/')[-3]
        season_folder = first_file_in_list.path.split('/')[-2]
        if len(season_folder.split(' ')[1]) > 1: # if the season number is greater than 9, a '0' is not appended to the start
            season_number = season_folder.split(' ')[1]
        else:
            season_number = '0' + season_folder.split(' ')[1]
        for file in unformatted_media_files:
            highest_episode_number += 1
            episode_number_string = str(highest_episode_number) if highest_episode_number > 10 else ('0' + str(highest_episode_number))
            # A '.' is not included for the extension for .file_extension() returns the dot with the extension
            new_file_name = f"{file.directory_path()}/{tv_show_name} - s{season_number}e{episode_number_string}{file.file_extension()}"
            # The str() is needed to convert the MediaFile class to a string, so it can be used by os.rename
            media_files_to_be_updated.append((str(file), new_file_name))

        # create a string message to user so they know what folder has files to be updated
        status_message = f'\t-- Folder: {tv_show_name}/{season_folder} -> # of Update Files: {len(media_files_to_be_updated)}'

    elif folder_and_files_patterns.extra_folder_check(first_file_in_list.path):
        # print("extra folder") # for debugging

        media_files_in_extra_folder = convert_elements_to_media_file_class(list_of_media_files)

        # get the name of the extra folder for checking if the files are formatted correctly
        # The removing the 's' from the folder name make the file name singular instead of plural.
        correct_file_format = media_files_in_extra_folder[0].folder_file_is_in().strip('s')

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

        # only proceed to the second step if there is files that need to be updated.
        if unformatted_media_files:
            # Now having the highest number, the next step is to create the correct file format name for each media files
            # that need to be updated. The directory is included to make it easer when using library os
            #
            # the correct file format for a media file in an extra folder is it matches the folder name and then
            # has an incremented number appended to the end of it.
            for file in unformatted_media_files:
                highest_file_number += 1
                # A '.' is not included for the extension for .file_extension() returns the dot with the extension
                new_file_name = f"{file.directory_path()}/{correct_file_format} {highest_file_number}{file.file_extension()}"
                # The str() is needed to convert the MediaFile class to a string, so it can be used by os.rename
                media_files_to_be_updated.append((str(file), new_file_name))

            # create a string message to user so they know what folder has files to be updated
            show_name = first_file_in_list.path.split('/')[-3]
            status_message = f'\t-- Folder: {show_name}/{correct_file_format}s -> # of Update Files: {len(media_files_to_be_updated)}'

    else: # movie folder
        # print('movie update') # for debugging

        # given there is only one media file in a movie media folder, there is no need
        # to loop through the list_of_media_files.
        old_movie_file_format = MediaFile(list_of_media_files[0].path)

        # the correct file format for a movie media file is it's matches the folder name it is in.
        # hence why the 'new file name' is the name of the folder the file is in.
        # A '.' is not included for the extension for .file_extension() returns the dot with the extension
        new_file_name = f"{old_movie_file_format.directory_path()}/{old_movie_file_format.folder_file_is_in()}{old_movie_file_format.file_extension()}"
        # The str() is needed to convert the MediaFile class to a string, so it can be used by os.rename
        media_files_to_be_updated.append((str(old_movie_file_format), new_file_name))

        # create a string message to user so they know what folder has files to be updated
        status_message = f'\t-- Folder: {old_movie_file_format.folder_file_is_in()} -> # of Update Files: {len(media_files_to_be_updated)}'

    # only start the process of updating the files if there is something to update. else skip
    if media_files_to_be_updated:
        update_file_name(media_files_to_be_updated)
        #print(media_files_to_be_updated) # for debugging
        return status_message
    else:
        return status_message