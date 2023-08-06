ezchat
======

| **ezchat** stands for easy chat.
| + No frills Python chat app. + Instant setup.

| Run from a notebook or command line.
| In both cases, new independent processes are spawn.

1 - Notebook
~~~~~~~~~~~~

See
`demo\_notebook <http://nbviewer.jupyter.org/urls/gitlab.com/oscar6echo/ezchat/raw/master/demo_ezchat.ipynb>`__.

2 - Command Line
~~~~~~~~~~~~~~~~

-  Launch Hub:

.. code:: python

    from ezchat.servers import hub

    h = hub(port=5001)

-  Launch Client:

.. code:: python

    from ezchat.servers import client

    c = client(port=5002)

-  Kill Hub and Clients:

.. code:: python

    from ezchat.servers import kill

    kill(h)
    kill(c)

.. raw:: html

