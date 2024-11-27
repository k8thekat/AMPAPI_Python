.. currentmodule:: ampapi

Controller Instance
~~~~~~~~~~~~~~~~~~~~
This class object is for Controller type Instances specifically providing the endpoints specific to it's type. 
This object is used to control all instances it has access to similar to main panel of your AMP.

.. autoclass:: AMPControllerInstance
   :members:

Generic Instance
~~~~~~~~~~~~~~~~~
This class object is for Generic type Instances specifically providing the endpoints specific to it's type.

.. autoclass:: AMPInstance
   :members:
   :exclude-members: has_controller


Target/ADS Instance
~~~~~~~~~~~~~~~~~~~
This class object is for Target/ADS type Instances specifically providing the endpoints specific to it's type.

.. autoclass:: AMPADSInstance
   :members:


Minecraft Instance
~~~~~~~~~~~~~~~~~~~
This class object is for Minecraft type Instances specifically providing the endpoints specific to it's type.

.. autoclass:: AMPMinecraftInstance
   :members:



API Utility
~~~~~~~~~~~~
This file is specifically designed to provide useful functions for data handling of API endpoints and development of the API.

.. automodule:: ampapi.util
   :members:
 
