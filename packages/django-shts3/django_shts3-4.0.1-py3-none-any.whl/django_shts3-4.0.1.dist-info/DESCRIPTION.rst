Django shortcuts
================

You spend too much time typing ``python3 manage.py``.

.. image:: https://badge.fury.io/py/django-shts3.svg
    :target: https://badge.fury.io/py/django-shts3

Usage
-----

Django shortcuts installs ``django``, ``dj``, ``d`` binaries that proxies
Django's ``manage.py``  scripts.

::

    $ django <command or shortcut>

    $ cd any/project/subdirectory
    $ d <command or shortcut>


Default shortcuts
---------


+-------------+---------+-----------------+
|             | Aliases | Command         |
+=============+=========+=================+
| Most common | c       | collectstatic   |
+             +---------+-----------------+
|             | r       | runserver       |
+             +---------+-----------------+
|             | s / sh  | shell           |
+             +---------+-----------------+
|             | t       | test            |
+-------------+---------+-----------------+
| Migrations  | m       | migrate         |
+             +---------+-----------------+
|             | mkm     | makemigrations  |
+-------------+---------+-----------------+
| Other       | csu     | createsuperuser |
+             +---------+-----------------+
|             | cpw     | changepassword  |
+             +---------+-----------------+
|             | sa      | startapp        |
+             +---------+-----------------+
|             | sp      | startproject    |
+-------------+---------+-----------------+

Configuration file
---------

If in home dirctory exists file .django_shts3, commands are loaded from it. They overwrite default commands. File format is 
::

    alias @@@ command 

Example:

I have docker container with django and I should bind to 0.0.0.0:8000 on runserver command, so I have:

::

    $ cat ~/.django_shts3
    r @@@ runserver 0.0.0.0:8000

That allows me to start Django server like:

::

    $ d r

Installation
------------

::

    $ pip3 install django-shts3


