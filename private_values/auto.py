from .main import Type_PvDict, PrivateAuth, PrivateTgBotAddress
from .env import PrivateEnv
from .ini import PrivateIni
from .json import PrivateJson

from typing import *


# =====================================================================================================================
class PrivateAuto(PrivateJson, PrivateIni, PrivateEnv):
    def get_as_dict(self) -> Union[Type_PvDict, NoReturn]:
        for cls in [PrivateAuto, PrivateJson, PrivateIni]:
            try:
                self.FILENAME = super(cls, self).FILENAME
                self.filepath_apply_new()

                data = super(cls, self).get_as_dict()
                if self.check_by_annotations(data):
                    return data
            except:
                pass


# =====================================================================================================================
class PrivateAuthAuto(PrivateAuth, PrivateAuto):
    pass


class PrivateTgBotAddressAuto(PrivateTgBotAddress, PrivateAuto):
    pass


# =====================================================================================================================
