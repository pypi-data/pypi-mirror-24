================================================================================
pyexcel-text - Let you focus on data, instead of text formats
================================================================================


.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel.github.io/master/images/patreon.png
   :target: https://www.patreon.com/pyexcel

.. image:: https://api.travis-ci.org/pyexcel/pyexcel-text.svg?branch=master
   :target: http://travis-ci.org/pyexcel/pyexcel-text

.. image:: https://codecov.io/gh/pyexcel/pyexcel-text/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/pyexcel/pyexcel-text

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/pyexcel/Lobby


It is a plugin to `pyexcel <https://github.com/pyexcel/pyexcel>`__ and extends
its capbility to present and write data in text fromats mainly through `tabulate`:

* "plain"
* "simple"
* "grid"
* "pipe"
* "orgtbl"
* "rst"
* "mediawiki"
* "latex"
* "latex_booktabs"
* "json"
* "html"

Since v0.2.7, `json` and `ndjson` input are also supported.


Usage
======

What's new?
--------------

.. code-block:: python

    >>> import pyexcel as pe
    >>> sheet = pe.Sheet()
    >>> sheet.json = '[[1,2],[2,3]]'
    >>> sheet
    pyexcel sheet:
    +---+---+
    | 1 | 2 |
    +---+---+
    | 2 | 3 |
    +---+---+
    >>> highspeedrail = pe.Sheet()
    >>> highspeedrail.json = """
    ... [{"year": 1903, "country": "Germany", "speed": "206.7km/h"},
    ... {"year": 1964, "country": "Japan", "speed": "210km/h"},
    ... {"year": 2008, "country": "China", "speed": "350km/h"}]
    ... """
    >>> highspeedrail.name = 'High Speed Train Speed Break Through (Source: Wikipedia)'
    >>> highspeedrail
    High Speed Train Speed Break Through (Source: Wikipedia):
    +---------+-----------+------+
    | country | speed     | year |
    +---------+-----------+------+
    | Germany | 206.7km/h | 1903 |
    +---------+-----------+------+
    | Japan   | 210km/h   | 1964 |
    +---------+-----------+------+
    | China   | 350km/h   | 2008 |
    +---------+-----------+------+
    >>> henley_on_thames_facts = pe.Sheet()
    >>> henley_on_thames_facts.json = """
    ... {"area": "5.58 square meters",
    ... "population": "11,619",
    ... "civial parish": "Henley-on-Thames",
    ... "latitude": "51.536",
    ... "longitude": "-0.898"
    ... }"""
    >>> henley_on_thames_facts
    pyexcel sheet:
    +--------------------+------------------+----------+-----------+------------+
    | area               | civial parish    | latitude | longitude | population |
    +--------------------+------------------+----------+-----------+------------+
    | 5.58 square meters | Henley-on-Thames | 51.536   | -0.898    | 11,619     |
    +--------------------+------------------+----------+-----------+------------+
    >>> ccs_insight = pe.Sheet()
    >>> ccs_insight.name = "Worldwide Mobile Phone Shipments (Billions), 2017-2021"
    >>> ccs_insight.json = """
    ... {"year": ["2017", "2018", "2019", "2020", "2021"],
    ... "smart phones": [1.53, 1.64, 1.74, 1.82, 1.90],
    ... "feature phones": [0.46, 0.38, 0.30, 0.23, 0.17]}"""
    >>> ccs_insight
    pyexcel sheet:
    +----------------+--------------+------+
    | feature phones | smart phones | year |
    +----------------+--------------+------+
    | 0.46           | 1.53         | 2017 |
    +----------------+--------------+------+
    | 0.38           | 1.64         | 2018 |
    +----------------+--------------+------+
    | 0.3            | 1.74         | 2019 |
    +----------------+--------------+------+
    | 0.23           | 1.82         | 2020 |
    +----------------+--------------+------+
    | 0.17           | 1.9          | 2021 |
    +----------------+--------------+------+

Here is a variant of json:

    >>> highspeedrail2 = pe.Sheet()
    >>> highspeedrail2.ndjson = """
    ... {"year": 1903, "country": "Germany", "speed": "206.7km/h"}
    ... {"year": 1964, "country": "Japan", "speed": "210km/h"}
    ... {"year": 2008, "country": "China", "speed": "350km/h"}
    ... """.strip()
    >>> highspeedrail2.name = 'High Speed Train Speed Break Through (Source: Wikipedia)'
    >>> highspeedrail2
    High Speed Train Speed Break Through (Source: Wikipedia):
    +---------+-----------+------+
    | country | speed     | year |
    +---------+-----------+------+
    | Germany | 206.7km/h | 1903 |
    +---------+-----------+------+
    | Japan   | 210km/h   | 1964 |
    +---------+-----------+------+
    | China   | 350km/h   | 2008 |
    +---------+-----------+------+
    >>> henley_on_thames_facts2 = pe.Sheet()
    >>> henley_on_thames_facts2.ndjson = """
    ... {"area": "5.58 square meters"}
    ... {"population": "11,619"}
    ... {"civial parish": "Henley-on-Thames"}
    ... {"latitude": "51.536"}
    ... {"longitude": "-0.898"}
    ... """.strip()
    >>> henley_on_thames_facts2
    pyexcel sheet:
    +---------------+--------------------+
    | area          | 5.58 square meters |
    +---------------+--------------------+
    | population    | 11,619             |
    +---------------+--------------------+
    | civial parish | Henley-on-Thames   |
    +---------------+--------------------+
    | latitude      | 51.536             |
    +---------------+--------------------+
    | longitude     | -0.898             |
    +---------------+--------------------+
    >>> ccs_insight2 = pe.Sheet()
    >>> ccs_insight2.name = "Worldwide Mobile Phone Shipments (Billions), 2017-2021"
    >>> ccs_insight2.ndjson = """
    ... {"year": ["2017", "2018", "2019", "2020", "2021"]}
    ... {"smart phones": [1.53, 1.64, 1.74, 1.82, 1.90]}
    ... {"feature phones": [0.46, 0.38, 0.30, 0.23, 0.17]}
    ... """.strip()
    >>> ccs_insight2
    pyexcel sheet:
    +----------------+------+------+------+------+------+
    | year           | 2017 | 2018 | 2019 | 2020 | 2021 |
    +----------------+------+------+------+------+------+
    | smart phones   | 1.53 | 1.64 | 1.74 | 1.82 | 1.9  |
    +----------------+------+------+------+------+------+
    | feature phones | 0.46 | 0.38 | 0.3  | 0.23 | 0.17 |
    +----------------+------+------+------+------+------+


Simple
------------

.. code-block:: python

    >>> import pyexcel as pe
    >>> content = [
    ...     ["Column 1", "Column 2", "Column 3"],
    ...     [1, 2, 3],
    ...     [4, 5, 6],
    ...     [7, 8, 9]
    ... ]
    >>> sheet = pe.Sheet(content)
    >>> print(sheet.simple)
    pyexcel sheet:
    --------  --------  --------
    Column 1  Column 2  Column 3
    1         2         3
    4         5         6
    7         8         9
    --------  --------  --------
    >>> sheet.name_columns_by_row(0)
    >>> print(sheet.simple)
    pyexcel sheet:
      Column 1    Column 2    Column 3
    ----------  ----------  ----------
             1           2           3
             4           5           6
             7           8           9


Grid
-------

.. code-block:: python

    >>> print(sheet.grid)
    pyexcel sheet:
    +------------+------------+------------+
    |   Column 1 |   Column 2 |   Column 3 |
    +============+============+============+
    |          1 |          2 |          3 |
    +------------+------------+------------+
    |          4 |          5 |          6 |
    +------------+------------+------------+
    |          7 |          8 |          9 |
    +------------+------------+------------+


Mediawiki
-------------

.. code-block:: python

    >>> multiple_sheets = {
    ...      'Sheet 1':
    ...          [
    ...              [1.0, 2.0, 3.0],
    ...              [4.0, 5.0, 6.0],
    ...              [7.0, 8.0, 9.0]
    ...          ],
    ...      'Sheet 2':
    ...          [
    ...              ['X', 'Y', 'Z'],
    ...              [1.0, 2.0, 3.0],
    ...              [4.0, 5.0, 6.0]
    ...          ],
    ...      'Sheet 3':
    ...          [
    ...              ['O', 'P', 'Q'],
    ...              [3.0, 2.0, 1.0],
    ...              [4.0, 3.0, 2.0]
    ...          ]
    ...  }
    >>> book = pe.Book(multiple_sheets)
    >>> book.save_as("myfile.mediawiki")
    >>> myfile = open("myfile.mediawiki")
    >>> print(myfile.read())
    Sheet 1:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | align="right"| 1 || align="right"| 2 || align="right"| 3
    |-
    | align="right"| 4 || align="right"| 5 || align="right"| 6
    |-
    | align="right"| 7 || align="right"| 8 || align="right"| 9
    |}
    Sheet 2:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | X   || Y   || Z
    |-
    | 1.0 || 2.0 || 3.0
    |-
    | 4.0 || 5.0 || 6.0
    |}
    Sheet 3:
    {| class="wikitable" style="text-align: left;"
    |+ <!-- caption -->
    |-
    | O   || P   || Q
    |-
    | 3.0 || 2.0 || 1.0
    |-
    | 4.0 || 3.0 || 2.0
    |}
    >>> myfile.close()

Html
----------

.. code-block:: python

    >>> book.save_as("myfile.html")
    >>> myfile = open("myfile.html")
    >>> print(myfile.read()) # doctest: +SKIP
    Sheet 1:
    <table>
    <tr><td style="text-align: right;">1</td><td style="text-align: right;">2</td><td style="text-align: right;">3</td></tr>
    <tr><td style="text-align: right;">4</td><td style="text-align: right;">5</td><td style="text-align: right;">6</td></tr>
    <tr><td style="text-align: right;">7</td><td style="text-align: right;">8</td><td style="text-align: right;">9</td></tr>
    </table>
    Sheet 2:
    <table>
    <tr><td>X  </td><td>Y  </td><td>Z  </td></tr>
    <tr><td>1.0</td><td>2.0</td><td>3.0</td></tr>
    <tr><td>4.0</td><td>5.0</td><td>6.0</td></tr>
    </table>
    Sheet 3:
    <table>
    <tr><td>O  </td><td>P  </td><td>Q  </td></tr>
    <tr><td>3.0</td><td>2.0</td><td>1.0</td></tr>
    <tr><td>4.0</td><td>3.0</td><td>2.0</td></tr>
    </table>

Please note tabulate 0.7.7 gives an extra tbody tag around tr tag.

Dependencies
============

* tabulate

Change log
================================================================================

0.2.7 - 30.07.2017
--------------------------------------------------------------------------------

Updated:
********************************************************************************

#. Read specific data structure from pure json format: two dimensional
   array, a dicionary of list or two dimensional list and a list of records.
#. Read newline delimited json. two dimensional arrays, a a dicionary of list
   or two dimensional list and a list of records are supported.

0.2.6 - 19.06.2017
--------------------------------------------------------------------------------

Updated:
********************************************************************************

#. Support pyexcel v0.5.0. Plugin interface updated to Renderer
#. removed deprecated save_as and save_to_memory functions


0.2.5 - 28.10.2016
--------------------------------------------------------------------------------

Updated:
********************************************************************************

#. Support pyexcel v0.4.0

0.2.4 - 28.10.2016
--------------------------------------------------------------------------------

Added:
********************************************************************************

#. support pyexcel v0.3.0


0.2.3 - 14.07.2016
--------------------------------------------------------------------------------

Added:
********************************************************************************

#. json format: serialize date and datetime

Updated:
********************************************************************************

#. if a sheet has row_names, its json output become records(a list of dictionary)
   instead of a dictionary of row name vs the rest of row values.

0.2.2 - 01.06.2016
--------------------------------------------------------------------------------

#. quick bug fix, see `issue #27 <https://github.com/pyexcel/pyexcel-text/issues/27>`_


0.2.1 - 01.06.2016
--------------------------------------------------------------------------------

#. compactibility with pyexcel-io 0.2.0 and pyexcel 0.2.2


0.2.0 - 23.04.2016
--------------------------------------------------------------------------------

It is a complete re-write of the whole extension.

Added
********************************************************************************

#. html support
#. support pyexcel 0.2.0's generator output
#. pypy and pypy3 in test targets
#. support file stream and dot notation, e.g. pyexcel.Sheet.rst will return rst text representation of it.

Updated
********************************************************************************

#. `#8 <https://github.com/pyexcel/pyexcel-text/issues/8>`_, write_header as an option(False) to disable header writing
#. the json output of multiple sheet book will be sorted by its sheet names.
#. No longer, pyexcel-text is pyexcel-io plugin but pyexcel.sources plugin.

0.1.1 - 30.01.2016
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. `#2 <https://github.com/pyexcel/pyexcel-text/issues/2>`_, fix a typo in setup.py


0.1.0 - 17.01.2016
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. support pyexcel 0.2.0


0.0.3 - 12.06.2015
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. `#1 <https://github.com/pyexcel/pyexcel-text/issues/1>`_, align api interface
    with other pyexcel plugins, e.g. save_as, save_book_as

0.0.2 - 30.11.2014
--------------------------------------------------------------------------------

Updated
********************************************************************************

#. support pyexcel 0.0.9


0.0.` - 20.11.2014
--------------------------------------------------------------------------------

Initial release






