from setuptools import find_packages, setup

from setup_utils import SetupConfig

setup(
    name="xfilios",
    version=SetupConfig.get_version_from_package(),
    author="Data Psycho",
    author_email="mr.data.psycho@gmail.com",
    url="https://github.com/DataPsycho/xfilios",
    description="Docx and Excel File handler for Streamlit or Dash",
    long_description=SetupConfig.read_metadata_from_readme(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=SetupConfig.get_install_requirements(),
    license="MIT",
    license_files=("LICENSE",),
    keywords="FileIO, Docx, Excel, Streamlit, Dash",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
    ],
    zip_safe=False,
    include_package_data=True,
)
