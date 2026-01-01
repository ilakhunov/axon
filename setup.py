from setuptools import setup, find_packages

setup(
    name="axon-ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pydantic",
        "rich"
    ],
)
