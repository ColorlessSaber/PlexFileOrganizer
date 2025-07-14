"""
File to hold custom objects--objects that are user control able
"""
import os
import pathlib
from collections import UserDict, UserString

class ExtraFolders(UserDict):
    """
    Custom semi-immutable dict. Only allow the user to the values at each key.
    """
    def __init__(self):
        super().__init__()
        self.data = {
                'trailers': False,
                'behind the scenes': False,
                'deleted scenes': False,
                'featurettes': False,
                'interviews': False,
                'scenes': False,
                'shorts': False,
                'other': False
            }

    def pop(self, s = None):
        raise RuntimeError("Deletion not allowed")

    def popitem(self, s= None):
        raise RuntimeError("Deletion not allowed")

    def update(self, m, /, **kwargs):
        raise RuntimeError("Adding new entry not allowed")

class MediaFile(UserString):
    """
    custom immutable string for the full path for a media file. Has built-in functions to do simple tasks-- return file name,
    return file_extension, return the folder the file is in.
    """

    def split(self, sep = None, maxsplit = -1):
        raise RuntimeError("Splitting not allowed")

    def __add__(self, other):
        raise RuntimeError("Adding not allowed")

    def file_name_no_extension(self):
        """
        Stips the path from the file, leaving only the name of the file without its extension
        :return: A string. The file name with no extension
        """
        file_path = pathlib.Path(self.data)
        return file_path.stem

    def file_extension(self):
        """
        Strips the path and file name, leaving only the extension.
        :return: A string. file's extension
        """
        _, extension = os.path.splitext(self.data)
        return extension

    def directory_path(self):
        """
        Strips the file name, leaving only the directory path the file is in.
        :return: A string. The directory path file is located
        """
        return os.path.dirname(os.path.abspath(self.data))

    def folder_file_is_in(self):
        """
        Strips away everything, leaving only the folder the file is in.
        :return: A string. The folder file is in.
        """
        return pathlib.Path(self.data).parent.resolve().name