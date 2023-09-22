import pathlib
from typing import *
import abc


# =====================================================================================================================
Type_PvDict = Dict[str, Optional[str]]
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
class PrivateBase:
    RAISE_EXX: bool = True

    def create_attributes(self, attrs: Dict[str, Any]) -> None:
        for key, value in attrs.items():
            setattr(self, key, value)
        self.check_annotations()

    def check_annotations(self) -> Optional[NoReturn]:
        # print(self.__class__.__mro__)
        annots = set()
        for cls in self.__class__.__mro__[:-1]:
            annots.update(set(cls.__annotations__))
        # print(annots)

        for attr in annots:
            # apply losercase for INI
            if not hasattr(self, attr) and hasattr(self, attr.lower()):
                setattr(self, attr, getattr(self, attr.lower()))

            if not hasattr(self, attr):
                msg = f"[CRITICAL]no[{attr=}]"
                if attr.lower() != attr:
                    msg += f"\nif used Ini - use only LOWERCASE attrs!!!"
                msg += f"\n{self.__class__.__name__}"
                msg += f"\nall your annotations={annots}"
                raise Exx_PvNotAccepted(msg)


# =====================================================================================================================
class _PrivateBaseWFile_Interface(abc.ABC):
    @abc.abstractmethod
    def _get_value_unsafe(self, name: str, section: str, text: str) -> Optional[str]:
        # NOTICE!!!! "section: Optional[str] = None" - dont code like this!!!
        # the method work always UNSAFE! any param can't be NONE!
        pass

    @abc.abstractmethod
    def _get_section_unsafe(self, section: str, text: str) -> Optional[Dict[str, Any]]:
        """
        return
            NONE - if no section! dont raise inside!
            {} - if no names!
        """
        pass


class PrivateBaseWFile(PrivateBase, _PrivateBaseWFile_Interface):
    SECTION: str = None

    DIRPATH: Type_Path = pathlib.Path.home()
    FILENAME: str = None

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

        self.get_section()

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

    # -----------------------------------------------------------------------------------------------------------------
    def get_section(
            self,
            _section: Optional[str] = None,
            _dirpath: Type_Path = None,
            _filename: str = None,
            _filepath: Type_Path = None,
            _raise_exx: Optional[bool] = None
    ) -> Union['PrivateBaseWFile', NoReturn, None]:
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
        if section_dict:
            self.create_attributes(section_dict)
            return self

        msg = f"[CRITICAL]no {_section=} in {_filepath=}!"
        msg += f"\n"
        msg += filetext

        if _raise_exx:
            raise Exx_PvNotAccepted(msg)
        else:
            print(msg)
            return


# =====================================================================================================================
