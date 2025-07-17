import os


def update_file_name(list_of_files_to_update):
    """
    Takes a list were each element is a tuple--tuples contain the following: (old file name, new file name)--and iterate
    through the list and update the file names to the new one.

    :param list_of_files_to_update: A list with tuple elements.
    :return: error: Returns blank if ran into error; returns error message if ran into error.
    """
    for file in list_of_files_to_update:
        old_file, new_file = file # extract the old and new file name from the tuple
        #print("Old file: {} \nNew file: {} \n".format(old_file, new_file))  # for debugging
        os.rename(old_file, new_file)
