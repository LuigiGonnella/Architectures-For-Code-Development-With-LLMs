import pytest
from dataclasses import FrozenInstanceError

from src.utils.config import Config, config


def test_config_default_values():
    """Test that default config values are set correctly"""
    assert config.model_name == "qwen2.5-coder:7b-instruct"
    assert config.temperature == 0.0
    assert config.max_retries == 2
    assert config.data_dir == "./data"


def test_config_is_frozen():
    """Test that config is immutable (frozen)"""
    with pytest.raises(FrozenInstanceError):
        config.model_name = "different-model"


def test_config_custom_values():
    """Test creating a custom config instance"""
    custom_config = Config(
        model_name="custom-model",
        temperature=0.5,
        max_retries=5,
        data_dir="/custom/path",
    )

    assert custom_config.model_name == "custom-model"
    assert custom_config.temperature == 0.5
    assert custom_config.max_retries == 5
    assert custom_config.data_dir == "/custom/path"


def test_config_partial_override():
    """Test creating config with partial overrides"""
    custom_config = Config(temperature=0.7)

    assert custom_config.temperature == 0.7
    assert custom_config.model_name == "qwen2.5-coder:7b-instruct"  # default
    assert custom_config.max_retries == 2  # default


def test_config_types():
    """Test that config fields have correct types"""
    assert isinstance(config.model_name, str)
    assert isinstance(config.temperature, float)
    assert isinstance(config.max_retries, int)
    assert isinstance(config.data_dir, str)
