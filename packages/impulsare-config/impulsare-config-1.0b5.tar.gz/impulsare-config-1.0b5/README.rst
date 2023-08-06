impulsare/config
==================================

.. image:: https://travis-ci.org/impulsare/config.svg?branch=master
    :target: https://travis-ci.org/impulsare/config

.. image:: https://scrutinizer-ci.com/g/impulsare/config/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/impulsare/config/


Overview
--------------------------
A config reader, that validates a YAML config file and add default values if required.

Extra values won't be verified, that any component / library defines its own config parameters
in a single configuration file without blocking other to do the same.

See `tests/static/` for examples.


Installation / Usage
--------------------------
To install use pip:

.. code-block:: bash

    $ pip install --upgrade impulsare-config


Example
--------------------------

.. code-block:: python

    from impulsare_config import Reader

    # Main Config File
    config_file = 'config/app.yml'
    # File with validation rules based on JSON Schema
    specs_file = 'config/specs.yml'
    # Default values
    default_file = 'config/default.yml'

    config = Reader().parse(config_file, specs_file, default_file)


Development & Tests
--------------------------

.. code-block:: bash

    $ pip install -r requirements.txt
    $ pip install -r requirements-dev.txt
    $ py.test --cov-report html --cov=impulsare_config tests/
