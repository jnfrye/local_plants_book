import sys
import site


PROJECT_FOLDER = "/"


def main():
    package_directories = site.getsitepackages()
    site_packages = [x for x in package_directories if 'site-packages' in x]
    if len(site_packages) == 0:
        raise ValueError("No site-package directory found!")
    elif len(site_packages) == 1:
        site_package_directory = site_packages[0]
    else:
        raise ValueError("Multiple site-packages found!")

    custom_site_file = \
        site_package_directory + PROJECT_FOLDER + "PyFloraBook.pth"
    source_directory = sys.path[0] + PROJECT_FOLDER
    print("Writing source directory ({}) to custom *.pth file:\n\n{}".format(
        '.' + PROJECT_FOLDER, custom_site_file
        ))
    with open(custom_site_file, 'w') as pth_file:
        pth_file.write(source_directory)

    print("\nDONE!")

if __name__ == "__main__":
    main()
