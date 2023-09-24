import pathlib
from typing import *
import abc

from annot_attrs import *


# =====================================================================================================================
Type_PvDict = Dict[str, Any]
Type_Path = Union[str, pathlib.Path]
Type_Value = Union[str, NoReturn, None]


# =====================================================================================================================
class Exx_PvNotAccepted(Exception):
    """
    Any final exception when value can't be get.
    """
    pass


# =====================================================================================================================
class PrivateAuth:
    USER: str
    PWD: str


class PrivateTgBotAddress:
    LINK_ID: str     # @mybot20230913
    NAME: str        # MyBotPublicName
    TOKEN: str


# =====================================================================================================================
class PrivateBase(AnnotAttrs, abc.ABC):
    SECTION: str = None

    DIRPATH: Type_Path = pathlib.Path.home()
    FILENAME: str = None

    def __init__(
            self,
            _section: Optional[str] = None,
            _dirpath: Type_Path = None,
            _filename: str = None,
            _filepath: Type_Path = None
    ):
        super().__init__()
        self.SECTION = _section or self.SECTION
        self.filepath_apply_new(
            _dirpath=_dirpath,
            _filename=_filename,
            _filepath=_filepath
        )
        self.load()

    def filepath_apply_new(
            self,
            _dirpath: Type_Path = None,
            _filename: str = None,
            _filepath: Type_Path = None
    ) -> Optional[NoReturn]:
        if not _filepath:
            self.DIRPATH = pathlib.Path(_dirpath or self.DIRPATH)
            self.FILENAME = _filename or self.FILENAME
        else:
            self.DIRPATH = pathlib.Path(_filepath).parent
            self.FILENAME = pathlib.Path(_filepath).name

        if self.filepath and not self.filepath.exists():
            msg = f'[CRITICAL]no[{self.filepath=}]'
            raise Exx_PvNotAccepted(msg)

    def __str__(self):
        result = f"{self.filepath=}"
        data = self.as_dict()
        if data:
            for key, value in data.items():
                result += f"\n{key}={value}"
        elif self.filepath and self.filepath.exists():
            result += f"\n{self.filepath.read_text()}"
        else:
            result += f"\ndata=None"
        return result

    @property
    def filepath(self) -> Optional[pathlib.Path]:
        try:
            if self.FILENAME:
                return pathlib.Path(self.DIRPATH, self.FILENAME)
        except:
            pass

    def apply_dict(self, attrs: Dict[str, Any]) -> None:
        for key, value in attrs.items():
            setattr(self, key, value)
        self.annots_check_values_exists()

    def load(self) -> Union[True, NoReturn]:
        section_dict = self.as_dict()
        if section_dict:
            self.apply_dict(section_dict)
            return True

        msg = f"[CRITICAL]no values!"
        if self.filepath and self.filepath.exists():
            msg += self.filepath.read_text()
        raise Exx_PvNotAccepted(msg)

    # -----------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def as_dict(self) -> Optional[Dict[str, Any]]:
        """
        return
            NONE - if no section! dont raise inside!
            {} - if no names!
        """
        pass


# =====================================================================================================================
