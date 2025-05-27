AMP API Python
==============
.. _PyPi: https://pypi.org/project/cc-ampapi/

The project can be found on `PyPi`_.


Key Features
============

- Pythonic API wrapper using `async` and `await`.
- Data is in dataclasses for easier management and interaction.
    - Optional parameter per function or global to disable formatting of data.
- Parent classes `ADSInstance` and `AMPInstance` to group endpoints together and make handling of multiple Instances easier.
    - This will also limit Instance specific API endpoints (eg. Minecraft) to that Instance type only.


Installing
==========

.. note::
    *Python 3.10 or higher is required*


To install run the below command in a Terminal.

.. code-block:: bash
    :linenos:

    # Linux/macOS/Windows
    pip install cc-ampapi



Basic Usage
===========
1. First you need to fill out the :py:class:`~ampapi.modules.APIParams` class with the required fields (``url``, ``user`` and ``password``).
2. Pass the :py:class:`~ampapi.modules.APIParams` class into the :py:class:`~ampapi.Bridge` class parameter ``api_params``.
    - You only need to make **ONE** :py:class:`~ampapi.Bridge` class; the rest of the API classes will get the same object and handle logging in for you.
3. You can then use the Parent :py:class:`~ampapi.instance.AMPADSInstance` or the smaller class :py:class:`~ampapi.instance.AMPInstance` or any of the API classes as a stand alone.
    - See `Quick Example`_ for a visual example.

.. _Quick Example: https://github.com/k8thekat/AMPAPI_Python/blob/main/docs/samples/sample.py


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
