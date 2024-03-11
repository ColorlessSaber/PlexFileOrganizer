import string
import unittest
import pathlib
import random
from PlexFileOrganizer.file_name_updater import file_name_updater
# TODO: Make the test check every file and presents a list of what passed and which failed.


class FileExistText(unittest.TestCase):

    def file_exist(self, file_path):
        """Test if file exist at location"""
        self.assertTrue(pathlib.Path(file_path).resolve().is_file(), f'File does not exist: {file_path}')


class FileNameUpdaterTest(FileExistText):
    """test the file_name_updater.py function"""

    def test_file_name_updater(self):
        new_file_name_list = ['1 - apple.txt', '2 - sonic.txt', '3 - tails.txt']
        old_file_name_list = []
        files_to_update = []

        def random_word(length):
            letters = string.ascii_letters
            return ''.join(random.choice(letters) for _ in range(length))

        # create three text files, with random names with number 1-3 attached to the front
        for i in range(1, 4):
            old_file_name_list.append(f'{i} - {random_word(5)}.txt')
            with open(old_file_name_list[-1], 'w') as f:
                f.write('Test file 1')

        # print out the old to new file name for record while creating list of files to update
        for old_file_name, new_file_name in zip(old_file_name_list, new_file_name_list):
            print(f'Old file name: {old_file_name} -> new file name: {new_file_name}')
            files_to_update.append([old_file_name, new_file_name])

        file_name_updater(files_to_update, pathlib.Path().resolve())

        # check files exist
        for new_file_name in new_file_name_list:
            file_to_test_path = ''.join([str(pathlib.Path().resolve()), '/', f'{new_file_name}'])
            self.file_exist(file_to_test_path)


if __name__ == '__main__':
    unittest.main()
