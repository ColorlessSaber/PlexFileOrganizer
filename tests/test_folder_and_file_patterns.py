from ..PlexFileOrganizer.classes import FolderAndFilePatterns

folder_and_file_patterns = FolderAndFilePatterns()

class TestFolderAndFilePatterns:
    """
    This class contains only unit tests to test the basic functionality of the FolderAndFilePatterns class
    """
    def test_move_file_regex_check(self):
        """
        Validate that a regex pattern for movie file works correctly
        """
        movie_title = "test"
        movie_filename = "test.mkv"
        assert folder_and_file_patterns.movie_file_format_regex_pattern.match(movie_filename).group('title') == movie_title

    def test_extra_file_regex_check(self):
        """
        Validate that the regex pattern for extra files works correctly
        """

        errors = []
        media_file_names = [
            "trailers 01.mkv",
            "behind the scenes 01.mkv",
            "deleted scenes 01.mkv",
            "featurettes 01.mkv",
            "interviews 01.mkv",
            "scenes 01.mkv",
            "shorts 01.mkv",
            "other 01.mkv",
        ]

        extra_folder_format = [
            "trailers",
            "behind the scenes",
            "deleted scenes",
            "featurettes",
            "interviews",
            "scenes",
            "shorts",
            "other"
        ]

        for i in zip(media_file_names, extra_folder_format):
            file_name, folder_name = i
            if not folder_and_file_patterns.extra_file_format_regex_pattern.match(file_name).group('title') == folder_name:
                errors.append(f"Error with folder '{folder_name}' pattern match")

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))

    def test_tv_episode_regex_check(self):
        """
        Validate that the regex pattern for episode files works correctly
        """
        errors = []
        single_episode_file = "test - s01e01.mkv"
        multiple_episode_file = "test - s01e01-e05.mkv"

        if folder_and_file_patterns.tv_episode_file_format_regex_pattern.match(single_episode_file) is None:
            errors.append(f"Error with single episode file pattern")

        if folder_and_file_patterns.tv_episode_file_format_regex_pattern.match(multiple_episode_file) is None:
            errors.append(f"Error with multiple episode file pattern")

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))

    def test_tv_episode_func_check(self):
        """
        Validate that the tv episode file function that validates the tv episode file is formatted correctly
        is working correctly
        """
        errors = []
        single_episode_file = "test - s01e01.mkv"
        multiple_episode_file = "test - s01e01-e05.mkv"

        if not folder_and_file_patterns.tv_show_episode_pattern_check(single_episode_file):
            errors.append(f"Error with single episode file pattern")

        if not folder_and_file_patterns.tv_show_episode_pattern_check(multiple_episode_file):
            errors.append(f"Error with multiple episode file pattern")

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))

    def test_movie_file_func_check(self):
        """
        Validate that the movie file function that validates the movie file is formatted correctly
        is working correctly
        """
        movie_file = "test.mkv"
        folder_name = "test"

        assert folder_and_file_patterns.movie_media_file_check(movie_file, folder_name)

    def test_extra_file_func_check(self):
        """
        Validate that the extra file function that validates the extra file is formatted correctly
        is working correctly
        """
        errors = []
        media_file_names = [
            "trailer 01.mkv",
            "behind the scene 01.mkv",
            "deleted scene 01.mkv",
            "featurette 01.mkv",
            "interview 01.mkv",
            "scene 01.mkv",
            "short 01.mkv",
            "other 01.mkv",
        ]

        extra_folder_format = [
            "trailers",
            "behind the scenes",
            "deleted scenes",
            "featurettes",
            "interviews",
            "scenes",
            "shorts",
            "other"
        ]

        for i in zip(media_file_names, extra_folder_format):
            file_name, folder_name = i
            if not folder_and_file_patterns.extra_media_file_check(file_name, folder_name):
                errors.append(f"Error with folder '{folder_name}' pattern match")

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))

    def test_tv_show_season_folder_func_check(self):
        """
        Validate that the tv show season folder function that validates the folder is a tv show folder
        is working correctly
        """
        errors = []
        folder_names = [
            "Season 01",
            "Season 100",
            "Specials",
        ]

        for folder_name in folder_names:
            if not folder_and_file_patterns.tv_show_season_folder_check(folder_name):
                errors.append(f"Error with folder '{folder_name}' pattern match")

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))

    def test_extra_folder_func_check(self):
        """
        Validate that the extra folder function that validates the folder is a extra folder
        is working correctly
        """
        errors = []
        extra_folder_formats = [
            "trailers",
            "behind the scenes",
            "deleted scenes",
            "featurettes",
            "interviews",
            "scenes",
            "shorts",
            "other"
        ]
        for extra_folder in extra_folder_formats:
            if not folder_and_file_patterns.extra_folder_check(extra_folder):
                errors.append(f"Error with folder '{extra_folder}' pattern match")

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))


class TestFilePatterns:
    """
    this class contains unit tests for testing situations that caused bug/issues
    """

    def test_close_to_movie_folder_name(self):
        """
        Bug: Ran into a situation where the file name was nearly identical to the folder name it was in. This
        caused a false positive.
        """
        folder_name = "Evangelion 1.0 You Are (Not) Alone"
        movie_file = "Evangelion 1.0 You Are (Not) Alone_01.mkv"

        assert folder_and_file_patterns.movie_media_file_check(movie_file, folder_name) == False, "Failed nearly identical file name to folder name; yielded false positive when it should be yielded false."