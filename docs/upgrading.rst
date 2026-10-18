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
``User``                        :class:`~ampapi.modules.UserInfo`
==============================  ==================================================

Renamed attributes: ``Base.url`` -> ``endpoint_url``, ``FileChunk.base_64_data`` -> ``base64_data``,
``InstanceDatastore.sanitized_name`` -> ``sanitised_name``, ``Module.end_point_ur`` -> ``endpoint_uri`` and
``PortInfo.us_user_defined`` -> ``is_user_defined``.


Moved modules
-------------

Everything public is still available straight from ``ampapi``.

- ``ampapi.controller`` was removed; :class:`~ampapi.instance.Controller` lives in ``ampapi.instance``.
- ``ampapi.enums_`` -> ``ampapi._enums``
- ``ampapi.types_`` -> ``ampapi._types``


Changed methods
---------------

- ``Base.dataclass_to_dict()`` and ``Base.json_to_dataclass()`` were removed. The dataclasses sent as API parameters
  have their own ``to_dict()``.
- :meth:`~ampapi.Core.login` renamed ``rememberME`` to ``remember_me``.
- :meth:`~ampapi.Core.get_oidc_login_url` dropped its ``state`` parameter and returns the login URL; 4.x always returned None.
- ``format_data`` was removed from methods whose response has no dataclass (eg. ``get_new_guid``, ``get_group``,
  ``set_configs``); passing it now raises a :exc:`TypeError`.
- ``Bridge.api_params`` was removed. :class:`~ampapi.Bridge` is an :class:`~ampapi.modules.APIParams` itself, so read
  ``bridge.url``, ``bridge.user`` and the rest straight off it. ``Bridge(api_params=...)`` still works.


Errors
------

API errors are now raised (see ``ampapi.errors``) instead of an ``ActionResultError`` being returned.


Returned data
-------------

- :meth:`~ampapi.Core.get_updates` fills the ``console_entries``, ``messages``, ``ports`` and ``tasks`` of
  :class:`~ampapi.modules.Updates` with dataclasses (``ConsoleEntries``, ``Messages``, ``Port`` and ``RunningTask``);
  4.x left them as dicts.
- :attr:`~ampapi.modules.Status.metrics` is built into a :class:`~ampapi.modules.Metrics` dataclass; 4.x left it as a dict.
