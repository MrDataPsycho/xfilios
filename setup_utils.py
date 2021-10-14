import os.path
import re


class SetupConfig:
    PACKAGE_NAME = "xfilios"

    @staticmethod
    def parse_pipfile():
        """Parse a Pipfile and store it in Dictionary"""
        pipfile_dict = dict()
        current_option = None
        with open("Pipfile", "r") as f:
            for line in f:
                if line.startswith("["):
                    option = re.sub(r"\[|\]|\n", "", line)
                    pipfile_dict[option] = list()
                    current_option = option.strip()
                if line != "" and not line.startswith("[") and len(line) > 0:
                    pipfile_dict[current_option].append(line.strip().replace('"', ""))
        return pipfile_dict

    @staticmethod
    def format_requirements(item):
        """Format Package name for install requires"""
        if "*" in item[1]:
            return item[0]
        return "".join(item)

    @classmethod
    def get_install_requirements(cls):
        """Generate Install Requirements"""
        try:
            pipfile_dict = cls.parse_pipfile()
            packages = [
                item.split(" = ")
                for item in pipfile_dict["packages"]
                if "editable" not in item and len(item) > 0
            ]
            packages = [cls.format_requirements(item) for item in packages]
            print("Following are the required packages: {}".format(", ".join(packages)))
            return packages
        except Exception as e:
            raise IOError(e)

    @staticmethod
    def read_metadata_from_readme():
        """Read the readme file for setup."""
        readme_txt = ""
        try:
            with open("README.md", "rt", encoding="utf-8") as f:
                readme_text = f.read()
                print("Read me read successfully !")
                return readme_text
        except FileNotFoundError as e:
            print(e)
            return readme_txt
        except Exception as e:
            print(e)
            return readme_txt

    @classmethod
    def get_version_from_package(cls):
        """Read the current version from the package"""
        with open(
            os.path.join("src", cls.PACKAGE_NAME, "__init__.py"), "rt", encoding="utf-8"
        ) as f:
            for line in f:
                if "VERSION" in line:
                    version: str = line.split("=")[1]
                    version = version.strip()
                    print(f"The version tag will be used for the build: {version}")
                    return version
        raise KeyError("Could not find the VERSION tag in the __init__.py file")
