=======
KdQuery
=======

KdQuery is a package that defines one possible implementation of kd-trees using python lists to avoid recursion and most importantly it defines a general method to find the nearest node for any kd-tree implementation.

Getting Started
===============

Prerequisites
-------------

* Python version 3.6 installed locally
* Pip installed locally

Installing
----------

The package can easily be installed via pip::

  pip install kdquery

Usage
=====

The Tree class with the default settings
----------------------------------------

.. code-block:: python

    from kdquery import Tree

    # Create a kd-tree (k = 2 and capacity = 10000 by default)
    tree = Tree()

    # Insert points with some attached data (or not)
    tree.insert((9, 1), {'description': 'point in the plane', 'label': 6})
    tree.insert((1, -8))
    tree.insert((-3, 3), data=None)
    tree.insert((0.2, 3.89), ["blue", "yellow", "python"])

    # Recover the data attached to (0, 3)
    node_id = tree.insert((0, 3), 'Important data')
    node = tree.get_node(node_id)
    print(node.data)  # 'Important data'

    # Find the node in the tree that is nearest to a given point
    query = (7.2, 1.2)
    node_id, dist = tree.find_nearest_point(query)
    print(dist)  # 1.8110770276274832

The Tree class with the optional arguments
------------------------------------------

.. code-block:: python

    from kdquery import Tree

    x_limits = [-100, 100]
    y_limits = [-10000, 250]
    z_limits = [-1500, 10]
    region = [x_limits, y_limits, z_limits]

    capacity = 3000000

    # 3d-tree with capacity of 3000000 nodes
    tree = Tree(3, capacity, region)

The nearest_point method
------------------------

Let's say that you work with some positions over the superface of the Earth in your application and that to store this data you implement a kd-tree where each node is represented as an element of an array with these specifications:

.. code-block:: python

    import numpy as np

    node_dtype = np.dtype([
       ('longitude', 'float64'),
       ('latitude', 'float64'),
       ('limit_left', 'float64'),
       ('limit_right', 'float64'),
       ('limit_bottom', 'float64'),
       ('limit_top', 'float64'),
       ('dimension', 'float64'),
       ('left', 'int32'),
       ('right', 'int32')
    ])

If given a point over the surface of the Earth you need to find the nearest position of your database, you can use the nearest_point method from this package. You only need to define a method that receives the index of a node in this representation and returns the coordinates of the node, the region where it is and the indices to the left and right child. For the implementation mentioned above, it could be something like:

.. code-block:: python

    def get_properties(node_id):
        node = tree[node_id]

        horizontal_limits = [node['limit_left'], node['limit_right']]
        vertical_limits = [node['limit_bottom'], node['limit_top']]

        # The region of the space definied by the node
        region = [horizontal_limits, vertical_limits]

        # The position of the point in the space
        coordinates = (node['longitude']), node['latitude']))

        # The dimension of the space divided by this node
        # 0 for longitude and 1 for latitude in this case
        dimension = node['dimension']

        # If you want this node to be considered
        # Set to true if this feature is not predicted by your implementation
        active = True

        # Indices to left and right children
        left, right = node['left'], node['right']

        return coordinates, region, dimension, active, left, right

To call the method:

.. code-block:: python

    import kdquery

    def spherical_dist(point1, point2):
        <statement-1>
        .
        .
        .
        <statement-N>
        return dist

    query = (2.21, 48.65)
    root_id = 0  # index of the root
    node_id, dist = kdquery.nearest_point(query, root_id, get_properties,
                                          spherical_dist)


