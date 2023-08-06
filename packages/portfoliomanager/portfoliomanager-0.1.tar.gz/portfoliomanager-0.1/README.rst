Portfolio Manager
===================

Tracks N number of investments equally weighted against IVV etf.

Installation
------------

To install Portfolio Manager from PyPI:

.. code-block:: bash

  $ pip install portfoliomanager 

From git repo:

.. code-block:: bash

  $ git clone https://github.com/JamesWhiteleyIV/Portfolio-Manager.git
  $ cd Portfolio-Manager 
  $ python setup.py install


Documentation
-------------

.. code:: python
  import datetime as dt
  import portfoliomanager as pm

  #initialize start and end dates of portfolio 1/1/2017 - current date
  start = dt.date(2017, 1, 1)
  end = dt.date.today()

  #create list of investments and name of portfolio
  tickers = ['OSUR', 'COHR', 'ENTG', 'HSKA', 'FIVE', 'MDSO', 'LOPE', 'MBUU', 'OLLI', 'TRU']
  name = "Stock Portfolio A"

  #initialize Portfolio object
  port = pm.Portfolio(tickers, start, end, name)

  #plot portfolio vs. IVV (S&P 500 etf) as a PDF in current directory
  port.pltPort()


Authors
-------

**James Whiteley IV** 

