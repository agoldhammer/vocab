from setuptools import setup, find_packages
setup(
    name="vocab",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "slexy = vocab.cli:main"
        ]
    }
)
