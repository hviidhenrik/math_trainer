from setuptools import find_packages, setup

from math_trainer.config.definitions import VERSION

setup(
    name="math_trainer",
    packages=find_packages(),
    version=VERSION,
    description="Simple Python program to practice mental math",
    author="Henrik Hviid Hansen",
)
