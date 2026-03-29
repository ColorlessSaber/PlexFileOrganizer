from src.functions import generate_correct_video_file_format


class TestTvShowFileFormats:
    def test_update_all_season_folders(self):
        files_to_update = (
            "/dir/dir1/Zenless Zone Zero/Season 1/ZZZ_s01_ep01.txt",
            "/dir/dir1/Zenless Zone Zero/Season 1/ZZZ_s01_ep02.txt",
            "/dir/dir1/Zenless Zone Zero/Season 1/ZZZ_s01_ep03.txt",
            "/dir/dir1/Zenless Zone Zero/Season 1/ZZZ_s01_ep06.txt",
        )

        correct_file_format = (
            "/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e01.txt",
            "/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e02.txt",
            "/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e03.txt",
            "/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e04.txt",
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 4:
            assert False, f"All files should be updated, but only found {len(result)}"

        for file_to_check in zip(result, correct_file_format):
            file_generated, file_correct = file_to_check
            if file_generated[1] != file_correct:
                assert False, (
                    f"Found file not properly formatted: {file_generated[1]} != {file_correct}"
                )

        assert True

    def test_update_all_specials_folders(self):
        files_to_update = (
            "/dir/dir1/Zenless Zone Zero/Specials/ZZZ_s01_ep01.txt",
            "/dir/dir1/Zenless Zone Zero/Specials/ZZZ_s01_ep02.txt",
            "/dir/dir1/Zenless Zone Zero/Specials/ZZZ_s01_ep03.txt",
            "/dir/dir1/Zenless Zone Zero/Specials/ZZZ_s01_ep06.txt",
        )

        correct_file_format = (
            "/dir/dir1/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e01.txt",
            "/dir/dir1/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e02.txt",
            "/dir/dir1/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e03.txt",
            "/dir/dir1/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e04.txt",
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 4:
            assert False, f"All files should be updated, but only found {len(result)}"

        for file_to_check in zip(result, correct_file_format):
            file_generated, file_correct = file_to_check
            if file_generated[1] != file_correct:
                assert False, (
                    f"Found file not properly formatted: {file_generated[1]} != {file_correct}"
                )

        assert True

    def test_mix_episodes_season_folder(self):
        files_to_update = (
            "/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e01.txt",
            "/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e02.txt",
            "/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e03-e05.txt",
            "/dir/dir1/Zenless Zone Zero/Season 1/ZZZ_s01_ep06.txt",
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, (
                f"Should only have one file that needs to be updated. {result}"
            )

        if (
            result[0][1]
            != "/dir/dir1/Zenless Zone Zero/Season 1/Zenless Zone Zero - s01e06.txt"
        ):
            assert False, (
                f"File for mix episodes season folder is not formatted correctly. {result[0][1]}"
            )

        assert True

    def test_mix_episodes_specials_folder(self):
        files_to_update = (
            "/dir/dir1/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e01.txt",
            "/dir/dir1/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e02.txt",
            "/dir/dir1/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e03-e05.txt",
            "/dir/dir1/Zenless Zone Zero/Specials/ZZZ_s01_ep06.txt",
        )

        result, _ = generate_correct_video_file_format(files_to_update)

        if len(result) != 1:
            assert False, (
                f"Should only have one file that needs to be updated. {result}"
            )

        if (
            result[0][1]
            != "/dir/dir1/Zenless Zone Zero/Specials/Zenless Zone Zero - s00e06.txt"
        ):
            assert False, (
                f"File for mix episodes specials folder is not formatted correctly. {result[0][1]}"
            )

        assert True
