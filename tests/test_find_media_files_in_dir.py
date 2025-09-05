from ..PlexFileOrganizer.functions import (
    find_media_files_in_dir,
    skip_extra_folders,
    default_folder_condition
)
import os

def txt_file_condition(file_path):
    """
    Created for this test to work with the test_library
    """
    if file_path.endswith('.txt'):
        return True
    else:
        return False

class TestFindMediaFilesInDir:

    def test_movie_folder(self):
        """
        Validate the find_media_files_in_dir function find all the files in the given movie folder directory
        """
        errors = []
        movie_directory = '/Volumes/Hub SSD/python projects/PlexFileOrganizer/tests/test_library/movies'

        for file_list in find_media_files_in_dir(txt_file_condition, default_folder_condition, movie_directory):
            directory_path = os.path.dirname(os.path.abspath(file_list[0]))

            func_file_count = len(file_list)
            os_scan_file_count = len([name for name in os.listdir(directory_path) if "." in name])

            if not func_file_count == os_scan_file_count:
                errors.append(
                    f"Directory: {directory_path} -> func file count: {func_file_count}, os scan file count: {os_scan_file_count}")

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))

    def test_tv_show_folder(self):
        """
        Validate the find_media_files_in_dir function find all the files in the given tv show folder directory
        """
        errors = []
        tv_show_directory = '/Volumes/Hub SSD/python projects/PlexFileOrganizer/tests/test_library/tv shows'

        for file_list in find_media_files_in_dir(txt_file_condition, default_folder_condition, tv_show_directory):
            directory_path = os.path.dirname(os.path.abspath(file_list[0]))

            func_file_count = len(file_list)
            os_scan_file_count = len([name for name in os.listdir(directory_path) if "." in name])

            if not func_file_count == os_scan_file_count:
                errors.append(
                    f"Directory: {directory_path} -> func file count: {func_file_count}, os scan file count: {os_scan_file_count}")

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))

    def test_skip_extra_folder(self):
        """
        Validate the find_media_files_in_dir function find all the files in the given extra folder directory
        """
        number_of_scanned_folders = 0
        extra_directory = '/Volumes/Hub SSD/python projects/PlexFileOrganizer/tests/test_library/tv shows/Zenless Zone Zero'

        for _ in find_media_files_in_dir(txt_file_condition, skip_extra_folders, extra_directory):
            number_of_scanned_folders += 1

        assert number_of_scanned_folders == 2