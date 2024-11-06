.. AMPAPI_Python documentation master file, created by
   sphinx-quickstart on Thu Oct 31 13:00:00 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AMP API Python
==============
.. _PyPi: https://pypi.org/project/cubecoders-amp-api-wrapper/

The project can be found on `PyPi`_.


Key Features
============

- Pythonic API wrapper using `async` and `await`.
- Data is in dataclasses for easier management and interaction.
    - Optional parameter per function or global to disable formatting of data.
- Parent classes `AMPADSInstance`, `AMPInstance`, `AMPMinecraftInstance` to group endpoints together and make handling of multiple Instances easier.
    - This will also limit Instance specific API endpoints (eg. Minecraft) to that Instance type only.
    - Built in functions to start, stop, restart and update AMPInstances that are NOT an ADS/Controller.


Installing
==========
.. note::
    *Python 3.10 or higher is required*


To install run the below command in a Terminal.

.. code-block:: bash
    :linenos:

    # Linux/macOS/Windows
    pip install cubecoders-amp-api-wrapper



Basic Usage
===========
1. First you need to fill out the :py:class:`~ampapi.dataclass.APIParams` class with the required fields (``url``, ``user`` and ``password``).
2. Pass the :py:class:`~ampapi.dataclass.APIParams` class into the :py:class:`~ampapi.bridge.Bridge` class parameter ``api_params``.
    - You only need to make __ONE__ :py:class:`~ampapi.bridge.Bridge` class; the rest of the API classes will get the same object and handle logging in for you.
3. You can then use the Parent :py:class:`~ampapi.instance.AMPADSInstance` or the smaller class :py:class:`~ampapi.instance.AMPInstance` or any of the API classes as a stand alone.
    - See `Quick Example`_ for a visual example.

.. _Quick Example: ../samples/sample.py

.. toctree::
    :maxdepth: 3
    :caption: Class Modules:

    modules

.. toctree::
    :maxdepth: 1
    :caption: Docs:
    
    docs
