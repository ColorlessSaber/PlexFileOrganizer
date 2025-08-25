from ..PlexFileOrganizer.classes import FolderAndFilePatterns
import pytest
folder_and_file_patterns = FolderAndFilePatterns()

class TestClass:
    def test_move_file_regex_check(self):
        movie_title = "test"
        movie_filename = "test.mkv"
        assert folder_and_file_patterns.movie_file_format_regex_pattern.match(movie_filename).group('title') == movie_title

    def test_extra_file_regex_check(self):
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
        errors = []
        single_episode_file = "test - s01e01.mkv"
        multiple_episode_file = "test - s01e01-e05.mkv"

        if folder_and_file_patterns.tv_episode_file_format_regex_pattern.match(single_episode_file) is None:
            errors.append(f"Error with single episode file pattern")

        if folder_and_file_patterns.tv_episode_file_format_regex_pattern.match(multiple_episode_file) is None:
            errors.append(f"Error with multiple episode file pattern")

        assert not errors, "errors occurred:\n{}".format("\n".join(errors))