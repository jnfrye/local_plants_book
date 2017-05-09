from pathlib import Path
import site
import json

import PyFloraBook.input_output.data_coordinator as dc


def add_project_to_pythonpath():
    """Add project folder to user's PYTHONPATH

    Uses a custom *.pth file to accomplish this
    """
    package_directories = site.getsitepackages()
    site_packages = [x for x in package_directories if 'site-packages' in x]
    if len(site_packages) == 0:
        raise ValueError("No site-package directory found!")
    elif len(site_packages) == 1:
        site_package_directory = Path(site_packages[0])
    else:
        raise ValueError("Multiple site-packages found!")

    pth_file_name = "PyFloraBook.pth"
    project_site_package = site_package_directory / pth_file_name
    project_folder = dc.locate_project_folder()
    with project_site_package.open(mode='w') as pth_file:
        pth_file.write(str(project_folder))

    print("Wrote project directory to {} in site-packages.".format(
          pth_file_name))


def create_config_file():
    """Create configuration file for project-wide globals

    For now, these are hard-coded to what I need. I will make these
    customizable later.
    """
    project_folder = dc.locate_project_folder()

    # The default data folder is one directory above the project folder
    data_folder_default = project_folder.parent / "data"
    data_folder = data_folder_default

    config_dict = {"data_folder": str(data_folder)}
    config_file_name = "configuration.json"
    with (project_folder / config_file_name).open(mode='w') \
            as config_file:
        json.dump(config_dict, config_file)

    print("Created project configuration file {}.".format(config_file_name))

if __name__ == "__main__":
    add_project_to_pythonpath()
    create_config_file()
