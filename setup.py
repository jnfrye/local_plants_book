from pathlib import Path
import site
import json


# GLOBALS
SRC_FOLDER = (Path(".") / "src").resolve()


def add_project_to_pythonpath():
    """Add project source folder to site-packages so it can be imported

    Uses a custom *.pth file to accomplish this.
    """
    # Find the site-packages directory, where the custom *.pth file goes
    package_directories = site.getsitepackages()
    site_packages = [x for x in package_directories if 'site-packages' in x]
    if len(site_packages) == 0:
        raise ValueError("No site-package directory found!")
    elif len(site_packages) == 1:
        site_package_directory = Path(site_packages[0])
    else:
        raise ValueError("Multiple site-packages found!")

    # Create the *.pth file in the site-packages directory
    pth_file = site_package_directory / "PyFloraBook.pth"

    # Write the path of the source code to the *.pth file
    with pth_file.open(mode='w') as pth:
        pth.write(str(SRC_FOLDER))

    print("Wrote project directory to `{}` in site-packages.".format(
        pth_file.name
        ))


def create_config_file():
    """Create configuration file for project-wide globals

    For now, these are hard-coded to what I need. I will make these
    customizable later.
    """
    # The default data folder is one directory above the project folder
    project_folder = SRC_FOLDER.parent
    data_folder_default = project_folder.parent / "data"
    data_folder = data_folder_default

    config_dict = {"data_folder": str(data_folder)}
    config_file_name = "configuration.json"
    with (project_folder / config_file_name).open(mode='w') \
            as config_file:
        json.dump(config_dict, config_file)

    print("Created project configuration file `{}`.".format(config_file_name))

if __name__ == "__main__":
    add_project_to_pythonpath()
    create_config_file()













