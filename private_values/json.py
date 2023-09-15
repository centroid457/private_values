from .main import *

import json


# =====================================================================================================================
class PrivateJson(PrivateBaseWFile):
    FILENAME: str = "pv.json"

    def _get_value_unsafe(self, name: str, section: str, text: str) -> Optional[str]:
        """
        section only in first level!
        """
        json_data = self._get_section_unsafe(section, text)

        if json_data:
            value = json_data.get(name)
            return value

    def _get_section_unsafe(self, section: str, text: str) -> Optional[Dict[str, Any]]:
        """
        section only in first level!
        """
        try:
            json_data = json.loads(text)
        except Exception as exx:
            msg = f"[CRITICAL] incorrect format file!\n{exx!r}"
            print(msg)
            raise Exx_PvNotAccepted(msg)

        if section:
            json_data = json_data.get(section)

        return json_data


# =====================================================================================================================
class PrivateJsonAuth(PrivateJson):
    USER: str
    PWD: str


class PrivateJsonTgBotAddress(PrivateJson):
    LINK_ID: str     # @mybot20230913
    NAME: str        # MyBotPublicName
    TOKEN: str


# =====================================================================================================================
