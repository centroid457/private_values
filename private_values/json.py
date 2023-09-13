from .main import *

import json


# =====================================================================================================================
class PrivateJson(PrivateBaseWFile):
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
