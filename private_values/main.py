import os
import pathlib
from configparser import ConfigParser
from typing import *


# =====================================================================================================================
Type_PvDict = Dict[str, Optional[str]]
Type_Path = Union[str, pathlib.Path]
Type_Value = Union[str, NoReturn, None]


class Exx_PvNotAccepted(Exception):
    """
    Any final exception when value can't be get.
    """
    pass


# =====================================================================================================================
class PrivateEnv:
    """
    read exact environ from Os Environment
    """
    RAISE_EXX: bool = True

    def get(cls, name: str, _raise_exx: Optional[bool] = None) -> Type_Value:
        if _raise_exx is None:
            _raise_exx = cls.RAISE_EXX

        result = os.getenv(name)
        if result is None:
            cls.show()

            msg = f"[CRITICAL]no [{name=}] in environment!"
            msg += f"\n\tIf you just now add it - dont forget reboot!"
            if _raise_exx:
                raise Exx_PvNotAccepted(msg)
            else:
                print(msg)
        return result

    @staticmethod
    def show(prefix: Optional[str] = None) -> Type_PvDict:
        """
        mainly it is only for PRINTing and debugging! don't use result!

        NOTE: be careful to use result as dict! especially if you have lowercase letters!

        REASON:
            import os

            name_lowercase = "name_lowercase"
            os.environ[name_lowercase] = name_lowercase

            print(os.getenv(name_lowercase))    # name_lowercase
            print(os.getenv(name_lowercase.upper()))    # name_lowercase

            print(os.environ[name_lowercase])   # name_lowercase
            print(os.environ[name_lowercase.upper()])   # name_lowercase

            print(dict(os.environ)[name_lowercase])     # KeyError: 'name_lowercase'
        """
        envs_all = os.environ
        result: Type_PvDict = {}

        # filter ---------------
        for name, value in envs_all.items():
            if not prefix or (prefix and name.upper().startswith(prefix.upper())):
                result.update({name: value})

        # print ---------------
        print()     # to pretty print in pytest only
        for name, value in result.items():
            print(f"{name}    ={value}")
        print()     # to pretty print in pytest only
        return result


# =====================================================================================================================
class PrivateIni:
    """
    read exact value from IniFile
    """
    RAISE_EXX: bool = True

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
