import re

class CorrectMediaFileFormat:

    def tv_show_episode_format(self, media_file):
        """
        Checks media_file to see if its formated correctly for tv show episode.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        tv_show_episode_format = re.compile(r"""
                    ^.+   # wildcard to handle name of show
                    \s  
                    -
                    \s
                    s\d+e\d+(-e\d+)?  # season, episode number and possible multiple episode
                    \.\w+ # file extension
                    """, re.VERBOSE | re.IGNORECASE)
        # TV show episodes can be saved in two different folders: Season # or Specials.
        if re.match(r'^(Season\s\d)|(Specials)$', media_file.path.split('/')[-2], re.IGNORECASE):
            if tv_show_episode_format.match(media_file.name):
                return True
            else:
                return False

    def movie_format(self, media_file):
        """
        Checks media_file to see if its formated correctly for movie.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        movie_format = re.compile(r"""
                    ^(?P<title>^.+)   # group 1: the name of the file
                    (?P<ext>\.\w+) # group 2: file extension
                    """, re.VERBOSE | re.IGNORECASE)
        if movie_format.match(media_file.name).group('title') == media_file.path.split('/')[-1]:
            return True
        else:
            return False

    def trailer_format(self, media_file):
        """
        Checks media_file to see if its formated correctly for trailer file.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        trailer_folder_format = re.compile(r"""
            ^.+       # wildcard to handle the name of the show
            _pv\d+   # the add on to identify its a Trailer
            \.\w+    # file extension
            """, re.VERBOSE | re.IGNORECASE)
        if re.match(r"^trailer(s)?$", media_file.path.split('/')[-2], re.IGNORECASE):
            if trailer_folder_format.match(media_file.name):
                return True
            else:
                return False

    def behind_the_scenes_format(self, media_file):
        """
        Checks media_file to see if its formated correctly for behind the scenes file.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        behind_the_scenes_format = re.compile(r"""
            ^.+       # wildcard to handle the name of the show
            _behind_sc\d+   # the add on to identify its a Behind The Scenes
            \.\w+    # file extension
            """, re.VERBOSE | re.IGNORECASE)
        if re.match(r"^behind the scenes$", media_file.path.split('/')[-2], re.IGNORECASE):
            if behind_the_scenes_format.match(media_file.name):
                return True
            else:
                return False

    def deleted_scenes_format(self, media_file):
        """
        Checks media_file to see if its formated correctly for deleted scenes file.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        deleted_scenes_format = re.compile(r"""
                ^.+       # wildcard to handle the name of the show
                _deleted_sc\d+   # the add on to identify its a Deleted Scenes
                \.\w+    # file extension
                """, re.VERBOSE | re.IGNORECASE)
        if re.match(r"^deleted scenes$", media_file.path.split('/')[-2], re.IGNORECASE):
            if deleted_scenes_format.match(media_file.name):
                return True
            else:
                return False

    def featurettes_format(self, media_file):
        """
        Checks media_file to see if its formated correctly for featurettes file.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        featurettes_format = re.compile(r"""
                    ^.+       # wildcard to handle the name of the show
                    _feat\d+   # the add on to identify its a Featurettes
                    \.\w+    # file extension
                    """, re.VERBOSE | re.IGNORECASE)
        if re.match(r"^featurettes$", media_file.path.split('/')[-2], re.IGNORECASE):
            if featurettes_format.match(media_file.name):
                return True
            else:
                return False

    def interviews_format(self, media_file):
        """
        Checks media_file to see if its formated correctly for interviews file.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        interviews_format = re.compile(r"""
                        ^.+       # wildcard to handle the name of the show
                        _inter\d+   # the add on to identify its a Interview
                        \.\w+    # file extension
                        """, re.VERBOSE | re.IGNORECASE)
        if re.match(r"^interviews$", media_file.path.split('/')[-2], re.IGNORECASE):
            if interviews_format.match(media_file.name):
                return True
            else:
                return False

    def scenes_format(self, media_file):
        """
        Checks media_file to see if its formated correctly for scenes file.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        scenes_format = re.compile(r"""
                            ^.+       # wildcard to handle the name of the show
                            _sc\d+   # the add on to identify its a Scenes
                            \.\w+    # file extension
                            """, re.VERBOSE | re.IGNORECASE)
        if re.match(r"^scenes$", media_file.path.split('/')[-2], re.IGNORECASE):
            if scenes_format.match(media_file.name):
                return True
            else:
                return False

    def shorts_format(self, media_file):
        """
        Checks media_file to see if its formated correctly for shorts file.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        shorts_format = re.compile(r"""
                    ^.+       # wildcard to handle the name of the show
                    _shorts\d+   # the add on to identify its a Shorts
                    \.\w+    # file extension
                    """, re.VERBOSE | re.IGNORECASE)
        if re.match(r"^shorts$", media_file.path.split('/')[-2], re.IGNORECASE):
            if shorts_format.match(media_file.name):
                return True
            else:
                return False

    def other_format(self, media_file):
        """
        Checks media_file to see if its formated correctly for other file.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        other_format = re.compile(r"""
                            ^.+       # wildcard to handle the name of the show
                            _other\d+   # the add on to identify its a Other
                            \.\w+    # file extension
                            """, re.VERBOSE | re.IGNORECASE)

        if re.match(r"^other$", media_file.path.split('/')[-2], re.IGNORECASE):
            if other_format.match(media_file.name):
                return True
            else:
                return False

    def all_formats(self, media_file):
        """
        Checks media_file against all formats and True or False based on if it passes any of them or not.

        :param media_file: a DirEntry object of media file to check
        :return:
        """
        if self.tv_show_episode_format(media_file):
            return True
        elif self.movie_format(media_file):
            return True
        elif self.trailer_format(media_file):
            return True
        elif self.behind_the_scenes_format(media_file):
            return True
        elif self.featurettes_format(media_file):
            return True
        elif self.interviews_format(media_file):
            return True
        elif self.scenes_format(media_file):
            return True
        elif self.shorts_format(media_file):
            return True
        elif self.other_format(media_file):
            return True
        else:
            return False