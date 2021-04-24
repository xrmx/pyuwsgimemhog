=============
pyuwsgimemhog
=============


.. image:: https://img.shields.io/pypi/v/pyuwsgimemhog.svg
        :target: https://pypi.python.org/pypi/pyuwsgimemhog

.. image:: https://github.com/xrmx/pyuwsgimemhog/actions/workflows/ci.yml/badge.svg
        :target: https://github.com/xrmx/pyuwsgimemhog/actions/workflows/ci.yml

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


Use from the command line
-------------------------

You need to pass a single uWSGI log file to *pyuwsgimemhog*:

::

    pyuwsgimemhog --logfile /path/to/log
    /api 975 200 4.9
    /another-api 502 2 251


That means that */api* contributed to increase the memory usage by 975 MB,
it has been accounted 200 times and it contributed 4.9 MB per call.
*/another-api* contributed 502 MB in two occurences so 251MB per call.


Use as a library
----------------

In addition to using *pyuwsgimemhog* as a command line utility, it can also be
used as a library. This allows passing a custom path normalization function
into the log analyzer in order to group requests based on that URL path.

A trivial example of using the Django URL resolver in order to normalize URLs
would be the following:

.. code-block:: python

    from django.urls import resolve, Resolver404
    from pyuwsgimemhog.pyuwsgimemhog import normalize_path, uwsgimemhog
    from urllib.parse import urlparse

    def normalize(url):
        try:
            return resolve(urlparse(url).path).view_name
        except Resolver404:
            # This view was not handled by Django so fall back to the default
            # normalization. Use normalize_path_with_nums to normalize numbers
            # in path to 0.
            return normalize_path(url)

    with open(logfile, 'r') as f:
        for view, memory, count in uwsgimemhog(
                f, threshold * 1_000_000, normalize):
            print('{} {} {} {:.1f}'.format(
                view, memory // 1_000_000, count, memory / count / 1_000_000
            ))


License
-------

MIT license

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
