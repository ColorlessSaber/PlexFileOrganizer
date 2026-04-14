from pathlib import Path
from . import find_media_files_in_dir, skip_extra_folders, video_file_condition


def rename_media_folder_and_contents(
        old_media_title: str,
        new_media_title: str,
        dir_path: str,
) -> None:
    """
    Renames the media folder to the new media title and renames all media files inside the folder to match
    the new media title.

    :param old_media_title: The old media title
    :param new_media_title: The new media title
    :param dir_path: The directory path to where the media folder is located.
    :return: None
    """

    media_folder_path = Path("{}/{}".format(dir_path, old_media_title))

    # Find all the files in the media folder that contain the media title with in the file name
    generator_find_media_files = find_media_files_in_dir(
        video_file_condition,
        skip_extra_folders,
        str(media_folder_path),
    )

    for files_to_rename in generator_find_media_files:
        for file in files_to_rename:

            old_file_name = Path(file).stem # getting the old file name
            new_file_path = Path(file).with_stem(
                old_file_name.replace(old_media_title, new_media_title)
            ) # replace the old media title in the file name to the new one while creating a new directory path

            Path(file).rename(new_file_path)


    # rename the media folder. This is done last so it doesn't mess up the renaming of the files
    media_folder_path.rename("{}/{}".format(dir_path, new_media_title))
