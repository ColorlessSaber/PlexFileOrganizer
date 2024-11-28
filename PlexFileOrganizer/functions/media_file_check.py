import re
import os

def media_file_check(media_file_list, directory):
    """
    Checks to see if the media file(s) in the directory have been updated or not.

    :param media_file_list: The list of media file(s) in the directory
    :param directory: Location of the media files
    :return: results: A string that holds the results
    """
    results = 'Files Not Updated'

    # Check to see if media file(s) match tv show/movie title.
    if 'season' in directory.lower():
        if all(re.split(r"\s-\ss\d+e\d+\.\w+", item)[0] in directory for item in media_file_list):
            results = 'Files Updated'
    else:
        if os.path.splitext(media_file_list[0])[0] in directory:
            results = 'Files Updated'

    return results
