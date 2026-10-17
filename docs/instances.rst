.. currentmodule:: ampapi

Controller Instance
~~~~~~~~~~~~~~~~~~~~
This class object is for Controller type Instances providing the endpoints specific to it's type. 
This object is used to control all instances it has access to similar to main panel of your AMP.

.. autoclass:: Controller
   :members:

Generic Instance
~~~~~~~~~~~~~~~~~
This class object is for Generic type Instances providing the endpoints specific to it's type.

.. autoclass:: Instance
   :members:
   :exclude-members: has_controller, app_state


Minecraft Instance
~~~~~~~~~~~~~~~~~~~
This class object is for Minecraft type Instances providing the endpoints specific to it's type.

.. autoclass:: MinecraftInstance
   :members:



API Utility
~~~~~~~~~~~~
This file is specifically designed to provide useful functions for data handling of API endpoints and development of the API.

.. automodule:: ampapi.util
   :members:
 
