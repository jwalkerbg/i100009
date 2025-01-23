# src/cli/app.py
import argparse
from importlib.metadata import version

import pymodule
from pymodule.core.config import Config
from pymodule.logger import get_app_logger
from pymodule.extensions.cmodulea.cmodulea import print_hello_cmodulea
from pymodule.extensions.cmoduleb.cmoduleb import print_hello_cmoduleb
from pymodule.extensions.hello_world import hello
from pymodule.extensions.worker import worker_func

logger = get_app_logger(__name__)

def parse_args():
    """Parse command-line arguments, including nested options for mqtt and MS Protocol."""
    parser = argparse.ArgumentParser(description='My CLI App with Config File and Overrides')

    # configuration file name
    parser.add_argument('--config', type=str, dest='config', default='config.toml',\
                        help="Name of the configuration file, default is 'config.toml'")
    parser.add_argument('--no-config', action='store_const', const='', dest='config',\
                        help="Do not use a configuration file (only defaults & options)")

    # version
    parser.add_argument('-v', dest='app_version', action='store_true',\
                        help='Show version information of the module')

    # Verbosity option
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument('--verbose', dest='verbose', action='store_const',\
                                 const=True, help='Enable verbose mode')
    verbosity_group.add_argument('--no-verbose', dest='verbose', action='store_const',\
                                 const=False, help='Disable verbose mode')

    # application options & parameters
    parser.add_argument('--param1', type=int, help="Parameter1")
    parser.add_argument('--param2', type=int, help="Parameter2")

    return parser.parse_args()

def main():
    """Main entry point of the CLI."""

    # Step 1: Create config object with default configuration
    cfg = Config()

    # Step 2: Parse command-line arguments
    args = parse_args()

    # Step 3: Try to load configuration from configuration file
    config_file = args.config
    try:
        cfg.load_config_file(config_file)
    except Exception as e:
        logger.info("Error with loading configuration file. Giving up.\n%s",str(e))
        return

    # Step 4: Merge default config, config.json, and command-line arguments
    cfg.merge_options(args)

    # Step 5: Show version info or run the application with collected configuration
    if cfg.config['metadata']['version']:
        app_version = version("pymodule")
        print(f"pymodule {app_version}")
    else:
        run_app(cfg)

# CLI application main function with collected options & configuration
def run_app(config:Config) -> None:
    try:
        # Add real application code here.
        logger.info("Running run_app")
        logger.info("config = %s",str(config.config))
        pymodule.hello_from_core_module_a()
        pymodule.goodbye_from_core_module_a()
        pymodule.hello_from_core_module_b()
        pymodule.goodbye_from_core_module_b()
        pymodule.hello_from_utils()
        pymodule.hello_from_ina236()
        print_hello_cmodulea()
        print_hello_cmoduleb()
        print(f"{hello()}")
        worker_func()

        pymodule.core.benchmark.benchmark(500000)
    finally:
        logger.info("Exiting run_app")


if __name__ == "__main__":
    main()
