from ...app.functions import generate_correct_video_file_format

class TestExtraFileFormats:
    def test_extra_file_trailer_format(self):
        files_to_update = (
            '/dir/dir1/Zenless Zone Zero/Trailers/Trailer 1.txt',
            '/dir/dir1/Zenless Zone Zero/Trailers/Trailer 2.txt',
            '/dir/dir1/Zenless Zone Zero/Trailers/new trailer.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/dir/dir1/Zenless Zone Zero/Trailers/Trailer 3.txt':
            assert False, f"Extra file for trailer folder is not formated correctly. {result[0][1]}"

    def test_extra_file_behind_scenes_format(self):
        files_to_update = (
            '/dir/dir1/Zenless Zone Zero/Behind the Scenes/Behind the Scene 1.txt',
            '/dir/dir1/Zenless Zone Zero/Behind the Scenes/Behind the Scene 2.txt',
            '/dir/dir1/Zenless Zone Zero/Behind the Scenes/new scene.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/dir/dir1/Zenless Zone Zero/Behind the Scenes/Behind the Scene 3.txt':
            assert False, f"Extra file for Behind the Scenes folder is not formated correctly. {result[0][1]}"

    def test_extra_file_deleted_scenes_format(self):
        files_to_update = (
            '/dir/dir1/Zenless Zone Zero/Deleted Scenes/Deleted Scene 1.txt',
            '/dir/dir1/Zenless Zone Zero/Deleted Scenes/Deleted Scene 2.txt',
            '/dir/dir1/Zenless Zone Zero/Deleted Scenes/new scene.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/dir/dir1/Zenless Zone Zero/Deleted Scenes/Deleted Scene 3.txt':
            assert False, f"Extra file for Deleted Scenes folder is not formated correctly. {result[0][1]}"

    def test_extra_file_featurettes_format(self):
        files_to_update = (
            '/dir/dir1/Zenless Zone Zero/Featurettes/Featurette 1.txt',
            '/dir/dir1/Zenless Zone Zero/Featurettes/Featurette 2.txt',
            '/dir/dir1/Zenless Zone Zero/Featurettes/new Featurettes.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/dir/dir1/Zenless Zone Zero/Featurettes/Featurette 3.txt':
            assert False, f"Extra file for Featurettes folder is not formated correctly. {result[0][1]}"

    def test_extra_file_interviews_format(self):
        files_to_update = (
            '/dir/dir1/Zenless Zone Zero/Interviews/Interview 1.txt',
            '/dir/dir1/Zenless Zone Zero/Interviews/Interview 2.txt',
            '/dir/dir1/Zenless Zone Zero/Interviews/new Interviews.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/dir/dir1/Zenless Zone Zero/Interviews/Interview 3.txt':
            assert False, f"Extra file for Interviews folder is not formated correctly. {result[0][1]}"

    def test_extra_file_scenes_format(self):
        files_to_update = (
            '/dir/dir1/Zenless Zone Zero/Scenes/Scene 1.txt',
            '/dir/dir1/Zenless Zone Zero/Scenes/Scene 2.txt',
            '/dir/dir1/Zenless Zone Zero/Scenes/new Scenes.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/dir/dir1/Zenless Zone Zero/Scenes/Scene 3.txt':
            assert False, f"Extra file for Scenes folder is not formated correctly. {result[0][1]}"

    def test_extra_file_shorts_format(self):
        files_to_update = (
            '/dir/dir1/Zenless Zone Zero/Shorts/Short 1.txt',
            '/dir/dir1/Zenless Zone Zero/Shorts/Short 2.txt',
            '/dir/dir1/Zenless Zone Zero/Shorts/new Shorts.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/dir/dir1/Zenless Zone Zero/Shorts/Short 3.txt':
            assert False, f"Extra file for Scenes folder is not formated correctly. {result[0][1]}"

    def test_extra_file_other_format(self):
        files_to_update = (
            '/dir/dir1/Zenless Zone Zero/Other/Other 1.txt',
            '/dir/dir1/Zenless Zone Zero/Other/Other 2.txt',
            '/dir/dir1/Zenless Zone Zero/Other/new Other.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/dir/dir1/Zenless Zone Zero/Other/Other 3.txt':
            assert False, f"Extra file for Others folder is not formated correctly. {result[0][1]}"
