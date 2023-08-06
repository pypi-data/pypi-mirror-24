BookIT Client
=============

.. image:: https://travis-ci.org/cmbrad/studentit-bookit-client.svg?branch=master
    :target: https://travis-ci.org/cmbrad/studentit-bookit-client

Python client to interface with the BookIT service.

Installation
------------

.. code-block:: bash

  pip install studentit-bookit-client


or

.. code-block:: bash

  python setup.py install


Usage
-----
Set the following environment variables to valid student or staff credentials:

.. code-block:: bash

  export BOOKIT_USERNAME=yourusername
  export BOOKIT_PASSWORD=yourpassword


Run the command line interface using the following command.

.. code-block:: bash

  python -m bookit.cli [command] [arguments] [options]
