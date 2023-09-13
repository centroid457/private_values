import pathlib
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
class PrivateBase:
    RAISE_EXX: bool = True


class PrivateBaseWFile(PrivateBase):
    SECTION: str = None

    DIRPATH: Type_Path = pathlib.Path.home()
    FILENAME: str = "pv.ini"

    def __init__(
            self,
            _section: Optional[str] = None,

            _dirpath: Type_Path = None,
            _filename: str = None,

            _filepath: Type_Path = None,
            _raise_exx: Optional[bool] = None
    ):
        super().__init__()

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

    # -----------------------------------------------------------------------------------------------------------------
    def get(
            self,
            name: str,
            _section: Optional[str] = None,
            _dirpath: Type_Path = None,
            _filename: str = None,
            _filepath: Type_Path = None,
            _raise_exx: Optional[bool] = None
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

        if _section is None:
            _section = self.SECTION

        filetext = _filepath.read_text()

        value = self._get_value_unsafe(name=name, section=_section, text=filetext)
        if value is not None:
            return value

        msg = f"[CRITICAL]no {name=}/{_section=} in {_filepath=}!"
        msg += f"\n"
        msg += filetext

        if _raise_exx:
            raise Exx_PvNotAccepted(msg)
        else:
            print(msg)
            return

    def _get_value_unsafe(self, name: str, section: str, text: str) -> Optional[str]:
        # NOTICE!!!! "section: Optional[str] = None" - dont code like this!!!
        # the method work always UNSAFE! any param can't be NONE!
        raise NotImplementedError

    # -----------------------------------------------------------------------------------------------------------------
    def get_section(
            self,
            _section: Optional[str] = None,
            _dirpath: Type_Path = None,
            _filename: str = None,
            _filepath: Type_Path = None,
            _raise_exx: Optional[bool] = None
    ) -> Optional['PrivateBaseWFile']:
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

        if _section is None:
            _section = self.SECTION

        filetext = _filepath.read_text()

        section_dict = self._get_section_unsafe(section=_section, text=filetext)
        if section_dict is not None:
            for key, value in section_dict.items():
                setattr(self, key, value)
            return self

        msg = f"[CRITICAL]no {_section=} in {_filepath=}!"
        msg += f"\n"
        msg += filetext

        if _raise_exx:
            raise Exx_PvNotAccepted(msg)
        else:
            print(msg)
            return

    def _get_section_unsafe(self, section: str, text: str) -> Optional[Dict[str, Any]]:
        """
        return
            None if NO section
            {} - if no names!
        """
        raise NotImplementedError


# =====================================================================================================================
