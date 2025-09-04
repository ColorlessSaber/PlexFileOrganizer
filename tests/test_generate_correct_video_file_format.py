from ..PlexFileOrganizer.functions import generate_correct_video_file_format

class TestTvShowFileFormats:
    def test_update_all_season_folders(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/ZZZ_s01_ep01.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/ZZZ_s01_ep02.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/ZZZ_s01_ep03.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/ZZZ_s01_ep06.txt',
        )

        correct_file_format = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e01.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e02.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e03.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e04.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 4:
            assert False, f"All files should be updated, but only found {len(result)}"

        for file_to_check in zip(result, correct_file_format):
            file_generated, file_correct = file_to_check
            if file_generated[1] != file_correct:
                assert False, f"Found file not properly formatted: {file_generated[1]} != {file_correct}"

        assert True

    def test_update_all_specials_folders(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/ZZZ_s01_ep01.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/ZZZ_s01_ep02.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/ZZZ_s01_ep03.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/ZZZ_s01_ep06.txt',
        )

        correct_file_format = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e01.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e02.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e03.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e04.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 4:
            assert False, f"All files should be updated, but only found {len(result)}"

        for file_to_check in zip(result, correct_file_format):
            file_generated, file_correct = file_to_check
            if file_generated[1] != file_correct:
                assert False, f"Found file not properly formatted: {file_generated[1]} != {file_correct}"

        assert True

    def test_mix_episodes_season_folder(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e01.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e02.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e03-e05.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/ZZZ_s01_ep06.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e06.txt':
            assert False, f"File for mix episodes season folder is not formatted correctly. {result[0][1]}"

        assert True

    def test_mix_episodes_specials_folder(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e01.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e02.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e03-e05.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/ZZZ_s01_ep06.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][
            1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e06.txt':
            assert False, f"File for mix episodes specials folder is not formatted correctly. {result[0][1]}"

        assert True

class TestExtraFileFormats:
    def test_extra_file_trailer_format(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Trailers/Trailer 1.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Trailers/Trailer 2.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Trailers/new trailer.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Trailers/Trailer 3.txt':
            assert False, f"Extra file for trailer folder is not formated correctly. {result[0][1]}"

    def test_extra_file_behind_scenes_format(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Behind the Scenes/Behind the Scene 1.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Behind the Scenes/Behind the Scene 2.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Behind the Scenes/new scene.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Behind the Scenes/Behind the Scene 3.txt':
            assert False, f"Extra file for Behind the Scenes folder is not formated correctly. {result[0][1]}"

    def test_extra_file_deleted_scenes_format(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Deleted Scenes/Deleted Scene 1.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Deleted Scenes/Deleted Scene 2.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Deleted Scenes/new scene.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Deleted Scenes/Deleted Scene 3.txt':
            assert False, f"Extra file for Deleted Scenes folder is not formated correctly. {result[0][1]}"

    def test_extra_file_featurettes_format(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Featurettes/Featurette 1.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Featurettes/Featurette 2.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Featurettes/new Featurettes.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Featurettes/Featurette 3.txt':
            assert False, f"Extra file for Featurettes folder is not formated correctly. {result[0][1]}"

    def test_extra_file_interviews_format(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Interviews/Interview 1.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Interviews/Interview 2.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Interviews/new Interviews.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Interviews/Interview 3.txt':
            assert False, f"Extra file for Interviews folder is not formated correctly. {result[0][1]}"

    def test_extra_file_scenes_format(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Scenes/Scene 1.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Scenes/Scene 2.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Scenes/new Scenes.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Scenes/Scene 3.txt':
            assert False, f"Extra file for Scenes folder is not formated correctly. {result[0][1]}"

    def test_extra_file_shorts_format(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Shorts/Short 1.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Shorts/Short 2.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Shorts/new Shorts.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Shorts/Short 3.txt':
            assert False, f"Extra file for Scenes folder is not formated correctly. {result[0][1]}"

    def test_extra_file_other_format(self):
        files_to_update = (
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Other/Other 1.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Other/Other 2.txt',
            '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Other/new Other.txt',
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, f"Should only have one file that needs to be updated. {result}"

        if result[0][1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Other/Other 3.txt':
            assert False, f"Extra file for Others folder is not formated correctly. {result[0][1]}"

def test_movie_format():
    file = '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/movie.txt'

    result, _ = generate_correct_video_file_format((file,))

    if result[0][1] != '/Volumes/Hub SSD/python projects/PlexFileOrganizer/dir/Zenless Zone Zero/Zenless Zone Zero.txt':
        assert False, f"File for movie folder is not formatted correctly {result[0][1]}"

    assert True