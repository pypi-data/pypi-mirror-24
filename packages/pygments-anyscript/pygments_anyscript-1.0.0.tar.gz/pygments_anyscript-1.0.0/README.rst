=========================
Pygments AnyScript plugin
=========================


.. image:: https://img.shields.io/pypi/v/pygments_anyscript.svg
        :target: https://pypi.python.org/pypi/pygments_anyscript

.. image:: https://img.shields.io/travis/AnyBody/pygments-anyscript.svg
        :target: https://travis-ci.org/AnyBody/pygments-anyscript


Pygments lexer and style for the AnyScript language. AnyScript is the
scripting langugage used for the AnyBody Modeling System; a system for
multibody musculoskeletal analysis.


Installation
------------
 * run ``pip install pygments-anyscript``
 * download source and execute ``python setup.py install``

Requirements
------------

 * pygments

Usage
-----

The lexer and style can be used with the Pygments api like any other lexer or style.
::

  $ pygmentize -l AnyScript MyAnyScriptFile.any
  $ pygmentize -l AnyScript -O style=anyscript MyAnyScriptFile.any
  $ pygmentize -l AnyScript -f html -O full,style=anyscript -o  MyAnyScriptFile.html MyAnyScriptFile.any

