from setuptools import setup, find_packages

setup(
    name="module_6",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
    ],
)