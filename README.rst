========
xafsflow
========


.. image:: https://img.shields.io/pypi/v/xafsflow.svg
        :target: https://pypi.python.org/pypi/xafsflow

.. image:: https://img.shields.io/travis/wpk-nist-gov/xafsflow.svg
        :target: https://travis-ci.com/wpk-nist-gov/xafsflow

.. image:: https://readthedocs.org/projects/xafsflow/badge/?version=latest
        :target: https://xafsflow.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Utilities to analyze XAFS data


* Free software: NIST license
* Documentation: https://xafsflow.readthedocs.io.

Installation
------------

This project is not yet available via conda or on pypi.  The recommended route is to install most dependencies via conda, then pip install directly from github.  For this, do the following:

If you'd like to create an isolated environment:

.. code-block:: console

    $ conda create -n {env-name} python=3.8

Activate the environment you'd like to install to with:

.. code-block:: console

   $ conda activate {env-name}

Install required dependencies with:

.. code-block:: console

   $ conda install -n {env-name} setuptools pandas xarray bottleneck scikit-learn matplotlib seaborn
   $ conda install -n {env-name} -c wpk-nist cmomy

Optional, but recommended

.. code-block:: console

   # to install jupyter
   $ conda install -n {env-name} jupyter

   # Or
   # to add just a kernel for this enviromenment
   $ conda install -n {env-name} ipykernel

Finally, install `xafsflow` in the active environment do:

.. code-block:: console

   $ pip install git+https://github.com/wpk-nist-gov/xafsflow.git@develop



Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `wpk-nist-gov/cookiecutter-pypackage`_ Project template forked from `audreyr/cookiecutter-pypackage`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`wpk-nist-gov/cookiecutter-pypackage`: https://github.com/wpk-nist-gov/cookiecutter-pypackage
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
