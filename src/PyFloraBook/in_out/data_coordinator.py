from pathlib import Path
import json
import inspect
import sys

import PyFloraBook


# Globals
OBSERVATIONS_FOLDER = "observations"
RAW_OBSERVATIONS_FOLDER = "raw_observations"
RAW_COUNTS_FOLDER = "raw_counts"
CLEANSED_FOLDER = "cleansed"
SCORES_FOLDER = "scored"
SELECTIONS_FOLDER = "selected"
NOMENCLATURE_FOLDER = "nomenclature"
PHYLOGENY_FOLDER = "phylogeny"
ORDERS_FOLDER = "orders"


def locate_source_folder() -> Path:
    """Locate top-level project source folder

    Returns:
        Path of the project source folder
    """
    package_path = Path(inspect.getsourcefile(PyFloraBook)).parent
    # This assumes that the highest-level project __init__ file is contained
    # in a sub-folder of the project folder
    return package_path.parent


def load_configuration() -> dict:
    """Load project configuration info

    Returns:
        Dictionary of configuration info.
    """
    configuration = Path(locate_source_folder().parent / "configuration.json")
    with configuration.open() as config_file:
        return json.load(config_file)


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
    return (
        locate_data_folder() / OBSERVATIONS_FOLDER / RAW_OBSERVATIONS_FOLDER
        )


def locate_nomenclature_folder() -> Path:
    """Return path of the nomenclature data folder

    Returns:
        Path of nomenclature data folder
    """
    return locate_data_folder() / NOMENCLATURE_FOLDER


def locate_orders_folder() -> Path:
    """Return path of the orders data folder

    Returns:
        Path of orders data folder
    """
    return locate_data_folder() / ORDERS_FOLDER


def locate_phylogeny_folder() -> Path:
    """Return path of the phylogeny data folder

    Returns:
        Path of phylogeny data folder
    """
    return locate_data_folder() / PHYLOGENY_FOLDER


def locate_raw_counts_folder() -> Path:
    """Return path of the raw counts data folder

    Returns:
        Path of raw counts data folder
    """
    return locate_data_folder() / OBSERVATIONS_FOLDER / RAW_COUNTS_FOLDER


def locate_cleansed_data_folder() -> Path:
    """Return path of the cleansed raw data folder

    Returns:
        Path of cleansed raw data folder
    """
    return locate_data_folder() / OBSERVATIONS_FOLDER / CLEANSED_FOLDER


def locate_scores_folder() -> Path:
    """Return path of the species scores folder

    Returns:
        Path of species scores folder
    """
    return locate_data_folder() / OBSERVATIONS_FOLDER / SCORES_FOLDER


def locate_selections_folder() -> Path:
    """Return path of the species selections folder

    Returns:
        Path of species selections folder
    """
    return locate_data_folder() / OBSERVATIONS_FOLDER / SELECTIONS_FOLDER


def locate_current_script_folder() -> Path:
    """Return path of the currently running script

    Returns:
        Path of current script
    """
    return Path(sys.path[0])
