==================================
Example Block Extension For Sphinx
==================================

This is a modified fork of Serge Domkowski's `examplecode extension <https://bitbucket.org/birkenfeld/sphinx-contrib/src/7f39b7f255e34bfe588f0065a5d9709a7d8e7614/examplecode/?at=default>`_ for Sphinx.

About
=====

This is a simple extension that, when rendered as HTML, will fold multiple
example blocks containing different examples into a single block
which can be toggled from one to another using buttons.

This extension adds the ``example-block`` directive which adds a class to
a container wrapping the code blocks that should be folded. The class allows
the included JavaScript and CSS to render the folded block and buttons.



Quick Example
-------------

Source would look something like this::

    .. example-block::
        .. code-block:: python

            import api

        .. code-block:: ruby

            require 'my-api'


Installation
------------

.. code-block:: console

    $ pip install sphinxcontrib-exampleblock


Enabling The eExtension In Sphinx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add sphinxcontrib.exampleblock to the list of extensions in the conf.py file. For example:

.. code-block:: console

    extensions = ['sphinxcontrib.example']


Contribute
----------

- `Issue Tracker <https://github.com/testthedocs/sphinxcontrib-exampleblock/issues>`_
- `Source Code <https://github.com/svx/sphinxcontrib-exampleblock>`_

Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under MIT.
