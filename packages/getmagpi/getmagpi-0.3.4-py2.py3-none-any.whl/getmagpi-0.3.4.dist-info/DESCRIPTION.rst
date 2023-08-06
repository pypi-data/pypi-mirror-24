
getmagpi
========

A simple utility to synchronize free MagPi PDF content. Compatible with
Python 2 & 3.

|PyPI1| |Travis| |PyPI2| |PyPI3| |PyPI4| |Custom|

Usage
-----

.. code:: text

    usage: getmagpi [-h] [-c] [-e] DOWNLOAD_PATH

                    _                               _
          __ _  ___| |_ _ __ ___   __ _  __ _ _ __ (_)
         / _` |/ _ \ __| '_ ` _ \ / _` |/ _` | '_ \| |
        | (_| |  __/ |_| | | | | | (_| | (_| | |_) | |
         \__, |\___|\__|_| |_| |_|\__,_|\__, | .__/|_|
         |___/                          |___/|_|

        Simple utility to sync free MagPi PDFs.

    positional arguments:
      DOWNLOAD_PATH       Destination folder for downloads

    optional arguments:
      -h, --help          show this help message and exit
      -c, --compare       Only display missing files (no downloads)
      -e, --english-only  Ignore non-English files (identified via description)

Demonstration
-------------

|asciicast|

Installation
------------

Manually
~~~~~~~~

1. Clone this repository:

   .. code:: bash

       $ git clone git@github.com:jnario/getmagpi.git

2. Install:

   .. code:: bash

       $ python setup.py install

Via PyPi
~~~~~~~~

   .. code:: bash

       $ pip install getmagpi


Dependencies
~~~~~~~~~~~~
-  requests
-  BeautifulSoup

License
-------

.. code:: text

    MIT License

    Copyright (c) 2017 Jose Nario

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

.. |PyPI1| image:: https://img.shields.io/pypi/v/getmagpi.svg?style=plastic
   :target: https://pypi.python.org/pypi/getmagpi
.. |Travis| image:: https://img.shields.io/travis/jnario/getmagpi.svg?style=plastic
   :target: https://travis-ci.org/jnario/getmagpi
.. |PyPI2| image:: https://img.shields.io/pypi/l/getmagpi.svg?style=plastic
   :target: https://github.com/jnario/getmagpi/blob/master/LICENSE.txt
.. |PyPI3| image:: https://img.shields.io/pypi/status/getmagpi.svg?style=plastic
   :target: https://pypi.python.org/pypi/getmagpi
.. |PyPI4| image:: https://img.shields.io/pypi/pyversions/getmagpi.svg?style=plastic
   :target: https://pypi.python.org/pypi/getmagpi
.. |Custom| image:: https://img.shields.io/badge/Overcooked-Yes-yellow.svg?style=plastic
.. |asciicast| image:: https://asciinema.org/a/132416.png
   :target: https://asciinema.org/a/132416


