import pathlib
from setuptools import setup
from setuptools import find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="python3-albow",
    version="2.4.2",
    description="A Little Bit of Widgetry for PyGame",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://hasii2011.github.io",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pygame", "pdoc3"]
)