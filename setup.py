from pathlib import Path
import site

import PyFloraBook.input_output.data_coordinator as dc


def add_project_to_pythonpath():
    package_directories = site.getsitepackages()
    site_packages = [x for x in package_directories if 'site-packages' in x]
    if len(site_packages) == 0:
        raise ValueError("No site-package directory found!")
    elif len(site_packages) == 1:
        site_package_directory = Path(site_packages[0])
    else:
        raise ValueError("Multiple site-packages found!")

    project_site_package = site_package_directory / "PyFloraBook.pth"
    project_directory = dc.locate_project_folder()
    with project_site_package.open(mode='w') as pth_file:
        pth_file.write(str(project_directory))

    print("Wrote project directory to custom *.pth file:\n\n{}".format(
          project_site_package))


def create_config_file():
    pass  # TODO LEFT OFF HERE

if __name__ == "__main__":
    add_project_to_pythonpath()
    create_config_file()
