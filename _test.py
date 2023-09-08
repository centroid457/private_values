import os
import pytest
from privet_values import PrivetValues, Exx_PvNotAccepted


# PREPARE VICTIM ======================================================================================================
class VictimRaise(PrivetValues):
    pass


class VictimNoRaise(PrivetValues):
    PV__RISE_EXCEPTION_IF_NONE = False


# TESTS ===============================================================================================================
class Test1_Env:
    VALUE_DEF: str = "VALUE_DEF"
    VALUE_OS: str = "VALUE_OS"

    env_name__NotExists: str = f"{PrivetValues.PV__PREFIX}NotExists"
    env_name__Exists_full: str = f"{PrivetValues.PV__PREFIX}Exists_full"
    env_name__Exists_short: str = f"{PrivetValues.PV__PREFIX}Exists_short"

    @classmethod
    def setup_class(cls):
        while cls.env_name__NotExists in os.environ:
            cls.env_name__NotExists = f"{cls.env_name__NotExists}_"

        while cls.env_name__Exists_full in os.environ:
            cls.env_name__Exists_full = f"{cls.env_name__Exists_full}_"

        while cls.env_name__Exists_short in os.environ:
            cls.env_name__Exists_short = f"{cls.env_name__Exists_short}_"

        os.environ[cls.env_name__Exists_full] = cls.VALUE_OS
        os.environ[cls.env_name__Exists_short[len(PrivetValues.PV__PREFIX):]] = cls.VALUE_OS

        print()
        print()
        print(f"{cls.env_name__NotExists=}")
        print(f"{cls.env_name__Exists_full=}")
        print(f"{cls.env_name__Exists_short=}")
        print()
        print()

    @classmethod
    def teardown_class(cls):
        del os.environ[cls.env_name__Exists_full]
        del os.environ[cls.env_name__Exists_short[len(PrivetValues.PV__PREFIX):]]

    # TESTS ===========================================================================================================
    # PVS__RISE_EXCEPTION_IF_NONE -------------------------------------------------------------------------------------
    def test__PVS__RISE_EXCEPTION_IF_NONE__True(self):
        Victim = VictimRaise
        setattr(Victim, self.env_name__NotExists, None)

        try:
            Victim()
        except Exx_PvNotAccepted:
            return

        assert False

    def test__PVS__RISE_EXCEPTION_IF_NONE__False(self):
        Victim = VictimNoRaise
        setattr(Victim, self.env_name__NotExists, None)

        try:
            Victim()
        except Exx_PvNotAccepted:
            assert False

    # ENV - NOT EXISTS ------------------------------------------------------------------------------------------------
    def test__NoExists_None(self):
        Victim = VictimRaise
        setattr(Victim, self.env_name__NotExists, None)

        try:
            Victim()
        except Exx_PvNotAccepted:
            return

        assert False

    def test__NoExists_NoNone(self):
        Victim = VictimRaise
        setattr(Victim, self.env_name__NotExists, self.VALUE_DEF)

        assert getattr(Victim(), self.env_name__NotExists) == self.VALUE_DEF

    # ENV - EXISTS ----------------------------------------------------------------------------------------------------
    def test__Exists_None(self):
        Victim = VictimRaise
        setattr(Victim, self.env_name__Exists_full, None)

        assert getattr(Victim(), self.env_name__Exists_full) == self.VALUE_OS

    def test__Exists_NoNone(self):
        Victim = VictimRaise
        setattr(Victim, self.env_name__Exists_full, self.VALUE_DEF)

        assert getattr(Victim(), self.env_name__Exists_full) == self.VALUE_OS

    # SHORT NAMES -----------------------------------------------------------------------------------------------------
    def test__ExistsShortName(self):
        Victim = VictimRaise
        setattr(Victim, self.env_name__Exists_short, self.VALUE_DEF)

        assert getattr(Victim(), self.env_name__Exists_short) == self.VALUE_OS

    # _pvs_detected --------------------------------------------------------------------------------------------------
    def test__envs_detected(self):
        Victim = VictimRaise
        setattr(Victim, self.env_name__NotExists, self.VALUE_DEF)
        setattr(Victim, self.env_name__Exists_full, self.VALUE_DEF)
        setattr(Victim, self.env_name__Exists_short, self.VALUE_DEF)

        assert Victim()._pv_detected == {
            self.env_name__NotExists: self.VALUE_DEF,
            self.env_name__Exists_full: self.VALUE_OS,
            self.env_name__Exists_short: self.VALUE_OS,
        }
        setattr(Victim, self.env_name__NotExists, self.VALUE_DEF)
        setattr(Victim, self.env_name__Exists_full, None)
        setattr(Victim, self.env_name__Exists_short, None)

        assert Victim()._pv_detected == {
            self.env_name__NotExists: self.VALUE_DEF,
            self.env_name__Exists_full: self.VALUE_OS,
            self.env_name__Exists_short: self.VALUE_OS,
        }

    # envs__show* ------------------------------------------------------------------------------------------------------
    def test__pvs__show_detected(self):
        Victim = VictimRaise

        setattr(Victim, self.env_name__NotExists, self.VALUE_DEF)
        setattr(Victim, self.env_name__Exists_full, None)
        setattr(Victim, self.env_name__Exists_short, None)

        assert Victim().pv__show_detected() == {
            self.env_name__NotExists: self.VALUE_DEF,
            self.env_name__Exists_full: self.VALUE_OS,
            self.env_name__Exists_short: self.VALUE_OS,
        }

    def test__pvs__show_os_env(self):
        Victim = VictimRaise
        # uppercase - see docstring for method!
        assert Victim.pv__show_os_env(prefix=Victim.PV__PREFIX).get(self.env_name__Exists_full.upper()) == self.VALUE_OS

# =====================================================================================================================
