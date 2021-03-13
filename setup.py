import pathlib
from setuptools import setup
from setuptools import find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

DATA_FILES = [('albow/themes/resources', ['albow/themes/resources/default-theme.ini']),
              ('albow/themes/resources', ['albow/themes/resources/Vera.ttf']),
              ('albow/themes/resources', ['albow/themes/resources/VeraBd.ttf']),
             ]
setup(
    name="python3-albow",
    version="2.90.0",
    author='Humberto A. Sanchez II',
    author_email='Humberto.A.Sanchez.II@gmail.com',
    description="A Little Bit of Widgetry for PyGame",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/albow-python-3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=['pygame']
)
