Installation
------------

To install ``the_silo``, type:

.. code-block:: bash

    $ pip install the_silo

Open Nuke's ``init.py`` file and add:

.. code-block:: python

    nuke.pluginAddPath('/path/to/your/local/python/site-packages')

Open Nuke's ``menu.py`` file and add:

.. code-block:: python

    import the_silo
