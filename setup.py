
from setuptools import setup, find_packages

setup(
    name='tbPy',
    version='1.0',
    description='A python library for creating twitch bots.',
    author='nortoh',
    author_email='christian@christianhorton.me',
    url='https://github.com/nortoh/tbPy',
    package_dir = {'': 'tbPy'},
    packages=find_packages(where='tbPy')
)