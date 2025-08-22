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

    extra_file_format = re.compile(r"""
                                            ^(?P<title>.+) # group 1: the name of the file
                                            \s
                                            (?P<number>\d+) # group 2: the number of the file
                                            \.\w+           # file extension
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
        Checks to see if the given video file matches the correct tv show episode file format.
        
        :param file_name: the file name to check against
        :return: A Bool value. True - formatted correctly, False - not formatted correctly
        """
        if self.tv_episode_file_format.match(file_name):
            return True
        else:
            return False

    def movie_pattern_check(self, file_name, file_path):
        """
        Checks to see if the given video file matches the correct movie file format.
        
        :param file_name: the file name to check against
        :param file_path: The absolute path to the file
        :return: A bool value. True - formatted correctly, False - not formatted correctly
        """
        if self.movie_file_format.match(file_name).group('title') == file_path.split('/')[-2]:
            return True
        else:
            return False

    def extra_pattern_check(self, file_name, file_path):
        """
        Checks to see if the given video file matches the correct extra file format.

        :param file_name: the file name to check against
        :param file_path: The absolute path to the file
        :return: True - formatted correctly, False - not formatted correctly
        """
        if self.extra_file_format.match(file_name):
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

    def check_files_in_folder(self, list_of_files):
        """
        Checks if the media files in the given list are all formated correctly for the media folder they are in

        :param list_of_files: a list where each element is the full-path to a file in a directory
        :return: Bool value. True -- all media files in folder are formated correctly. False -- at lest one media file in the folder isn't formated correctly
        """
        for file_path in list_of_files:
            file_name = file_path.split('/')[-1]
            if self.tv_show_season_folder_check(file_path) and self.tv_show_episode_pattern_check(file_name):
                continue
            elif self.movie_pattern_check(file_name, file_path):
                continue
            elif self.extra_folder_check(file_path) and self.extra_pattern_check(file_name, file_path):
                continue
            else:
                return False
        return True
