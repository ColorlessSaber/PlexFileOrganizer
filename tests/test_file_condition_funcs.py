from ..src.functions import video_file_condition

class TestFileConditionFunctions:
    def test_video_file_condition(self):
        """
        Validate that the video_file_condition function returns true when passed a video file.
        """
        assert video_file_condition("test.mkv")
        assert video_file_condition("test.mp4")
        assert video_file_condition("test.avi")