from src.functions import generate_correct_video_file_format


def test_movie_format():
    file = "/dir/dir1/Zenless Zone Zero/movie.txt"

    result, _ = generate_correct_video_file_format((file,))

    if result[0][1] != "/dir/dir1/Zenless Zone Zero/Zenless Zone Zero.txt":
        assert False, f"File for movie folder is not formatted correctly {result[0][1]}"

    assert True
