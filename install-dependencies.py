#!/usr/bin/env python
"""Install Package Dependencies."""
import argparse
import subprocess
import sys

# Terminal color constants.
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
NC = "\033[0m"

# Base install args
BASE_INSTALL_ARGS = ["python", "-m", "pip", "install"]


def main():
    """Main entry point method."""

    # Parse command line args.
    parser = argparse.ArgumentParser()
    parser.description = (
        "Install dependencies for package and optionally specify additional dependency groups to install."
    )
    parser.add_argument(
        "--build",
        default=False,
        action="store_true",
        help="Additionally install dependencies needed to build the package.",
    )
    parser.add_argument(
        "--dev",
        default=False,
        action="store_true",
        help="Additionally install dependencies needed to develop the package.",
    )
    parser.add_argument(
        "--doc",
        default=False,
        action="store_true",
        help="Additionally install dependencies needed to build and develop the documentation for the package.",
    )
    parser.add_argument(
        "--test",
        default=False,
        action="store_true",
        help="Additionally install dependencies needed to test the package.",
    )
    parser.add_argument(
        "--ci-36",
        default=False,
        action="store_true",
        help="Additionally install dependencies needed to do Github actions CI on python 3.6 or 3.7.",
    )
    parser.add_argument(
        "--ci-38",
        default=False,
        action="store_true",
        help="Additionally install dependencies needed to do Github actions CI on python 3.8 and up.",
    )

    args = parser.parse_args()

    # Handle based python version
    if sys.version_info.major == 3 and sys.version_info.minor < 11:
        # Install dependencies with tomli support
        install_dependencies_with_tomli(args)
    elif sys.version_info.major == 3 and sys.version_info.minor >= 11:
        # Install dependencies with native toml support.
        install_dependencies_with_tomllib(args)
    else:
        print_error("Python 3.7 or greater is required to use this script.")
        exit_with_code(1)


def install_dependencies_with_tomli(args):
    """Install dependencies with tomli."""
    try:
        import tomli  # pylint: disable=import-outside-toplevel
    except ImportError:
        print_error("The tomli package is required to run this script because your python version is < 3.11.")
        print_error("Install tomli with the following command and then re-run the script.")
        print("python -m pip install tomli")
        exit_with_code(1)

    with open("pyproject.toml", "rb") as f:
        pyproject_data = tomli.load(f)
        install_dependencies(args, pyproject_data)


def install_dependencies_with_tomllib(args):
    """Install dependencies using built in toml support."""
    try:
        import tomllib  # pylint: disable=import-outside-toplevel
    except ImportError:
        print_error("Unknown problem importing the required tomllib library for python >= 3.11.")
        exit_with_code(1)

    with open("pyproject.toml", "rb") as f:
        pyproject_data = tomllib.load(f)
        install_dependencies(args, pyproject_data)


def install_dependencies(args, pyproject_data):
    """Install the dependencies"""
    dependencies = pyproject_data["tool"]["django-adminlte2-pdq"]["dependency-groups"]
    if args.build:
        run_args = BASE_INSTALL_ARGS + dependencies["build"]
        return_code = run_command(run_args)

    elif args.dev:
        run_args = (
            BASE_INSTALL_ARGS + dependencies["build"] + dependencies["dev"] + dependencies["doc"] + dependencies["test"]
        )
        return_code = run_command(run_args)

    elif args.doc:
        run_args = BASE_INSTALL_ARGS + dependencies["doc"]
        return_code = run_command(run_args)

    elif args.test:
        run_args = BASE_INSTALL_ARGS + dependencies["test"]
        return_code = run_command(run_args)

    elif args.ci_36:
        run_args = BASE_INSTALL_ARGS + dependencies["test"]
        return_code = run_command(run_args)

    elif args.ci_38:
        run_args = BASE_INSTALL_ARGS + dependencies["doc"] + dependencies["test"] + dependencies["test-extra"]
        return_code = run_command(run_args)

    else:
        run_args = BASE_INSTALL_ARGS + pyproject_data["project"]["dependencies"]
        return_code = run_command(run_args)

    exit_with_code(return_code)


def run_command(run_args):
    """Run the commands provided by the run_args and return the exit code."""
    print_command(f"{' '.join(run_args)}")
    proc = subprocess.run(run_args, check=False)
    return proc.returncode


def exit_with_code(exit_code):
    """Print out the exit code and exit."""
    if exit_code != 0:
        print_error(f"Command failed with exit code of: {exit_code}")
    else:
        print_success(f"Command completed successfully with exit code of: {exit_code}")
    sys.exit(exit_code)


def print_primary(objects):
    """Print colored as blue."""
    print(f"{BLUE}{objects}{NC}")


def print_info(objects):
    """Print colored as cyan."""
    print(f"{CYAN}{objects}{NC}")


def print_success(objects):
    """Print colored as green."""
    print(f"{GREEN}{objects}{NC}")


def print_warning(objects):
    """Print colored as yellow."""
    print(f"{YELLOW}{objects}{NC}")


def print_error(objects):
    """Print colored as red."""
    print(f"{RED}{objects}{NC}")


def print_command(command):
    """Print command that will execute."""
    print(f"COMMAND: {BLUE}{command}{NC}")


# Prevent running on import.
if __name__ == "__main__":
    main()
