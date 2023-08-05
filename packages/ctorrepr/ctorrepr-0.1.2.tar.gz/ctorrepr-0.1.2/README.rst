========
ctorrepr
========


.. image:: https://img.shields.io/pypi/v/ctorrepr.svg
        :target: https://pypi.python.org/pypi/ctorrepr

.. image:: https://img.shields.io/travis/astralblue/ctorrepr.svg
        :target: https://travis-ci.org/astralblue/ctorrepr

.. image:: https://readthedocs.org/projects/ctorrepr/badge/?version=latest
        :target: https://ctorrepr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/astralblue/ctorrepr/shield.svg
     :target: https://pyup.io/repos/github/astralblue/ctorrepr/
     :alt: Updates


A mix-in that provides __repr__() from constructor arguments.


* Free software: MIT license
* Documentation: https://ctorrepr.readthedocs.io.


Usage
-----

To use, simply inherit from `~ctorrepr.CtorRepr` then implement its
`~ctorrepr.CtorRepr._collect_repr_args()` to match your existing
``__init__()`` method::

    >>> from ctorrepr import CtorRepr
    >>> class X(CtorRepr):
    ...     def __init__(self, x1='x1', x2='x2', *poargs, **kwargs):
    ...         super().__init__(*poargs, **kwargs)
    ...         self.x1 = x1
    ...         self.x2 = x2
    ...     def _collect_repr_args(self, poargs, kwargs):
    ...         super()._collect_repr_args(poargs, kwargs)
    ...         poargs[:0] = self.x1, self.x2
    >>> class Y(CtorRepr):
    ...     def __init__(self, *y, **kwargs):
    ...         super().__init__(**kwargs)
    ...         self.y = y          # completely consumes positional args
    ...     def _collect_repr_args(self, poargs, kwargs):
    ...         super()._collect_repr_args(poargs, kwargs)
    ...         poargs[:0] = self.y
    >>> class Z(CtorRepr):
    ...     def __init__(self, *poargs, zk='zk', **kwargs):
    ...         super().__init__(*poargs, **kwargs)
    ...         self.zk = zk
    ...     def _collect_repr_args(self, poargs, kwargs):
    ...         super()._collect_repr_args(poargs, kwargs)
    ...         kwargs.update(zk=self.zk)
    >>> class W(X, Y, Z):
    ...     def __str__(self):
    ...         return repr(self)
    >>> print(' '.join(t.__name__ for t in W.mro()))
    W X Y Z CtorRepr object
    >>> print(W())
    W('x1', 'x2', zk='zk')
    >>> print(W(24))
    W(24, 'x2', zk='zk')
    >>> w = W(24, 25, 'y1', 'y2')
    >>> w.y
    ('y1', 'y2')
    >>> print(w)
    W(24, 25, 'y1', 'y2', zk='zk')
    >>> print(W(zk=100))
    W('x1', 'x2', zk=100)

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

