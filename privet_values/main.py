import os
import pathlib
from configparser import ConfigParser
from typing import *


# =====================================================================================================================
Type_PvsDict = Dict[str, Optional[str]]
Type_Path = Union[str, pathlib.Path]


class Exx_PvNotAccepted(Exception):
    pass


class PrivetValues:
    """
    update special params from OsEnvirons, RC file or use default.
    if not exists finally some value of them - RAISE!

    add all ENVS with type STR!

    firstly it will try to get value from OsEnv
    then if not will be used already set as default!

    define env NAMES
        ENV__MAIL_USER: str = None  # will find ENV__MAIL_USER/MAIL_USER
        ENV__myEnv: str = None  # will find ENV__myEnv/myEnv
        MAIL_USER: str = None  # this is not expected as env!

    so if you already have Env in you Os add prefix ENV__ to use it in your class.

    set default VALUES
        ENV__MAIL_USER: str = None      # no default value
        ENV__MAIL_USER: str = "hello"   # def value set!

    When updated values - any value even blank string will be used!
    """
    PV__RISE_EXCEPTION_IF_NONE: bool = True
    PV__PREFIX: str = "PV__"

    PV__ENV_BETTER_THEN_RC: bool = True

    PV__RC_SECTION: str = "DEFAULT"
    PV__RC_DIRPATH: Type_Path = pathlib.Path.home()
    PV__RC_FILENAME: str = ".pv_rc"

    def __init__(self):
        super().__init__()

        self._pv_detected: Type_PvsDict = {}
        self.PV__RC_FILEPATH = self.PV__RC_DIRPATH.joinpath(self.PV__RC_FILENAME)

        self.pv__detect_names()

        if self.PV__ENV_BETTER_THEN_RC:
            self.pv__update_from_rc()
            self.pv__update_from_os_env()
        else:
            self.pv__update_from_os_env()
            self.pv__update_from_rc()

        self.pv__check_no_None()



    def pv__detect_names(self) -> None:
        for name in dir(self):
            if name.startswith(self.PV__PREFIX) and not callable(getattr(self, name)):
                self._pv_detected.update({name: getattr(self, name)})

    def pv__update_from_os_env(self) -> None:
        for name_w_prefix in self._pv_detected:
            name_wo_prefix = name_w_prefix.replace(self.PV__PREFIX, "", 1)

            env_name__os = None

            if name_w_prefix in os.environ:
                env_name__os = name_w_prefix
            elif name_wo_prefix in os.environ:
                env_name__os = name_wo_prefix

            if env_name__os:
                env_value__os = os.getenv(env_name__os)
                setattr(self, name_w_prefix, env_value__os)

                self._pv_detected.update({name_w_prefix: env_value__os})

    def pv__update_from_rc(self) -> None:
        if not self.PV__RC_FILEPATH.exists():
            print(f'[INFO]not exists {self.PV__RC_FILEPATH=}')
            return

        cfg = ConfigParser()
        cfg.read_file(self.PV__RC_FILEPATH.read_text())

        for name_w_prefix in self._pv_detected:
            # in RC we will use only WO prefix!
            name_wo_prefix = name_w_prefix.replace(self.PV__PREFIX, "", 1)

            try:
                value = cfg.get(section=self.PV__RC_SECTION, option=name_wo_prefix)
            except Exception:
                print(f'[INFO]not exists option [{name_wo_prefix}]')
                continue

            setattr(self, name_w_prefix, value)
            self._pv_detected.update({name_w_prefix: value})

    def pv__check_no_None(self) -> Union[NoReturn, bool]:
        for name in self._pv_detected:
            if getattr(self, name) is None:
                msg = f"[CRITICAL] There is no [{name=}] in EnvsOs and not exists default value! Add it manually!!!"
                print(msg)
                if self.PV__RISE_EXCEPTION_IF_NONE:
                    raise Exx_PvNotAccepted(msg)
                else:
                    return False
        return True

    @classmethod
    def pv__show_os_env(cls, prefix: str = None) -> Type_PvsDict:
        """
        mainly it is only for PRINTing! dont use result!

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
        envs_all = dict(os.environ)
        envs_result: Type_PvsDict = {}

        # filter ---------------
        if not prefix:
            envs_result = envs_all
        else:
            for name, value in envs_all.items():
                if name.startswith(prefix):
                    envs_result.update({name: value})

        # print ---------------
        print()     # to pretty print in pytest only
        for name, value in envs_result.items():
            print(f"{name}    ={value}")
        print()     # to pretty print in pytest only
        return envs_result

    def pv__show_detected(self) -> Type_PvsDict:
        print()     # to pretty print in pytest only
        for name, value in self._pv_detected.items():
            print(f"{name}    ={value}")
        print()     # to pretty print in pytest only
        return self._pv_detected


# =====================================================================================================================
if __name__ == "__main__":
    PrivetValues.pv__show_os_env(PrivetValues.PV__PREFIX)
