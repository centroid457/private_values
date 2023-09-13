from .main import *

from configparser import ConfigParser


# =====================================================================================================================
class PrivateIni(PrivateBaseWFile):
    """
    read exact value from IniFile
    """
    SECTION: str = "DEFAULT"
    FILENAME: str = "pv.ini"

    def _get_value_unsafe(self, name: str, section: str, text: str) -> Optional[str]:
        ini = ConfigParser()
        ini.read_string(text)

        if ini.has_option(section=section, option=name):
            value = ini.get(section=section, option=name)
            return value

    def _get_section_unsafe(self, section: str, text: str) -> Optional[Dict[str, Any]]:
        ini = ConfigParser()
        ini.read_string(text)

        if section == "DEFAULT" or ini.has_section(section=section):
            result = dict(ini[section])
            return result


# =====================================================================================================================
