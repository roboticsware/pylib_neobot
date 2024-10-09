from setuptools import setup, find_packages

setup(
	name="neopia",
	version="0.3.6",
	author="RoboticsWare",
	author_email="neopia.uz@google.com",
	description="Python library for NEOPIA Neobot",
	url="https://github.com/roboticsware/pylib_neobot.git",
	download_url="https://github.com/roboticsware/pylib_neobot/archive/refs/heads/master.zip",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=[
        "pyserial", 
        "websocket-client",
        "pynput",
        "opencv-python==4.6.0.66",
        "opencv-contrib-python==4.6.0.66",
        "speechrecognition",
        "pyaudio",
        "gtts",
        "playsound",
        "mediapipe",
	],
	packages=find_packages(exclude=["examples", "tests"]),
    package_data={'neopia': ['model/*.*']},
	python_requires=">=3",
	zip_safe=False,
	classifiers=[
		"License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)"
	],
	keywords=['neopia', 'neobot', 'neosoco'],
)