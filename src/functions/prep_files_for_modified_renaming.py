def prep_files_for_modified_renaming(file_list: list) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    """
    Preps the files in the provided list for identification and renaming.

    :param file_list: A list of files to rename.
    :return: Two lists, one containing what files have been identified by renaming, and another containing
    what the files after the identification will be renamed too.
    """
    file_rename_extension_identification = "_ToBeRenamed"

    # identify the files to be renamed in the directory
    files_identified_for_renaming = [(file[0] + "/" + file[1] + file[3],
                                      file[0] + "/" + file[1] + file_rename_extension_identification + file[3])
                                     for file in file_list]

    # Create a list where each element is a tuple containing the following: (old file name, new file name)
    file_to_rename_list = [(file[0] + "/" + file[1] + file_rename_extension_identification + file[3],
                            file[0] + "/" + file[2] + file[3]) for file in file_list]

    return files_identified_for_renaming, file_to_rename_list