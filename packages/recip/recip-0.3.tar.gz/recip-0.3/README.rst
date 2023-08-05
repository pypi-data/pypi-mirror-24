=========================
REpository of Complex multIPlication SageMath code
=========================
.. image:: https://travis-ci.org/mstreng/recip.svg?branch=master
    :target: https://travis-ci.org/mstreng/recip

This package is designed as a simple `SageMath <http://www.sagemath.org>`_ package
example to serve as a good practice reference for package developers. We follow
python recommendations and adapt them to the SageMath community. You can find more
advanced documentation on python package creation on
`How To Package Your Python Code <https://packaging.python.org/>`_.

Once the Travis CI set-up has been completed, the documentation for the package can be found at https://mstreng.github.io/recip/doc/html/

Installation
------------

Local install from source
^^^^^^^^^^^^^^^^^^^^^^^^^

Download the source from the git repository::

    $ git clone https://github.com/mstreng/recip.git

Change to the root directory and run::

    $ sage -pip install --upgrade --no-index -v .

For convenience this package contains a [makefile](makefile) with this
and other often used commands. Should you wish too, you can use the
shorthand::

    $ make install

Usage
-----

Once the package is installed, you can use it in Sage with::

    sage: from recip import answer_to_ultimate_question
    sage: answer_to_ultimate_question()
    42

Source code
-----------

All source code is stored in the folder ``recip`` using the same name as the
package. This is not mandatory but highly recommended for clarity. All source folder
must contain a ``__init__.py`` file with needed includes.

Tests
-----

This package is configured for tests written in the documentation
strings, also known as ``doctests``. For examples, see this
[source file](recip/ultimate_question.py). See also
[SageMath's coding conventions and best practices document](http://doc.sagemath.org/html/en/developer/coding_basics.html#writing-testable-examples).
With additional configuration, it would be possible to include unit
tests as well.

Once the package is installed, one can use the SageMath test system
configured in ``setup.py`` to run the tests::

    $ sage setup.py test

This is just calling ``sage -t`` with appropriate flags.

Shorthand::

    $ make test

Documentation
-------------

The documentation of the package can be generated using Sage's
``Sphinx`` installation::

    $ cd docs
    $ sage -sh -c "make html"

Shorthand::

    $ make doc
