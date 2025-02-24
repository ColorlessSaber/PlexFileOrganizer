import os

def directory_scanner(directory_path):
    """
    A generator function that drills into a directory with multiple directories, subdirectories, etc.
    Yields any files it finds.

    :param directory_path: The directory path that will be scanned.
    :return: a DirEntry that contains two entries -- path and name.
    """
    with os.scandir(directory_path) as directory_to_scan:
        for entry in directory_to_scan:
            if entry.is_dir():
                yield from directory_scanner(entry.path)
            elif not entry.name.startswith('.') and entry.is_file():
                yield entry


if __name__ == '__main__':
    for entry in directory_scanner("/Volumes/Media Library/Anime TV Shows/Frieren Beyond Journey's End"):
        print(entry.name)
