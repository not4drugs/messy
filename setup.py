import os

from setuptools import (setup,
                        find_packages)

import messy
from messy.config import PROJECT_NAME

project_base_url = 'https://github.com/not4drugs/messy/'

setup_requires = [
    'pytest-runner>=3.0',
]
install_requires = [
    'pycryptodomex>=3.4.7',
    'click>=6.7',
    'aiohttp>=2.3.9',
    'pydevd>=1.1.1',  # debugging
]
tests_require = [
    'hypothesis>=3.38.5',
    'pytest>=3.3.0',
    'pytest-cov>=2.5.1',
    'pydevd>=1.1.1',  # debugging
]

setup(name=PROJECT_NAME,
      packages=find_packages(exclude=['tests']),
      scripts=[os.path.join('scripts', 'messy')],
      version=messy.__version__,
      description=messy.__doc__,
      long_description=open('README.md').read(),
      author='John Doe',
      author_email='not4drugs@protonmail.com',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.zip',
      setup_requires=setup_requires,
      install_requires=install_requires,
      tests_require=tests_require)
