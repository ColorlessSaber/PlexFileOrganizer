"""
File to hold custom objects--objects that are user control able
"""

import pathlib
from collections import UserDict, UserString
from enum import StrEnum


class MediaCategory(StrEnum):
    MOVIE = "movie"
    TV = "tv"
    UNCATEGORIZED = "uncategorized"

    def is_movie(self) -> bool:
        return self.value == MediaCategory.MOVIE

    def is_tv(self) -> bool:
        return self.value == MediaCategory.TV


class ExtraFolders(UserDict):
    """
    Custom semi-immutable dict. Only allow the user to modify the values at each key.
    """

    def __init__(self):
        super().__init__()
        self.data = {
            "trailers": False,
            "behind the scenes": False,
            "deleted scenes": False,
            "featurettes": False,
            "interviews": False,
            "scenes": False,
            "shorts": False,
            "other": False,
        }

    def __setitem__(self, key, value) -> None:
        if key not in self.data:
            raise KeyError(key)
        self.data[key] = value

    def pop(self, s=None) -> None:
        raise RuntimeError("Deletion not allowed")

    def popitem(self, s=None) -> None:
        raise RuntimeError("Deletion not allowed")

    def update(self, m, /, **kwargs) -> None:
        raise RuntimeError("Adding new entry not allowed")


class MediaFile(UserString):
    """
    custom immutable string for the full path for a media file. Has built-in functions to do simple tasks--
    return file name, file's extension, directory path, folder file is in
    """

    def __add__(self, other):
        raise RuntimeError("Adding not allowed")

    def file_name(self, with_extension=True) -> str:
        """
        Returns the name of the file, with the option to showing the file extension with the file name.

        :param with_extension: Keeps or strips extension from file name. Default True to keep extension
        :return: The file name with no extension
        """
        file_path = pathlib.Path(self.data)
        if with_extension:
            return file_path.name
        else:
            return file_path.stem

    def file_extension(self) -> str:
        """
        Strips the path and file name, leaving only the extension.

        :return: The file's extension
        """
        return pathlib.Path(self.data).suffix

    def directory_path(self) -> str:
        """
        Strips the file name, leaving only the directory path the file is in.

        :return: The directory path file is located
        """
        # str() is needed to convert PosixPath to string
        return str(pathlib.Path(self.data).parent)

    def folder_file_is_in(self) -> str:
        """
        Strips away everything, leaving only the folder the file is in.

        :return: The folder file is in.
        """
        return pathlib.Path(self.data).parent.resolve().name
