from src.functions import default_folder_condition, skip_extra_folders

class TestFolderConditionFuncs:
    def test_default_folder_condition(self):
        """
        Validates that the default folder condition works as expected.
        """
        assert default_folder_condition("test")

    def test_skip_extra_folders(self):
        """
        Validatest that the skip_extra_folders functions skips all extra folders.
        """
        extra_folder_format = [
            "trailers",
            "behind the scenes",
            "deleted scenes",
            "featurettes",
            "interviews",
            "scenes",
            "shorts",
            "other"
        ]

        assert skip_extra_folders(extra_folder_format[0]) is False
        assert skip_extra_folders(extra_folder_format[1]) is False
        assert skip_extra_folders(extra_folder_format[2]) is False
        assert skip_extra_folders(extra_folder_format[3]) is False
        assert skip_extra_folders(extra_folder_format[4]) is False
        assert skip_extra_folders(extra_folder_format[5]) is False
        assert skip_extra_folders(extra_folder_format[6]) is False
        assert skip_extra_folders(extra_folder_format[7]) is False
