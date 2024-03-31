import os


def file_name_updater(file_list, directory):
    """
    A function that takes in a list of files that need their name changed.

    :param file_list: A list were each entry is a file with their old name and their new name--
    ((old_file_name, new_file_name),...)
    :param directory: The location of the file(s) that need their names changed.
    :return: N/A
    """
    # iterate through the file_list
    for filename in file_list:
        os.rename(os.path.join(directory, filename[0]), os.path.join(directory, filename[1]))
