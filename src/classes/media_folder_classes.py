from enum import Enum, unique, auto
from pathlib import Path
from dataclasses import dataclass, field
from ..custom_objects import ExtraFolders, MediaCategory

@unique
class FolderNameModification(Enum):
    """
    Help keep track of what modifications, if any, need to be made to an existing
    Media Folder.
    """
    KEEP_FOLDER_NAME = auto()
    CHANGE_FOLDER_NAME = auto()
    KEEP_EDITION_TAG = auto()
    CHANGE_EDITION_TAG = auto()
    REMOVE_EDITION_TAG = auto()

@dataclass
class MediaFolderData:
    """
    A dataclass to hold the information and folder(s) to make for the Media Folder.
    """

    directory: str = field(default=None)
    media_title: str = field(default=None)
    edition_tag: str = field(default="")
    media_type: MediaCategory = field(default=MediaCategory.UNCATEGORIZED)
    number_of_seasons: int = field(default=0)
    specials_season: bool = field(default=False)
    extra_folders: dict = field(default_factory=ExtraFolders)

    def media_folder_name(self) -> str:
        """
        Creates the name of the media folder.
        """
        if self.edition_tag != "" and not self.edition_tag.isspace():
            return f"{self.media_title} {{edition-{self.edition_tag}}}"
        else:
            return self.media_title

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

    new_media_title: str = field(default="")
    folder_name_modification: FolderNameModification = field(default=FolderNameModification.KEEP_FOLDER_NAME)
    new_edition_tag: str = field(default="")
    edition_tag_modification: FolderNameModification = field(default=FolderNameModification.KEEP_EDITION_TAG)
    number_of_new_seasons: int = field(default=0)

    def new_media_folder_name(self) -> str:
        """
        Creates the name of the media folder.
        """
        if self.new_edition_tag != "" and not self.new_edition_tag.isspace():
            return f"{self.new_media_title} {{edition-{self.new_edition_tag}}}"
        else:
            return self.new_media_title

    def generate_new_season_folders(self) -> None:
        """
        Generates one or more new season folders.

        :return:
        """
        media_folder_name = self.media_folder_name()

        # added plus one to start range so it doesn't use an existing number;
        # added plus one to end range to generate the correct number of new season folder(s)
        for season_num in range(
            self.number_of_seasons + 1,
            self.number_of_seasons + self.number_of_new_seasons + 1,
        ):
            Path("{}/{}/Season {}".format(self.directory, media_folder_name, season_num)).mkdir()

    def generate_specials_season_folder(self) -> None:
        """
        Generates the special season folder.

        :return:
        """
        media_folder_name = self.media_folder_name()

        Path("{}/{}/Specials".format(self.directory, media_folder_name)).mkdir()

    def generate_new_extra_folders(self) -> None:
        """
        Creates the extra folder(s) the user selected.

        :return:
        """
        media_folder_name = self.media_folder_name()

        for key in self.extra_folders:
            if self.extra_folders[key]:
                Path("{}/{}/{}".format(self.directory, media_folder_name, key.title())).mkdir()


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
        media_folder_name = self.media_folder_name()

        media_folder_path = Path("{}/{}".format(self.directory, media_folder_name))
        if media_folder_path.is_dir():
            return True
        else:
            return False

    def generate_media_folder(self) -> None:
        """
        Create the media folder in selected directory.

        :return:
        """
        media_folder_name = self.media_folder_name()

        Path("{}/{}".format(self.directory, media_folder_name)).mkdir()

    def generate_seasons(self) -> None:
        """
        Creates the number of season folder(s).

        :return:
        """
        media_folder_name = self.media_folder_name()

        # plus one is added to generate the correct number of season folder(s).
        for season_num in range(1, self.number_of_seasons + 1):
            Path(
                "{}/{}/Season {}".format(self.directory, media_folder_name, season_num)
            ).mkdir()

    def generate_specials_season_folder(self) -> None:
        """
        Generates the special season folder.

        :return:
        """
        media_folder_name = self.media_folder_name()
        Path("{}/{}/Specials".format(self.directory, media_folder_name)).mkdir()

    def generate_extra_folders(self) -> None:
        """
        Creates the extra folder(s) the user selected.

        :return:
        """
        media_folder_name = self.media_folder_name()
        for key in self.extra_folders:
            if self.extra_folders[key]:
                Path(
                    "{}/{}/{}".format(self.directory, media_folder_name, key.title())
                ).mkdir()
