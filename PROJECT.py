from typing import *


# =====================================================================================================================
class PROJECT:
    # AUX --------------------------------------------------
    _VERSION_TEMPLATE: Tuple[int] = (0, 0, 2)

    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "private_values"
    NAME_INSTALL: str = NAME_IMPORT.replace("_", "-")
    KEYWORDS: List[str] = [
      "environs", "environment",
      "private",
      "rc", "ini", "csv"
      "json"
    ]
    CLASSIFIERS_TOPICS_ADD: List[str] = [
        # "Topic :: Communications",
        # "Topic :: Communications :: Email",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "update values into class attrs from OsEnvironment or Ini/Json File"
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
         "IniFile",
         "JsonFile",
         "CsvFile",
         "direct text instead of file",
         "direct dict instead of file",
         ],

        ["attr access",
         "via any lettercase",
         "by instance attr",
         "like dict key on instance", ],

        ["work with dict", "apply", "update", "preupdate"],

        "update_dict as cumulative result - useful in case of settings result",
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 5, 8)
    VERSION_STR: str = ".".join(map(str, VERSION))
    TODO: List[str] = [
        "add Lock param after load"
    ]
    FIXME: List[str] = [
        "..."
    ]
    NEWS: List[str] = [
        ["add in init", "_dict", "_dont_check_values_exists"],
    ]


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================
