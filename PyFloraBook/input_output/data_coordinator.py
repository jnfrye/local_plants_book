from pathlib import Path
import json
import inspect
import sys

import PyFloraBook


OBSERVATIONS_FOLDER = "observation_data"
RAW_DATA_FOLDER = "raw"


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


def locate_raw_data_folder() -> Path:
    """Return path of the raw data folder

    Returns:
        Path of raw data folder
    """
    return locate_data_folder() / OBSERVATIONS_FOLDER / RAW_DATA_FOLDER


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
