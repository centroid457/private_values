import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser
from private_values import PrivateValues, Exx_PvNotAccepted, env_value_get, IniValues


# =====================================================================================================================
class Test__env_value_get:
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

    def test__Exists(self):
        assert env_value_get(self.NAME_Exists) == self.VALUE

    def test__notExists_Rise(self):
        try:
            env_value_get(self.NAME_NotExists)
        except Exx_PvNotAccepted:
            return

        assert False

    def test__notExists_noRise(self):
        assert env_value_get(self.NAME_NotExists, raise_exx=False) is None


# =====================================================================================================================
class Victim(PrivateValues):
    """
    necessary to hide original class attributes
    """
    pass


# =====================================================================================================================
class Test:
    VICTIM: Type[Victim] = Victim

    VALUE_DEF: str = "VALUE_DEF"
    VALUE_ENV: str = "VALUE_ENV"
    VALUE_RC: str = "VALUE_RC"

    pv_name__NotExists_short: str = "NotExists"
    pv_name__NotExists_full: str = f"{PrivateValues.PV__PREFIX}{pv_name__NotExists_short}"
    pv_name__Exists_short: str = "Exists"
    pv_name__Exists_full: str = f"{PrivateValues.PV__PREFIX}{pv_name__Exists_short}"

    DIRPATH_RC: pathlib.Path = pathlib.Path(TemporaryDirectory().name)

    @classmethod
    def setup_class(cls):
        while cls.pv_name__NotExists_short in os.environ:
            cls.pv_name__NotExists_short = f"{cls.pv_name__NotExists_short}_"
            cls.pv_name__NotExists_full: str = f"{PrivateValues.PV__PREFIX}{cls.pv_name__NotExists_short}"

        while cls.pv_name__Exists_short in os.environ:
            cls.pv_name__Exists_short = f"{cls.pv_name__Exists_short}_"
            cls.pv_name__Exists_full: str = f"{PrivateValues.PV__PREFIX}{cls.pv_name__Exists_short}"

        os.environ[cls.pv_name__Exists_short] = cls.VALUE_ENV

        print()
        print()
        print(f"{cls.pv_name__NotExists_short=}")
        print(f"{cls.pv_name__NotExists_full=}")
        print(f"{cls.pv_name__Exists_short=}")
        print(f"{cls.pv_name__Exists_full=}")
        print()
        print()

        # RC ------------------------------------------------------------
        cls.DIRPATH_RC.mkdir()

        rc = ConfigParser()
        rc.set(section=cls.VICTIM.PV__RC_SECTION, option=cls.pv_name__Exists_short, value=cls.VALUE_RC)

        with open(cls.DIRPATH_RC.joinpath(cls.VICTIM.PV__RC_FILENAME), 'w', errors=None) as rc_file:
            rc.write(rc_file)

    def setup_method(self, method):
        self.VICTIM = Victim
        self.VICTIM._cls_set_defaults()
        self.VICTIM.PV__RC_DIRPATH = self.DIRPATH_RC

    @classmethod
    def teardown_class(cls):
        del os.environ[cls.pv_name__Exists_short]
        shutil.rmtree(cls.DIRPATH_RC)

    # PVS__RISE_EXCEPTION_IF_NONE -------------------------------------------------------------------------------------
    @pytest.mark.parametrize(argnames="env,rc", argvalues=[(True, False), (False, True), (True, True)])
    def test__RISE_EXCEPTION_IF_NONE__True(self, env, rc):
        self.VICTIM.PV__USE_ENV = env
        self.VICTIM.PV__USE_RC = rc

        setattr(self.VICTIM, self.pv_name__NotExists_full, None)

        try:
            self.VICTIM()
        except Exx_PvNotAccepted:
            return

        assert False

    @pytest.mark.parametrize(argnames="env,rc", argvalues=[(True, False), (False, True), (True, True)])
    def test__RISE_EXCEPTION_IF_NONE__False(self, env, rc):
        self.VICTIM.PV__USE_ENV = env
        self.VICTIM.PV__USE_RC = rc

        self.VICTIM.PV__RISE_EXCEPTION_IF_NONE = False
        setattr(self.VICTIM, self.pv_name__NotExists_full, None)

        try:
            self.VICTIM()
        except Exx_PvNotAccepted:
            assert False

    # ENV - NOT EXISTS ------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(argnames="env,rc", argvalues=[(True, False), (False, True), (True, True)])
    def test__NoExists_NoDef(self, env, rc):
        self.VICTIM.PV__USE_ENV = env
        self.VICTIM.PV__USE_RC = rc

        setattr(self.VICTIM, self.pv_name__NotExists_full, None)

        try:
            self.VICTIM()
        except Exx_PvNotAccepted:
            return

        assert False

    @pytest.mark.parametrize(argnames="env,rc", argvalues=[(True, False), (False, True), (True, True)])
    def test__NoExists_Def(self, env, rc):
        self.VICTIM.PV__USE_ENV = env
        self.VICTIM.PV__USE_RC = rc

        setattr(self.VICTIM, self.pv_name__NotExists_full, self.VALUE_DEF)

        assert getattr(self.VICTIM(), self.pv_name__NotExists_full) == self.VALUE_DEF

    # ENV - EXISTS ----------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(argnames="env,rc", argvalues=[(True, False), (False, True), (True, True)])
    def test__Exists_NoDef(self, env, rc):
        self.VICTIM.PV__USE_ENV = env
        self.VICTIM.PV__USE_RC = rc

        setattr(self.VICTIM, self.pv_name__Exists_full, None)

        expected = None
        if env:
            expected = self.VALUE_ENV
        elif rc:
            expected = self.VALUE_RC
        assert getattr(self.VICTIM(), self.pv_name__Exists_full) == expected

    @pytest.mark.parametrize(argnames="env,rc,envBetterRc", argvalues=[
        (False, False, False),

        (True, False, True), (False, True, True), (True, True, True),
        (True, False, False), (False, True, False), (True, True, False),
    ])
    def test__Exists_Def__with_ENV_BETTER_THEN_RC(self, env, rc, envBetterRc):
        self.VICTIM.PV__USE_ENV = env
        self.VICTIM.PV__USE_RC = rc
        self.VICTIM.PV__ENV_BETTER_THEN_RC = envBetterRc

        setattr(self.VICTIM, self.pv_name__Exists_full, self.VALUE_DEF)

        expected = self.VALUE_DEF
        if envBetterRc:
            if env:
                expected = self.VALUE_ENV
            elif rc:
                expected = self.VALUE_RC
        else:
            if rc:
                expected = self.VALUE_RC
            elif env:
                expected = self.VALUE_ENV

        assert getattr(self.VICTIM(), self.pv_name__Exists_full) == expected

    # _pvs_detected ---------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(argnames="env,rc", argvalues=[(True, False), (False, True), (True, True)])
    def test__pv_detected(self, env, rc):
        self.VICTIM.PV__USE_ENV = env
        self.VICTIM.PV__USE_RC = rc

        expected = None
        if env:
            expected = self.VALUE_ENV
        elif rc:
            expected = self.VALUE_RC

        setattr(self.VICTIM, self.pv_name__NotExists_full, self.VALUE_DEF)
        setattr(self.VICTIM, self.pv_name__Exists_full, self.VALUE_DEF)

        assert self.VICTIM()._pv_detected == {
            self.pv_name__NotExists_short: self.VALUE_DEF,
            self.pv_name__Exists_short: expected,
        }
        setattr(self.VICTIM, self.pv_name__NotExists_full, self.VALUE_DEF)
        setattr(self.VICTIM, self.pv_name__Exists_full, None)

        assert self.VICTIM()._pv_detected == {
            self.pv_name__NotExists_short: self.VALUE_DEF,
            self.pv_name__Exists_short: expected,
        }

    # envs__show* -----------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(argnames="env,rc", argvalues=[(True, False), (False, True), (True, True)])
    def test__pv__show_detected(self, env, rc):
        self.VICTIM.PV__USE_ENV = env
        self.VICTIM.PV__USE_RC = rc

        expected = None
        if env:
            expected = self.VALUE_ENV
        elif rc:
            expected = self.VALUE_RC

        setattr(self.VICTIM, self.pv_name__NotExists_full, self.VALUE_DEF)
        setattr(self.VICTIM, self.pv_name__Exists_full, None)

        assert self.VICTIM().pv__show_detected() == {
            self.pv_name__NotExists_short: self.VALUE_DEF,
            self.pv_name__Exists_short: expected,
        }

    def test__pv__show_os_env(self):
        # uppercase - see docstring for method!
        envs = self.VICTIM._pv__show_env(self.pv_name__Exists_short)
        print(envs)
        assert envs.get(self.pv_name__Exists_short.upper()) == self.VALUE_ENV


# =====================================================================================================================
