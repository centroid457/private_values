import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser
from private_values import *


# =====================================================================================================================
class Test__EnvValues:
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

    def test__Exists(self):
        assert EnvValues.get(self.NAME_Exists) == self.VALUE

    def test__notExists_Rise(self):
        try:
            EnvValues.get(self.NAME_NotExists)
        except Exx_PvNotAccepted:
            return

        assert False

    def test__notExists_noRise(self):
        assert EnvValues.get(self.NAME_NotExists, _raise_exx=False) is None

    def test__show(self):
        # uppercase - see docstring for method!
        envs = EnvValues.show(self.NAME_Exists)
        print(envs)
        assert envs.get(self.NAME_Exists.upper()) == self.VALUE


# =====================================================================================================================
class Test__IniValues:
    VICTIM: Type[IniValues] = type("VICTIM", (IniValues, ), {})
    VICTIM2: Type[IniValues] = type("VICTIM2", (IniValues, ), {"FILENAME": f"{IniValues.FILENAME}2"})
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
        self.VICTIM = type("VICTIM", (IniValues, ), {})
        self.VICTIM2 = type("VICTIM2", (IniValues, ), {"FILENAME": f"{IniValues.FILENAME}2"})
        self.VICTIM.DIRPATH = self.DIRPATH
        self.VICTIM2.DIRPATH = self.DIRPATH

    def test__notExist_file(self):
        self.VICTIM.FILENAME = "12345.ini"

        try:
            self.VICTIM.get("name")
        except Exx_PvNotAccepted:
            return

        assert False

    def test__notExist_name(self):
        try:
            self.VICTIM.get("name999")
        except Exx_PvNotAccepted:
            return

        assert False

    def test__Exist_name(self):
        # VICTIM1
        assert self.VICTIM.get("name", _raise_exx=False) == "valueDef"
        assert self.VICTIM.get("name0", _raise_exx=False) == "valueDef"
        assert self.VICTIM.get("name1", _raise_exx=False) is None

        assert self.VICTIM.get("name", section="SEC1", _raise_exx=False) == "value1"
        assert self.VICTIM.get("name0", section="SEC1", _raise_exx=False) == "valueDef"
        assert self.VICTIM.get("name1", section="SEC1", _raise_exx=False) == "value1"

        # VICTIM2
        assert self.VICTIM2.get("name", _raise_exx=False) == "valueDef2"
        assert self.VICTIM2.get("name0", _raise_exx=False) == "valueDef2"
        assert self.VICTIM2.get("name1", _raise_exx=False) is None

        assert self.VICTIM2.get("name", section="SEC1", _raise_exx=False) == "value12"
        assert self.VICTIM2.get("name0", section="SEC1", _raise_exx=False) == "valueDef2"
        assert self.VICTIM2.get("name1", section="SEC1", _raise_exx=False) == "value12"


# =====================================================================================================================
