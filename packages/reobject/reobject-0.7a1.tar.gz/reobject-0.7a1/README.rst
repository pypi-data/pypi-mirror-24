reobject
========

|Build Status| |PyPI version| |PyPI| |codecov|

*reobject* is an ORM layer for your objects. Simple, add a mixin to your
Python class and assume the ability to track and query objects at
runtime!

**Warning:** This is an alpha software, and the API is subject to
change.

Installation
~~~~~~~~~~~~

.. code:: sh

    pip install reobject

Example usage
~~~~~~~~~~~~~

.. code:: py3

    from reobject.models import Model, Field

    class Book(Model):
        title = Field()
        authors = Field()
        price = Field()

    >>> # Create a bunch of objects:
    >>> Book(title='The C Programming Language', authors=['Kernighan', 'Ritchie'], price=52)
    >>> Book(title='The Go Programming Language', authors=['Donovan', 'Kernighan'], price=30)

    >>> # Get all books
    >>> Book.objects.all()
    [<Book: 140707840041088>, <Book: 140707840125584>]

    >>> # Get the titles of all books which cost less than 50 USD:
    >>> Book.objects.filter(price__lt=50).values('title')
    [{'title': 'The Go Programming Language'}, {'title': 'The C Programming Language'}]

    >>> # Get titles of all books co-authored by Brian Kernighan:
    >>> Book.objects.filter(authors__contains='Kernighan').values_list('title', flat=True)
    ['The Go Programming Language', 'The C Programming Language']

Features
~~~~~~~~

-  Elegant data-model syntax inspired by Django ORM.
-  Plug and play: works without refactoring your existing codebase.
-  Chainable operations on querysets.
-  Transactions.
-  [TBA] Attribute indexes for fast lookups.
-  [TBA] Many-to-one class relationships.

Crunching Design Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~

+-------------+--------------------------------------------+---------+------------+
| Pattern     | Description                                | Pure    | reobject   |
|             |                                            | Python  |            |
+=============+============================================+=========+============+
| Flyweight   | Reuse existing instances of objects with   | `Link < | `Link <exa |
|             | identical state                            | https:/ | mples/flyw |
|             |                                            | /github | eight.py>` |
|             |                                            | .com/fa | __         |
|             |                                            | if/pyth |            |
|             |                                            | on-patt |            |
|             |                                            | erns/bl |            |
|             |                                            | ob/mast |            |
|             |                                            | er/stru |            |
|             |                                            | ctural/ |            |
|             |                                            | flyweig |            |
|             |                                            | ht.py>` |            |
|             |                                            | __      |            |
+-------------+--------------------------------------------+---------+------------+
| Memento     | Transactional rollback of an object to a   | `Link < | `Link <tes |
|             | previous state in case of an exception     | https:/ | ts/unit/te |
|             |                                            | /github | st_transac |
|             |                                            | .com/fa | tion.py>`_ |
|             |                                            | if/pyth | _          |
|             |                                            | on-patt |            |
|             |                                            | erns/bl |            |
|             |                                            | ob/mast |            |
|             |                                            | er/beha |            |
|             |                                            | vioral/ |            |
|             |                                            | memento |            |
|             |                                            | .py>`__ |            |
+-------------+--------------------------------------------+---------+------------+
| Prototype   | Create clones of a prototype without       | `Link < | `Link <exa |
|             | instantiation                              | https:/ | mples/prot |
|             |                                            | /github | otype.py>` |
|             |                                            | .com/fa | __         |
|             |                                            | if/pyth |            |
|             |                                            | on-patt |            |
|             |                                            | erns/bl |            |
|             |                                            | ob/mast |            |
|             |                                            | er/crea |            |
|             |                                            | tional/ |            |
|             |                                            | prototy |            |
|             |                                            | pe.py>` |            |
|             |                                            | __      |            |
+-------------+--------------------------------------------+---------+------------+
| Singleton   | Restrict a class to provide only a single  | `Link < | `Link <exa |
|             | instance                                   | http:// | mples/sing |
|             |                                            | python- | leton.py>` |
|             |                                            | 3-patte | __         |
|             |                                            | rns-idi |            |
|             |                                            | oms-tes |            |
|             |                                            | t.readt |            |
|             |                                            | hedocs. |            |
|             |                                            | io/en/l |            |
|             |                                            | atest/S |            |
|             |                                            | ingleto |            |
|             |                                            | n.html> |            |
|             |                                            | `__     |            |
+-------------+--------------------------------------------+---------+------------+
| Facade      | Encapsulate a complex subsystem within a   | `Link < | `Link <exa |
|             | single interface object                    | https:/ | mples/faca |
|             |                                            | /github | de.py>`__  |
|             |                                            | .com/fa |            |
|             |                                            | if/pyth |            |
|             |                                            | on-patt |            |
|             |                                            | erns/bl |            |
|             |                                            | ob/mast |            |
|             |                                            | er/stru |            |
|             |                                            | ctural/ |            |
|             |                                            | facade. |            |
|             |                                            | py>`__  |            |
+-------------+--------------------------------------------+---------+------------+
| Flux        | Event-driven state management inspired by  | `Link < | `Link <exa |
|             | Facebook Flux                              | https:/ | mples/flux |
|             |                                            | /github | .py>`__    |
|             |                                            | .com/on |            |
|             |                                            | yb/pyth |            |
|             |                                            | on-flux |            |
|             |                                            | /blob/m |            |
|             |                                            | aster/f |            |
|             |                                            | lux/sto |            |
|             |                                            | re.py>` |            |
|             |                                            | __      |            |
+-------------+--------------------------------------------+---------+------------+

Note: The idea is not to provide accurate implementations of various
patterns, but to demonstrate what reobject is capable of. Pull requests
are most welcome.

Why?
~~~~

-  You are refactoring a codebase with years of accumulated code-vomit.
-  Your code looks like a Christmas tree.
-  You want to implement design patterns without the boilerplate.
-  You care about maintainability, and cleanliness.

Contributing
~~~~~~~~~~~~

Want to help? Please review the `contributing
guidelines <CONTRIBUTING.md>`__, and take a look at some `good first
bugs <https://github.com/onyb/reobject/issues?q=is%3Aissue+is%3Aopen+label%3Abitesize>`__!

.. |Build Status| image:: https://travis-ci.org/onyb/reobject.svg?branch=master
   :target: https://travis-ci.org/onyb/reobject
.. |PyPI version| image:: https://badge.fury.io/py/reobject.svg
   :target: https://badge.fury.io/py/reobject
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/reobject.svg
   :target: https://pypi.python.org/pypi/reobject
.. |codecov| image:: https://codecov.io/gh/onyb/reobject/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/onyb/reobject
