from src.classes import ModifyMediaFolder
from pyfakefs.fake_filesystem_unittest import TestCase
import os


class TestModifyMediaFolder(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir("/media_folder/Tv Show Series")
        self.fs.create_dir("/media_folder/Tv Show Series {edition-full screen}")
        self.fs.create_dir("/media_folder/Extra Folder")
        self.fs.create_dir("/media_folder/Extra Folder {edition-full screen}")

    def test_generate_new_media_folder_name_no_edition_tag(self):
        """
        Validates the built-in method generates the correct new media folder name without edition tag.
        """
        media_folder = ModifyMediaFolder()
        media_folder.new_media_title = "Legend of Zelda"
        media_folder.new_edition_tag = ""

        new_folder_name = media_folder.new_media_folder_name()

        assert new_folder_name == "Legend of Zelda"

    def test_generate_new_media_folder_name_with_edition_tag(self):
        """
        Validates the built-in method generates the correct new media folder name with edition tag.
        """
        media_folder = ModifyMediaFolder()
        media_folder.new_media_title = "Legend of Zelda"
        media_folder.new_edition_tag = "full screen"

        new_folder_name = media_folder.new_media_folder_name()

        assert new_folder_name == "Legend of Zelda {edition-full screen}"

    def test_check_if_extra_folders_to_be_generated_method(self):
        """
        Validates that the GenerateMediaFolder object's check_if_new_extra_folders_are_needed method returns True
        when there are extra folder(s) to be generated and false otherwise.
        """

        media_folder = ModifyMediaFolder()
        media_folder.extra_folders["other"] = True

        assert media_folder.check_if_new_extra_folders_are_needed() is True, (
            "Failed to detect extra folder(s) to be generated."
        )

        media_folder = ModifyMediaFolder()
        media_folder.extra_folders["other"] = False

        assert media_folder.check_if_new_extra_folders_are_needed() is False, (
            "Failed to detect no extra folder(s) needed to be generated."
        )

    def test_modify_tv_show_folder(self):
        """
        Validates the built-in function generates the correct number of new season folders
        """
        media_folder = ModifyMediaFolder()
        media_folder.directory = "/media_folder"
        media_folder.media_title = "Tv Show Series"
        media_folder.number_of_seasons = 1
        media_folder.number_of_new_seasons = 3

        media_folder.generate_new_season_folders()

        assert os.path.isdir("media_folder/Tv Show Series/Season 2")
        assert os.path.isdir("media_folder/Tv Show Series/Season 3")
        assert os.path.isdir("media_folder/Tv Show Series/Season 4")

    def test_modify_tv_show_folder_with_edition_tag(self):
        """
        Validates the built-in function generates the correct number of new season folders for a media folder
        that has an edition tag.
        """
        media_folder = ModifyMediaFolder()
        media_folder.directory = "/media_folder"
        media_folder.media_title = "Tv Show Series"
        media_folder.edition_tag = "full screen"
        media_folder.number_of_seasons = 1
        media_folder.number_of_new_seasons = 3

        media_folder.generate_new_season_folders()

        assert os.path.isdir("media_folder/Tv Show Series {edition-full screen}/Season 2")
        assert os.path.isdir("media_folder/Tv Show Series {edition-full screen}/Season 3")
        assert os.path.isdir("media_folder/Tv Show Series {edition-full screen}/Season 4")

    def test_adding_new_extra_folders(self):
        """
        Validates the build-in function generates the extra folders
        """
        extra_folder = ModifyMediaFolder()
        extra_folder.directory = "/media_folder"
        extra_folder.media_title = "Extra Folder"
        extra_folder.extra_folders["trailers"] = True
        extra_folder.extra_folders["behind the scenes"] = True
        extra_folder.extra_folders["deleted scenes"] = True
        extra_folder.extra_folders["featurettes"] = True
        extra_folder.extra_folders["interviews"] = True
        extra_folder.extra_folders["scenes"] = True
        extra_folder.extra_folders["shorts"] = True
        extra_folder.extra_folders["other"] = True

        extra_folder.generate_new_extra_folders()

        assert os.path.isdir("/media_folder/Extra Folder/Trailers")
        assert os.path.isdir("/media_folder/Extra Folder/Behind The Scenes")
        assert os.path.isdir("/media_folder/Extra Folder/Deleted Scenes")
        assert os.path.isdir("/media_folder/Extra Folder/Featurettes")
        assert os.path.isdir("/media_folder/Extra Folder/Interviews")
        assert os.path.isdir("/media_folder/Extra Folder/Scenes")
        assert os.path.isdir("/media_folder/Extra Folder/Shorts")
        assert os.path.isdir("/media_folder/Extra Folder/Other")

    def test_adding_new_extra_folders_with_edition_tag(self):
        """
        Validates the build-in function generates the extra folders for a media folder that has
        an edition tag.
        """
        extra_folder = ModifyMediaFolder()
        extra_folder.directory = "/media_folder"
        extra_folder.media_title = "Extra Folder"
        extra_folder.edition_tag = "full screen"
        extra_folder.extra_folders["trailers"] = True
        extra_folder.extra_folders["behind the scenes"] = True
        extra_folder.extra_folders["deleted scenes"] = True
        extra_folder.extra_folders["featurettes"] = True
        extra_folder.extra_folders["interviews"] = True
        extra_folder.extra_folders["scenes"] = True
        extra_folder.extra_folders["shorts"] = True
        extra_folder.extra_folders["other"] = True

        extra_folder.generate_new_extra_folders()

        assert os.path.isdir("/media_folder/Extra Folder {edition-full screen}/Trailers")
        assert os.path.isdir("/media_folder/Extra Folder {edition-full screen}/Behind The Scenes")
        assert os.path.isdir("/media_folder/Extra Folder {edition-full screen}/Deleted Scenes")
        assert os.path.isdir("/media_folder/Extra Folder {edition-full screen}/Featurettes")
        assert os.path.isdir("/media_folder/Extra Folder {edition-full screen}/Interviews")
        assert os.path.isdir("/media_folder/Extra Folder {edition-full screen}/Scenes")
        assert os.path.isdir("/media_folder/Extra Folder {edition-full screen}/Shorts")
        assert os.path.isdir("/media_folder/Extra Folder {edition-full screen}/Other")
