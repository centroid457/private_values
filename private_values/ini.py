from .main import *

from configparser import ConfigParser


# =====================================================================================================================
class PrivateIni(PrivateBase):
    """
    Not recommended using DEFAULT SECTION!
    """
    FILENAME: str = "pv.ini"

    def get_as_dict(self) -> Union[Type_PvDict, NoReturn]:
        ini = ConfigParser()

        try:
            ini.read_string(self.filepath.read_text())
        except Exception as exx:
            msg = f"[CRITICAL] incorrect format file!\n{exx!r}"
            raise Exx_PvNotAccepted(msg)

        if not self.SECTION or self.SECTION == "DEFAULT" or ini.has_section(section=self.SECTION):
            result = dict(ini[self.SECTION or "DEFAULT"])
            return result
        else:
            msg = f"[CRITICAL] NO [{self.SECTION=} in {self.filepath=}]\n"
            msg += self.filepath.read_text()
            raise Exx_PvNotAccepted(msg)


# =====================================================================================================================
class PrivateAuthIni(PrivateAuth, PrivateIni):
    pass


class PrivateTgBotAddressIni(PrivateTgBotAddress, PrivateIni):
    pass


# =====================================================================================================================
