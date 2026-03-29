from src.functions import (
    find_media_files_in_dir,
    skip_extra_folders,
    default_folder_condition,
)
import os
from pyfakefs.fake_filesystem_unittest import TestCase


def txt_file_condition(file_path):
    """
    Created for this test to work with the test_library
    """
    if file_path.endswith(".txt"):
        return True
    else:
        return False


class TestFindMediaFilesInDir(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        # test directory for movie folder
        self.fs.create_file("/foo/movie/movie.txt")
        self.fs.create_file("/foo/movie/Trailers/trailer 1.txt")
        self.fs.create_file("/foo/movie/Behind the Scenes/behind the scene 1.txt")
        self.fs.create_file("/foo/movie/Deleted Scenes/deleted scene 1.txt")
        self.fs.create_file("/foo/movie/Featurettes/featuret 1.txt")
        self.fs.create_file("/foo/movie/Interviews/interview 1.txt")
        self.fs.create_file("/foo/movie/Scenes/scene 1.txt")
        self.fs.create_file("/foo/movie/Shorts/short 1.txt")
        self.fs.create_file("/foo/movie/Other/other 1.txt")

        # test directory for tv show folder
        self.fs.create_file("/foo/tv show/Season 01/s1e01.txt")
        self.fs.create_file("/foo/tv show/Season 01/s1e02.txt")
        self.fs.create_file("/foo/tv show/Season 01/s1e03.txt")
        self.fs.create_file("/foo/tv show/Trailers/trailer 1.txt")
        self.fs.create_file("/foo/tv show/Behind the Scenes/behind the scene 1.txt")
        self.fs.create_file("/foo/tv show/Deleted Scenes/deleted scene 1.txt")
        self.fs.create_file("/foo/tv show/Featurettes/featuret 1.txt")
        self.fs.create_file("/foo/tv show/Interviews/interview 1.txt")
        self.fs.create_file("/foo/tv show/Scenes/scene 1.txt")
        self.fs.create_file("/foo/tv show/Shorts/short 1.txt")
        self.fs.create_file("/foo/tv show/Other/other 1.txt")

        # test directory for extra folder
        self.fs.create_file("/foo/extra/Trailers/trailer 1.txt")
        self.fs.create_file("/foo/extra/Behind the Scenes/behind the scene 1.txt")
        self.fs.create_file("/foo/extra/Deleted Scenes/deleted scene 1.txt")
        self.fs.create_file("/foo/extra/Featurettes/featuret 1.txt")
        self.fs.create_file("/foo/extra/Interviews/interview 1.txt")
        self.fs.create_file("/foo/extra/Scenes/scene 1.txt")
        self.fs.create_file("/foo/extra/Shorts/short 1.txt")
        self.fs.create_file("/foo/extra/Other/other 1.txt")

    def test_movie_folder(self):
        """
        Validate the find_media_files_in_dir function find all the files in the given movie folder directory
        """
        errors = []
        movie_directory = "/foo/movie"

        for file_list in find_media_files_in_dir(
            txt_file_condition, default_folder_condition, movie_directory
        ):
            directory_path = os.path.dirname(os.path.abspath(file_list[0]))

            func_file_count = len(file_list)
            os_scan_file_count = len(
                [name for name in os.listdir(directory_path) if "." in name]
            )

            if not func_file_count == os_scan_file_count:
                errors.append(
                    f"Directory: {directory_path} -> func file count: {func_file_count}, os scan file count: {os_scan_file_count}"
                )

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))

    def test_tv_show_folder(self):
        """
        Validate the find_media_files_in_dir function find all the files in the given tv show folder directory
        """
        errors = []
        tv_show_directory = "/foo/tv show"

        for file_list in find_media_files_in_dir(
            txt_file_condition, default_folder_condition, tv_show_directory
        ):
            directory_path = os.path.dirname(os.path.abspath(file_list[0]))

            func_file_count = len(file_list)
            os_scan_file_count = len(
                [name for name in os.listdir(directory_path) if "." in name]
            )

            if not func_file_count == os_scan_file_count:
                errors.append(
                    f"Directory: {directory_path} -> func file count: {func_file_count}, os scan file count: {os_scan_file_count}"
                )

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))

    def test_skip_extra_folders(self):
        """
        Validate the find_media_files_in_dir function will skip all extra folders then told to do so
        """
        number_of_scanned_folders = 0
        extra_directory = "/foo/extra"

        for file_list in find_media_files_in_dir(
            txt_file_condition, skip_extra_folders, extra_directory
        ):
            if file_list:
                number_of_scanned_folders += 1

        assert number_of_scanned_folders == 0
