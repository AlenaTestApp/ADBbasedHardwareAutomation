import pytest
from core.device_controller import unlock_device


@pytest.fixture(autouse=True)
def setup_device():
    """Automatically unlock device before each test"""
    unlock_device()
