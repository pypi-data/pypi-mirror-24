keras-datasets
==============

A package to download common deep learning and machine datasets, convert
them in hdf5 format in order to be in your Keras graph with a queue
runner

|Open Source Love| |Open Source License| |GitHub contributors|
|Documentation Status|

|Build Status| |Coverage| |PyUP Updates| |Python 3|

|PyPI Python Versions| |GitHub release| |PyPI Release| |PyPI Wheel|
|PyPI|

Issues
------

Feel free to submit issues and enhancement requests.

Copyright and Licensing
-----------------------

The project is released under the MIT License, which gives you the
following rights in summary:

+--------------------+-------------------+----------------------------------+
| **Permissions**    | **Limitations**   | **Conditions**                   |
+====================+===================+==================================+
| *Commercial use*   | *Liability*       | *License and copyright notice*   |
+--------------------+-------------------+----------------------------------+
| *Modification*     | *Warranty*        |                                  |
+--------------------+-------------------+----------------------------------+
| *Distribution*     |                   |                                  |
+--------------------+-------------------+----------------------------------+
| *Private use*      |                   |                                  |
+--------------------+-------------------+----------------------------------+

Contributing guidelines
-----------------------

Please have a look to the `Contributing Guidelines <CONTRIBUTING.md>`__
first.

We follow the "fork-and-pull" Git workflow.

1. **Fork** the repo on GitHub
2. **Clone** the project to your own machine
3. **Commit** changes to your own branch
4. **Push** your work back up to your fork
5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull
request!

Installation of the library
---------------------------

Installation for production
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Available with the Python Package Index:
https://pypi.python.org/pypi/keras-datasets/

.. code:: shell

    pip install keras-datasets

If prefered, the library can be compiled with following commands:

.. code:: shell

    ## First clone the repository
    git clone https://github.com/DEKHTIARJonathan/keras-datasets.git

    cd keras-datasets
    python setup.py install

Development Commands and Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please run tests before commit to the repository or sending a Pull
Request. If you add any new functionnality, be sure to implement the
corresponding tests.

.. code:: shell

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

Where to add new dependencies in your contributions ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your contribution requires to install a new package in the dependencies.
Be sure to only add a package if it is only necessary and no other
existing package is required.

If so, please edit the file `setup.py <setup.py>`__ and edit the
following settings:

.. code:: python

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

.. |Open Source Love| image:: https://badges.frapsoft.com/os/v2/open-source.svg?v=103
   :target: https://opensource.org/licenses/MIT/
.. |Open Source License| image:: https://img.shields.io/github/license/DEKHTIARJonathan/keras-datasets.svg
   :target: https://github.com/DEKHTIARJonathan/keras-datasets/releases
.. |GitHub contributors| image:: https://img.shields.io/github/contributors/DEKHTIARJonathan/keras-datasets.svg
   :target: https://github.com/DEKHTIARJonathan/keras-datasets
.. |Documentation Status| image:: https://readthedocs.org/projects/keras-datasets/badge/?version=latest
   :target: http://keras-datasets.readthedocs.io/en/latest/?badge=latest
.. |Build Status| image:: https://travis-ci.org/DEKHTIARJonathan/keras-datasets.svg?branch=master
   :target: https://travis-ci.org/DEKHTIARJonathan/keras-datasets
.. |Coverage| image:: https://coveralls.io/repos/github/DEKHTIARJonathan/keras-datasets/badge.svg?branch=master
   :target: https://coveralls.io/github/DEKHTIARJonathan/keras-datasets?branch=master
.. |PyUP Updates| image:: https://pyup.io/repos/github/DEKHTIARJonathan/keras-datasets/shield.svg
   :target: https://pyup.io/repos/github/DEKHTIARJonathan/keras-datasets/
.. |Python 3| image:: https://pyup.io/repos/github/DEKHTIARJonathan/keras-datasets/python-3-shield.svg
   :target: https://pyup.io/repos/github/DEKHTIARJonathan/keras-datasets/
.. |PyPI Python Versions| image:: https://img.shields.io/pypi/pyversions/keras-datasets.svg
   :target: https://pypi.python.org/pypi/keras-datasets/
.. |GitHub release| image:: https://img.shields.io/github/release/DEKHTIARJonathan/keras-datasets.svg?label=github-release
   :target: https://github.com/DEKHTIARJonathan/keras-datasets/releases
.. |PyPI Release| image:: https://img.shields.io/pypi/v/keras-datasets.svg?label=pypi-release
   :target: https://pypi.python.org/pypi/keras-datasets/
.. |PyPI Wheel| image:: https://img.shields.io/pypi/wheel/keras-datasets.svg
   :target: https://pypi.python.org/pypi/keras-datasets/
.. |PyPI| image:: https://img.shields.io/pypi/status/keras-datasets.svg?label=pypi-status
   :target: https://pypi.python.org/pypi/keras-datasets/
