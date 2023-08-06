PyTimeNSW
=========

PyTimeNSW is a fork of `PyTime <https://github.com/shnode/PyTime>`__
with additional days added for NSW public holidays.

Installation (not yet complete)
-------------------------------

.. code:: python

    pip install pytimeNSW

Basic Usage
-----------

.. code:: python

    >>>from pytimeNSW import pytimeNSW
    >>>
    >>>queen = pytimeNSW.queen()           # Queen's Birthday
    >>>print(queen)
    datetime.date(2017, 6, 12)
    >>>
    >>>pytimeNSW.public(easter)             # Easter Public Holidays
    [datetime.date(2017, 3, 30),
     datetime.date(2017, 3, 31),
     datetime.date(2017, 4, 1),
     datetime.date(2017, 4, 2)]
    >>>
    >>> labour = pytimeNSW.labour(2019)      # 2019 Labour Day
    >>>print(labour)
    datetime.date(2019, 10, 7)

Other public holidays

.. code:: python

    >>>pytimeNSW.boxing()                      # Boxing Day
    datetime.date(2015, 12, 26)
    >>>
    >>>pytimekr.anzac()                    # Anzac Day
    datetime.date(2017, 4, 25)
    >>>
    >>>pytimekr.australia()                # Australia Day
    datetime.date(2017, 1, 26)

License
-------

MIT
