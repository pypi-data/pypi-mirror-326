from setuptools import setup, find_packages

setup(
    name="prepare_dataset_two",
    package_dir={"": "./src/prepare_dataset_package"},
    packages=find_packages(where="./src/prepare_dataset_package"),
    version="0.0.2"
)