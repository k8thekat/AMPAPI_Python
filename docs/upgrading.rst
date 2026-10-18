Upgrading from 4.x
==================

**5.0.0 is a major version bump, because it breaks backwards compatibility with 4.x.**
Code written for ``4.6.0`` will need a few changes before it runs, so pin ``cc-ampapi<5`` if you aren't ready to upgrade yet~

.. code-block:: bash

    pip install "cc-ampapi<5"


Requirements
------------

- Python 3.12 or higher (4.x supported 3.10).
- AMP ``2.6.2.8`` or newer. The session is sent in the ``Authorization`` header now, and the old ``SESSIONID`` parameter is gone.


Renamed classes
---------------

==============================  ==================================================
4.x                             5.0.0
==============================  ==================================================
``AMPControllerInstance``       :class:`~ampapi.instance.Controller`
``AMPInstance``                 :class:`~ampapi.instance.Instance`
``AMPMinecraftInstance``        :class:`~ampapi.instance.MinecraftInstance`
``AMPADSInstance``              :class:`~ampapi.instance.TargetADS`
``AMPInstanceState``            :class:`~ampapi.InstanceState`
``Metric``                      :class:`~ampapi.modules.Metrics`
==============================  ==================================================


Moved modules
-------------

Everything public is still available straight from ``ampapi``.

- ``ampapi.controller`` was removed; :class:`~ampapi.instance.Controller` lives in ``ampapi.instance``.
- ``ampapi.enums_`` -> ``ampapi._enums``
- ``ampapi.types_`` -> ``ampapi._types``


Errors
------

API errors are now raised (see ``ampapi.errors``) instead of an ``ActionResultError`` being returned.


Returned data
-------------

- :meth:`~ampapi.Core.get_updates` fills the ``console_entries``, ``messages``, ``ports`` and ``tasks`` of
  :class:`~ampapi.modules.Updates` with dataclasses (``ConsoleEntries``, ``Messages``, ``Port`` and ``RunningTask``);
  4.x left them as dicts.
- :attr:`~ampapi.modules.Status.metrics` is built into a :class:`~ampapi.modules.Metrics` dataclass; 4.x left it as a dict.
