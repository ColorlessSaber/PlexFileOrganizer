import re

def correct_media_file_format(media_file):
    """
    checks the media_file and verifies if it has been formated correctly or not based on folder its under.

    :param media_file:
    :return:
    """
    tv_show_formated = re.compile(r"""
            ^.+   # wildcard to handle name of show
            \s  
            -
            \s
            s\d+e\d+(-e\d+)?  # season, episode number and possible multiple episode
            \.\w+ # file extension
            """, re.VERBOSE | re.IGNORECASE)
    trailer_folder_formated = re.compile(r"""
    ^.+       # wildcard to handle the name of the show
    _pv\d+   # the add on to identify its a trailer
    .\w+    # file extension
    """, re.VERBOSE | re.IGNORECASE)

    if re.match(r'Season\s\d', media_file.path.split('/')[-2]): # media folder is a TV show
        if not tv_show_formated.match(media_file.name):
            return True
    elif re.match(r"trailer",media_file.path.split('/')[-1],re.IGNORECASE): # trailer folder
        if not trailer_folder_formated.match(media_file.name):
            return True
    else:
        return False