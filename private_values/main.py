import pathlib
from typing import *
import abc


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
class PrivateBase(abc.ABC):
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
        for key, value in self.as_dict():
            result += f"\n{key}={value}"
        return "hello"

    def __getattr__(self, item: str) -> Union[str, NoReturn]:
        if item in ["__isabstractmethod__", ]:
            return
        else:
            return self.get_case_insensitive(item)

    def __getitem__(self, key: str) -> Union[str, NoReturn]:
        return self.get_case_insensitive(key)

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
        self.check_by_annotations()

    def check_by_annotations(self, _sample: Optional[dict] = None) -> Union[bool, NoReturn]:
        """
        check all annotations get values!
        check withing self (Raise if not any value) or _sample dict (if used, return bool!)
        """
        # print(self.__class__.__mro__)
        annots = set()
        for cls in self.__class__.__mro__[:-1]:
            for name in set(cls.__annotations__):
                if not hasattr(cls, name):
                    annots.update({name, })
        # print(annots)

        for attr in annots:
            try:
                self.get_case_insensitive(attr, _sample)
            except Exception as exx:
                if _sample:
                    return False
                else:
                    raise exx
        return True

    def get_case_insensitive(self, name: str, _sample: Optional[dict] = None) -> Union[str, NoReturn]:
        """
        get value for attr name without case sense.
        from self or _sample dict

        if no attr name in source - raise!
        """
        if _sample:
            attrs_all = list(_sample)
        else:
            attrs_all = list(filter(lambda attr: not callable(getattr(self, attr)) and not attr.startswith("__"), dir(self)))

        attrs_similar = list(filter(lambda attr: attr.lower() == name.lower(), attrs_all))
        if len(attrs_similar) == 1:
            if _sample:
                return _sample[attrs_similar[0]]
            else:
                return getattr(self, attrs_similar[0])
        elif len(attrs_similar) == 0:
            msg = f"[CRITICAL]no[{name=}] in any cases [{attrs_all=}]"
            raise Exx_PvNotAccepted(msg)
        else:
            msg = f"[CRITICAL]exists several similar [{attrs_similar=}]"
            raise Exx_PvNotAccepted(msg)

    def print(self) -> None:
        print(self)

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
