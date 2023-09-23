from .main import *

from configparser import ConfigParser


# =====================================================================================================================
class PrivateIni(PrivateBase):
    """
    read exact section from IniFile
    Not recommended using DEFAULT SECTION!
    """
    SECTION: str = "DEFAULT"
    FILENAME: str = "pv.ini"

    def get_as_dict(self) -> Union[Type_PvDict, NoReturn]:
        ini = ConfigParser()

        try:
            ini.read_string(self.filepath.read_text())
        except Exception as exx:
            msg = f"[CRITICAL] incorrect format file!\n{exx!r}"
            raise Exx_PvNotAccepted(msg)

        if self.SECTION == "DEFAULT" or ini.has_section(section=self.SECTION):
            result = dict(ini[self.SECTION])
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
