"""
Config module that tries to fetch the matching config for given profile
 from PROJECT_PATH/config.
 """
import logging
import os
from pathlib import Path
from typing import Dict, Any

import yaml

_config_yaml: Dict[str, Any]
_log = logging.getLogger(__name__)


def init(profile: str):
    """ Init config file from path. """
    global _config_yaml

    config_path = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(
        config_path,
        f'../configuration/pump_light-{profile.lower().strip()}.yaml')
    yaml_path = Path(config_path)
    if yaml_path.exists():
        with yaml_path.open('r') as yaml_file:
            _config_yaml = yaml.load(yaml_file, Loader=yaml.Loader)
    else:
        _config_yaml = dict()
        _log.debug('No "%s" found.', config_path)


def get_config(name: str):
    """
    Checks first the environment variable for a config.
    When it is not available it will look for it in the
    config file. It can only fetch simple types (int,
    str, float) or a list of str from an environment variable.
    The list must be colon separated.

    Example for config name: "database.authentication_source" is equal to

    in config file
    '''
    database:
        authentication_source: admin
    '''

    OR

    environment variable (watch out "_" becomes "__" and gets the "IOT_" prefix)
    '''
    IOT_DATABASE_AUTHENTICATION__SOURCE
    '''

    """
    # 1. Check environment variables
    env_name = name.replace('_', '__').replace('.', '_').upper()
    env_val = os.getenv('IOT_' + env_name)
    if env_val:
        if ';' in env_val:
            return [v.strip() for v in env_val.split(';')]
        return env_val

    # 2. Check config file
    keys = name.split('.')
    val = _config_yaml
    for k in keys:
        if isinstance(val, dict):
            val = val.get(k, {})

    if val:
        return val
    raise ValueError(f'"{name} not found')
