import string
import unittest
import pathlib
import random
import os
from PlexFileOrganizer.file_name_updater import file_name_updater


class FileExistTest(unittest.TestCase):
    """test the file_name_updater.py function"""
    new_file_name_list = ['1 - apple.txt', '2 - sonic.txt', '3 - tails.txt']

    def test_prep_work(self):
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
        for old_file_name, new_file_name in zip(old_file_name_list, self.new_file_name_list):
            print(f'Old file name: {old_file_name} -> new file name: {new_file_name}')
            files_to_update.append([old_file_name, new_file_name])

        file_name_updater(files_to_update, pathlib.Path().resolve())

    def test_file_one(self):
        file_one = ''.join([str(pathlib.Path().resolve()), '/', f'{self.new_file_name_list[0]}'])
        self.assertTrue(pathlib.Path(file_one).resolve().is_file(), f'File does not exist: {file_one}')

    def test_file_two(self):
        file_two = ''.join([str(pathlib.Path().resolve()), '/', f'{self.new_file_name_list[1]}'])
        self.assertTrue(pathlib.Path(file_two).resolve().is_file(), f'File does not exist: {file_two}')

    def test_file_three(self):
        file_three = ''.join([str(pathlib.Path().resolve()), '/', f'{self.new_file_name_list[2]}'])
        self.assertTrue(pathlib.Path(file_three).resolve().is_file(), f'File does not exist: {file_three}')


def suite():
    # this forces the unittest to run the test in a specific order.
    # This will make sure the files are always created first.
    suite_order = unittest.TestSuite()
    suite_order.addTest(FileExistTest('test_prep_work'))
    suite_order.addTest(FileExistTest('test_file_one'))
    suite_order.addTest(FileExistTest('test_file_two'))
    suite_order.addTest(FileExistTest('test_file_three'))

    return suite_order


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

