import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="centreon-sdk",
    version="0.0.1",
    author="myOmikron",
    author_email="kontakt@omikron.pw",
    description="A SDK for python to communicate with Centreon",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/myOmikron/TelegramBotAPI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "wheel",
        "httpx",
        "jsonpickle"
    ]
)
