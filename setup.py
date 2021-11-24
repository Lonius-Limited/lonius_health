from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in lonius_health/__init__.py
from lonius_health import __version__ as version

setup(
	name="lonius_health",
	version=version,
	description="App for Lonius Limited",
	author="Lonius Limited Innovation",
	author_email="info@lonius.co.ke",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
