import argparse
import asyncio
import logging
import sys

from pathlib import Path

from app import main

__version__ = "0.0.1a"

sys.path.append(Path(__file__).parent)

DEFAULT_NAME = f"Python/TornadoWeb/HelloWorld/{__version__}"
DESCRIPTION = """This is a Python Tornado Web "Hello World" HTTP service.

Run the program:
  python3 ./cli.py
  python3 ./cli.py -v --port 8888
"""

if __name__ == "__main__":

    # Arguments
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--port",
        metavar="<int>",
        type=int,
        default=8888,
        help="Set the port to listen for HTTP traffic (default: 8888)",
    )

    parser.add_argument(
        "--message",
        metavar="<str>",
        default="Hello, World!",
        help='Set the response message (default: "Hello, World!")',
    )

    parser.add_argument("--version", "-V", action="version", version=DEFAULT_NAME)
    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=False,
        help="Run with verbose messages enabled (Default: False)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Run with noisy debug messages enabled (Default: False)",
    )
    # Parse all arguments
    argv, remaining_argv = parser.parse_known_args()

    # Pass the program __version__ in as an attribute
    argv.version = __version__

    # Configure logging
    # https://docs.python.org/3/howto/logging.html
    if argv.debug:
        log_level = logging.DEBUG
    elif argv.verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S.%f %Z",
        level=log_level,
    )
    logging.debug(f"{__name__} - sys.argv: {sys.argv}")
    logging.debug(f"{__name__} - argv: {argv}")

    # Run the program
    try:
        # Pass all parsed arguments to the main function as key word arguments
        asyncio.run(main(**vars(argv)))
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.error(f"{sys.exc_info()[0]}; {err}")
        # Cause the program to exit on error when running in debug mode
        if hasattr(argv, "debug") and argv.debug:
            raise
