from pathlib import Path
import json
import inspect

import PyFloraBook


def load_configuration() -> dict:
    """Load project configuration info

    Returns:
        Dictionary of configuration info.
    """
    source_path = Path(inspect.getsourcefile(PyFloraBook)).parent
    # This assumes that the PyFloraBook __init__ file is contained in a
    # sub-folder of the project path
    project_path = source_path.parent
    configuration = Path(project_path / "configuration.json")
    with configuration.open() as config_file:
        return json.load(config_file)


def locate_data_folder() -> Path:
    """Locate folder for project data

    Returns:
        Path of the data folder
    """
    return load_configuration()["data_folder"]
