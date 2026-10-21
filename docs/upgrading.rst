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
``APISPecEndpointData``         :class:`~ampapi._types.APISpecEndpointData`
``DCConsumes``                  :class:`~ampapi.modules.Consumes`
``DCParameterMapping``          :class:`~ampapi.modules.ParameterMapping`
==============================  ==================================================

Renamed attributes: ``Base.url`` -> ``endpoint_url``, ``FileChunk.base_64_data`` -> ``base64_data``,
``InstanceDatastore.sanitized_name`` -> ``sanitised_name``, ``Module.end_point_ur`` -> ``endpoint_uri`` and
``PortInfo.us_user_defined`` -> ``is_user_defined``.

- The raw response TypedDicts in ``ampapi._types`` (4.x ``ampapi.types_``) are named after their dataclass, with a
  ``Response`` suffix: ``types_.Consumes`` -> ``ConsumesResponse``, ``MethodsData`` -> ``MethodsResponse``,
  ``types_.ParameterMapping`` -> ``ParameterMappingResponse`` and ``MCUserData`` -> ``MCUserResponse``. ``Consumes``
  and ``ParameterMapping`` are now the dataclasses in :mod:`ampapi.modules`.


Moved modules
-------------

Everything public is still available straight from ``ampapi``.

- ``ampapi.controller`` was removed; :class:`~ampapi.instance.Controller` lives in ``ampapi.instance``.
- ``ampapi.enums_`` -> ``ampapi._enums``
- ``ampapi.types_`` -> ``ampapi._types``
- ``ampapi.util`` holds developer tools and is no longer star-imported, so its functions (eg. ``amp_api_update``,
  ``find_missing_endpoints``) are no longer on ``ampapi``. Import the module instead: ``from ampapi import util``.


Changed methods
---------------

- ``Base.dataclass_to_dict()`` and ``Base.json_to_dataclass()`` were removed. The dataclasses sent as API parameters
  have their own ``to_dict()``.
- :meth:`~ampapi.Core.login` renamed ``rememberME`` to ``remember_me``.
- ``Base.call_end_point()`` is now ``_call_end_point()``; it is a dev tool for testing endpoints that have no wrapper yet.
- :meth:`~ampapi.Core.get_oidc_login_url` dropped its ``state`` parameter and returns the login URL; 4.x always returned None.
- ``format_data`` was removed from methods whose response has no dataclass (eg. ``get_new_guid``, ``get_group``,
  ``set_configs``); passing it now raises a :exc:`TypeError`.
- ``Bridge.api_params`` was removed. :class:`~ampapi.Bridge` is an :class:`~ampapi.modules.APIParams` itself, so read
  ``bridge.url``, ``bridge.user`` and the rest straight off it. ``Bridge(api_params=...)`` still works.
- :meth:`~ampapi.adsmodule.ADSModule.create_instance`, :meth:`~ampapi.adsmodule.ADSModule.create_instance_from_spec`
  and :meth:`~ampapi.adsmodule.ADSModule.apply_instance_configuration` return a :class:`~ampapi.modules.RunningTask`,
  which is what AMP sends. 4.x returned an ``ActionResult``, and the last two raised on AMP 2.8's reply.
- :meth:`~ampapi.minecraft.MinecraftModule.mc_reject_eula` returns a bool like ``mc_accept_eula``; 4.x returned None.
- :meth:`~ampapi.adsmodule.ADSModule.create_local_instance` is deprecated. AMP 2.8.0.8 answers a null reference to
  every Instance shape sent, and its ``LocalAMPInstance`` is undocumented. Use ``create_instance`` or
  ``create_instance_from_spec``.
- :class:`~ampapi.instance.Instance` has the :class:`~ampapi.generic.GenericModule` and
  :class:`~ampapi.steamcmd.SteamCMDPlugin` endpoints, which Generic Instances (module ``GenericModule`` or ``Generic``)
  serve. On any other module they raise :exc:`RuntimeError`.
- ``PostCreateActionsState`` was removed; it never matched AMP's ``PostCreateAppActions`` (eg. its ``start_instance``
  was AMP's ``update_once``, and ``every_time`` = 16 doesn't exist). :class:`~ampapi.CreateInstance`,
  ``DeploymentTemplate``, ``create_instance_from_spec`` and ``create_local_instance`` take
  :class:`~ampapi.PostCreateState`, whose values are AMP's.
- :class:`~ampapi.modules.CreateInstance` fills ``new_instance_id`` with the zero GUID (AMP picks the ID),
  ``admin_username`` with ``"admin"`` and ``admin_password`` with a generated password, since AMP rejects empty values.
- ``Base.version_validation()`` takes the ``endpoint`` it guards, and :meth:`~ampapi.Core.get_webserver_metrics` raises
  the :exc:`RuntimeError` instead of returning it.
- ``Base.clean_up()`` takes a keyword-only ``logout`` (default False) to call ``Core/Logout`` before closing the session.
- Every :class:`~ampapi.instance.Instance` knows the ADS that holds it, :attr:`~ampapi.instance.Instance.ads`: the
  :class:`~ampapi.instance.Controller` for its own Instances, the :class:`~ampapi.instance.TargetADS` for a remote
  Target's. :meth:`~ampapi.instance.Instance.start_instance`, ``stop_instance``, ``restart_instance``,
  ``update_instance`` and ``get_instance_status`` go through that ADS, so the name is looked up on the right one. 4.x
  sent them to the Controller, which acts on its own Instance when two ADSs share a name (every ADS is ``ADS01``).
- :attr:`~ampapi.instance.Controller.instances` is no longer flat. It holds only the Instances the Controller itself
  holds (its local Target), and the remote Targets are in the new :attr:`~ampapi.instance.Controller.targets`, keyed by
  the Target's ADS ID. Each :class:`~ampapi.instance.TargetADS` holds its own Instances in
  :attr:`~ampapi.instance.TargetADS.instances`. Code that read a remote Target's Instances from
  ``Controller.instances`` has to read them from ``Controller.targets`` instead.
- :meth:`~ampapi.instance.Controller.get_instances` fills every ``TargetADS.instances`` at the same time, with one extra
  call per Target. A Target that fails logs a warning and keeps an empty ``instances``. A Target that does not list its
  own ADS Instance is skipped.
- :meth:`~ampapi.instance.Controller.get_instance` raises a :exc:`ValueError` for an Instance a cached ``TargetADS``
  holds, because the Controller's copy of it differs from the Target's own data. Use
  :meth:`~ampapi.instance.TargetADS.get_instance` for it. A Target's ADS ID returns the cached ``TargetADS``.
- :meth:`~ampapi.adsmodule.ADSModule.get_provision_fitness` returns None when AMP has no fitness data (JSON null),
  instead of raising.
- :meth:`~ampapi.adsmodule.ADSModule.get_group` returns the Target dictionary (the shape of one
  :meth:`~ampapi.adsmodule.ADSModule.get_instances` entry), or None when AMP answers JSON null.
- :meth:`~ampapi.filemanager.FileManagerPlugin.write_file_chunk` renamed ``append`` to ``final_chunk``. It was always
  sent as AMP's ``FinalChunk``, which marks the last chunk of the file, not an append.
- ``APIParams`` (and so :class:`~ampapi.Bridge`) strips a trailing ``/`` from ``url``.
- :attr:`~ampapi.instance.Instance.url` is ``Union[str, None]`` and defaults to None, since AMP never sends a URL
  for an Instance; 4.x typed it ``str``. A :class:`~ampapi.instance.TargetADS` holds its Target's URL. Instance fields
  AMP sends as null hold their documented default (``""`` for ``description``, ``display_image_source`` and
  ``module_display_name``, None otherwise).
- ``Base.sanitize_path`` (used by every file method) only drops leading ``/`` now. 4.x refused any ``_`` (so
  ``AMP_Logs`` was out of reach), turned ``..`` into ``.`` and stripped a leading ``.`` (so ``.trash`` became
  ``trash``). AMP takes all of those as given.
- ``DeploymentTemplate.settings_mappings`` is now ``setting_mappings``, AMP's own key; its ``description``, ``module``,
  ``template_role`` and ``template_base_app`` can be None. With templates present, 4.x could not build the class at all.
- ``Base.version_validation()`` checked the wrong way round and never fired; it now raises once AMP is at or past the
  version the endpoint was removed in.


Errors
------

API errors are now raised (see ``ampapi.errors``) instead of an ``ActionResultError`` being returned. Every error
class can be imported from ``ampapi`` directly (eg. ``from ampapi import AMPAPIResponseError``).


Returned data
-------------

- :meth:`~ampapi.Core.get_updates` fills the ``console_entries``, ``messages``, ``ports`` and ``tasks`` of
  :class:`~ampapi.modules.Updates` with dataclasses (``ConsoleEntries``, ``Messages``, ``Port`` and ``RunningTask``);
  4.x left them as dicts.
- ``dataclass-wizard`` is no longer a dependency. A key AMP sends that a dataclass doesn't declare is still dropped,
  as in 4.x, but is now logged once as a warning. Nested data is built into its dataclass as in 4.x (eg.
  ``RemoteTargetInfo.platform_info``, ``Methods.consumes``).
- :meth:`~ampapi.Core.get_setting_spec` builds on AMP 2.8, which sends no ``branding`` category. The
  :class:`~ampapi.modules.SettingsSpecParent` gains ``backups``, ``meta_config`` and ``minecraft``, and ``modules``
  holds the categories with a colon in the name (eg. ``valheim:stadiacontroller``) as a dict of lists of
  :class:`~ampapi.modules.SettingSpec`.
- :meth:`~ampapi.Core.get_webauthn_credential_ids` returns the dict AMP sends (``ids`` and ``challenge``). The wrapper
  typed it as a list, and raised on every call.
- :meth:`~ampapi.filebackup.LocalFileBackupPlugin.take_backup` returns a :class:`~ampapi.modules.RunningTask`, which is
  what AMP sends. The wrapper expected an ``ActionResult`` and raised, although the backup was taken.
- :meth:`~ampapi.instance.Instance.get_updates` and :meth:`~ampapi.instance.Instance.get_application_status` take
  ``request_params`` and the ``**response_params`` the other methods take (eg. ``to_file``).
- :class:`~ampapi.modules.ParameterMapping` holds the arguments of every task method in AMP 2.8.0.8 (eg.
  ``seconds``, ``message``, ``input``); 4.x kept only ``user``, ``reason``, ``title`` and ``subtitle``. An argument
  the task doesn't hold is ``None``, not ``""``. Booleans, numbers, ``state``, ``operation`` (:class:`~ampapi.IfOperators`),
  ``priority`` (:class:`~ampapi.MailPriority`) and ``when`` (a naive ``datetime``) are converted from AMP's strings
  (a value that doesn't parse stays a string).
- :attr:`~ampapi.modules.RemoteTargetInfo.datastores` holds :class:`~ampapi.modules.TargetDatastore` (an ID and a
  name, all AMP sends there); 4.x typed it as ``InstanceDatastore``.
- ``AnalyticsCountryData.session_percent`` is renamed
  :attr:`~ampapi.modules.AnalyticsCountryData.sessions_percent`, the key AMP sends; 4.x never filled it.
- :attr:`~ampapi.modules.Status.metrics` is built into a :class:`~ampapi.modules.Metrics` dataclass; 4.x left it as a dict.
- :attr:`~ampapi.modules.Module.branding` is a :class:`~ampapi.modules.Branding` dataclass; 4.x left it as a dict.
- :attr:`~ampapi.modules.AnalyticsSummary.busiest_time`, ``quietest_time`` and ``graph_data`` hold
  :class:`~ampapi.modules.AnalyticsGraphData` (``date``, ``end_date`` and ``count``); 4.x left them as dicts.
- :attr:`~ampapi.modules.Messages.parameters` is a :class:`~ampapi.modules.MessageParameters` (its ``metrics`` a
  :class:`~ampapi.modules.Metrics`, its ``uptime`` an :class:`~ampapi.modules.Uptime` and its ``state`` an
  :class:`~ampapi.InstanceState`). 4.x had no ``parameters``.
- :attr:`~ampapi.instance.Instance.application_endpoints` holds :class:`~ampapi.modules.Endpoints`, and the
  ``datastores`` of a :class:`~ampapi.instance.Controller` or :class:`~ampapi.instance.TargetADS` hold
  :class:`~ampapi.modules.TargetDatastore`; 4.x left both as dicts.
- :meth:`~ampapi.Core.get_permissions_spec` returns :class:`~ampapi.modules.PermissionNode` dataclasses (with
  ``children`` built the same way) and takes ``format_data``. 4.x returned the dicts, which are now
  ``ampapi._types.PermissionNodeResponse``.
- :meth:`~ampapi.instance.Controller.get_instances` leaves the Controller's own ADS Instance (eg. ``ADS01``) out of
  :attr:`~ampapi.instance.Controller.instances`, since that Instance is the Controller; its data is copied onto the
  Controller. The ADS Instances of remote Targets come back as :class:`~ampapi.instance.TargetADS` in
  :attr:`~ampapi.instance.Controller.targets`; 4.x returned an ``AMPADSInstance`` for every ADS Instance, the
  Controller's own included.
- The Controller attributes copied from :meth:`~ampapi.instance.Controller.get_instances` (eg. ``friendly_name``,
  ``state``) raise an ``AttributeError`` naming ``get_instances()`` until it has run, and log a warning on each read
  once that data is older than 300 seconds.
- ``get_instances`` no longer takes ``include_self`` (on ``ADSModule``, :class:`~ampapi.instance.Controller` and
  :class:`~ampapi.instance.TargetADS`). AMP's ``ForceIncludeSelf`` is always sent as True, which was the 4.x default.
  False either changed nothing or dropped a Controller's local Target, leaving the Controller's own data unset.
- Keys holding a dot are AMP setting nodes and keep AMP's spelling (eg. ``deployment_args`` keeps
  ``ADSModule.Defaults.DefaultAuthServerURL``); 4.x rewrote them like field names
  (``ads_module._defaults._default_auth_server_url``).


Target ADS
----------

- :class:`~ampapi.instance.TargetADS` gains the :class:`~ampapi.adsmodule.ADSModule` methods, and they go to that
  Target.
- Its :meth:`~ampapi.instance.TargetADS.start_instance`, :meth:`~ampapi.instance.TargetADS.stop_instance` and
  :meth:`~ampapi.instance.TargetADS.restart_instance` now take an ``instance_name`` and act on an Instance on that
  Target. In 4.6.0 they took no argument and went through the Controller by name, so for an ADS named like the
  Controller's (eg. ``ADS01``) they acted on the Controller's own ADS.
- :meth:`~ampapi.instance.Controller.get_instance` on the Controller's own ADS ID (and
  :meth:`~ampapi.instance.TargetADS.get_instance` on a ``TargetADS``'s own ID) returns that object itself. The
  Controller learns its own ADS ID from :meth:`~ampapi.instance.Controller.get_instances`, or from the new
  ``auto_detect=True`` argument. Without either, an ADS Instance logs a warning and comes back as a ``TargetADS``.
- :meth:`~ampapi.instance.TargetADS.get_instances` returns the Instances on that Target, leaving out the Target's own
  ADS Instance, and keeps them on ``TargetADS.instances``. The Target's own data in the reply refreshes the
  ``TargetADS`` itself, and each returned Instance has the ``TargetADS`` as its ``ads``.
- A ``TargetADS`` carries its Target's data flat on itself like the ``Controller`` does (``platform``, ``url``,
  ``state``, ``datastores``, ``available_instances`` and the rest). ``friendly_name``, ``description`` and ``tags``
  stay the Instance's values. The data arrives with :meth:`~ampapi.instance.Controller.get_instances` (the
  Controller's copy), then the ``TargetADS``'s own :meth:`~ampapi.instance.TargetADS.get_instances` replaces it with
  the Target's own view. Reading it before that raises :exc:`AttributeError`, as on the ``Controller``.
- :meth:`~ampapi.instance.Controller.get_instances` and :meth:`~ampapi.instance.TargetADS.get_instances` update
  existing objects in place, matched by Instance ID, instead of building new ones. ``Controller.targets``,
  ``Controller.instances`` and ``TargetADS.instances`` stay the same objects, so a reference to an Instance or a
  ``TargetADS`` stays valid across refreshes. Instances AMP no longer lists are dropped.
