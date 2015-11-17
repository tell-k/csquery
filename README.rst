A simple query builder for Amazon Cloudsearch Structured query parser.

|travis| |coveralls| |downloads| |version| |license| |requires|

.. contents::
   :local:
   :depth: 1

Features
========
* Provide a simple query builder for Amazon Cloudsearch Structured query parser.
* Please refer to the following link regarding **Structured Search Syntax** .

  * http://docs.aws.amazon.com/cloudsearch/latest/developerguide/search-api.html

Caution
========
* At the moment, this library is compatible only to **Structured Search Syntax** .
* It does not have any plans corresponding to the other query parser(lucene, dismax, simple).
* If you want the lucene query builder, it's a good idea is to use the following library.

  * https://pypi.python.org/pypi/lucene-querybuilder

* This library does not handle to generate queries that are not related to **Structured Search Syntax**. Ex) size, facets ...

Set up
======

Make environment with pip::

  $ pip install csquery

Usage
=====

and
---

Syntax: (and boost=N EXPRESSION EXPRESSION ... EXPRESSIONn)

.. code-block:: python

  from csquery.structured import and_, field

  q = and_(title='star', actors='Harrison Ford', year=('', 2000))
  q() #=> (and title:'star' actors:'Harrison Ford' year:{,2000])

  # with option
  q = and_({'title': 'star'}, {'title': 'star2'}, boost=2)
  q() #=> (and boost=2 title:'star' title:'star2')

  # another writing
  and_({'title': 'star'}, {'actors': 'Harrison Ford'}, {'year': ('', 2000)})
  and_(field('star', 'title'), field('Harrison Ford', 'actors'), field(('', 2000), 'year'))

or
---

Syntax: (or boost=N EXPRESSION1 EXPRESSION2 ... EXPRESSIONn)


.. code-block:: python

  from csquery.structured import or_, field

  q = or_(title='star', actors='Harrison Ford', year=('', 2000))
  q() #=> (or title:'star' actors:'Harrison Ford' year:{,2000])

  # with option
  q = or_({'title': 'star'}, {'title': 'star2'}, boost=2)
  q() #=> (or boost=2 title:'star' title:'star2')


not
----

Syntax: (not boost=N EXPRESSION)

.. code-block:: python

  from csquery.structured import not_, and_

  q = not_(and_(actors='Harrison Ford', year=('', 2010)))
  q() #=> (not (and actors:'Harrison Ford' year:{,2010]))

  # with option
  q = not_(and_(actors='Harrison Ford', year=('', 2010)), boost=2)
  q() #=> (not boost=2 (and actors:'Harrison Ford' year:{,2010]))

near
-----

Syntax: (near field=FIELD distance=N boost=N 'STRING')

.. code-block:: python

  from csquery.structured import near

  q = near('teenage vampire', boost=2, field='plot', distance=2)
  q() #=> (near field=plot distance=2 boost=2 'teenage vampire')

phrase
-------

Syntax: (phrase field=FIELD boost=N 'STRING')

.. code-block:: python

  from csquery.structured import phrase

  q = phrase('star', boost=2, field='title')
  q() #=> (phrase field=title boost=2 'star')

prefix
-------

Syntax: (prefix field=FIELD boost=N 'STRING')

.. code-block:: python

  from csquery.structured import prefix

  q = prefix('star', boost=2, field='title')
  q() #=> (prefix field=title boost=2 'star')

range
------

Syntax: (range field=FIELD boost=N RANGE)

.. code-block:: python

  from csquery.structured import range_

  q = range_((1990, 2000))
  q() #=> (range [1990,2000])
  q = range_((None, 2000))
  q() #=> (range {,2000])
  q = range_((1990,))
  q() #=> (range [1990,})

  # with opition
  q = range_((1990, 2000), field='date', boost=2)
  q() #=> (range field=date boost=2 [1990,2000])

  # another writing
  q = range_('[1990,2000]')
  q() #=> (range [1990,2000])

  q = range_(('', 2000))
  q() #=> (range {,2000])
  q = range_('{,2000]')
  q() #=> (range {,2000])

  q = range_((1990, None))
  q() #=> (range [1990,})
  q = range_((1990, ''))
  q() #=> (range [1990,})
  q = range_('[1990,}')
  q() #=> (range [1990,})

term
--------

Syntax: (term field=FIELD boost=N 'STRING'\|VALUE)

.. code-block:: python

  from csquery.structured import term

  q = term(2000, field='year', boost=2)
  q() #=> (term field=year boost=2 2000)

  q = term('star', field='title', boost=2)
  q() #=> (term field=title boost=2 'star')

Complex query sample
----------------------

.. code-block:: python

  from csquery.structured import and_, or_, not_, term

  q = and_(
      not_('test', field='genres'),
      or_(
          term('star', field='title', boost=2),
          term('star', field='plot')
      )
  )
  q() #=> (and (not field=genres 'test') (or (term field=title boost=2 'star') (term field=plot 'star')))

Using with boto
-----------------

http://boto.readthedocs.org/en/latest/ref/cloudsearch2.html

.. code-block:: python

  from csquery.structured import and_
  from boto.cloudsearch2.layer2 import Layer2

  conn = Layer2(
      region='ap-northeast-1',
      aws_access_key_id=[AWS ACCESSS KEY ID],
      aws_secret_access_key=[AWS SECRET KEY],
  )
  domain = conn.lookup('search_domain_name')
  search_service = domain.get_search_service()

  q = and_(title='star', actors='Harrison Ford', year=('', 2000))
  result = search_service.search(q=q(), parser='structured')

Python Support
==============
* Python 2.7, 3,3, 3.4 or later.

License
=======
* Source code of this library Licensed under the MIT License.

See the LICENSE.rst file for specific terms.

Authors
=======

* tell-k <ffk2005 at gmail.com>

Contributors
==============

Thanks.

* @podhmo
* @furi

History
=======

0.1.2(Nov 18, 2015)
---------------------

* Fixed escape bug. `#2 <https://github.com/tell-k/csquery/pull/2>`_.

0.1.1(Nov 6, 2015)
---------------------

* Fixed bug. `#1 <https://github.com/tell-k/csquery/pull/1>`_.

0.1.0(Jun 8, 2015)
---------------------
* First release

.. |travis| image:: https://travis-ci.org/tell-k/csquery.svg?branch=master
    :target: https://travis-ci.org/tell-k/csquery

.. |coveralls| image:: https://coveralls.io/repos/tell-k/csquery/badge.png
    :target: https://coveralls.io/r/tell-k/csquery
    :alt: coveralls.io

.. |requires| image:: https://requires.io/github/tell-k/csquery/requirements.svg?branch=master
    :target: https://requires.io/github/tell-k/csquery/requirements/?branch=master
    :alt: requirements status

.. |downloads| image:: https://img.shields.io/pypi/dm/csquery.svg
    :target: http://pypi.python.org/pypi/csquery/
    :alt: downloads

.. |version| image:: https://img.shields.io/pypi/v/csquery.svg
    :target: http://pypi.python.org/pypi/csquery/
    :alt: latest version

.. |license| image:: https://img.shields.io/pypi/l/csquery.svg
    :target: http://pypi.python.org/pypi/csquery/
    :alt: license
