import pathlib
from typing import *


# =====================================================================================================================
Type_PvDict = Dict[str, Optional[str]]
Type_Path = Union[str, pathlib.Path]
Type_Value = Union[str, NoReturn, None]


class Exx_PvNotAccepted(Exception):
    """
    Any final exception when value can't be get.
    """
    pass


# =====================================================================================================================
