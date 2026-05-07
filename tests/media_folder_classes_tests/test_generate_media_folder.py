from src.classes import GenerateMediaFolder
from src.custom_objects import MediaCategory
from pyfakefs.fake_filesystem_unittest import TestCase
import os


class TestGenerateMediaFolder(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir("/media_folder")
        self.fs.create_dir("/media_folder/Zenless Zone Zero")
        self.fs.create_dir("/media_folder/Zenless Zone Zero {edition-widescreen}")

    def test_generate_media_folder_name_no_edition_tag(self):
        """
        Validates the built-in method generates the correct media folder name without edition tag.
        """
        media_folder = GenerateMediaFolder()
        media_folder.media_title = "Legend of Zelda"
        media_folder.edition_tag = ""

        new_folder_name = media_folder.media_folder_name()

        assert new_folder_name == "Legend of Zelda"

    def test_generate_media_folder_name_with_edition_tag(self):
        """
        Validates the built-in method generates the correct media folder name with edition tag.
        """
        media_folder = GenerateMediaFolder()
        media_folder.media_title = "Legend of Zelda"
        media_folder.edition_tag = "full screen"

        new_folder_name = media_folder.media_folder_name()

        assert new_folder_name == "Legend of Zelda {edition-full screen}"

    def test_generate_media_folder_detects_existing_folder(self):
        """
        Validates that the GenerateMediaFolder object detects existing folder.
        """
        media_folder = GenerateMediaFolder()
        media_folder.directory = "/media_folder"
        media_folder.media_title = "Zenless Zone Zero"

        assert media_folder.check_if_media_folder_exists() is True, (
            "Failed to detect existing folder."
        )

    def test_generate_media_folder_detects_existing_folder_with_edition_tag(self):
        """
        Validates that the GenerateMediaFolder object detects existing folder that has edition tag.
        """
        media_folder = GenerateMediaFolder()
        media_folder.directory = "/media_folder"
        media_folder.media_title = "Zenless Zone Zero"
        media_folder.edition_tag = "widescreen"

        assert media_folder.check_if_media_folder_exists() is True, (
            "Failed to detect existing folder."
        )

    def test_check_if_extra_folders_to_be_generated_method(self):
        """
        Validates that the GenerateMediaFolder object's check_if_new_extra_folders_are_needed method returns True
        when there are extra folder(s) to be generated and false otherwise.
        """

        media_folder = GenerateMediaFolder()
        media_folder.extra_folders["other"] = True

        assert media_folder.check_if_new_extra_folders_are_needed() is True, (
            "Failed to detect extra folder(s) to be generated."
        )

        media_folder = GenerateMediaFolder()
        media_folder.extra_folders["other"] = False

        assert media_folder.check_if_new_extra_folders_are_needed() is False, (
            "Failed to detect no extra folder(s) needed to be generated."
        )

    def test_generate_all_extra_folders(self):
        """
        Checks to see that all extra folders will be generated.
        """
        extra_folder = GenerateMediaFolder()
        extra_folder.directory = "/media_folder"
        extra_folder.media_title = "Extra Test"
        extra_folder.media_type = MediaCategory.MOVIE
        extra_folder.extra_folders["trailers"] = True
        extra_folder.extra_folders["behind the scenes"] = True
        extra_folder.extra_folders["deleted scenes"] = True
        extra_folder.extra_folders["featurettes"] = True
        extra_folder.extra_folders["interviews"] = True
        extra_folder.extra_folders["scenes"] = True
        extra_folder.extra_folders["shorts"] = True
        extra_folder.extra_folders["other"] = True

        extra_folder.generate_media_folder()
        extra_folder.generate_extra_folders()

        assert os.path.isdir("/media_folder/Extra Test/Trailers")
        assert os.path.isdir("/media_folder/Extra Test/Behind The Scenes")
        assert os.path.isdir("/media_folder/Extra Test/Deleted Scenes")
        assert os.path.isdir("/media_folder/Extra Test/Featurettes")
        assert os.path.isdir("/media_folder/Extra Test/Interviews")
        assert os.path.isdir("/media_folder/Extra Test/Scenes")
        assert os.path.isdir("/media_folder/Extra Test/Shorts")
        assert os.path.isdir("/media_folder/Extra Test/Other")

    def test_generate_all_extra_folders_with_edition_tag(self):
        """
        Checks to see that all extra folders will be generated for a media folder with an edition tag.
        """
        extra_folder = GenerateMediaFolder()
        extra_folder.directory = "/media_folder"
        extra_folder.media_title = "Extra Test"
        extra_folder.edition_tag = "widescreen"
        extra_folder.media_type = MediaCategory.MOVIE
        extra_folder.extra_folders["trailers"] = True
        extra_folder.extra_folders["behind the scenes"] = True
        extra_folder.extra_folders["deleted scenes"] = True
        extra_folder.extra_folders["featurettes"] = True
        extra_folder.extra_folders["interviews"] = True
        extra_folder.extra_folders["scenes"] = True
        extra_folder.extra_folders["shorts"] = True
        extra_folder.extra_folders["other"] = True

        extra_folder.generate_media_folder()
        extra_folder.generate_extra_folders()

        assert os.path.isdir("/media_folder/Extra Test {edition-widescreen}/Trailers")
        assert os.path.isdir("/media_folder/Extra Test {edition-widescreen}/Behind The Scenes")
        assert os.path.isdir("/media_folder/Extra Test {edition-widescreen}/Deleted Scenes")
        assert os.path.isdir("/media_folder/Extra Test {edition-widescreen}/Featurettes")
        assert os.path.isdir("/media_folder/Extra Test {edition-widescreen}/Interviews")
        assert os.path.isdir("/media_folder/Extra Test {edition-widescreen}/Scenes")
        assert os.path.isdir("/media_folder/Extra Test {edition-widescreen}/Shorts")
        assert os.path.isdir("/media_folder/Extra Test {edition-widescreen}/Other")

    def test_generate_new_tv_show_folder(self):
        """
        Checks to see that it properly generates a new TV show media folder.
        """
        media_folder = GenerateMediaFolder()

        # provide the tv show media folder contents
        media_folder.directory = "/media_folder"
        media_folder.media_title = "Legend of Zelda Series"
        media_folder.media_type = MediaCategory.TV
        media_folder.number_of_seasons = 2
        media_folder.extra_folders["trailers"] = True
        media_folder.extra_folders["shorts"] = True

        media_folder.generate_media_folder()
        media_folder.generate_seasons()
        media_folder.generate_extra_folders()

        assert os.path.isdir("/media_folder/Legend of Zelda Series")
        assert os.path.isdir("/media_folder/Legend of Zelda Series/Season 1")
        assert os.path.isdir("/media_folder/Legend of Zelda Series/Season 2")
        assert os.path.isdir("/media_folder/Legend of Zelda Series/Trailers")
        assert os.path.isdir("/media_folder/Legend of Zelda Series/Shorts")

    def test_generate_new_tv_show_folder_with_edition_tag(self):
        """
        Checks to see that it properly generates a new TV show media folder with edition tag.
        """
        media_folder = GenerateMediaFolder()

        # provide the tv show media folder contents
        media_folder.directory = "/media_folder"
        media_folder.media_title = "Legend of Zelda Series"
        media_folder.edition_tag = "japanese audio"
        media_folder.media_type = MediaCategory.TV
        media_folder.number_of_seasons = 2
        media_folder.extra_folders["trailers"] = True
        media_folder.extra_folders["shorts"] = True

        media_folder.generate_media_folder()
        media_folder.generate_seasons()
        media_folder.generate_extra_folders()

        assert os.path.isdir("/media_folder/Legend of Zelda Series {edition-japanese audio}")
        assert os.path.isdir("/media_folder/Legend of Zelda Series {edition-japanese audio}/Season 1")
        assert os.path.isdir("/media_folder/Legend of Zelda Series {edition-japanese audio}/Season 2")
        assert os.path.isdir("/media_folder/Legend of Zelda Series {edition-japanese audio}/Trailers")
        assert os.path.isdir("/media_folder/Legend of Zelda Series {edition-japanese audio}/Shorts")

    def test_generate_new_movie_folder(self):
        """
        Checks to see that it properly generates a new movie folder.
        """
        media_folder = GenerateMediaFolder()
        media_folder.directory = "/media_folder"
        media_folder.media_title = "Re:Creators"
        media_folder.media_type = MediaCategory.MOVIE
        media_folder.extra_folders["trailers"] = True
        media_folder.extra_folders["shorts"] = True

        media_folder.generate_media_folder()
        media_folder.generate_extra_folders()

        assert os.path.isdir("/media_folder/Re:Creators")
        assert os.path.isdir("/media_folder/Re:Creators/Trailers")
        assert os.path.isdir("/media_folder/Re:Creators/Shorts")

    def test_generate_new_movie_folder_with_edition_tag(self):
        """
        Checks to see that it properly generates a new movie folder with edition tag.
        """
        media_folder = GenerateMediaFolder()
        media_folder.directory = "/media_folder"
        media_folder.media_title = "Re:Creators"
        media_folder.edition_tag = "english audio"
        media_folder.media_type = MediaCategory.MOVIE
        media_folder.extra_folders["trailers"] = True
        media_folder.extra_folders["shorts"] = True

        media_folder.generate_media_folder()
        media_folder.generate_extra_folders()

        assert os.path.isdir("/media_folder/Re:Creators {edition-english audio}")
        assert os.path.isdir("/media_folder/Re:Creators {edition-english audio}/Trailers")
        assert os.path.isdir("/media_folder/Re:Creators {edition-english audio}/Shorts")
