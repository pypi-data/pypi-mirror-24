.. include:: ../../README.rst

Here's an example of using Eliot, and the output rendered by the third-party `eliot-tree`_ utility:

.. literalinclude:: ../../examples/linkcheck.py

.. code-block:: shell

   $ python examples/linkcheck.py | eliot-tree
   4c42a789-76f5-4f0b-b154-3dd0e3041445
   +-- check_links@1/started
       `-- urls: [u'http://google.com', u'http://nosuchurl']
       +-- download@2,1/started
           `-- url: http://google.com
           +-- download@2,2/succeeded
       +-- download@3,1/started
           `-- url: http://nosuchurl
           +-- download@3,2/failed
               |-- exception: requests.exceptions.ConnectionError
               |-- reason: ('Connection aborted.', gaierror(-2, 'Name or service not known'))
       +-- check_links@4/failed
           |-- exception: exceptions.ValueError
           |-- reason: ('Connection aborted.', gaierror(-2, 'Name or service not known'))

.. _eliot-tree: https://warehouse.python.org/project/eliot-tree/

Contents:

.. toctree::
   introduction
   news
   generating/index
   outputting/index
   reading/index
   development
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

