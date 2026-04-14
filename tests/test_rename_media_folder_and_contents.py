from src.functions import rename_media_folder_and_contents
from pyfakefs.fake_filesystem_unittest import TestCase
from pathlib import Path

class TestRenameMediaFolderAndContents(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        self.fs.create_file("/foo/ZZZ/ZZZ.mkv")
        self.fs.create_file("/foo/Legend of Zelda/Season 1/Legend of Zelda - s01e01.mkv")
        self.fs.create_file("/foo/Legend of Zelda/Season 1/Legend of Zelda - s01e02.mkv")
        self.fs.create_file("/foo/Legend of Zelda/Season 1/Legend of Zelda - s01e03.mkv")

    def test_rename_movie_media_folder(self):
        """
        Rename a media folder that is for a movie and its file
        """
        old_title = "ZZZ"
        new_title = "Zenless Zone Zero"
        directory = "/foo"
        rename_media_folder_and_contents(old_title, new_title, directory)

        assert Path("/foo/Zenless Zone Zero/Zenless Zone Zero.mkv").exists(), "Failed to rename file and folder"

    def test_rename_tv_show_media_folder(self):
        """
        Rename a media folder that is for a tv show and files
        """
        old_title = "Legend of Zelda"
        new_title = "The Legend of Zelda Twilight Princess"
        directory = "/foo"
        rename_media_folder_and_contents(old_title, new_title, directory)

        assert Path("/foo/The Legend of Zelda Twilight Princess/Season 1/The Legend of Zelda Twilight Princess - s01e01.mkv").exists(), "Failed to rename file and folder"
        assert Path("/foo/The Legend of Zelda Twilight Princess/Season 1/The Legend of Zelda Twilight Princess - s01e02.mkv").exists(), "Failed to rename file and folder"
        assert Path("/foo/The Legend of Zelda Twilight Princess/Season 1/The Legend of Zelda Twilight Princess - s01e03.mkv").exists(), "Failed to rename file and folder"
