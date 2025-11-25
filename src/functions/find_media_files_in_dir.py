import pathlib
from typing import Callable, Generator
from . import directory_scanner

def find_media_files_in_dir(
        file_condition: Callable[..., bool],
        folder_condition: Callable[..., bool],
        directory: str) -> Generator[tuple[str], None, None]:
    """
    A generator that returns all files in a given directory that meet the condition given by the
    file_condition function.

    :param file_condition: A function that specifies that condition the file needs to be met.
    :param directory: The directory to scan for files
    :param folder_condition: A function that specifies that condition the folder needs to be met.
    :return: A tuple of all the files in a given directory
    """
    files_in_directory = []

    for entry in directory_scanner(directory):
        file_folder_is_in = pathlib.Path(entry).parent.resolve().name

        if file_condition(entry.name) and folder_condition(file_folder_is_in):
            # Compare the new media file to the last appended file in the list to see if they are in
            # the same directory. If they are in the same directory, append the media file to the list.
            # If they aren't in the same directory, yield the list.
            # When the generator is called again, clear the list and append the file that wasn't append to the previous list.
            if len(files_in_directory) > 0:
                last_appended_file = files_in_directory[-1]
                if pathlib.Path(last_appended_file).parent.resolve() == pathlib.Path(entry.path).parent.resolve():
                    files_in_directory.append(entry.path)
                else:
                    yield tuple(files_in_directory)
                    files_in_directory = [entry.path]
            else:
                files_in_directory.append(entry.path)

    # this is necessary for when scanning a folder with just files or reaching the final folder of the directory
    yield tuple(files_in_directory)
