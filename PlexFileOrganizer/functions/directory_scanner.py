import os

def directory_scanner(directory_path):
    """
    A generator function that steps through the directory path given and returns one entry at a time
    what is finds.

    :param directory_path: The directory path that will be scanned
    :return: a DirEntry that contains two entries -- path and name.
    """

    with os.scandir(directory_path) as directory_to_scan:
        for entry in directory_to_scan:
            if not entry.name.startswith("."):  # skips over hidden folders/files.
                yield entry
