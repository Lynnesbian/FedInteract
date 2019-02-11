import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="fedinteract",
	version="0.0.1",
	author="Lynnesbian",
	author_email="lynne@lynnesbian.space",
	description="A simple (both in usage complexity and features) wrapper to interact with various types of Fediverse instances with a single command.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Lynnesbian/FedInteract",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
		"Operating System :: OS Independent",
	],
)
