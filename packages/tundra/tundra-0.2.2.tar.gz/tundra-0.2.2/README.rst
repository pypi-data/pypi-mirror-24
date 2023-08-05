Tundra
======

.. raw:: html

   <!-- nopypi  -->

|Build Status| |Coverage Status| |Codacy Badge| |PyPI| |PyPI| |PyPI|

Pure Python Graph Algorithms module

Installing
----------

``pip install tundra``

Overview
--------

Structures
~~~~~~~~~~

-  `Graph class <tundra/core/graph.py>`__
-  `Digraph class <tundra/core/digraph.py>`__

Algorithms
~~~~~~~~~~

Search
^^^^^^

-  `Depth-first search <tundra/algorithm/search.py>`__
-  `Breadth-first search <tundra/algorithm/search.py>`__

Spanning tree
^^^^^^^^^^^^^

-  `Kruskal's Algorithm <tundra/algorithm/spanning_tree.py>`__
-  `Prim's Algorithm <tundra/algorithm/spanning_tree.py>`__

Path
^^^^

-  `Dijskra's Algoritm <tundra/algorithm/path.py>`__
-  `Floyd-Warshall Algoritm <tundra/algorithm/path.py>`__
-  `Nearest-neighbors hamiltonian cycle <tundra/algorithm/path.py>`__

Miscellaneous
^^^^^^^^^^^^^

-  `Fringe <tundra/algorithm/misc.py>`__
-  `Greedy coloring <tundra/algorithm/misc.py>`__
-  `Proprety tests (is\_tree, is\_complete,
   ...) <tundra/algorithm/tests.py>`__

Utilities
~~~~~~~~~

-  `DOT language conversion <tundra/util.py>`__
-  `Export Graph to PNG <tundra/util.py>`__

.. |Build Status| image:: https://travis-ci.org/caiopo/tundra.svg?branch=master
   :target: https://travis-ci.org/caiopo/graph
.. |Coverage Status| image:: https://coveralls.io/repos/github/caiopo/tundra/badge.svg?branch=master
   :target: https://coveralls.io/github/caiopo/tundra?branch=master
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/9e2d5134e9244501b10fafe5a2e85556
   :target: https://www.codacy.com/app/caiopo/tundra?utm_source=github.com&utm_medium=referral&utm_content=caiopo/tundra&utm_campaign=Badge_Grade
.. |PyPI| image:: https://img.shields.io/pypi/v/tundra.svg
   :target: https://pypi.python.org/pypi/tundra
.. |PyPI| image:: https://img.shields.io/pypi/pyversions/tundra.svg
   :target: https://pypi.python.org/pypi/tundra
.. |PyPI| image:: https://img.shields.io/pypi/l/tundra.svg
   :target: https://pypi.python.org/pypi/tundra
