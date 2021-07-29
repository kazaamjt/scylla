import setuptools

setuptools.setup(
	name="scylla-http",
	version="1.0.0",
	description="The multi downloader.",
	url='https://github.com/kazaamjt/Scylla',
	author="kazaamjt",
	author_email='kazaamjt@gmail.com',
	license='MIT',
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
