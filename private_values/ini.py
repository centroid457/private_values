from .env import *

from configparser import ConfigParser


# =====================================================================================================================
class PrivateIni(PrivateBaseWFile):
    """
    read exact value from IniFile
    """
    SECTION: str = "DEFAULT"

    def _get_value_unsafe(self, name: str, section: str, text: str) -> Optional[str]:
        rc = ConfigParser()
        rc.read_string(text)

        if rc.has_option(section=section, option=name):
            value = rc.get(section=section, option=name)
            return value

    def _get_section_unsafe(self, section: str, text: str) -> Optional[Dict[str, Any]]:
        rc = ConfigParser()
        rc.read_string(text)

        if rc.has_section(section=section):
            result = dict(rc[section])
            return result


# =====================================================================================================================
