from ..src.functions import scan_media_folder
from pyfakefs.fake_filesystem_unittest import TestCase

class TestScanMediaFolder(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        # test directory for tv media folder
        self.fs.create_dir("/foo/tv show/Season 01")
        self.fs.create_dir("/foo/tv show/Trailers")
        self.fs.create_dir("/foo/tv show/Behind the Scenes")
        self.fs.create_dir("/foo/tv show/Deleted Scenes")
        self.fs.create_dir("/foo/tv show/Featurettes")
        self.fs.create_dir("/foo/tv show/Interviews")
        self.fs.create_dir("/foo/tv show/Scenes")
        self.fs.create_dir("/foo/tv show/Shorts")
        self.fs.create_dir("/foo/tv show/Other")

        # test for movie media folder
        self.fs.create_file("/foo/movie/movie.mp4")
        self.fs.create_dir("/foo/movie/Trailers")
        self.fs.create_dir("/foo/movie/Behind the Scenes")
        self.fs.create_dir("/foo/movie/Deleted Scenes")
        self.fs.create_dir("/foo/movie/Featurettes")
        self.fs.create_dir("/foo/movie/Interviews")
        self.fs.create_dir("/foo/movie/Scenes")
        self.fs.create_dir("/foo/movie/Shorts")
        self.fs.create_dir("/foo/movie/Other")

        # test for non media folder
        self.fs.create_dir("/foo/misc")

    def test_scan_tv_media_folder(self):
        """
        Validate scan_media_folder returns correct media folder object for tv media folder.
        """
        media_folder_info, folder_is_a_media_folder = scan_media_folder("/foo/tv show")

        assert folder_is_a_media_folder, "Failed to detect tv media folder"
        assert media_folder_info.media_type == "tv", "Failed to detect media folder is tv show"
        assert media_folder_info.extra_folders['trailers'] == True, "Failed to detect extra folder - trailers"
        assert media_folder_info.extra_folders['behind the scenes'] == True, "Failed to detect extra folder - behind the scenes"
        assert media_folder_info.extra_folders['deleted scenes'] == True, "Failed to detect extra folder - deleted scenes"
        assert media_folder_info.extra_folders['featurettes'] == True, "Failed to detect extra folder - featurettes"
        assert media_folder_info.extra_folders['interviews'] == True, "Failed to detect extra folder - interviews"
        assert media_folder_info.extra_folders['scenes'] == True, "Failed to detect extra folder - scenes"
        assert media_folder_info.extra_folders['shorts'] == True, "Failed to detect extra folder - shorts"
        assert media_folder_info.extra_folders['other'] == True, "Failed to detect extra folder - other"

    def test_scan_movie_media_folder(self):
        """
        Validate scan_media_folder returns correct media folder object for movie media folder.
        """
        media_folder_info, folder_is_a_media_folder = scan_media_folder("/foo/movie")

        assert folder_is_a_media_folder, "Failed to detect movie media folder"
        assert media_folder_info.media_type == "movie", "Failed to detect media folder is tv show"
        assert media_folder_info.extra_folders['trailers'] == True, "Failed to detect extra folder - trailers"
        assert media_folder_info.extra_folders['behind the scenes'] == True, "Failed to detect extra folder - behind the scenes"
        assert media_folder_info.extra_folders['deleted scenes'] == True, "Failed to detect extra folder - deleted scenes"
        assert media_folder_info.extra_folders['featurettes'] == True, "Failed to detect extra folder - featurettes"
        assert media_folder_info.extra_folders['interviews'] == True, "Failed to detect extra folder - interviews"
        assert media_folder_info.extra_folders['scenes'] == True, "Failed to detect extra folder - scenes"
        assert media_folder_info.extra_folders['shorts'] == True, "Failed to detect extra folder - shorts"
        assert media_folder_info.extra_folders['other'] == True, "Failed to detect extra folder - other"

    def test_scan_not_media_folder(self):
        """
        Validate scan_media_folder returns an error when folder isn't a media folder.
        """
        media_folder_info, folder_is_a_media_folder = scan_media_folder("/foo/misc")
        assert folder_is_a_media_folder == False, "Failed to detect folder is not a media folder"