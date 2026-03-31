"""
An enum that holds the different media categories. Includes methods to help identify what "category"
the media folder is.
"""
from enum import StrEnum


class MediaCategory(StrEnum):
    MOVIE = "movie"
    TV = "tv"
    UNCATEGORIZED = "uncategorized"

    def is_movie(self) -> bool:
        return self.value == MediaCategory.MOVIE

    def is_tv(self) -> bool:
        return self.value == MediaCategory.TV