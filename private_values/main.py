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

    def __getattr__(self, item: str) -> Union[str, NoReturn]:
        return self.attr_get_case_insensitive(item)

    def attrs_create(self, attrs: Dict[str, Any]) -> None:
        for key, value in attrs.items():
            setattr(self, key, value)
        self.attrs_check_values()

    def attrs_check_values(self) -> Optional[NoReturn]:
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

    def attr_get_case_insensitive(self, name) -> Union[str, NoReturn]:
        attrs_all = list(filter(lambda attr: not callable(getattr(self, attr)), dir(self)))
        attrs_similar = list(filter(lambda attr: attr.lower() == name.lower(), attrs_all))
        if len(attrs_similar) == 1:
            return getattr(self, attrs_similar[0])
        elif len(attrs_similar) == 0:
            msg = f"[CRITICAL]no[{name=}] in any cases [{attrs_all=}]"
            raise Exx_PvNotAccepted(msg)
        else:
            msg = f"[CRITICAL]exists several similar [{attrs_similar=}]"
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
            _filepath: Type_Path = None
    ):
        super().__init__()

        self.SECTION = _section or self.SECTION

        if not _filepath:
            self.DIRPATH = pathlib.Path(_dirpath or self.DIRPATH)
            self.FILENAME = _filename or self.FILENAME
        else:
            self.DIRPATH = pathlib.Path(_filepath).parent
            self.FILENAME = pathlib.Path(_filepath).name

        self.load_values()

    @property
    def filepath(self) -> pathlib.Path:
        return pathlib.Path(self.DIRPATH, self.FILENAME)

    # -----------------------------------------------------------------------------------------------------------------
    def load_values(self) -> Union[True, NoReturn]:
        if not self.filepath.exists():
            msg = f'[CRITICAL]no[{self.filepath=}]'
            raise Exx_PvNotAccepted(msg)

        filetext = self.filepath.read_text()

        section_dict = self._get_section_unsafe(section=self.SECTION, text=filetext)
        if section_dict:
            self.attrs_create(section_dict)
            return True

        msg = f"[CRITICAL]no {self.SECTION=} in {self.filepath=}!"
        msg += f"\n"
        msg += filetext

        raise Exx_PvNotAccepted(msg)


# =====================================================================================================================
