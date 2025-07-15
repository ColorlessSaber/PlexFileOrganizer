import re

class FolderAndFilePatterns:
    """
    Contains regex expressions to check to see if media file is in an extra folder or a tv show season folder, and if the
    media file is properly name for the folder they are in.
    """
    movie_file_format = re.compile(r"""
                                    ^(?P<title>.+)   # group 1: the name of the file
                                    (?P<ext>\.\w+) # group 2: file extension
                                    """, re.VERBOSE | re.IGNORECASE)

    extra_media_file_format = re.compile(r"""
                                            ^(?P<title>.+) # group 1: the name of the file
                                            (?P<number>\d+) # group 2: the number of the file
                                            """, re.VERBOSE | re.IGNORECASE)

    # tv episode format is as follows: name_of_show - sxxeyy
    # xx - the season number. For Specials folder, the season number is 00
    # yy - episode number
    #
    # The format has two groups to make is easy to grab the episode number(s) from an existing episode media file.
    tv_episode_file_format = re.compile(r"""
                                    ^.+   # wildcard to handle name of show
                                    \s-\s # dash between name of show and season and episode number
                                    s\d+  # season number
                                    e(?P<first_ep>\d+)  # episode number
                                    (-e(?P<second_ep>\d+))?  # possible multiple episode number
                                    \.\w+ # file extension
                                    """, re.VERBOSE | re.IGNORECASE)

    def tv_show_episode_pattern_check(self, file_name):
        """
        Checks to see if the given media file matches the correct tv show episode format
        
        :param file_name: the file name to check against
        :return: A Bool value. True - media file is formatted correctly for tv show folder. False - media file is
        not formatted correctly for tv show folder.
        """

        if self.tv_episode_file_format.match(file_name):
            return True
        else:
            return False

    def movie_pattern_check(self, file_name, file_path):
        """
        The regex expression for the correct movie media file name.
        
        :param file_name: the file name to check against
        :param file_path: The absolute path to the file
        :return: The regex expression to check against file.
        """

        if self.movie_file_format.match(file_name).group('title') == file_path.split('/')[-2]:
            return True
        else:
            return False

    def tv_show_season_folder_check(self, file_path):
        """
        Checks the given file's path to see if it is in a tv show folder or not.

        :param file_path: The absolute path to the file
        :return: Bool value. True - file is in a tv show season folder, false - file is not in a tv show season folder
        """
        # tv show season folders come in two types: Season # and Specials. Hence, the checking for two patterns.
        if re.match(r'^(Season\s\d)|(Specials)$', file_path.split('/')[-2], re.IGNORECASE):
            return True
        else:
            return False

    def extra_folder_check(self, file_path):
        """
        Checks the given file's path to see if it is in an extra folder or not.

        :param file_path: The absolute path to the file
        :return: Bool value. True - file is in an extra folder, false - file is not in an extra folder
        """
        extra_folder_format = [
            r"trailers$",
            r"behind the scenes$",
            r"deleted scenes$",
            r"featurettes$",
            r"interviews$",
            r"scenes$",
            r"shorts$",
            r"other$"
        ]
        # run through the list above against the directory path for a match
        extra_folder_format_check_results = [re.match(pattern, file_path.split('/')[-2], re.IGNORECASE) for pattern in extra_folder_format]
        if any(extra_folder_pattern_match for extra_folder_pattern_match in extra_folder_format_check_results):
            return True
        else:
            return False

def check_files_in_media_folder(media_file_list):
    """
    Checks if the media files in the given list are all formated correctly for tv show or movie folder they are in.

    :param media_file_list: a list where each element is an DirEntry object of media file to check
    :return: Bool value. True -- all media files in folder are formated correctly. False -- at lest one media file in the folder isn't formated correctly
    """
    folder_and_file_patterns = FolderAndFilePatterns()
    for file in media_file_list:
        if folder_and_file_patterns.tv_show_season_folder_check(file.path) and folder_and_file_patterns.tv_show_episode_pattern_check(file.name):
            pass
        elif folder_and_file_patterns.movie_pattern_check(file.name, file.path):
            pass
        else:
            return False
    return True


# TODO remove this function once its no longer used.
def correct_media_file_format(media_file, files_in_extra_folders_are_formated = True):
    """
    Checks the media_file to see if it is formated correctly for tv show or movie, and all files in extra folders
    if desired.

    :param media_file: a DirEntry object of media file to check
    :param files_in_extra_folders_are_formated: a flag that makes the function define all files in extra folders are formated correctly or not. True - formated correctly, False - not formated correctly.
    :return:
    """
    tv_show_episode_format = re.compile(r"""
                        ^.+   # wildcard to handle name of show
                        \s  
                        -
                        \s
                        s\d+e\d+(-e\d+)?  # season, episode number and possible multiple episode
                        \.\w+ # file extension
                        """, re.VERBOSE | re.IGNORECASE)
    movie_format = re.compile(r"""
                        ^(?P<title>^.+)   # group 1: the name of the file
                        (?P<ext>\.\w+) # group 2: file extension
                        """, re.VERBOSE | re.IGNORECASE)

    # check see if the folder is an extra folder
    extra_folder_format = [
        r"trailer(s)?$",
        r"behind the scenes$",
        r"deleted scenes$",
        r"featurettes$",
        r"interviews$",
        r"scenes$",
        r"shorts$",
        r"other$"
    ]
    extra_folder_format_check_results = [re.match(pattern, media_file.path.split('/')[-2], re.IGNORECASE) for pattern in extra_folder_format]

    # TV show episodes can be saved in two different folders: Season # or Specials.
    if re.match(r'^(Season\s\d)|(Specials)$', media_file.path.split('/')[-2], re.IGNORECASE) and tv_show_episode_format.match(media_file.name):
        return True
    elif movie_format.match(media_file.name).group('title') == media_file.path.split('/')[-1]:
        return True
    elif any(extra_folder_pattern_match for extra_folder_pattern_match in extra_folder_format_check_results) and files_in_extra_folders_are_formated:
        return True
    else:
        return False