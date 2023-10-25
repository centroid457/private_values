import pathlib
from typing import *
import abc

from annot_attrs import *


# =====================================================================================================================
Type_PvDict = Dict[str, Any]
Type_Path = Union[str, pathlib.Path]
Type_Value = Union[str, NoReturn, None]


# =====================================================================================================================
class Exx_FileNotExists(Exception):
    """
    Any final exception when value can't be get.
    """
    pass


# =====================================================================================================================
class PrivateAuth:
    """Typical structure for AUTH

    :ivar USER: user login name
    :ivar PWD: password
    """
    USER: str
    PWD: str


class PrivateTgBotAddress:
    """Typical structure for Telegram bot address

    :ivar LINK_ID: just a bot id, not important
    :ivar NAME: just a bot public name, not important
    :ivar TOKEN: bot token for connection, important!
    """
    LINK_ID: str     # @mybot20230913
    NAME: str        # MyBotPublicName
    TOKEN: str


# =====================================================================================================================
class PrivateBase(AnnotAttrs, abc.ABC):
    """Base class to get values from sources.

    :ivar SECTION: first level name in source, for ini - root section, for json - rootKey, for env - not used
    :ivar DIRPATH: file destination
    :ivar FILENAME: file name

    USAGE
    -----
    if you dont need RAISE when no value get for exact annotated name - just define None!
    """
    SECTION: str = None

    DIRPATH: Optional[Type_Path] = pathlib.Path.home()
    FILENAME: Optional[str] = None

    _text: Optional[str] = None     # TODO: need tests!!!

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(
            self,
            _section: Optional[str] = None,
            _dirpath: Type_Path = None,
            _filename: str = None,
            _filepath: Type_Path = None,
            _text: Optional[str] = None
    ):
        super().__init__()
        self.SECTION = _section or self.SECTION

        if _text:
            self.DIRPATH = None
            self.FILENAME = None
            self._text = _text
        else:
            self._filepath_apply_new(
                _dirpath=_dirpath,
                _filename=_filename,
                _filepath=_filepath
            )

        self.load_dict()
        self.annots_check_values_exists()

    def __str__(self):
        """return pretty string
        """
        result = f"{self.filepath=}"
        data = self.as_dict()
        if data:
            for key, value in data.items():
                result += f"\n{key}={value}"
        elif self.filepath and self.filepath.exists():
            result += f"\n{self._text}"
        else:
            result += f"\ndata=None"
        return result

    # -----------------------------------------------------------------------------------------------------------------
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
            raise Exx_FileNotExists(msg)

        if self.filepath:
            self._text = self.filepath.read_text()

    @property
    def filepath(self) -> Optional[pathlib.Path]:
        """compose final pathlib instance for file
        """
        try:
            if self.FILENAME:
                return pathlib.Path(self.DIRPATH, self.FILENAME)
        except:
            pass

    # -----------------------------------------------------------------------------------------------------------------
    def load_dict(self) -> None:
        """load values from source into instance attributes.
        """
        section_dict = self.as_dict()
        if section_dict:
            self._apply_dict(section_dict)

    def _apply_dict(self, attrs: Dict[str, Any]) -> None | NoReturn:
        """Apply passes dict into instance and check consistence.
        """
        for key, value in attrs.items():
            setattr(self, key, value)

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
