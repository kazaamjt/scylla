import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
with open(this_directory/"README.md", encoding="utf-8") as f:
	long_description = f.read()


setuptools.setup(
	name="scylla-http",
	version="1.0.0",
	description="The parallel downloader.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/kazaamjt/Scylla",
	author="kazaamjt",
	author_email="kazaamjt@gmail.com",
	license="MIT",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	packages=setuptools.find_packages(),
	python_requires=">=3.9",
	install_requires=[
		"aiohttp==3.7.4.post0",
		"click==8.0.1",
	],
	entry_points={
		"console_scripts": [
			"scylla=scylla.main:main"
		]
	},
)
