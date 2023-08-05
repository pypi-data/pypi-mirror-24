=============================
Acoustic Scene Classification
=============================

+------------------+---------------------------------+
| **Development**  | |travis| |coveralls|            |
+------------------+---------------------------------+
| **Last release** | |v| |pyversions| |dependencies| |
+------------------+---------------------------------+
| **PyPI status**  | |format| |status| |l|           |
+------------------+---------------------------------+

.. |travis| image::
  https://travis-ci.org/mattberjon/asc-cnn.svg?branch=master
  :target: https://travis-ci.org/mattberjon/asc-cnn
  :alt: Travis CI builds

.. |coveralls| image::
  https://coveralls.io/repos/github/mattberjon/asc-cnn/badge.svg?branch=master
  :target: https://coveralls.io/github/mattberjon/asc-cnn?branch=master
  :alt: Coverall coverage report

.. |v| image:: 
  https://img.shields.io/pypi/v/asc.svg
  :target: https://pypi.python.org/pypi/asc/
  :alt: PyPI Latest Version

.. |pyversions| image::
  https://img.shields.io/pypi/pyversions/asc.svg
  :target: https://pypi.python.org/pypi/asc/
  :alt: Python versions (PyPI)

.. |dependencies| image::
  https://pyup.io/repos/github/mattberjon/asc-cnn/shield.svg
  :target: https://pyup.io/repos/github/mattberjon/asc-cnn/
  :alt: Updates

.. |format| image::
  https://img.shields.io/pypi/format/asc.svg 
  :target: https://pypi.python.org/pypi/asc
  :alt: Distribution format (PyPI)

.. |status| image::
  https://img.shields.io/pypi/status/asc.svg
  :target: https://pypi.python.org/pypi/asc
  :alt: Project status (PyPI)

.. |l| image::
  https://img.shields.io/pypi/l/asc.svg
  :target: https://pypi.python.org/pypi/asc
  :alt: License (PyPI)


Acoustic Scene Auditory (ASC) using Convolutional Neural Network (CNN) is a
project being part of the Machine Learning Nanodegreen program given by
Udacity. For a description of the proposal, you can refer to its `web
version`_.

Dataset
-------

The dataset can be downloaded on the `Zenodo`_ server.

Features
--------

* TODO

Credits
---------

Project created by `Matthieu Berjon`_ and based on the work of Simone Battaglino,
Ludovick Lepauloux and Nicholas Evans.

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`web version`: http://berjon.net/blog/2017/07/22/acoustic-scene-classficiation-using-cnn/
.. _`Zenodo`: https://zenodo.org/record/400515
.. _`Matthieu Berjon`: http://berjon.net


=======
History
=======

0.2.3 (2017-08-07)
------------------

Added
^^^^^

* Travis config file
* pytest suite
* CLI tests
* `issue #5`_: Package coverage for the development setup
* `issue #6`_: adding of a `clear_zip()` to clean the archive files

Changed
^^^^^^^

* Python 3.3 testing removed

Deprecated
^^^^^^^^^^

* Nothing

Removed
^^^^^^^

* Nothing

Fixed
^^^^^

* `Issue #4`_: invalid functools dependency
* `Issue #7`_: update of docstring `unzip_data()`

Security
^^^^^^^^

* Nothing


0.2.2 (2017-07-31)
------------------

Added
^^^^^

* nothing

Changed
^^^^^^^

* Updated of the ChangeLog (HISTORY.rst)

Deprecated
^^^^^^^^^^

* nothing

Removed
^^^^^^^

* nothing

Fixed
^^^^^

* nothing

Security
^^^^^^^^

* nothing

0.2.1 (2017-07-31)
------------------

Added
^^^^^
* nothing

Changed
^^^^^^^

* nothing

Deprecated
^^^^^^^^^^

* nothing

Removed
^^^^^^^

* nothing

Fixed
^^^^^

* unzip_data() url list issue
* download of temporary files in the right directory  

Security
^^^^^^^^

* nothing

0.2.0 (2017-07-31)
------------------

Added
^^^^^

* Adding of a documentation (with docstrings)
* CLI command to download and unzip data automatically
* creation of a python package
* configuration of Tox
* download() method in data class

Changed
^^^^^^^

* Use of RST instead of markdown for all the documentation
* development packages are now in requirements_dev.txt

Deprecated
^^^^^^^^^^
* nothing

Removed
^^^^^^^

* nothing

Fixed
^^^^^

* source files satisfy PEP8
* bug fix on getdata cli

Security
^^^^^^^^

* Update of all packages to their latest versions

0.1.0 (2017-07-25)
------------------

* First release as a package.


.. _Issue #4: https://github.com/mattberjon/asc-cnn/issues/4
.. _Issue #7: https://github.com/mattberjon/asc-cnn/issues/7
.. _Issue #5: https://github.com/mattberjon/asc-cnn/issues/5
.. _Issue #6: https://github.com/mattberjon/asc-cnn/issues/6


