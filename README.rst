=============
pyuwsgimemhog
=============


.. image:: https://img.shields.io/pypi/v/pyuwsgimemhog.svg
        :target: https://pypi.python.org/pypi/pyuwsgimemhog

.. image:: https://img.shields.io/travis/xrmx/pyuwsgimemhog.svg
        :target: https://travis-ci.org/xrmx/pyuwsgimemhog


Do you want to find out which path of your application running under uWSGI 
is leaking memory?

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

Please note that it's possible to have meaningful results only if you
are using one thread per process.


Usage
-----

You need to pass a single uWSGI log file to *pyuwsgimemhog*:

::

    pyuwsgimemhog --logfile /path/to/log
    /api 975 200 4.9
    /another-api 502 2 251


That means that */api* contributed to increase the memory usage by 975 MB,
it has been accounted 200 times and it contributed 4.9 MB per call.
*/another-api* contributed 502 MB in two occurences so 251MB per call.


License
-------

MIT license

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
