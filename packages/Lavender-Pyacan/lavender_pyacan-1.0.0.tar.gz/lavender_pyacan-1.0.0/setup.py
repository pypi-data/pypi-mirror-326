from setuptools import setup, find_packages

setup(
    name="Lavender-Pyacan",
    version="1.0.0",
    author="Zeyu Xie",
    author_email="xie.zeyu20@gmail.com",
    description="A pip library of multiple functions.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Zeyu-Xie/Lavender-Pyacan",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
