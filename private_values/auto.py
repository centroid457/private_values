from .main import Type_PvDict, PrivateAuth, PrivateTgBotAddress
from .env import PrivateEnv
from .ini import PrivateIni
from .json import PrivateJson
from .csv import PrivateCsv

from typing import *


# =====================================================================================================================
class PrivateAuto(PrivateJson, PrivateIni, PrivateEnv):
    """This class will try all variants in order Json-Ini-Env.
    and take values ONLY from FIRST ONE source with all needed values!
    It will not merge sources!
    """
    def as_dict(self) -> Union[Type_PvDict, NoReturn]:
        annots = self.annots_get_set()
        annots_lower = set(map(str.lower, annots))

        for cls in [PrivateAuto, PrivateJson, PrivateIni, PrivateCsv]:
            try:
                self.FILENAME = super(cls, self).FILENAME
                self._filepath_apply_new()
                data = super(cls, self).as_dict()
                data_lower = set(map(str.lower, data))
                if data_lower.issuperset(annots_lower):
                    return data
            except:
                pass


# =====================================================================================================================
class PrivateAuthAuto(PrivateAuth, PrivateAuto):
    pass


class PrivateTgBotAddressAuto(PrivateTgBotAddress, PrivateAuto):
    pass


# =====================================================================================================================
