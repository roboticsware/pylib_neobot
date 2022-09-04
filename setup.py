from setuptools import setup, find_packages

setup(
	name="neopia",
	version="0.1.4",
	author="RoboticsWare",
	author_email="neopia.uz@google.ocm",
	description="Python library for Neopia neobot",
	url="https://github.com/roboticsware/pylib_neobot.git",
	download_url="https://github.com/roboticsware/pylib_neobot/archive/refs/heads/master.zip",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=["pyserial", "websocket-client"],
	packages=find_packages(exclude=["examples", "tests"]),
	python_requires=">=3",
	zip_safe=False,
	classifiers=[
		"License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)"
	],
	keywords=['neopia', 'neobot', 'neosoco'],
)