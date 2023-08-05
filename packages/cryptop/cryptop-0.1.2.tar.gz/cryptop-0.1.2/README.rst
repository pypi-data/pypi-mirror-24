cryptop
=======
cryptop is a lightweight command line based cryptocurrency portfolio.
Built on python and ncurses with simplicity in mind, cryptop updates in realtime.

.. image:: img\cryptop.png

Installation
------------

The easiest way to install cryptop is through pip

.. code:: bash

    sudo pip install cryptop

cryptop can be installed manually, download the repo and run

.. code:: bash

    sudo python setup.py install

pip and setup.py can be run with a --user flag if you would prefer
not to sudo. Please note cryptop requires Python 3 to run, and is 
only tested in Python 3.6 so far.

Usage
-----

Start from a terminal.

.. code:: bash

    cryptop

Follow the on screen instructions to add/remove cryptocurrencies from your portfolio.

Customisation
-------------

Cryptop creates two config files in a .cryptop folder in your home directory.

.crypto/config.ini contains currency and theme configuration (text and backgrounds colors)

.. image:: img\fall.png

.. image:: img\aesth.png

.cryptop/wallet.json contains the coins and amounts you hold, you shouldn't need to edit it manually

Credits
-------

Uses the `cryptocompare.com API
<http://www.cryptocompare.com/>`_.

Support
-------

Support cryptop's development here.

BTC: 15wNW29q7XAEbC8yus49CWvt91JkhcdkoW

Disclaimer
----------

I am not liable for the accuracy of this program’s output nor actions
performed based upon it.
