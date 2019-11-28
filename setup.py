import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="centreon-sdk",
    version="0.0.2",
    author="Niklas Pfister",
    author_email="contact@omikron.pw",
    description="A SDK for python to communicate with Centreon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myOmikron/TelegramBotAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "wheel",
        "requests",
        "jsonpickle"
    ]
)
