from ..app.functions import default_folder_condition, skip_extra_folders

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

        assert skip_extra_folders(extra_folder_format[0]) == False
        assert skip_extra_folders(extra_folder_format[1]) == False
        assert skip_extra_folders(extra_folder_format[2]) == False
        assert skip_extra_folders(extra_folder_format[3]) == False
        assert skip_extra_folders(extra_folder_format[4]) == False
        assert skip_extra_folders(extra_folder_format[5]) == False
        assert skip_extra_folders(extra_folder_format[6]) == False
        assert skip_extra_folders(extra_folder_format[7]) == False
