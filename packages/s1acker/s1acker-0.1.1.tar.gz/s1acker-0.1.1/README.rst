s1acker
=======

Search and download images from stage1st.

example
-------

.. code:: bash

    s1acker "喵片" -o "temp"

Usage
-----

.. code:: bash

    s1acker [-h] [-n UNAME] [-d] [-o DIR] [-v | -q] [--version]
            SRCHTXT [SRCHTXT ...]

See ``s1acker --help`` for details.

Requirements
------------

``s1acker`` only support ``python3``, and is only tested under
``python3.6``.

Installation
------------

.. code:: bash

    pip install s1acker

Note that ``s1acker`` is not available on pypi yet.

Or, for development,

.. code:: bash

    git clone https://github.com/quinoa42/s1acker.git
    cd s1acker
    pip install -e .
