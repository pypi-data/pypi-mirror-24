Data-Chan Python
================

Data-Chan-python allows you to use the
`data-chan <https://github.com/neroreflex/data-chan>`__ comunication
library with Python and `Jupyter <http://jupyter.org/>`__.

Releasing
=========

.. code:: shell

    pip install bump

    # Bump patch/major/minor
    bump setup.py -b
    bump setup.py -m
    bump setup.py -M

    # Create .tar.gz archive
    python setup.py sdist

    # Upload to PyPi the latest file
    twine upload dist/$(ls -tp dist | grep -v /$ | head -1)
