from .main import *

import json


# =====================================================================================================================
class PrivateJson(PrivateBaseWFile):
    """
    get object from json file by exact level
    """
    SECTION: str = "DEFAULT"
    DIRPATH: Type_Path = pathlib.Path.home()
    FILENAME: str = "pv.ini"

    def __init__(
            self,
            _raise_exx: Optional[bool] = None,
            _section: Optional[str] = None,

            _dirpath: Type_Path = None,
            _filename: str = None,

            _filepath: Type_Path = None
    ):
        self.RAISE_EXX = _raise_exx or self.RAISE_EXX
        self.SECTION = _section or self.SECTION

        if not _filepath:
            self.DIRPATH = pathlib.Path(_dirpath or self.DIRPATH)
            self.FILENAME = _filename or self.FILENAME
        else:
            self.DIRPATH = pathlib.Path(_filepath).parent
            self.FILENAME = pathlib.Path(_filepath).name

    @property
    def filepath(self) -> pathlib.Path:
        return pathlib.Path(self.DIRPATH, self.FILENAME)

    def get(
            self,
            name: str,
            _section: Optional[str] = None,
            _raise_exx: Optional[bool] = None,
            _dirpath: Type_Path = None,
            _filename: str = None,
            _filepath: Type_Path = None
    ) -> Type_Value:
        if _raise_exx is None:
            _raise_exx = self.RAISE_EXX

        if not _filepath:
            _filepath = pathlib.Path(_dirpath or self.DIRPATH, _filename or self.FILENAME)

        if not _filepath or not _filepath.exists():
            msg = f'[CRITICAL]no file [{_filepath=}]'
            if _raise_exx:
                raise Exx_PvNotAccepted(msg)
            else:
                print(msg)
                return

        _section = _section or self.SECTION
        filetext = _filepath.read_text()

        rc = ConfigParser()
        rc.read_string(filetext)

        if rc.has_option(section=_section, option=name):
            value = rc.get(section=_section, option=name)
            return value

        msg = f"[CRITICAL]no {name=}/{_section=} in {_filepath=}!"
        msg += f"\n"
        msg += filetext

        if _raise_exx:
            raise Exx_PvNotAccepted(msg)
        else:
            print(msg)
            return


# =====================================================================================================================
