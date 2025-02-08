from setuptools import setup, find_packages

setup(
    name="nillion-signatures",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "cryptography>=3.4.7",
        "nilql>=0.0.0a9",
        "requests>=2.32.3"
    ],
    author="Dave Butler",
    author_email="",
    description="A signature library for the Nillion Network",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NillionNetwork/signatures-py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 