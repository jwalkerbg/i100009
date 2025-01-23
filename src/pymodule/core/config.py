# core/config.py

import sys
from typing import Dict, Any
import argparse
from jsonschema import validate, ValidationError

from pymodule.logger import get_app_logger

logger = get_app_logger(__name__)

# Check Python version at runtime
if sys.version_info >= (3, 11):
    import tomllib as toml # Use the built-in tomllib for Python 3.11+
else:
    import tomli as toml # Use the external tomli for Python 3.7 to 3.10

class Config:
    def __init__(self) -> None:
        self.config = self.DEFAULT_CONFIG

    DEFAULT_CONFIG = {
        'template': {
            'template_name': "pymodule",
            'template_version': "3.1.3",
            'template_description': { 'text': """Template with CLI interface, configuration options in a file, logger and unit tests""", 'content-type': "text/plain" }
        },
        'metadata': {
            'version': False
        },
        'logging': {
            'verbose': False
        },
        'parameters': {
            'param1': 1,
            'param2': 2
        }
    }

    # When adding / removing changing configuration parameters, change following validation appropriately
    CONFIG_SCHEMA = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "properties": {
            "metadata": {
                "type": "object",
                "properties": {
                    "version": {
                        "type": "boolean"
                    }
                },
                "additionalProperties": False
            },
            "logging": {
                "type": "object",
                "properties": {
                    "verbose": {
                        "type": "boolean"
                    }
                },
                "additionalProperties": False
            },
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "number"
                    },
                    "param2": {
                        "type": "number"
                    }
                },
                "additionalProperties": False
            }
        },
        "additionalProperties": False
    }

    def load_toml(self,file_path) -> Dict:
        """
        Load a TOML file with exception handling.

        :param file_path: Path to the TOML file
        :return: Parsed TOML data as a dictionary
        :raises FileNotFoundError: If the file does not exist
        :raises tomli.TOMLDecodeError / tomllib.TOMLDecodeError: If there is a parsing error
        """
        try:
            # Open the file in binary mode (required by both tomli and tomllib)
            with open(file_path, 'rb') as f:
                return toml.load(f)

        except FileNotFoundError as e:
            logger.error("%s",str(e))
            raise e  # Optionally re-raise the exception if you want to propagate it
        except toml.TOMLDecodeError as e:
            logger.error("Error: Failed to parse TOML file '%s'. Invalid TOML syntax.",file_path)
            raise e  # Re-raise the exception for further handling
        except Exception as e:
            logger.error("An unexpected error occurred while loading the TOML file: %s",str(e))
            raise e  # Catch-all for any other unexpected exceptions

    def load_config_file(self, file_path: str="config.toml") -> Dict:
        # skip the configuration file if an empty name is given
        if file_path == '':
            return {}
        # Convert None to default value of 'config.json'
        if file_path == "config.toml":
            logger.error("CFG: Using default '%s'",file_path)
            file_path = 'config.toml'
        try:
            config_file = self.load_toml(file_path=file_path)
            validate(instance=config_file, schema=self.CONFIG_SCHEMA)
        except ValidationError as e:
            logger.warning("Configuration validation error in %s: %s",file_path,str(e))
            raise ValueError from e
        except Exception as e:
            logger.error("Exception when trying to load %s: %s",file_path,str(e))
            raise e

        self.deep_update(config=self.config, config_file=config_file)

        return config_file

    def deep_update(self,config: Dict[str, Any], config_file: Dict[str, Any]) -> None:
        """
        Recursively updates a dictionary (`config`) with the contents of another dictionary (`config_file`).
        It performs a deep merge, meaning that if a key contains a nested dictionary in both `config`
        and `config_file`, the nested dictionaries are merged instead of replaced.

        Parameters:
        - config (Dict[str, Any]): The original dictionary to be updated.
        - config_file (Dict[str, Any]): The dictionary containing updated values.

        Returns:
        - None: The update is done in place, so the `config` dictionary is modified directly.
        """
        for key, value in config_file.items():
            if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                # If both values are dictionaries, recurse to merge deeply
                self.deep_update(config[key], value)
            else:
                # Otherwise, update the key with the new value from config_file
                config[key] = value

    def merge_options(self, config_cli:argparse.Namespace=None) -> Dict:
        # handle CLI options if started from CLI interface
        # replace param1 and param2 with actual parameters, defined in app:parse_args()
        if config_cli:

            if config_cli.app_version is not None:
                self.config['metadata']['version'] = config_cli.app_version
            # Handle general options
            if config_cli.verbose is not None:
                self.config['logging']['verbose'] = config_cli.verbose

            # sample parameters that should be changed in real applications
            if config_cli.param1 is not None:
                self.config['parameters']['param1'] = config_cli.param1
            if config_cli.param2 is not None:
                self.config['parameters']['param2'] = config_cli.param2

        return self.config
