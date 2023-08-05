=====
Creh Url Trace
=====

Creh-urltrace is a simple Django app, get the url reference  and insert in a group of url's.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. creh-urltrace can be obtained directly from PyPI, and can be installed with pip:

    pip install creh-urltrace

1. Add "urltrace" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'urltrace',
        ...
    ]

2. Run "python manage.py migrate" to create the log models.

3. Use

    MIDDLEWARE_CLASSES = (
    ...
    'urltrace.middleware.UrlTraceMiddleware',
    ...
    )