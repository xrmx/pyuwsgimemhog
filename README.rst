=============
pyuwsgimemhog
=============


.. image:: https://img.shields.io/pypi/v/pyuwsgimemhog.svg
        :target: https://pypi.python.org/pypi/pyuwsgimemhog

.. image:: https://img.shields.io/travis/xrmx/pyuwsgimemhog.svg
        :target: https://travis-ci.org/xrmx/pyuwsgimemhog

.. image:: https://readthedocs.org/projects/pyuwsgimemhog/badge/?version=latest
        :target: https://pyuwsgimemhog.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Do you want to find out which path of your application run under uWSGI
is leaking memory? you can use *pyuwsgimemhog* to find it out.
*pyuwsgimemhog* parses uWSGI logs to point out which paths contributes to
uWSGI processes RSS memory increase.

Installation
------------

::

    pip install pyuwsgimemhog


Requirements
------------

In order to have the needed information you have to run uWSGI with the 
*memory-report* enabled.


Usage
-----

You need to pass a single uWSGI log file to *pyuwsgimemhog*:

::

    pyuwsgimemhog --logfile /path/to/log
    /api 975
    /another-api 502


That means that */api* contributed to increase the memory usage by 975 MB
and */another-api* by 502 MB.


License
-------

MIT license

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
