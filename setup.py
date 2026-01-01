from setuptools import setup, find_packages

setup(
    name="axon-framework",
    version="0.5.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pydantic",
        "rich"
    ],
)
