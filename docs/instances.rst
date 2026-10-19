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


Target ADS Instance
~~~~~~~~~~~~~~~~~~~~~
This class object is for the Target ADS Instances held in :attr:`Controller.instances`. It is an :class:`Instance` that also has
every :class:`ADSModule` method, so calls go to that Target and act on the Instances it holds.
:meth:`~TargetADS.start_instance`, :meth:`~TargetADS.stop_instance`, :meth:`~TargetADS.restart_instance`,
:meth:`~TargetADS.delete_instance_users`, :meth:`~TargetADS.get_instance` and :meth:`~TargetADS.get_instances` are overridden.

.. autoclass:: TargetADS
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
 
