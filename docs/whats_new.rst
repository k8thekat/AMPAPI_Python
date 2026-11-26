.. currentmodule:: ampapi

What's New
==========

What changed in each release, newest first. Each section is also the release's notes on
`GitHub <https://github.com/k8thekat/AMPAPI_Python/releases>`_. The full record of every commit is the
`CHANGELOG <https://github.com/k8thekat/AMPAPI_Python/blob/main/CHANGELOG.md>`_, and :doc:`upgrading` has the long
form of each change since 4.x.


v5.1.0
------

5.1.0 types each Target's fitness data, checked against a live AMP 2.8 panel, and makes `format_data` keyword-only on
every method. Code written for 5.0 that reads `fitness` as a dict, or passes `format_data` by position, needs a change.

.. rubric:: Breaking changes

- :attr:`Controller.fitness` and :attr:`TargetADS.fitness` hold a :class:`~ampapi.modules.Fitness` dataclass
  instead of a dict. Read ``fitness.score`` where 5.0 read ``fitness["score"]``. As in 5.0, `fitness` is None when AMP
  sends no fitness data.
- `format_data` is keyword-only on the last six :class:`Instance` methods that took it by position:
  :meth:`~Instance.get_application_status`, :meth:`~Instance.get_updates`, :meth:`~Instance.start_instance`,
  :meth:`~Instance.stop_instance`, :meth:`~Instance.restart_instance` and :meth:`~Instance.upgrade_instance`. Write
  ``instance.get_updates(format_data=True)`` where 5.0 allowed ``instance.get_updates(True)``.

.. rubric:: New

- :meth:`Instance.start_instance`, :meth:`~Instance.stop_instance`, :meth:`~Instance.restart_instance` and
  :meth:`~Instance.upgrade_instance` take `request_params` and ``**response_params``, like every other method.

.. rubric:: Fixes

- :class:`~ampapi.modules.Provision` gains `score_description` and `score_zero_factors`, which
  :meth:`~ADSModule.get_provision_fitness` dropped with a warning.
- :meth:`ADSModule.upgrade_instance`, :meth:`Instance.upgrade_instance` and :meth:`TargetADS.upgrade_instance` return
  a :class:`~ampapi.modules.RunningTask`, which is what AMP 2.8 sends. In 5.0 they raised
  :exc:`~ampapi.errors.AMPAPIKeyError` on every call, although AMP started the upgrade.

.. rubric:: Docs

- AMP only sends fitness data on a licence that includes it. On an AMP Professional licence,
  :meth:`~ADSModule.get_provision_fitness` returns None and `fitness` is None.
- :meth:`~ADSModule.deploy_template` is confirmed to return a :class:`~ampapi.modules.RunningTask`.
- :doc:`upgrading` gains a "New methods" list, the new `typing_extensions` dependency, and the 4.x calls that pass
  `format_data` by position.


v5.0.1
------

5.x is a rewrite of the wrapper for AMP 2 panels. It breaks code written for 4.x. 5.0.0 was never published, so 5.0.1
is the first 5.x release, and this section covers everything since 4.6.0. :doc:`upgrading` lists every change
in detail.

.. code-block:: bash

    pip install -U cc-ampapi

.. rubric:: Before you upgrade

- Python 3.12 or newer. 4.x ran on Python 3.10.
- An AMP 2 panel, AMP 2.6.2.8 or newer. The login session is sent in the `Authorization` header, and the old
  `SESSIONID` parameter is gone.
- An AMP 3 panel needs the 6.x beta API. 5.x raises :exc:`~ampapi.errors.AMPAPIPanelVersionError` when the panel is
  AMP 3. Every 6.x version is a beta until 6.0.0 is released, so install it with ``pip install --pre "cc-ampapi>=6"``.
- To stay on 4.x for now, pin it with ``pip install "cc-ampapi<5"``.
- ``dataclass-wizard`` is no longer a dependency. `typing_extensions` is a new dependency.

.. rubric:: Breaking changes

The two changes most code meets first are the class names and errors being raised:

.. code-block:: python

    # 4.x
    from ampapi import ActionResultError, AMPControllerInstance, APIParams, Bridge

    Bridge(api_params=APIParams(url="http://192.168.1.10:8080", user="amp_user", password="amp_password"))
    ads = AMPControllerInstance()
    status = await ads.get_status()
    if isinstance(status, ActionResultError):
        print(status.reason)

.. code-block:: python

    # 5.x
    from ampapi import AMPAPIResponseError, APIParams, Bridge, Controller

    Bridge(api_params=APIParams(url="http://192.168.1.10:8080", user="amp_user", password="amp_password"))
    async with Controller() as controller:
        try:
            status = await controller.get_status()
        except AMPAPIResponseError as error:
            print(error)

- **Renamed classes.** `AMPControllerInstance` is :class:`Controller`, `AMPInstance` is :class:`Instance`,
  `AMPMinecraftInstance` is :class:`MinecraftInstance` and `AMPADSInstance` is :class:`TargetADS`. Everything public
  still imports straight from `ampapi`. :doc:`upgrading` has the full table, and the moved modules.
- **Errors are raised.** `ActionResultError` is gone. A failed call raises an error from :mod:`ampapi.errors`, and
  :exc:`~ampapi.errors.AMPAPIError` catches every error the library raises. Methods that return None now raise when
  AMP's reply reports a failure.
- **Sessions and the Bridge.** Every object made with a :class:`Bridge` sends its calls through the Bridge's `aiohttp.ClientSession`.
  Close it with ``await controller.clean_up()`` or ``async with Controller() as controller:``. To use your own
  session, pass it as ``Bridge(api_params=..., session=...)``. `session_ttl` is removed, and `Bridge.api_params` is
  removed because the :class:`Bridge` is an :class:`~ampapi.modules.APIParams` itself.
- **Calling methods.** `format_data` is keyword-only, so write ``get_status(format_data=False)``. Several methods are
  renamed or removed (eg. `update_instance` is now `upgrade_instance`), and the 16 `MinecraftModule` methods whose
  endpoints AMP 2.6.5.0 removed are deprecated.
- **Controller and Targets.** :attr:`Controller.instances` holds only the Controller's own Instances. Each remote
  Target is a :class:`TargetADS` in the new :attr:`Controller.targets`, with its Instances in
  :attr:`TargetADS.instances`.
- **Returned data.** The response dataclasses are slotted, nested data is built into dataclasses, and several methods
  return what AMP sends (eg. `create_instance` returns a :class:`~ampapi.modules.RunningTask`).

.. rubric:: New

- **OIDC logins.** Set ``auth_mode=AuthMode.oidc`` on :class:`~ampapi.modules.APIParams` for an AMP user who signs in
  through an OIDC provider, then pass the provider's `code` and `state` to :meth:`Core.oidc_login`.
- **async with and clean_up** on every class and on the :class:`Bridge`. ``clean_up(logout=True)`` ends the AMP login
  session first.
- **Typed responses.** Every response dataclass has ``from_response()``, and with ``format_data=False`` each method is
  typed with the matching `*Response` TypedDict from `ampapi._types`.
- **Targets.** :class:`TargetADS` has the :class:`ADSModule` methods, and each :class:`Instance` knows the ADS that
  holds it as `Instance.ads`.
- **Generic Instances.** :class:`Instance` has the :class:`GenericModule` and :class:`SteamCMDPlugin` endpoints.
- ``create_instance(wait=True)`` waits for the creation task to finish.
- New wrappers for AMP 2.8 endpoints, listed in :doc:`upgrading`, and the optional parameters from AMP's API spec.
- Calls made at once on the same Instance share a single login, and the repr of :class:`~ampapi.modules.APIParams` and
  :class:`Bridge` leaves out the password, the token and the stored login sessions.

.. rubric:: Fixes

These were bugs in 4.6.0 that you may have hit:

- `take_backup` raised, although AMP took the backup.
- `get_webauthn_credential_ids` raised on every call, and `get_user_info` raised on AMP 2.8's `DisplayName` key.
- `apply_instance_configuration` and `create_instance_from_spec` raised on AMP 2.8's reply.
- `update_instance_info` always failed. :class:`~ampapi.modules.InstanceInfo` now needs only `instance_id`, and AMP
  leaves every field you don't set unchanged.
- `add_datastore` and `update_datastore` saved a datastore with no name, and the ADS then failed to start until it
  was removed.
- Starting, stopping or restarting an Instance on a remote Target could act on the Controller's own Instance when both
  had the same name (eg. `ADS01`).
- `oidc_login`, `get_remote_login_token`, `deploy_template`, `edit_interval_trigger` and `refresh_setting_value_list`
  sent parameters AMP rejected.
- `logout` could log in first and end that new login session, and 4.x logged in again every 240 seconds, which left
  each old login session alive on AMP.
- `CreateInstance` defaulted `ip_binding` to ``"192.168.0.1"``, which AMP rejects on a machine without that address.
  It now defaults to ``"0.0.0.0"``.
- File paths with an underscore were refused (eg. `AMP_Logs`). Paths are now sent as given.
