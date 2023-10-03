from .main import *

import json


# =====================================================================================================================
class PrivateJson(PrivateBase):
    FILENAME: str = "pv.json"

    def as_dict(self) -> Union[Type_PvDict, NoReturn]:
        """
        section only in first level!
        """
        try:
            json_data = json.loads(self.filepath.read_text())
        except Exception as exx:
            msg = f"[CRITICAL] incorrect format file!\n{exx!r}"
            print(msg)
            if self.RAISE:
                raise Exx_PvNotAccepted(msg)
            else:
                return {}

        if self.SECTION:
            json_data = json_data.get(self.SECTION)

        if json_data:
            return json_data
        else:
            msg = f"[CRITICAL] NO [{self.SECTION=} in {self.filepath=}]\n"
            msg += self.filepath.read_text()
            if self.RAISE:
                raise Exx_PvNotAccepted(msg)
            else:
                return {}

# =====================================================================================================================
class PrivateAuthJson(PrivateAuth, PrivateJson):
    pass


class PrivateTgBotAddressJson(PrivateTgBotAddress, PrivateJson):
    pass


# =====================================================================================================================
