import pathlib
from PlexFileOrganizer.functions import directory_scanner

def find_media_files_in_dir(file_condition, directory):
    """
    A generator that returns all files in a given directory that meet the condition given by the
    file_condition function.

    :param file_condition: A function that specifies that condition the file needs to be met.
    :param directory: The directory to scan for files
    :return: A tuple of all the files in a given directory
    """
    files_in_directory = []

    for entry in directory_scanner(directory):
        if file_condition(entry.path):
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

# *** File Condition Functions ***
def video_file_condition(file_path):
    """
    The condition that validates that the file found is a video file.

    :param file_path: The directory location of the file
    :return:
    """
    if any(file_path.endswith(file_extension) for file_extension in ['.mkv', '.mp4', '.avi']):
        return True
    else:
        return False

if __name__ == '__main__':
    dir_path = "/Volumes/Media Library/Anime TV Shows/Frieren Beyond Journey's End"
    for file_list in find_media_files_in_dir(video_file_condition, dir_path):
        print(file_list)
