import os
from dataclasses import dataclass, field
from PlexFileOrganizer.functions import ExtraFolders

@dataclass
class MediaFolder:
    """
    A dataclass to hold the information and folder(s) to make for the Media Folder.
    """
    directory: str = field(default=None)
    media_title: str = field(default=None)
    movie_or_tv: str = field(default=None)
    number_of_seasons: int = field(default=None)
    extra_folders: dict = field(default_factory=ExtraFolders)

    def check_if_media_folder_exists(self):
        """
        Checks to see if media folder already exists in directory
        :return: A bool
        """
        does_directory_exist = os.path.isdir('{}/{}'.format(self.directory, self.media_title))
        if does_directory_exist:
            return True
        else:
            return False

    def generate_media_folder(self):
        """
        Create the media folder in selected directory
        :return:
        """
        os.mkdir('{}/{}'.format(self.directory, self.media_title))

    def generate_seasons(self):
        """
        Creates the number of season folder(s)
        :return:
        """
        for season_num in range(1, self.number_of_seasons+1):
            os.mkdir('{}/{}/Season {}'.format(self.directory, self.media_title, season_num))

    def generate_extra_folders(self):
        """
        Creates the extra folder(s) the user selected
        :return: a bool flag to indicate if an extra folder was created
        """
        an_extra_folder_was_created = False # a flag to indicate if an extra folder was created.
        for key in self.extra_folders:
            if self.extra_folders[key]:
                os.mkdir('{}/{}/{}'.format(self.directory, self.media_title, key))
                an_extra_folder_was_created = True
        return an_extra_folder_was_created