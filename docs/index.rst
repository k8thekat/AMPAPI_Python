AMP API Python
==============
.. _PyPi: https://pypi.org/project/cc-ampapi/

The project can be found on `PyPi`_.


Key Features
============

- Pythonic API wrapper using `async` and `await`.
- Data is in dataclasses for easier management and interaction.
    - Optional parameter per function or global to disable formatting of data.
- Parent classes `Controller` and `Instance` to group endpoints together and make handling of multiple Instances easier.
    - This will also limit Instance specific API endpoints (eg. Minecraft) to that Instance type only.


Installing
==========

.. note::
    *Python 3.12 or higher is required*


To install run the below command in a Terminal.

.. code-block:: bash
    :linenos:

    # Linux/macOS/Windows
    pip install cc-ampapi

.. note::
    5.0.0 breaks backwards compatibility with 4.x; see :doc:`upgrading` for what changed.



Basic Usage
===========
1. First you need to fill out the :py:class:`~ampapi.modules.APIParams` class with the required fields (``url``, ``user`` and ``password``).
2. Pass the :py:class:`~ampapi.modules.APIParams` class into the :py:class:`~ampapi.Bridge` class parameter ``api_params``.
    - You only need to make **ONE** :py:class:`~ampapi.Bridge` class; the rest of the API classes will get the same object and handle logging in for you.
3. You can then use the Parent :py:class:`~ampapi.instance.Controller` or the smaller class :py:class:`~ampapi.instance.Instance` or any of the API classes as a stand alone.
    - See `Quick Example`_ for a visual example.

.. _Quick Example: https://github.com/k8thekat/AMPAPI_Python/blob/main/docs/samples/sample.py


.. toctree::
    :maxdepth: 2
    :caption: Upgrading:

    upgrading

.. toctree::
    :maxdepth: 3
    :caption: API Classes:

    modules

.. toctree:: 
    :maxdepth: 3
    :caption: AMP Instance Classes:

    instances


.. toctree:: 
    :maxdepth: 3
    :caption: Types:

    types


.. toctree::
    :name: Documentation
    :caption: Docs:
    :glob:

    events/*
    nodes/* 
