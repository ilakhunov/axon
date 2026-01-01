from setuptools import setup, find_packages

setup(
    name="axon-framework",
    version="0.8.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pydantic",
        "rich",
        "click",
        "fastapi",
        "uvicorn",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "axon=axon.cli:cli",
        ],
    },
)
