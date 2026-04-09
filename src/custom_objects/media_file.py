import pathlib
from collections import UserString


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
