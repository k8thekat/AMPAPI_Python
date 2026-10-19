.. currentmodule:: ampapi


Bridge
~~~~~~~
This is used to handle your login credentials and AMP Login Sessions.

.. autoclass:: Bridge
   :members:
   :exclude-members: _get_bridge


Base
~~~~~~~~~~~~
All Modules/Plugins inherit from this class.

.. autoclass:: Base
   :members:

Response Handler Options
~~~~~~~~~~~~~~~~~~~~~~~~~
The keyword arguments every endpoint forwards to its response handler through ``**response_params``.

.. autoclass:: ResponseHandlerOptions
   :members:


ADS Module
~~~~~~~~~~~
.. autoclass:: ADSModule
   :members:
   :show-inheritance:

Analytics Module
~~~~~~~~~~~~~~~~~
.. autoclass:: AnalyticsPlugin
   :members:
   :show-inheritance:

Core Module
~~~~~~~~~~~~
.. autoclass:: Core
   :members:
   :show-inheritance:

Email Sender Module
~~~~~~~~~~~~~~~~~~~~
.. autoclass:: EmailSenderPlugin
   :members:
   :show-inheritance:

File Manager Module
~~~~~~~~~~~~~~~~~~~~
.. autoclass:: FileManagerPlugin
   :members:
   :show-inheritance:

Local File Backup Module
~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: LocalFileBackupPlugin
   :members:
   :show-inheritance:

Minecraft Module
~~~~~~~~~~~~~~~~~~~~~~~~~
.. autoclass:: MinecraftModule
   :members:
   :show-inheritance:


Exponential Backoff
~~~~~~~~~~~~~~~~~~~~
Calculates the delay between retries, growing exponentially with each attempt.

.. autoclass:: ExponentialBackoff
   :members:


Error Classes
~~~~~~~~~~~~~
Every error the library raises inherits from :class:`~ampapi.errors.AMPAPIError`, and all of them are importable from ``ampapi``.

.. automodule:: ampapi.errors
   :members:
   :show-inheritance:
