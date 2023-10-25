from .main import *

from configparser import ConfigParser


# =====================================================================================================================
class PrivateCsv(PrivateBase):
    """Get values from CSV file.

    this is not actually about private values!
    It was created for parsing stdout from CLI commands about device info,
    which is has data like
    '
        C:\Users\a.starichenko>STM32_Programmer_CLI --verbosity 1 --connect port=swd index=0
              -------------------------------------------------------------------
                               STM32CubeProgrammer v2.14.0
              -------------------------------------------------------------------

        ST-LINK SN  : 323609013212354D434B4E00
        ST-LINK FW  : V2J29S7
        Board       : --
        Voltage     : 3.26V
        SWD freq    : 4000 KHz
        Connect mode: Normal
        Reset mode  : Software reset
        Device ID   : 0x410
        Revision ID : Rev X
        Device name : STM32F101/F102/F103 Medium-density
        Flash size  : 128 KBytes (default)
        Device type : MCU
        Device CPU  : Cortex-M3
        BL Version  : --


        C:\Users\a.starichenko>
    '
    """
    FILENAME: str = "pv.csv"

    def as_dict(self) -> Union[Type_PvDict, NoReturn]:
        ini = ConfigParser()

        try:
            ini.read_string(self._text)
        except Exception as exx:
            msg = f"[CRITICAL] incorrect format file!\n{exx!r}"
            print(msg)
            raise exx

        if not self.SECTION or self.SECTION == "DEFAULT" or ini.has_section(section=self.SECTION):
            result = dict(ini[self.SECTION or "DEFAULT"])
            return result
        else:
            msg = f"[CRITICAL] NO [{self.SECTION=} in {self.filepath=}]\n"
            msg += self._text
            print(msg)


# =====================================================================================================================
class PrivateAuthIni(PrivateAuth, PrivateIni):
    pass


class PrivateTgBotAddressIni(PrivateTgBotAddress, PrivateIni):
    pass


# =====================================================================================================================
