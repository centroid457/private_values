import os
import pathlib
from configparser import ConfigParser
from typing import *


# =====================================================================================================================
Type_PvsDict = Dict[str, Optional[str]]
Type_Path = Union[str, pathlib.Path]


class Exx_PvNotAccepted(Exception):
    pass


class PrivateValues:
    """
    update special params from OsEnvirons, RC file or use default.
    if we have finally None value in updated params - RAISE!

    Use type STR for all PVs!

    STEPS
     1. detect all appropriate names
     2. create dict with default values
     3. update values from OsEnv and RcFile in order depends on PV__ENV_BETTER_THEN_RC
        if param exists and have new blank value "" it will update any last value, obviously.
     4. check None values existed - rise if have and PV__RISE_EXCEPTION_IF_NONE

    EXAMPLES

    define env NAMES
        PV___MAIL_USER: str = None  # will find PV___MAIL_USER/MAIL_USER
        PV___myEnv: str = None  # will find PV___myEnv/myEnv
        MAIL_USER: str = None  # this is not expected as env!

    set default VALUES
        PV___MAIL_USER: str = None      # no default value
        PV___MAIL_USER: str = "hello"   # def value set!
    """
    PV__RISE_EXCEPTION_IF_NONE: bool = True
    PV__PREFIX: str = "PV___"

    PV__ENV_BETTER_THEN_RC: bool = True

    PV__USE_ENV: bool = True
    PV__USE_RC: bool = True

    PV__RC_SECTION: str = "DEFAULT"
    PV__RC_DIRPATH: Type_Path = pathlib.Path.home()
    PV__RC_FILENAME: str = ".pv_rc"

    def __init__(self):
        super().__init__()

        if self.PV__RC_DIRPATH:
            self.PV__RC_DIRPATH = pathlib.Path(self.PV__RC_DIRPATH)
        self._PV__RC_FILEPATH = self.PV__RC_DIRPATH.joinpath(self.PV__RC_FILENAME)

        self._pv_detected: Type_PvsDict = {}    # it is just for debugging!
        self.pv__detect_names()

        if self.PV__ENV_BETTER_THEN_RC:
            self.pv__update_from_rc()
            self.pv__update_from_env()
        else:
            self.pv__update_from_env()
            self.pv__update_from_rc()

        self.pv__check_no_None()

    @classmethod
    def _cls_set_defaults(cls):
        """
        creating for tests!
        set all attrs in upper class at defaults from this class!
        """
        for name in dir(PrivateValues):
            if not callable(getattr(PrivateValues, name)) and not name.startswith("_"):
                value = getattr(PrivateValues, name)
                setattr(cls, name, value)

    def _pv__get_name_wo_prefix(self, name: str) -> str:
        if name.startswith(self.PV__PREFIX):
            name = name[len(self.PV__PREFIX):]
        return name

    def pv__detect_names(self) -> None:
        for name_w_prefix in dir(self):
            if name_w_prefix.startswith(self.PV__PREFIX) and not callable(getattr(self, name_w_prefix)):
                self._pv_detected.update({self._pv__get_name_wo_prefix(name_w_prefix): getattr(self, name_w_prefix)})

    def pv__update_from_env(self) -> None:
        if not self.PV__USE_ENV:
            return

        for name_wo_prefix in self._pv_detected:
            name_w_prefix = f"{self.PV__PREFIX}{name_wo_prefix}"
            if name_wo_prefix in os.environ:
                value = os.getenv(name_wo_prefix)
                setattr(self, name_w_prefix, value)
                self._pv_detected.update({name_wo_prefix: value})

    def pv__update_from_rc(self) -> None:
        if not self.PV__USE_RC:
            return

        if not self._PV__RC_FILEPATH or not self._PV__RC_FILEPATH.exists():
            print(f'[INFO]not exists {self._PV__RC_FILEPATH=}')
            return

        rc = ConfigParser()
        rc.read_string(self._PV__RC_FILEPATH.read_text())

        for name_wo_prefix in self._pv_detected:
            # in RC we will use only WO prefix!
            name_w_prefix = f"{self.PV__PREFIX}{name_wo_prefix}"

            if rc.has_option(section=self.PV__RC_SECTION, option=name_wo_prefix):
                value = rc.get(section=self.PV__RC_SECTION, option=name_wo_prefix)
                setattr(self, name_w_prefix, value)
                self._pv_detected.update({name_wo_prefix: value})

    def pv__check_no_None(self) -> Union[NoReturn, bool]:
        for name in self._pv_detected:
            if getattr(self, f"{self.PV__PREFIX}{name}") is None:
                msg = f"[CRITICAL] There is no [{name=}] in EnvsOs or RcFile and not exists default value! Add it manually!!!"
                print(msg)
                if self.PV__RISE_EXCEPTION_IF_NONE:
                    raise Exx_PvNotAccepted(msg)
                else:
                    return False
        return True

    # SHOW ------------------------------------------------------------------------------------------------------------
    @classmethod
    def _pv__show_env(cls, prefix: str = None) -> Type_PvsDict:
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
        result: Type_PvsDict = {}

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

    def pv__show_detected(self) -> Type_PvsDict:
        print()     # to pretty print in pytest only
        for name, value in self._pv_detected.items():
            print(f"{name}    ={value}")
        print()     # to pretty print in pytest only
        return self._pv_detected


# =====================================================================================================================
if __name__ == "__main__":
    PrivateValues._cls_set_defaults()
