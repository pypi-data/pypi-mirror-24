.. image:: https://travis-ci.org/jgonggrijp/pip-review.svg?branch=master
    :alt: Build status
    :target: https://secure.travis-ci.org/jgonggrijp/pip-review

pip-review
==========

``pip-review`` is a convenience wrapper around ``pip``. It can list available updates by deferring to ``pip list --outdated``. It can also automatically or interactively install available updates for you by deferring to ``pip install``. 

Example, report-only:

.. code:: console

    $ pip-review
    requests==0.13.4 is available (you have 0.13.2)
    redis==2.4.13 is available (you have 2.4.9)
    rq==0.3.2 is available (you have 0.3.0)

Example, actually install everything:

.. code:: console

    $ pip-review --auto
    ... <pip install output>

Example, run interactively, ask to upgrade for each package:

.. code:: console

    $ pip-review --interactive
    requests==0.14.0 is available (you have 0.13.2)
    Upgrade now? [Y]es, [N]o, [A]ll, [Q]uit y
    ...
    redis==2.6.2 is available (you have 2.4.9)
    Upgrade now? [Y]es, [N]o, [A]ll, [Q]uit n
    rq==0.3.2 is available (you have 0.3.0)
    Upgrade now? [Y]es, [N]o, [A]ll, [Q]uit y
    ...

Run ``pip-review -h`` for a complete overview of the options.

Since version 0.5, you can also invoke pip-review as ``python -m pip_review``.

Before version 1.0, ``pip-review`` had its own logic for finding package updates instead of relying on ``pip list --outdated``.


Installation
============

To install, simply use pip:

.. code:: console

    $ pip install pip-review

Decide for yourself whether you want to install the tool system-wide, or
inside a virtual env.  Both are supported.


Testing
=======

To test with your active Python version:

.. code:: console

    $ ./run-tests.sh

To test under all (supported) Python versions:

.. code:: console

    $ tox

The tests run quite slow, since they actually interact with PyPI, which
involves downloading packages, etc.  So please be patient.


Origins
=======

``pip-review`` was originally part of pip-tools_ but 
has been discontinued_ as such. See `Pin Your Packages`_ by Vincent
Driessen for the original introduction. Since there are still use cases, the
tool now lives on as a separate package.


.. _pip-tools: https://github.com/nvie/pip-tools/
.. _discontinued: https://github.com/nvie/pip-tools/issues/185
.. _Pin Your Packages: http://nvie.com/posts/pin-your-packages/
.. _cram: https://bitheap.org/cram/
