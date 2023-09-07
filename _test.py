import os
import pytest
from environs_os_getter_class import EnvsOsGetterClass, Exx_EnvsNotAccepted


# PREPARE VICTIM ======================================================================================================
class VictimRaise(EnvsOsGetterClass):
    pass


class VictimNoRaise(EnvsOsGetterClass):
    ENVS_RISE_EXCEPTION = False


# TESTS ===============================================================================================================
class Test:
    VALUE_DEF: str = "VALUE_DEF"
    VALUE_OS: str = "VALUE_OS"

    env_name__NotExists: str = "ENV__NotExists"
    env_name__Exists_full: str = "ENV__Exists_full"
    env_name__Exists_short: str = "ENV__Exists_short"

    @classmethod
    def setup_class(cls):
        while cls.env_name__NotExists in os.environ:
            cls.env_name__NotExists = f"{cls.env_name__NotExists}_"

        while cls.env_name__Exists_full in os.environ:
            cls.env_name__Exists_full = f"{cls.env_name__Exists_full}_"

        while cls.env_name__Exists_short in os.environ:
            cls.env_name__Exists_short = f"{cls.env_name__Exists_short}_"

        os.environ[cls.env_name__Exists_full] = cls.VALUE_OS
        os.environ[cls.env_name__Exists_short[5:]] = cls.VALUE_OS

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
        del os.environ[cls.env_name__Exists_short[5:]]

    # TESTS ===========================================================================================================
    # ENVS_RISE_EXCEPTION ---------------------------------------------------------------------------------------------
    def test__ENVS_RISE_EXCEPTION__True(self):
        Victim = VictimRaise
        setattr(Victim, self.env_name__NotExists, None)

        try:
            Victim()
        except Exx_EnvsNotAccepted:
            return

        assert False

    def test__ENVS_RISE_EXCEPTION__False(self):
        Victim = VictimNoRaise
        setattr(Victim, self.env_name__NotExists, None)

        try:
            Victim()
        except Exx_EnvsNotAccepted:
            assert False

    # ENV - NOT EXISTS ------------------------------------------------------------------------------------------------
    def test__NoExists_None(self):
        Victim = VictimRaise
        setattr(Victim, self.env_name__NotExists, None)

        try:
            Victim()
        except Exx_EnvsNotAccepted:
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

    # _envs_detected --------------------------------------------------------------------------------------------------
    def test__envs_detected(self):
        Victim = VictimRaise
        setattr(Victim, self.env_name__NotExists, self.VALUE_DEF)
        setattr(Victim, self.env_name__Exists_full, self.VALUE_DEF)
        setattr(Victim, self.env_name__Exists_short, self.VALUE_DEF)

        assert Victim()._envs_detected == {
            self.env_name__NotExists: self.VALUE_DEF,
            self.env_name__Exists_full: self.VALUE_OS,
            self.env_name__Exists_short: self.VALUE_OS,
        }
        setattr(Victim, self.env_name__NotExists, self.VALUE_DEF)
        setattr(Victim, self.env_name__Exists_full, None)
        setattr(Victim, self.env_name__Exists_short, None)

        assert Victim()._envs_detected == {
            self.env_name__NotExists: self.VALUE_DEF,
            self.env_name__Exists_full: self.VALUE_OS,
            self.env_name__Exists_short: self.VALUE_OS,
        }

    # envs__show* ------------------------------------------------------------------------------------------------------
    def test__envs__show_used(self):
        Victim = VictimRaise

        setattr(Victim, self.env_name__NotExists, self.VALUE_DEF)
        setattr(Victim, self.env_name__Exists_full, None)
        setattr(Victim, self.env_name__Exists_short, None)

        assert Victim().envs__show_used() == {
            self.env_name__NotExists: self.VALUE_DEF,
            self.env_name__Exists_full: self.VALUE_OS,
            self.env_name__Exists_short: self.VALUE_OS,
        }

    def test__show_os_all(self):
        Victim = VictimRaise

        assert Victim.envs__show_os_all(prefix=Victim.ENVS_PREFIX).get(self.env_name__Exists_full.upper()) == self.VALUE_OS

# =====================================================================================================================
