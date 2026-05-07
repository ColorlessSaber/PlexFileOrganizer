from src.functions import scan_media_folder
from src.custom_objects import MediaCategory
from pyfakefs.fake_filesystem_unittest import TestCase


class TestScanMediaFolder(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        # test directory for TV media folder
        self.fs.create_dir("/foo/Zenless Zone Zero/Season 01")
        self.fs.create_dir("/foo/Zenless Zone Zero/Specials")
        self.fs.create_dir("/foo/Zenless Zone Zero/Trailers")
        self.fs.create_dir("/foo/Zenless Zone Zero/Behind the Scenes")
        self.fs.create_dir("/foo/Zenless Zone Zero/Deleted Scenes")
        self.fs.create_dir("/foo/Zenless Zone Zero/Featurettes")
        self.fs.create_dir("/foo/Zenless Zone Zero/Interviews")
        self.fs.create_dir("/foo/Zenless Zone Zero/Scenes")
        self.fs.create_dir("/foo/Zenless Zone Zero/Shorts")
        self.fs.create_dir("/foo/Zenless Zone Zero/Other")

        # test for movie media folder
        self.fs.create_file("/foo/The Legend of Zelda/The Legend of Zelda.mp4")
        self.fs.create_dir("/foo/The Legend of Zelda/Trailers")
        self.fs.create_dir("/foo/The Legend of Zelda/Behind the Scenes")
        self.fs.create_dir("/foo/The Legend of Zelda/Deleted Scenes")
        self.fs.create_dir("/foo/The Legend of Zelda/Featurettes")
        self.fs.create_dir("/foo/The Legend of Zelda/Interviews")
        self.fs.create_dir("/foo/The Legend of Zelda/Scenes")
        self.fs.create_dir("/foo/The Legend of Zelda/Shorts")
        self.fs.create_dir("/foo/The Legend of Zelda/Other")

        # test for non media folder
        self.fs.create_dir("/foo/misc")
        self.fs.create_file("/foo/misc/.movie.yml")

    def test_scan_tv_media_folder(self):
        """
        Validate scan_media_folder returns correct media folder object for tv media folder.
        """
        media_folder_info, folder_is_a_media_folder = scan_media_folder("/foo/Zenless Zone Zero/")

        assert folder_is_a_media_folder, "Failed to detect tv media folder"
        assert media_folder_info.media_title == "Zenless Zone Zero", (
            "Failed to grab name of media folder"
        )
        assert media_folder_info.media_type == MediaCategory.TV, (
            "Failed to detect media folder is tv show"
        )
        assert media_folder_info.number_of_seasons == 1, (
            "Failed to not count Special season folder"
        )
        assert media_folder_info.specials_season is True, (
            "Failed to detect Special season folder"
        )
        assert media_folder_info.extra_folders["trailers"] is True, (
            "Failed to detect extra folder - trailers"
        )
        assert media_folder_info.extra_folders["behind the scenes"] is True, (
            "Failed to detect extra folder - behind the scenes"
        )
        assert media_folder_info.extra_folders["deleted scenes"] is True, (
            "Failed to detect extra folder - deleted scenes"
        )
        assert media_folder_info.extra_folders["featurettes"] is True, (
            "Failed to detect extra folder - featurettes"
        )
        assert media_folder_info.extra_folders["interviews"] is True, (
            "Failed to detect extra folder - interviews"
        )
        assert media_folder_info.extra_folders["scenes"] is True, (
            "Failed to detect extra folder - scenes"
        )
        assert media_folder_info.extra_folders["shorts"] is True, (
            "Failed to detect extra folder - shorts"
        )
        assert media_folder_info.extra_folders["other"] is True, (
            "Failed to detect extra folder - other"
        )

    def test_scan_movie_media_folder(self):
        """
        Validate scan_media_folder returns correct media folder object for movie media folder.
        """
        media_folder_info, folder_is_a_media_folder = scan_media_folder("/foo/The Legend of Zelda/")

        assert folder_is_a_media_folder, "Failed to detect movie media folder"
        assert media_folder_info.media_title == "The Legend of Zelda", (
            "Failed to grab name of media folder"
        )
        assert media_folder_info.media_type == MediaCategory.MOVIE, (
            "Failed to detect media folder is movie"
        )
        assert media_folder_info.extra_folders["trailers"] is True, (
            "Failed to detect extra folder - trailers"
        )
        assert media_folder_info.extra_folders["behind the scenes"] is True, (
            "Failed to detect extra folder - behind the scenes"
        )
        assert media_folder_info.extra_folders["deleted scenes"] is True, (
            "Failed to detect extra folder - deleted scenes"
        )
        assert media_folder_info.extra_folders["featurettes"] is True, (
            "Failed to detect extra folder - featurettes"
        )
        assert media_folder_info.extra_folders["interviews"] is True, (
            "Failed to detect extra folder - interviews"
        )
        assert media_folder_info.extra_folders["scenes"] is True, (
            "Failed to detect extra folder - scenes"
        )
        assert media_folder_info.extra_folders["shorts"] is True, (
            "Failed to detect extra folder - shorts"
        )
        assert media_folder_info.extra_folders["other"] is True, (
            "Failed to detect extra folder - other"
        )

    def test_scan_not_media_folder(self):
        """
        Validate scan_media_folder returns an error when folder isn't a media folder.
        """
        media_folder_info, folder_is_a_media_folder = scan_media_folder("/foo/misc")
        assert folder_is_a_media_folder is False, (
            "Failed to detect folder is not a media folder"
        )
