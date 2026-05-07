from src.functions.media_file_format_funcs import movie_file_format
from src.custom_objects import MediaFile

def test_movie_format():
    file = "/dir/dir1/Zenless Zone Zero/movie.txt"

    result, _ = movie_file_format([MediaFile(file)])

    if result[0][1] != "/dir/dir1/Zenless Zone Zero/Zenless Zone Zero.txt":
        assert False, f"File for movie folder is not formatted correctly {result[0][1]}"

    assert True
