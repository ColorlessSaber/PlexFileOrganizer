from ..PlexFileOrganizer.classes import MediaFile

class TestMediaFileObject:

    def test_file_name_with_extension(self):
        """
        Validate it returns just the file with extension
        """
        file = MediaFile('/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e01.txt')
        assert (file.file_name() == "Zenless Zone Zero - s01e01.txt"), "Failed to return just file with extension."

    def test_file_name_without_extension(self):
        """
        Validate it returns just the file without extension
        """
        file = MediaFile('/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e01.txt')
        assert (file.file_name(with_extension=False) == "Zenless Zone Zero - s01e01"), "Failed to return just file with extension."

    def test_file_extension(self):
        """
        Validate it returns just the file extension
        """
        file = MediaFile('/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e01.txt')
        assert (file.file_extension() == ".txt"), "Failed to return just file with extension."

    def test_directory_path(self):
        """
        Validate it returns just the directory path to the file
        """
        file = MediaFile('/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e01.txt')
        assert (file.directory_path() == '/dir/dir1/Zenless Zone Zero/Season 1')

    def test_folder_file_is_in(self):
        """
        Validate it returns just the folder the file is in
        """
        file = MediaFile('/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e01.txt')
        assert (file.folder_file_is_in() == 'Season 1'), "Failed to return just folder with extension."
