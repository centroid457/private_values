from .main import *

import json


# =====================================================================================================================
class PrivateJson(PrivateBaseWFile):
    def _get_value_unsafe(self, name: str, section: str, text: str) -> Optional[str]:
        json_data = self._get_section_unsafe(section, text)

        if json_data:
            value = json_data.get(name)
            return value

    def _get_section_unsafe(self, section: str, text: str) -> Optional[Dict[str, Any]]:
        json_data = json.loads(text)

        if section:
            json_data = json_data.get(section)

        return json_data


# =====================================================================================================================
