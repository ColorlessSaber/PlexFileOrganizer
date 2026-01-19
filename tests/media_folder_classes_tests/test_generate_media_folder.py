from src.classes import GenerateMediaFolder
from pyfakefs.fake_filesystem_unittest import TestCase
import os

class TestGenerateMediaFolder(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir('/media_folder')
        self.fs.create_dir('/media_folder/Zenless Zone Zero')

    def test_generate_all_extra_folders(self):
        """
        Checks to see that all extra folders will be generated.
        """
        extra_folder = GenerateMediaFolder()
        extra_folder.directory = '/media_folder'
        extra_folder.media_title = 'Extra Test'
        extra_folder.media_type = 'movie'
        extra_folder.extra_folders['trailers'] = True
        extra_folder.extra_folders['behind the scenes'] = True
        extra_folder.extra_folders['deleted scenes'] = True
        extra_folder.extra_folders['featurettes'] = True
        extra_folder.extra_folders['interviews'] = True
        extra_folder.extra_folders['scenes'] = True
        extra_folder.extra_folders['shorts'] = True
        extra_folder.extra_folders['other'] = True

        extra_folder.generate_media_folder()
        extra_folder.generate_extra_folders()

        assert os.path.isdir('/media_folder/Extra Test/Trailers')
        assert os.path.isdir('/media_folder/Extra Test/Behind the Scenes'), print(os.listdir('/media_folder/Extra Test/'))
        assert os.path.isdir('/media_folder/Extra Test/Deleted Scenes')
        assert os.path.isdir('/media_folder/Extra Test/Featurettes')
        assert os.path.isdir('/media_folder/Extra Test/Interviews')
        assert os.path.isdir('/media_folder/Extra Test/Scenes')
        assert os.path.isdir('/media_folder/Extra Test/Shorts')
        assert os.path.isdir('/media_folder/Extra Test/Other')

    def test_check_if_extra_folders_to_be_generated_method(self):
        """
        Validates that the GenerateMediaFolder object's check_if_new_extra_folders_are_needed method returns True
        when there are extra folder(s) to be generated and false otherwise.
        """

        media_folder = GenerateMediaFolder()
        media_folder.extra_folders['other'] = True

        assert media_folder.check_if_new_extra_folders_are_needed() is True, 'Failed to detect extra folder(s) to be generated.'

        media_folder = GenerateMediaFolder()
        media_folder.extra_folders['other'] = False

        assert media_folder.check_if_new_extra_folders_are_needed() is False, 'Failed to detect no extra folder(s) needed to be generated.'

    def test_generate_new_tv_show_folder(self):
        """
        Checks to see that it properly generates a new TV show media folder.
        """
        media_folder = GenerateMediaFolder()

        # provide the tv show media folder contents
        media_folder.directory = '/media_folder'
        media_folder.media_title = 'Legend of Zelda Series'
        media_folder.media_type = 'tv'
        media_folder.number_of_seasons = 2
        media_folder.extra_folders['trailers'] = True
        media_folder.extra_folders['shorts'] = True

        media_folder.generate_media_folder()
        media_folder.generate_seasons()
        media_folder.generate_extra_folders()

        assert os.path.isdir('/media_folder/Legend of Zelda Series')
        assert os.path.isdir('/media_folder/Legend of Zelda Series/Season 1')
        assert os.path.isdir('/media_folder/Legend of Zelda Series/Season 2')
        assert os.path.isdir('/media_folder/Legend of Zelda Series/Trailers')
        assert os.path.isdir('/media_folder/Legend of Zelda Series/Shorts')

    def test_generate_new_movie_folder(self):
        """
        Checks to see that it properly generates a new movie folder.
        """
        media_folder = GenerateMediaFolder()
        media_folder.directory = '/media_folder'
        media_folder.media_title = 'Re:Creators'
        media_folder.media_type = 'movie'
        media_folder.extra_folders['trailers'] = True
        media_folder.extra_folders['shorts'] = True

        media_folder.generate_media_folder()
        media_folder.generate_extra_folders()

        assert os.path.isdir('/media_folder/Re:Creators')
        assert os.path.isdir('/media_folder/Re:Creators/Trailers')
        assert os.path.isdir('/media_folder/Re:Creators/Shorts')

    def test_generate_media_folder_detects_existing_folder(self):
        """
        Validates that the GenerateMediaFolder object detects existing folder.
        """
        media_folder = GenerateMediaFolder()
        media_folder.directory = '/media_folder'
        media_folder.media_title = 'Zenless Zone Zero'

        assert media_folder.check_if_media_folder_exists() is True, "Failed to detect existing folder."
