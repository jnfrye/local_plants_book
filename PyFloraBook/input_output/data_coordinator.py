from pathlib import Path
import json
import inspect
import sys

import PyFloraBook


# Globals
OBSERVATIONS_FOLDER = "observation_data"
RAW_OBSERVATIONS_FOLDER = "raw_observations"
RAW_COUNTS_FOLDER = "raw_counts"


def locate_project_folder() -> Path:
    """Locate top-level project folder

    Returns:
        Path of the project folder
    """
    source_path = Path(inspect.getsourcefile(PyFloraBook)).parent
    # This assumes that the highest-level project __init__ file is contained
    # in a sub-folder of the project folder
    return source_path.parent


def locate_data_folder() -> Path:
    """Return path of the data IO folder

    Returns:
        Path of data IO folder
    """
    return Path(load_configuration()["data_folder"])


def locate_raw_observations_folder() -> Path:
    """Return path of the raw observations data folder

    Returns:
        Path of raw observations data folder
    """
    return (locate_data_folder() / OBSERVATIONS_FOLDER /
            RAW_OBSERVATIONS_FOLDER)


def locate_raw_counts_folder() -> Path:
    """Return path of the raw counts data folder

    Returns:
        Path of raw counts data folder
    """
    return locate_data_folder() / OBSERVATIONS_FOLDER / RAW_COUNTS_FOLDER


def load_configuration() -> dict:
    """Load project configuration info

    Returns:
        Dictionary of configuration info.
    """
    configuration = Path(locate_project_folder() / "configuration.json")
    with configuration.open() as config_file:
        return json.load(config_file)


def locate_current_script_folder() -> Path:
    """Return path of the currently running script

    Returns:
        Path of current script
    """
    return Path(sys.path[0])
