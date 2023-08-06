===========
PylpChanged
===========


Information
===========

| **pylpchanged** is a plugin for `Pylp`_ that filter unchanged files.
|
| **Note**: this plugin cannot filter unchanged files with a name transformed by another
  plugin further into the stream (``pylprename`` for example).


Installation
============

Install **pylpchanged** with ``pip``::

    pip install pylpchanged

If you don't have Python ``Scripts`` folder in your PATH, you can run also::

    python -m pip install pylpchanged


Usage
=====

The usual use of **pylpchanged** is as follows:

.. code:: python

    import pylp
    from pylpchanged import pylpchanged

    pylp.task('default', lambda:
        pylp.src('lib/*.py')
          .pipe(changed())
        # .pipe(another_plugin())
          .pipe(pylp.dest('build'))
    )

| Without parameters, **pylpchanged** will wait for the destination stream (i.e. ``pylp.dest``)
  to compare the last result with the source files.
|
| For a faster execution, you can pass directly the destination path like this:

.. code:: python

    import pylp
    from pylpchanged import pylpchanged

    pylp.task('default', lambda:
        pylp.src('lib/*.py')
          .pipe(changed('build'))
        # .pipe(another_plugin())
          .pipe(pylp.dest('build'))
    )


.. _Pylp: https://github.com/pylp/pylp

