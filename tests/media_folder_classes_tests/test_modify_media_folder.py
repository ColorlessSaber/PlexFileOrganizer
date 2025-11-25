from ...src.classes import ModifyMediaFolder
from pyfakefs.fake_filesystem_unittest import TestCase
import os

class TestModifyMediaFolder(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir('/media_folder/Tv Show Series')
        self.fs.create_dir('/media_folder/Extra Folder')

    def test_modify_tv_show_folder(self):
        """
        Validates the built-in function generates the correct number of new season folders
        """
        media_folder = ModifyMediaFolder()
        media_folder.directory = '/media_folder/Tv Show Series'
        media_folder.number_of_seasons = 1
        media_folder.number_of_new_seasons = 3

        media_folder.generate_new_season_folders()

        assert os.path.isdir('media_folder/Tv Show Series/Season 2')
        assert os.path.isdir('media_folder/Tv Show Series/Season 3')
        assert os.path.isdir('media_folder/Tv Show Series/Season 4')

    def test_adding_new_extra_folders(self):
        """
        Validates the build-in function generates the extra folders
        """
        extra_folder = ModifyMediaFolder()
        extra_folder.directory = '/media_folder/Extra Folder'
        extra_folder.extra_folders['trailers'] = True
        extra_folder.extra_folders['behind the scenes'] = True
        extra_folder.extra_folders['deleted scenes'] = True
        extra_folder.extra_folders['featurettes'] = True
        extra_folder.extra_folders['interviews'] = True
        extra_folder.extra_folders['scenes'] = True
        extra_folder.extra_folders['shorts'] = True
        extra_folder.extra_folders['other'] = True

        extra_folder.generate_new_extra_folders()

        assert os.path.isdir('/media_folder/Extra Folder/Trailers')
        assert os.path.isdir('/media_folder/Extra Folder/Behind the Scenes')
        assert os.path.isdir('/media_folder/Extra Folder/Deleted Scenes')
        assert os.path.isdir('/media_folder/Extra Folder/Featurettes')
        assert os.path.isdir('/media_folder/Extra Folder/Interviews')
        assert os.path.isdir('/media_folder/Extra Folder/Scenes')
        assert os.path.isdir('/media_folder/Extra Folder/Shorts')
        assert os.path.isdir('/media_folder/Extra Folder/Other')