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


# =====================================================================================================================
class PrivateEnv:
    """
    read exact environ from Os Environment
    """
    RAISE_EXX: bool = True

    @classmethod
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

    @classmethod
    @property
    def FILEPATH(cls) -> pathlib.Path:
        return pathlib.Path(cls.DIRPATH, cls.FILENAME)

    @classmethod
    def get(cls, name: str, section: Optional[str] = None, _raise_exx: Optional[bool] = None) -> Type_Value:
        if _raise_exx is None:
            _raise_exx = cls.RAISE_EXX

        if not cls.FILEPATH or not cls.FILEPATH.exists():
            msg = f'[CRITICAL]no file [{cls.FILEPATH=}]'
            if _raise_exx:
                raise Exx_PvNotAccepted(msg)
            else:
                print(msg)
                return

        section = section or cls.SECTION
        filetext = cls.FILEPATH.read_text()

        rc = ConfigParser()
        rc.read_string(filetext)

        if rc.has_option(section=section, option=name):
            value = rc.get(section=section, option=name)
            return value

        msg = f"[CRITICAL]no {name=}/{section=} in {cls.FILEPATH=}!"
        msg += f"\n"
        msg += filetext

        if _raise_exx:
            raise Exx_PvNotAccepted(msg)
        else:
            print(msg)
            return


# =====================================================================================================================
