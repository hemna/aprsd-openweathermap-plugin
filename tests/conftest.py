"""Pytest configuration and fixtures for aprsd_openweathermap_plugin tests."""

import pytest
from aprsd.conf.plugin_common import register_opts as register_common_opts
from oslo_config import cfg

from aprsd_openweathermap_plugin.conf.main import register_opts


@pytest.fixture(autouse=True)
def setup_config():
    """Set up oslo_config for tests."""
    # Clear any existing config
    cfg.CONF.reset()

    # Register common plugin config options (aprs_fi, etc.)
    register_common_opts(cfg.CONF)

    # Register the plugin config options
    register_opts(cfg.CONF)

    # Set default values for config options
    cfg.CONF.set_default("apiKey", "test_owm_key", group="aprsd_openweathermap_plugin")
    cfg.CONF.set_default("enabled", True, group="aprsd_openweathermap_plugin")
    cfg.CONF.set_default("apiKey", "test_aprs_fi_key", group="aprs_fi")

    # Register units config only if it doesn't already exist
    # (it may be registered by aprsd core config)
    from oslo_config.cfg import DuplicateOptError

    try:
        units_opts = [
            cfg.StrOpt("units", default="metric", help="Units for weather data"),
        ]
        cfg.CONF.register_opts(units_opts)
    except DuplicateOptError:
        # Already registered, just set the default
        cfg.CONF.set_default("units", "metric")
    except Exception:
        # Some other error, try to set default anyway
        try:
            cfg.CONF.set_default("units", "metric")
        except Exception:
            # Ignore if we can't set it - tests will mock it
            pass

    yield

    # Cleanup
    cfg.CONF.reset()
