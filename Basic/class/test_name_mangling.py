import pytest
from name_mangling import BaseService, SpecializedService


@pytest.fixture
def base_service():
    """Fixture for a standard BaseService instance."""
    return BaseService(settings=["init_1", "init_2"])


@pytest.fixture
def specialized_service():
    """Fixture for a SpecializedService instance."""
    return SpecializedService(settings=["init_1", "init_2"])


def test_base_service_initialization(base_service: BaseService):
    """Verifies that BaseService correctly uppercases initial settings."""
    assert base_service.active_config == ["INIT_1", "INIT_2"]


def test_base_service_configure(base_service: BaseService):
    """Verifies that subsequent calls to configure append uppercased strings."""
    base_service.configure(settings=["new_setting"])
    assert base_service.active_config == ["INIT_1", "INIT_2", "NEW_SETTING"]


def test_specialized_service_initialization(specialized_service: SpecializedService):
    """
    CRITICAL TEST: Verifies name mangling works.
    Even though SpecializedService overrides 'configure' with an incompatible
    signature, the __init__ call (via BaseService) should still work.
    """
    assert specialized_service.active_config == ["INIT_1", "INIT_2"]


def test_specialized_service_configure(specialized_service: SpecializedService):
    """Verifies that the specialized 2-argument configure works as expected."""
    specialized_service.configure(key="timeout", value="30s")
    # Note: Specialized override does NOT uppercase, unlike the base class.
    assert specialized_service.active_config == ["INIT_1", "INIT_2", "timeout:30s"]
