import os
from typing import *


# =====================================================================================================================
class EnvsNotAccepted(Exception):
    pass


class EnvsOsGetterClass:
    """
    get environs from OS or use default!
    if not exists some value of them - RAISE!

    # add all ENVS with type STR!

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
    """
    ENVS_RISE_EXCEPTION: bool = True
    ENVS_PREFIX: str = "ENV__"

    def __init__(self):
        super().__init__()

        self._envs_detected: Dict[str, Optional[str]] = {}

        self.envs__detect_names()
        self.envs__update_values_from_os()
        self.envs__check_no_blanks()

    def envs__detect_names(self):
        for name in dir(self):
            if name.startswith(self.ENVS_PREFIX):
                self._envs_detected.update({name: getattr(self, name)})

    def envs__update_values_from_os(self):
        for name_w_prefix in self._envs_detected:
            name_wo_prefix = name_w_prefix.replace(self.ENVS_PREFIX, "", 1)

            env_name__os = None

            if name_w_prefix in os.environ:
                env_name__os = name_w_prefix
            elif name_wo_prefix in os.environ:
                env_name__os = name_wo_prefix

            if env_name__os:
                env_value__os = os.getenv(env_name__os)
                setattr(self, name_w_prefix, env_value__os)

                self._envs_detected.update({name_w_prefix: env_value__os})

    def envs__check_no_blanks(self) -> Union[NoReturn, bool]:
        for name in self._envs_detected:
            if getattr(self, name) is None:
                msg = f"[CRITICAL] There is no [{name=}] in EnvsOs and not exists default value! Add it manually!!!"
                print(msg)
                if self.ENVS_RISE_EXCEPTION:
                    raise EnvsNotAccepted(msg)
                else:
                    return False
        return True

# =====================================================================================================================
