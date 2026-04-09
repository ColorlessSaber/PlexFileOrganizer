from src.functions import prep_files_for_modified_renaming

class TestPrepFilesForModifiedRenaming:
    def test_prep_files_for_modified_renaming(self):
        """
        Validates the prep_files_for_modified_renaming is working properly
        """
        temp_file_list = [
            ["/foo/bar", "zzz", "Zenless Zone Zero", ".mkv"],
            ["/foo2/bar", "legend of zelda tp", "The Legend of Zelda Twilight Princess", ".mp4"],
            ["/foo3/bar", "GOD BLESSING THE MISTAKEN", "God Bless the Mistaken", ".avi"]
        ]

        correct_files_identified = [
            ("/foo/bar/zzz.mkv", "/foo/bar/zzz_ToBeRenamed.mkv"),
            ("/foo2/bar/legend of zelda tp.mp4", "/foo2/bar/legend of zelda tp_ToBeRenamed.mp4"),
            ("/foo3/bar/GOD BLESSING THE MISTAKEN.avi", "/foo3/bar/GOD BLESSING THE MISTAKEN_ToBeRenamed.avi")
        ]

        correct_file_to_rename = [
            ("/foo/bar/zzz_ToBeRenamed.mkv", "/foo/bar/Zenless Zone Zero.mkv"),
            ("/foo2/bar/legend of zelda tp_ToBeRenamed.mp4", "/foo2/bar/The Legend of Zelda Twilight Princess.mp4"),
            ("/foo3/bar/GOD BLESSING THE MISTAKEN_ToBeRenamed.avi", "/foo3/bar/God Bless the Mistaken.avi")
        ]

        files_identified_list, file_to_rename_list = prep_files_for_modified_renaming(temp_file_list)

        assert correct_files_identified == files_identified_list, "Failed to add identification extension to files"
        assert correct_file_to_rename == file_to_rename_list, "Failed to pair up old file name to new file name"