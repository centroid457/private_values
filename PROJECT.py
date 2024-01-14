from typing import *


# =====================================================================================================================
class PROJECT:
    # AUX --------------------------------------------------
    _VERSION_TEMPLATE: Tuple[int] = (0, 0, 1)

    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # PROJECT ----------------------------------------------
    NAME_INSTALL: str = "private-values"
    NAME_IMPORT: str = "private_values"
    KEYWORDS: List[str] = [
      "environs", "environment",
      "private",
      "rc", "ini", "csv"
      "json"
    ]

    # GIT --------------------------------------------------
    DESCRIPTION_SHORT: str = "update values into class attrs from OsEnvironment or Ini/Json File"

    # README -----------------------------------------------
    pass

    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_LONG: str = """
Designed to use private data like username/pwd kept secure in OsEnvironment or Ini/Json-File for your several home projects at ones.  
And not open it in public.  

**CAUTION:**  
in requirements for other projects use fixed version! because it might be refactored so you would get exception soon.

    """
    FEATURES: List[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        ["load values to instance attrs from",
         "Environment",
         "iniFile",
         "JsonFile",
         ],
        ["attr access",
         "via any lettercase",
         "by instance attr",
         "like dict key on instance", ]
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 5, 4)
    VERSION_STR: str = ".".join(map(str, VERSION))
    TODO: List[str] = [
        "..."
    ]
    FIXME: List[str] = [
        "..."
    ]
    NEWS: List[str] = [
        "apply new pypi template"
    ]


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================
