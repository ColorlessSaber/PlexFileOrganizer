import os


def update_files_in_directory(list_of_files_to_update: list[tuple[str, str]]) -> None:
    """
    Takes a list were each element is a tuple--each tuple contain the following: (old file name, new file name)--and iterate
    through the list and update the file names to the new one.

    :param list_of_files_to_update: A list with tuple elements.
    :return:
    """
    for file in list_of_files_to_update:
        old_file, new_file = file
        #print("Old file: {} \nNew file: {} \n".format(old_file, new_file))  # for debugging
        os.rename(old_file, new_file)
