from setuptools import setup, find_packages

setup(
    name="axon-framework",
    version="0.9.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pydantic",
        "rich",
        "click",
        "fastapi",
        "uvicorn",
        "numpy",
        "beautifulsoup4"
    ],
    entry_points={
        "console_scripts": [
            "axon=axon.cli:cli",
        ],
    },
)
