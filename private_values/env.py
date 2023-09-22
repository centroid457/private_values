from .main import *

import os


# =====================================================================================================================
class PrivateEnv(PrivateBase):
    """
    read exact environ from Os Environment
    """
    def __init__(
            self,
            _name: Optional[str] = None,
    ):
        super().__init__()


    @classmethod
    def get(cls, name: str) -> Type_Value:
        result = os.getenv(name)
        if result is None:
            cls.show()

            msg = f"[CRITICAL]no [{name=}] in environment!"
            msg += f"\n\tIf you just now add it - dont forget reboot!"
            raise Exx_PvNotAccepted(msg)
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
