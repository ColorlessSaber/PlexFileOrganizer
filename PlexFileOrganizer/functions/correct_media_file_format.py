import re

def correct_media_file_format(media_file, files_in_extra_folders_are_formated = True):
    """
    Checks the media_file to see if it is formated correctly for tv show or movie, and all files in extra folders
    if desired.

    :param media_file: a DirEntry object of media file to check
    :param files_in_extra_folders_are_formated: a flag that makes the function define all files in extra folders are
    formated correctly or not
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
        r"^trailer(s)?$",
        r"^behind the scenes$",
        r"^deleted scenes$",
        r"^featurettes$",
        r"^interviews$",
        r"^scenes$",
        r"^shorts$",
        r"^other$"
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