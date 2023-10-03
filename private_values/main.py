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
    """Typical structure for AUTH

    :USER: user login name
    :PWD: password
    """
    USER: str
    PWD: str


class PrivateTgBotAddress:
    """Typical structure for Telegram bot address

    :LINK_ID: just a bot id, not important
    :NAME: just a bot public name, not important
    :TOKEN: bot token for connection, important!
    """
    LINK_ID: str     # @mybot20230913
    NAME: str        # MyBotPublicName
    TOKEN: str


# =====================================================================================================================
class PrivateBase(AnnotAttrs, abc.ABC):
    """Base class to get values from sources.

    :SECTION: first level name in source, for ini - root section, for json - rootKey, for env - not used
    :DIRPATH: file destination
    :FILENAME: file name
    :RAISE: True - raise Exx_PvNotAccepted in any incomplete values
        usefull if you have a messaging system connected to you project jast for fan
        and you dont want to raise if you dont configured it.
    """
    SECTION: str = None

    DIRPATH: Type_Path = pathlib.Path.home()
    FILENAME: str = None

    RAISE: bool = True

    def __init__(
            self,
            _section: Optional[str] = None,
            _dirpath: Type_Path = None,
            _filename: str = None,
            _filepath: Type_Path = None
    ):
        super().__init__()
        self.SECTION = _section or self.SECTION
        self._filepath_apply_new(
            _dirpath=_dirpath,
            _filename=_filename,
            _filepath=_filepath
        )
        self.load()

    def _filepath_apply_new(
            self,
            _dirpath: Type_Path = None,
            _filename: str = None,
            _filepath: Type_Path = None
    ) -> Optional[NoReturn]:
        """apply new file destination
        """
        if not _filepath:
            self.DIRPATH = pathlib.Path(_dirpath or self.DIRPATH)
            self.FILENAME = _filename or self.FILENAME
        else:
            self.DIRPATH = pathlib.Path(_filepath).parent
            self.FILENAME = pathlib.Path(_filepath).name

        if self.filepath and not self.filepath.exists():
            msg = f'[CRITICAL]no[{self.filepath=}]'
            if self.RAISE:
                raise Exx_PvNotAccepted(msg)

    def __str__(self):
        """return pretty string
        """
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

    def _apply_dict(self, attrs: Dict[str, Any]) -> None | NoReturn:
        """Apply passes dict into instance.
        """
        for key, value in attrs.items():
            setattr(self, key, value)
        if self.RAISE:
            self.annots_check_values_exists()

    def load(self) -> Union[True, NoReturn, None]:
        """load values from source into instance.
        """
        section_dict = self.as_dict()
        if section_dict:
            self._apply_dict(section_dict)
            return True

        msg = f"[CRITICAL]no values!"
        if self.filepath and self.filepath.exists():
            msg += self.filepath.read_text()
        if self.RAISE:
            raise Exx_PvNotAccepted(msg)

    # -----------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def as_dict(self) -> Optional[Dict[str, Any]]:
        """Obtain existed values from source in dict structure.

        return
            NONE - if no section! dont raise inside!
            {} - if no names!
        """
        pass


# =====================================================================================================================
