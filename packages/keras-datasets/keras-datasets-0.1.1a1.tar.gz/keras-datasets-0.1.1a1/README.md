# keras-datasets

A package to download common deep learning and machine datasets, convert them in hdf5 format in order to be in your Keras graph with a queue runner

[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://opensource.org/licenses/MIT/)
[![Open Source License](https://img.shields.io/github/license/DEKHTIARJonathan/keras-datasets.svg)](https://github.com/DEKHTIARJonathan/keras-datasets/releases)
[![GitHub contributors](https://img.shields.io/github/contributors/DEKHTIARJonathan/keras-datasets.svg)](https://github.com/DEKHTIARJonathan/keras-datasets)
[![Documentation Status](https://readthedocs.org/projects/keras-datasets/badge/?version=latest)](http://keras-datasets.readthedocs.io/en/latest/?badge=latest)

[![Build Status](https://travis-ci.org/DEKHTIARJonathan/keras-datasets.svg?branch=master)](https://travis-ci.org/DEKHTIARJonathan/keras-datasets)
[![Coverage](https://coveralls.io/repos/github/DEKHTIARJonathan/keras-datasets/badge.svg?branch=master)](https://coveralls.io/github/DEKHTIARJonathan/keras-datasets?branch=master)
[![PyUP Updates](https://pyup.io/repos/github/DEKHTIARJonathan/keras-datasets/shield.svg)](https://pyup.io/repos/github/DEKHTIARJonathan/keras-datasets/)
[![Python 3](https://pyup.io/repos/github/DEKHTIARJonathan/keras-datasets/python-3-shield.svg)](https://pyup.io/repos/github/DEKHTIARJonathan/keras-datasets/)

[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/keras-datasets.svg)](https://pypi.python.org/pypi/keras-datasets/)
[![GitHub release](https://img.shields.io/github/release/DEKHTIARJonathan/keras-datasets.svg?label=github-release)](https://github.com/DEKHTIARJonathan/keras-datasets/releases)
[![PyPI Release](https://img.shields.io/pypi/v/keras-datasets.svg?label=pypi-release)](https://pypi.python.org/pypi/keras-datasets/)
[![PyPI Wheel](https://img.shields.io/pypi/wheel/keras-datasets.svg)](https://pypi.python.org/pypi/keras-datasets/)
[![PyPI](https://img.shields.io/pypi/status/keras-datasets.svg?label=pypi-status)](https://pypi.python.org/pypi/keras-datasets/)

## Issues

Feel free to submit issues and enhancement requests.

## Copyright and Licensing

The project is released under the MIT License, which gives you the following rights in summary:

|**Permissions**  |**Limitations**|**Conditions**                 |
|---------------- |-------------- |------------------------------ |
|*Commercial use* |*Liability*    |*License and copyright notice* |
|*Modification*   |*Warranty*     |                               |
|*Distribution*   |               |                               |
|*Private use*    |               |                               |

## Contributing guidelines

Please have a look to the [Contributing Guidelines](CONTRIBUTING.md) first.

We follow the "fork-and-pull" Git workflow.

1. **Fork** the repo on GitHub
2. **Clone** the project to your own machine
3. **Commit** changes to your own branch
4. **Push** your work back up to your fork
5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

## Installation of the library

### Installation for production

Available with the Python Package Index: <https://pypi.python.org/pypi/keras-datasets/>

```shell
pip install keras-datasets
```

If prefered, the library can be compiled with following commands:

```shell
## First clone the repository
git clone https://github.com/DEKHTIARJonathan/keras-datasets.git

cd keras-datasets
python setup.py install
```
### Development Commands and Environment

Please run tests before commit to the repository or sending a Pull Request.<br>
If you add any new functionnality, be sure to implement the corresponding tests.

```shell
## First clone the repository and change the working directory
git clone https://github.com/DEKHTIARJonathan/keras-datasets.git
cd keras-datasets

########################################################
# =============== Create a virtualenv  =============== #
########################################################

## Install virtualenv if necessary
pip install virtualenv

## Then create a virtualenv called venv inside
virtualenv venv

########################################################
# ============= Activate the virtualenv  ============= #
########################################################

# Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate.bat

##########################################################
# ======== Install the development dependencies  ======= #
##########################################################

## Only necessary if you want to contribute to the project
pip install -e .[dev]

########################################################
# =============== Running Unit Tests  =============== #
########################################################

coverage run setup.py test
coverage report -m
coverage html

########################################################
# ================= Install Library  ================= #
########################################################

python setup.py install
```

### Where to add new dependencies in your contributions ?
Your contribution requires to install a new package in the dependencies. Be sure to only add a package if it is only necessary and no other existing package is required.

If so, please edit the file [setup.py](setup.py) and edit the following settings:

```python
#  If your package is necessary to make the library work, please add the package here:
install_requires=[
    'prod_package1==1.2.3',
    'prod_package2==2.3.4',
    '...'
],

#  If your package is necessary for development / testing / upload to PyPI but not for the production version, please add the package here:
extras_require={
    'dev': [
        'dev_package1==1.2.3',
        'dev_package2==2.3.4',
        '...'
    ]
}
```
