WSGI Monitor 3
===============

Monitor that will reload wsgi process after changes to source code. Useful for
development environments using apache.

This code is originally from the mod_wsgi_ wiki page on SourceCodeReloading_,
and was written by Graham Dumpleton. It had been modified to support Python 2
and 3.

Installation
-------------

::

 pip install wsgi-monitor3


Usage
------

For Django projects, put the following in your ``wsgi.py``  file::

 from wsgi_monitor3 import monitor

 monitor.start(interval=1.0)


.. _`mod_wsgi`: http://www.modwsgi.org
.. _`SourceCodeReloading`: http://code.google.com/p/modwsgi/wiki/ReloadingSourceCode
