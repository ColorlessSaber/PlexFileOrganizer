from ..app.functions import directory_scanner
from pyfakefs.fake_filesystem_unittest import TestCase

class TestDirectoryScanner(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        # create the three level tear folder system
        self.fs.create_file("/foo1/foo2/foo3/foo3_test1.txt")
        self.fs.create_file("/foo1/foo2/foo3/foo3_test2.txt")
        self.fs.create_file("/foo1/foo2/foo3/foo3_test3.txt")
        self.fs.create_file("/foo1/foo2/foo2_test1.txt")
        self.fs.create_file("/foo1/foo2/foo2_test2.txt")
        self.fs.create_file("/foo1/foo2/foo2_test3.txt")
        self.fs.create_file("/foo1/foo1_test1.txt")
        self.fs.create_file("/foo1/foo1_test2.txt")
        self.fs.create_file("/foo1/foo1_test3.txt")

    def test_directory_scanner_no_sub_folders(self):
        """
        Validate that the directory_scanner functions finds all files in a folder with no folder
        """
        number_of_files_found = 0
        for _ in directory_scanner("/foo1/foo2/foo3"):
            number_of_files_found += 1

        assert number_of_files_found == 3

    def test_directory_scanner_one_sub_folder(self):
        """
        Validate that the directory_scanner functions finds all files in a folder and one sub folder down
        """
        number_of_files_found = 0
        for _ in directory_scanner("/foo1/foo2"):
            number_of_files_found += 1

        assert number_of_files_found == 6

    def test_directory_scanner_two_sub_folders(self):
        """
        Validate that the directory_scanner functions finds all files in a folder with a sub folder and that folder
        having its own sub folder
        """
        number_of_files_found = 0
        for _ in directory_scanner("/foo1"):
            number_of_files_found += 1

        assert number_of_files_found == 9