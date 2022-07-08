from setuptools import setup, find_packages

setup(
	name="neobot",
	version="0.1.0",
	author="RoboticsWare",
	author_email="neopia.uz@google.ocm",
	description="Python Package for NEO SoCo",
	url="https://github.com/roboticsware/pylib_neobot.git",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=["pyserial", "websocket-client"],
	packages=find_packages(exclude=["examples", "tests"]),
	python_requires=">=3",
	zip_safe=False,
	classifiers=[
		"License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)"
	]
)