from collections import UserDict


class ExtraFolders(UserDict):
    """
    Custom semi-immutable dict. Only allow the user to modify the values at each key.
    """

    def __init__(self):
        super().__init__()
        self.data = {
            "trailers": False,
            "behind the scenes": False,
            "deleted scenes": False,
            "featurettes": False,
            "interviews": False,
            "scenes": False,
            "shorts": False,
            "other": False,
        }

    def __setitem__(self, key, value) -> None:
        if key not in self.data:
            raise KeyError(key)
        self.data[key] = value

    def pop(self, s=None) -> None:
        raise RuntimeError("Deletion not allowed")

    def popitem(self, s=None) -> None:
        raise RuntimeError("Deletion not allowed")

    def update(self, m, /, **kwargs) -> None:
        raise RuntimeError("Adding new entry not allowed")

