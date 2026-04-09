import os
from dataclasses import dataclass, field
from ..custom_objects import ExtraFolders, MediaCategory


@dataclass
class MediaFolderData:
    """
    A dataclass to hold the information and folder(s) to make for the Media Folder.
    """

    directory: str = field(default=None)
    media_title: str = field(default=None)
    media_type: MediaCategory = field(default=MediaCategory.UNCATEGORIZED)
    number_of_seasons: int = field(default=0)
    specials_season: bool = field(default=False)
    extra_folders: dict = field(default_factory=ExtraFolders)

    def check_if_new_extra_folders_are_needed(self) -> bool:
        """
        Checks to see if there are new extra folder(s) that need to be created.

        :return: True -- There are extra folder(s) that need to be created,
        False -- no extra folder(s) need to be created
        """
        for key in self.extra_folders:
            if self.extra_folders[key]:
                return True
        return False


@dataclass
class ModifyMediaFolder(MediaFolderData):
    """
    Holds methods to generate more folders for an existing media folder

    Inheritance MediaFolderData.
    """

    number_of_new_seasons: int = field(default=0)

    def generate_new_season_folders(self) -> None:
        """
        Generates one or more new season folders.

        :return:
        """
        # added plus one to start range so it doesn't use an existing number;
        # added plus one to end range to generate the correct number of new season folder(s)
        for season_num in range(
            self.number_of_seasons + 1,
            self.number_of_seasons + self.number_of_new_seasons + 1,
        ):
            os.mkdir("{}/Season {}".format(self.directory, season_num))

    def generate_specials_season_folder(self) -> None:
        """
        Generates the special season folder.

        :return:
        """
        os.mkdir("{}/Specials".format(self.directory))

    def generate_new_extra_folders(self) -> None:
        """
        Creates the extra folder(s) the user selected.

        :return:
        """
        for key in self.extra_folders:
            if self.extra_folders[key]:
                os.mkdir("{}/{}".format(self.directory, key.title()))


class GenerateMediaFolder(MediaFolderData):
    """
    Holds methods to generate a media folder based on user's selections.

    Inheritance MediaFolderData.
    """

    def check_if_media_folder_exists(self) -> bool:
        """
        Checks to see if media folder already exists in directory.

        :return: True -- directory exists, False -- directory not exists
        """
        does_directory_exist = os.path.isdir(
            "{}/{}".format(self.directory, self.media_title)
        )
        if does_directory_exist:
            return True
        else:
            return False

    def generate_media_folder(self) -> None:
        """
        Create the media folder in selected directory.

        :return:
        """
        os.mkdir("{}/{}".format(self.directory, self.media_title))

    def generate_seasons(self) -> None:
        """
        Creates the number of season folder(s).

        :return:
        """
        for season_num in range(
            1, self.number_of_seasons + 1
        ):  # plus one is added to generate the correct number of season folder(s).
            os.mkdir(
                "{}/{}/Season {}".format(self.directory, self.media_title, season_num)
            )

    def generate_specials_season_folder(self) -> None:
        """
        Generates the special season folder.

        :return:
        """
        os.mkdir("{}/{}/Specials".format(self.directory, self.media_title))

    def generate_extra_folders(self) -> None:
        """
        Creates the extra folder(s) the user selected.

        :return:
        """
        for key in self.extra_folders:
            if self.extra_folders[key]:
                os.mkdir(
                    "{}/{}/{}".format(self.directory, self.media_title, key.title())
                )
