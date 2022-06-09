from setuptools import find_packages, setup
setup(
    name='MyToolPackage',
    version='2.1.4',
    packages=find_packages(),
    author='Su Tiaotiao',
    zip_safe=True,
    include_package_data=True,
    exclude_package_data = { '': ['README.txt'] }
)
