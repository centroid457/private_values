import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser
from private_values import *


# =====================================================================================================================
class Test__Env:
    VICTIM: Type[PrivateEnv] = type("VICTIM", (PrivateEnv,), {})

    VALUE: str = "VALUE"
    NAME_Exists: str = "Exists"
    NAME_NotExists: str = "NotExists"

    @classmethod
    def setup_class(cls):
        while cls.NAME_Exists in os.environ:
            cls.NAME_Exists = f"{cls.NAME_Exists}_"

        while cls.NAME_NotExists in os.environ:
            cls.NAME_NotExists = f"{cls.NAME_NotExists}_"

        os.environ[cls.NAME_Exists] = cls.VALUE

        print()
        print()
        print(f"{cls.NAME_Exists=}")
        print(f"{cls.NAME_NotExists=}")
        print()
        print()

    @classmethod
    def teardown_class(cls):
        del os.environ[cls.NAME_Exists]

    def setup_method(self, method):
        self.VICTIM = type("VICTIM", (PrivateEnv,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__ClassMethod_and_obj(self):
        assert self.VICTIM.get(self.NAME_Exists) == self.VALUE
        assert self.VICTIM().get(self.NAME_Exists) == self.VALUE

    def test__Exists(self):
        assert self.VICTIM().get(self.NAME_Exists) == self.VALUE

    def test__notExists(self):
        assert self.VICTIM().get(self.NAME_NotExists, _raise_exx=False) is None

        self.VICTIM.RAISE_EXX = False
        assert self.VICTIM().get(self.NAME_NotExists) is None

        self.VICTIM.RAISE_EXX = True
        try:
            self.VICTIM().get(self.NAME_NotExists)
        except Exx_PvNotAccepted:
            return

        assert False

    def test__show(self):
        # uppercase - see docstring for method!
        envs = self.VICTIM.show(self.NAME_Exists)
        print(envs)
        assert envs.get(self.NAME_Exists.upper()) == self.VALUE


# =====================================================================================================================
class Test__Ini:
    VICTIM: Type[PrivateIni] = type("VICTIM", (PrivateIni,), {})
    VICTIM2_FILENAME: str = f"{PrivateIni.FILENAME}2"
    VICTIM2: Type[PrivateIni] = type("VICTIM2", (PrivateIni,), {"FILENAME": VICTIM2_FILENAME})
    DIRPATH: pathlib.Path = pathlib.Path(TemporaryDirectory().name)

    TEXT1: str = f"""
[DEFAULT]
name=valueDef
name0=valueDef

[SEC1]
name=value1
name1=value1
    """
    TEXT2: str = f"""
[DEFAULT]
name=valueDef2
name0=valueDef2

[SEC1]
name=value12
name1=value12
        """
    @classmethod
    def setup_class(cls):
        cls.DIRPATH.mkdir()
        cls.DIRPATH.joinpath(cls.VICTIM.FILENAME).write_text(cls.TEXT1)
        cls.DIRPATH.joinpath(cls.VICTIM2.FILENAME).write_text(cls.TEXT2)

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.DIRPATH)

    def setup_method(self, method):
        self.VICTIM = type("VICTIM", (PrivateIni,), {})
        self.VICTIM2 = type("VICTIM2", (PrivateIni,), {"FILENAME": self.VICTIM2_FILENAME})
        self.VICTIM.DIRPATH = self.DIRPATH
        self.VICTIM2.DIRPATH = self.DIRPATH

    # -----------------------------------------------------------------------------------------------------------------
    def test__notExist_file(self):
        self.VICTIM.FILENAME = "12345.ini"

        try:
            self.VICTIM().get("name")
        except Exx_PvNotAccepted:
            return

        assert False

    def test__notExist_name(self):
        assert self.VICTIM().get("name999", _raise_exx=False) is None

        self.VICTIM.RAISE_EXX = False
        assert self.VICTIM().get("name999") is None

        self.VICTIM.RAISE_EXX = True
        try:
            self.VICTIM().get("name999")
        except Exx_PvNotAccepted:
            return

        assert False

    def test__Exist_name(self):
        # VICTIM1
        assert self.VICTIM().get("name", _raise_exx=False) == "valueDef"
        assert self.VICTIM().get("name0", _raise_exx=False) == "valueDef"
        assert self.VICTIM().get("name1", _raise_exx=False) is None

        assert self.VICTIM().get("name", _section="SEC1", _raise_exx=False) == "value1"
        assert self.VICTIM().get("name0", _section="SEC1", _raise_exx=False) == "valueDef"
        assert self.VICTIM().get("name1", _section="SEC1", _raise_exx=False) == "value1"

        # VICTIM2
        assert self.VICTIM2().get("name", _raise_exx=False) == "valueDef2"
        assert self.VICTIM2().get("name0", _raise_exx=False) == "valueDef2"
        assert self.VICTIM2().get("name1", _raise_exx=False) is None

        assert self.VICTIM2().get("name", _section="SEC1", _raise_exx=False) == "value12"
        assert self.VICTIM2().get("name0", _section="SEC1", _raise_exx=False) == "valueDef2"
        assert self.VICTIM2().get("name1", _section="SEC1", _raise_exx=False) == "value12"

    def test__use_get_with_other_params(self):
        # VICTIM1
        assert self.VICTIM().get("name") == "valueDef"
        assert self.VICTIM().get("name", _filepath=pathlib.Path(self.VICTIM2.DIRPATH, self.VICTIM2_FILENAME)) == "valueDef2"
        assert self.VICTIM().get("name", _filename=self.VICTIM2_FILENAME) == "valueDef2"
        assert self.VICTIM().get("name", _filename=self.VICTIM2_FILENAME, _section="SEC1") == "value12"
        assert self.VICTIM().get("name1", _filename=self.VICTIM2_FILENAME, _section="SEC1") == "value12"

    def test__use_init(self):
        assert self.VICTIM().get("name") == "valueDef"
        assert self.VICTIM(_filepath=pathlib.Path(self.VICTIM2.DIRPATH, self.VICTIM2_FILENAME)).get("name") == "valueDef2"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME).get("name") == "valueDef2"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1").get("name") == "value12"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1").get("name1") == "value12"

        VICTIM_obj = self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1")
        assert VICTIM_obj.get("name1") == "value12"

    def test__get_section(self):
        VICTIM_obj = self.VICTIM().get_section()
        assert VICTIM_obj.name == "valueDef"
        assert VICTIM_obj.name0 == "valueDef"


# =====================================================================================================================
class Test__Json:
    VICTIM: Type[PrivateJson] = type("VICTIM", (PrivateJson,), {})
    VICTIM2_FILENAME: str = f"{PrivateJson.FILENAME}2"
    VICTIM2: Type[PrivateJson] = type("VICTIM2", (PrivateJson,), {"FILENAME": VICTIM2_FILENAME})
    DIRPATH: pathlib.Path = pathlib.Path(TemporaryDirectory().name)

    TEXT1: str = """
{
"SEC1": {
    "name1": "value1",
    "name2": "value11"
    },
"SEC2": {
    "name1": "value2",
    "name2": "value22"
    }
}
    """
    TEXT2: str = """
{
"SEC1": {
    "name1": "value1*",
    "name2": "value11*"
    },
"SEC2": {
    "name1": "value2*",
    "name2": "value22*"
    }
}
    """
    @classmethod
    def setup_class(cls):
        cls.DIRPATH.mkdir()
        cls.DIRPATH.joinpath(cls.VICTIM.FILENAME).write_text(cls.TEXT1)
        cls.DIRPATH.joinpath(cls.VICTIM2.FILENAME).write_text(cls.TEXT2)

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.DIRPATH)

    def setup_method(self, method):
        self.VICTIM = type("VICTIM", (PrivateJson,), {})
        self.VICTIM2 = type("VICTIM2", (PrivateJson,), {"FILENAME": self.VICTIM2_FILENAME})

        self.VICTIM.DIRPATH = self.DIRPATH
        self.VICTIM2.DIRPATH = self.DIRPATH

        self.VICTIM.SECTION = "SEC1"
        self.VICTIM2.SECTION = "SEC1"

    # -----------------------------------------------------------------------------------------------------------------
    def test__notExist_file(self):
        self.VICTIM.FILENAME = "12345.ini"

        try:
            self.VICTIM().get("name")
        except Exx_PvNotAccepted:
            return

        assert False

    def test__notExist_name(self):
        assert self.VICTIM().get("name999", _raise_exx=False) is None

        self.VICTIM.RAISE_EXX = False
        assert self.VICTIM().get("name999") is None

        self.VICTIM.RAISE_EXX = True
        try:
            self.VICTIM().get("name999")
        except Exx_PvNotAccepted:
            return

        assert False

    def test__Exist_name(self):
        # VICTIM1
        assert self.VICTIM().get("name1", _raise_exx=False) == "value1"
        assert self.VICTIM().get("name2", _raise_exx=False) == "value11"
        assert self.VICTIM().get("name3", _raise_exx=False) is None

        assert self.VICTIM().get("name1", _section="SEC2", _raise_exx=False) == "value2"
        assert self.VICTIM().get("name2", _section="SEC2", _raise_exx=False) == "value22"
        assert self.VICTIM().get("name3", _section="SEC2", _raise_exx=False) is None

        assert self.VICTIM().get("name1", _section="SEC3", _raise_exx=False) is None

        # VICTIM2
        assert self.VICTIM2().get("name1", _raise_exx=False) == "value1*"
        assert self.VICTIM2().get("name2", _raise_exx=False) == "value11*"
        assert self.VICTIM2().get("name3", _raise_exx=False) is None

    def test__use_get_with_other_params(self):
        # VICTIM1
        assert self.VICTIM().get("name1") == "value1"
        assert self.VICTIM().get("name1", _filepath=pathlib.Path(self.VICTIM2.DIRPATH, self.VICTIM2_FILENAME)) == "value1*"
        assert self.VICTIM().get("name1", _filename=self.VICTIM2_FILENAME) == "value1*"
        assert self.VICTIM().get("name1", _filename=self.VICTIM2_FILENAME, _section="SEC2") == "value2*"
        assert self.VICTIM().get("name2", _filename=self.VICTIM2_FILENAME, _section="SEC1") == "value11*"

    def test__use_init(self):
        assert self.VICTIM().get("name1") == "value1"
        assert self.VICTIM(_filepath=pathlib.Path(self.VICTIM2.DIRPATH, self.VICTIM2_FILENAME)).get("name1") == "value1*"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME).get("name1") == "value1*"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1").get("name1") == "value1*"
        assert self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1").get("name2") == "value11*"

        VICTIM_obj = self.VICTIM(_filename=self.VICTIM2_FILENAME, _section="SEC1")
        assert VICTIM_obj.get("name1") == "value1*"

    def test__get_section(self):
        VICTIM_obj = self.VICTIM().get_section()
        assert VICTIM_obj.name1 == "value1"
        assert VICTIM_obj.name2 == "value11"

        VICTIM_obj = self.VICTIM().get_section("")
        assert VICTIM_obj.SEC1 == {
            "name1": "value1",
            "name2": "value11"
        }
        assert VICTIM_obj.SEC2 == {
            "name1": "value2",
            "name2": "value22"
        }
        

# =====================================================================================================================
