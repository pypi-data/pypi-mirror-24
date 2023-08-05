.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.


Report Bugs and Submit Feedback
~~~~~~~~~~~

Bugs and feedback can be given at https://github.com/anybody/pygments_anyscript/issues.


Get Started!
------------

Ready to contribute? Here's how to set up `pygments_anyscript` for local development.

1. Fork the `pygments-anyscript` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pygments-anyscript.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv pygments-anyscript
    $ cd pygments-anyscript/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests::

    $ python setup.py install
    $ pytest --flake8

   To get pytest and pytest-flake, just pip install them.

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, 3.5, 3.6. Check
   https://travis-ci.org/AnyBody/pygments-anyscript/pull_requests
   and make sure that the tests pass for all supported Python versions.
