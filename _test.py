import os
import pytest
from typing import *
from private_values import PrivateValues, Exx_PvNotAccepted

pass    # ENV =========================================================================================================
pass    # ENV =========================================================================================================
pass    # ENV =========================================================================================================
pass    # ENV =========================================================================================================


# PREPARE VICTIM ======================================================================================================
class VictimEnvCls(PrivateValues):
    PV__USE_RC = False
    pass


@pytest.fixture()
def VictimEnv():
    VictimEnvCls._cls_set_defaults()
    yield VictimEnvCls


# =====================================================================================================================
class Test1_Env:
    VALUE_DEF: str = "VALUE_DEF"
    VALUE_ENV: str = "VALUE_ENV"

    env_name__NotExists_short: str = "NotExists"
    env_name__NotExists_full: str = f"{PrivateValues.PV__PREFIX}{env_name__NotExists_short}"
    env_name__Exists_short: str = "Exists"
    env_name__Exists_full: str = f"{PrivateValues.PV__PREFIX}{env_name__Exists_short}"

    @classmethod
    def setup_class(cls):
        while cls.env_name__NotExists_short in os.environ:
            cls.env_name__NotExists_short = f"{cls.env_name__NotExists_short}_"
            cls.env_name__NotExists_full: str = f"{PrivateValues.PV__PREFIX}{cls.env_name__NotExists_short}"

        while cls.env_name__Exists_short in os.environ:
            cls.env_name__Exists_short = f"{cls.env_name__Exists_short}_"
            cls.env_name__Exists_full: str = f"{PrivateValues.PV__PREFIX}{cls.env_name__Exists_short}"

        os.environ[cls.env_name__Exists_short] = cls.VALUE_ENV

        print()
        print()
        print(f"{cls.env_name__NotExists_short=}")
        print(f"{cls.env_name__NotExists_full=}")
        print(f"{cls.env_name__Exists_short=}")
        print(f"{cls.env_name__Exists_full=}")
        print()
        print()

    @classmethod
    def teardown_class(cls):
        del os.environ[cls.env_name__Exists_short]

    # PVS__RISE_EXCEPTION_IF_NONE -------------------------------------------------------------------------------------
    def test__PVS__RISE_EXCEPTION_IF_NONE__True(self, VictimEnv):
        setattr(VictimEnv, self.env_name__NotExists_full, None)

        try:
            VictimEnv()
        except Exx_PvNotAccepted:
            return

        assert False

    def test__PVS__RISE_EXCEPTION_IF_NONE__False(self, VictimEnv):
        setattr(VictimEnv, "PV__RISE_EXCEPTION_IF_NONE", False)
        setattr(VictimEnv, self.env_name__NotExists_full, None)

        try:
            VictimEnv()
        except Exx_PvNotAccepted:
            assert False

    # ENV - NOT EXISTS ------------------------------------------------------------------------------------------------
    def test__NoExists_None(self, VictimEnv):
        setattr(VictimEnv, self.env_name__NotExists_full, None)

        try:
            VictimEnv()
        except Exx_PvNotAccepted:
            return

        assert False

    def test__NoExists_NoNone(self, VictimEnv):
        setattr(VictimEnv, self.env_name__NotExists_full, self.VALUE_DEF)

        assert getattr(VictimEnv(), self.env_name__NotExists_full) == self.VALUE_DEF

    # ENV - EXISTS ----------------------------------------------------------------------------------------------------
    def test__Exists_None(self, VictimEnv):
        setattr(VictimEnv, self.env_name__Exists_full, None)

        assert getattr(VictimEnv(), self.env_name__Exists_full) == self.VALUE_ENV

    def test__Exists_NoNone(self, VictimEnv):
        setattr(VictimEnv, self.env_name__Exists_full, self.VALUE_DEF)

        assert getattr(VictimEnv(), self.env_name__Exists_full) == self.VALUE_ENV

    # _pvs_detected --------------------------------------------------------------------------------------------------
    def test__envs_detected(self, VictimEnv):
        setattr(VictimEnv, self.env_name__NotExists_full, self.VALUE_DEF)
        setattr(VictimEnv, self.env_name__Exists_full, self.VALUE_DEF)

        assert VictimEnv()._pv_detected == {
            self.env_name__NotExists_short: self.VALUE_DEF,
            self.env_name__Exists_short: self.VALUE_ENV,
        }
        setattr(VictimEnv, self.env_name__NotExists_full, self.VALUE_DEF)
        setattr(VictimEnv, self.env_name__Exists_full, None)

        assert VictimEnv()._pv_detected == {
            self.env_name__NotExists_short: self.VALUE_DEF,
            self.env_name__Exists_short: self.VALUE_ENV,
        }

    # envs__show* ------------------------------------------------------------------------------------------------------
    def test__pvs__show_detected(self, VictimEnv):
        setattr(VictimEnv, self.env_name__NotExists_full, self.VALUE_DEF)
        setattr(VictimEnv, self.env_name__Exists_full, None)

        assert VictimEnv().pv__show_detected() == {
            self.env_name__NotExists_short: self.VALUE_DEF,
            self.env_name__Exists_short: self.VALUE_ENV,
        }

    def test__pvs__show_os_env(self, VictimEnv):
        # uppercase - see docstring for method!
        envs = VictimEnv._pv__show_env(self.env_name__Exists_short)
        print(envs)
        assert envs.get(self.env_name__Exists_short.upper()) == self.VALUE_ENV


pass    # RC ==========================================================================================================
pass    # RC ==========================================================================================================
pass    # RC ==========================================================================================================
pass    # RC ==========================================================================================================


# PREPARE VICTIM ======================================================================================================
class VictimRaise_RC(PrivateValues):
    PV__USE_ENV = False


class VictimNoRaise_RC(PrivateValues):
    PV__USE_ENV = False
    PV__RISE_EXCEPTION_IF_NONE = False


# =====================================================================================================================
class Test2_Rc:
    VALUE_DEF: str = "VALUE_DEF"
    VALUE_RC: str = "VALUE_RC"

    @classmethod
    def setup_class(cls):


        print()
        print()
        print(f"{cls.env_name__NotExists_short=}")
        print(f"{cls.env_name__NotExists_full=}")
        print(f"{cls.env_name__Exists_short=}")
        print(f"{cls.env_name__Exists_full=}")
        print()
        print()

    @classmethod
    def teardown_class(cls):
        pass


# =====================================================================================================================
