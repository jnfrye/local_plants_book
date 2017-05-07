import sys
import site


# TODO Eventually, I want to this to do things like create symlinks to the
# TODO scripts on linux computers (maybe)

# TODO Instead of hard-coding "PyFloraBook", maybe get it from project
PROJECT_FOLDER = "/PyFloraBook"


def main():
    package_directories = site.getsitepackages()
    site_packages = [x for x in package_directories if 'site-packages' in x]
    if len(site_packages) == 0:
        raise ValueError("No site-package directory found!")
    elif len(site_packages) == 1:
        site_package_directory = site_packages[0]
    else:
        raise ValueError("Multiple site-packages found!")

    custom_site_file = site_package_directory + PROJECT_FOLDER + ".pth"
    source_directory = sys.path[0] + PROJECT_FOLDER
    print("Writing source directory ({}) to custom *.pth file:\n\n{}".format(
        '.' + PROJECT_FOLDER, custom_site_file
        ))
    with open(custom_site_file, 'w') as pth_file:
        pth_file.write(source_directory)

    print("\nDONE!")

if __name__ == "__main__":
    # TODO Disabled for now (not needed with new project layout)
    # main()
    pass
