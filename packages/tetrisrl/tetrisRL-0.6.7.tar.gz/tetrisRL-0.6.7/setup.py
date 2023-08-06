from setuptools import setup, find_packages

setup(
    name="tetrisRL",
    version="0.6.7",
    author="Jay Butera",
    author_email="buterajay@gmail.com",
    license="MIT",
    url="https://github.com/jaybutera/tetrisRL",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.13'
    ],
)
