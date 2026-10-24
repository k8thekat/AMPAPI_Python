# pyright: ignore[reportUnusedImport]  # noqa: D100
from __future__ import annotations

import datetime
import json
import logging
from configparser import ConfigParser
from dataclasses import fields
from pathlib import Path
from typing import Any, Union

import pytest

from ampapi import APIParams, Bridge, Core
from ampapi.adsmodule import ADSModule
from ampapi.instance import MinecraftInstance
from ampapi.modules import (
    ActionResult,
    AuditLogEntry,
    Diagnostics,
    LoginResults,
    LoginUserInfo,
    Module,
    Port,
    Role,
    RunningTask,
    ScheduleData,
    Session,
    SettingSpec,
    Status,
    UpdateInfo,
    Updates,
    UserApplicationData,
    UserInfo,
)

LOGGER: logging.Logger = logging.getLogger(__name__)
# _response_dir = Path(__file__).parent / "_responses"
# The 2.6.5 ADS and Core captures these tests read, since `_responses/` is grouped by AMP version and kind (#31).
_response_dir = Path(__file__).parent / "_responses" / "2.6.5" / "ads"


def _load_response(filename: str) -> dict[str, Any] | list[Any]:
    """Load a saved JSON response file from _responses/."""
    path = _response_dir / filename
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _response_exists(filename: str) -> bool:
    return (_response_dir / filename).is_file()


def get_api_params(section: str) -> APIParams:
    """Create our APIParams from the local.ini."""
    file: Path = Path("./local.ini")
    if file.is_file():
        settings = ConfigParser(converters={"list": lambda setting: [value.strip() for value in setting.split(",")]})
        settings.read(filenames=file.as_posix())
        return APIParams(
            url=settings.get(section=section, option="URL"),
            user=settings.get(section=section, option="USER"),
            password=settings.get(section=section, option="PASSWORD"),
            token=settings.get(section=section, option="TOKEN"),
        )
    msg = "Failed to load .ini"
    raise ValueError(msg)


async def core_unit_test() -> None:  # noqa: D103
    bridge = Bridge(api_params=get_api_params(section="LIVE"), singleton=True)
    bridge.use_2fa = True
    core = Core(bridge=bridge)
    await core._reauth()  # pyright: ignore[reportPrivateUsage]
    core._module = "ADS"  # pyright: ignore[reportPrivateUsage]
    await core.get_active_amp_sessions()


# region Endpoint Response Capture


class EndpointResult:
    """Container for an endpoint call result, whether success or failure."""

    def __init__(self, endpoint: str, data: Any = None, error: Union[Exception, None] = None) -> None:  # noqa: D107
        self.endpoint = endpoint
        self.data = data
        self.error = error

    @property
    def success(self) -> bool:  # noqa: D102
        return self.error is None

    def __repr__(self) -> str:
        if self.success:
            return f"EndpointResult({self.endpoint!r}, success)"
        return f"EndpointResult({self.endpoint!r}, error={self.error!r})"


async def _safe_call(endpoint: str, coro: Any) -> EndpointResult:  # noqa: ANN401
    """Await a coroutine and capture the result or exception."""
    try:
        data = await coro
        return EndpointResult(endpoint=endpoint, data=data)
    except Exception as e:  # noqa: BLE001
        LOGGER.warning("Endpoint %s failed: %s", endpoint, e)
        return EndpointResult(endpoint=endpoint, error=e)


async def capture_responses(section: str = "LIVE") -> list[EndpointResult]:
    """Call all read-only Core endpoints with ``to_file=True`` to generate JSON response files.

    Parameters
    ----------
    section: :class:`str`
        The local.ini section to use for credentials, by default "LIVE".

    Returns
    -------
    list[:class:`EndpointResult`]
        A list of results for each endpoint call.

    """
    bridge = Bridge(api_params=get_api_params(section=section), singleton=True)
    bridge.use_2fa = True
    core = Core(bridge=bridge)
    await core._reauth()  # pyright: ignore[reportPrivateUsage]
    core._module = "ADS"  # pyright: ignore[reportPrivateUsage]

    rp: dict[str, Any] = {"to_file": True, "path": _response_dir}
    results: list[EndpointResult] = []

    # Lambdas defer coroutine creation until iteration so _reauth has completed.
    endpoints: dict[str, Any] = {
        "get_active_amp_sessions": lambda: core.get_active_amp_sessions(format_data=False, **rp),
        "get_all_amp_user_info": lambda: core.get_all_amp_user_info(format_data=False, **rp),
        "get_amp_users_summary": lambda: core.get_amp_users_summary(format_data=False, **rp),
        "get_audit_log_entries": lambda: core.get_audit_log_entries(count=5, format_data=False, **rp),
        "get_diagnostics_info": lambda: core.get_diagnostics_info(format_data=False, **rp),
        "get_module_info": lambda: core.get_module_info(format_data=False, **rp),
        "get_port_summaries": lambda: core.get_port_summaries(format_data=False, **rp),
        "get_role_data": lambda: core.get_role_data(format_data=False, **rp),
        "get_role_ids": lambda: core.get_role_ids(**rp),
        "get_schedule_data": lambda: core.get_schedule_data(format_data=False, **rp),
        "get_status": lambda: core.get_status(format_data=False, **rp),
        "get_tasks": lambda: core.get_tasks(format_data=False, **rp),
        "get_update_info": lambda: core.get_update_info(format_data=False, **rp),
        "get_updates": lambda: core.get_updates(format_data=False, **rp),
        "get_user_list": lambda: core.get_user_list(format_data=False, **rp),
    }

    for name, factory in endpoints.items():
        results.append(await _safe_call(name, factory()))

    await core.clean_up()
    return results


async def capture_and_report(section: str = "LIVE") -> None:
    """Run capture_responses and print a summary report."""
    results = await capture_responses(section=section)
    success_count = sum(1 for r in results if r.success)
    fail_count = sum(1 for r in results if not r.success)

    LOGGER.info("--- Response Capture Report ---")
    LOGGER.info("Total: %d | Success: %d | Failed: %d", len(results), success_count, fail_count)
    for r in results:
        if r.success:
            LOGGER.info("  OK:   %s", r.endpoint)
        else:
            LOGGER.error("  FAIL: %s -> %s", r.endpoint, r.error)


async def capture_ads_responses(section: str = "LIVE") -> list[EndpointResult]:
    """Call read-only ADSModule endpoints with ``to_file=True`` to generate JSON response files.

    Parameterized endpoints (eg. `get_application_endpoints`, `get_datastore`) are resolved
    automatically from the no-parameter results. If a required value cannot be discovered, the
    endpoint is skipped with a warning.

    Parameters
    ----------
    section: :class:`str`
        The local.ini section to use for credentials, by default "LIVE".

    Returns
    -------
    list[:class:`EndpointResult`]
        A list of results for each endpoint call.

    """
    bridge = Bridge(api_params=get_api_params(section=section), singleton=True)
    bridge.use_2fa = True
    ads = ADSModule(bridge=bridge)

    rp: dict[str, Any] = {"to_file": True, "path": _response_dir}
    results: list[EndpointResult] = []

    # No-parameter endpoints run first; later calls depend on their output for IDs.
    no_param_endpoints: dict[str, Any] = {
        "get_supported_applications": lambda: ads.get_supported_applications(format_data=False, **rp),
        "get_datastores": lambda: ads.get_datastores(format_data=False, **rp),
        "get_deployment_templates": lambda: ads.get_deployment_templates(format_data=False, **rp),
        "get_instance_statuses": lambda: ads.get_instance_statuses(format_data=False, **rp),
        "get_provision_fitness": lambda: ads.get_provision_fitness(format_data=False, **rp),
        "get_target_info": lambda: ads.get_target_info(format_data=False, **rp),
        "get_instances": lambda: ads.get_instances(include_self=True, **rp),
    }

    # Collect results and resolve IDs for parameterized endpoints.
    discovered: dict[str, Any] = {}
    for name, factory in no_param_endpoints.items():
        result = await _safe_call(name, factory())
        results.append(result)

        if result.success and name == "get_instances" and isinstance(result.data, list):
            for controller_entry in result.data:
                for inst in controller_entry.get("available_instances", []):
                    discovered.setdefault("instance_id", inst.get("instance_id"))
                    discovered.setdefault("instance_name", inst.get("instance_name"))
                    discovered.setdefault("module_name", inst.get("module"))

        if result.success and name == "get_datastores" and isinstance(result.data, list) and result.data:
            discovered.setdefault("datastore_id", result.data[0].get("id"))

    # Parameterized endpoints; skipped when the required value was never discovered.
    if "instance_id" in discovered:
        results.append(await _safe_call(
            "get_application_endpoints",
            ads.get_application_endpoints(instance_id=discovered["instance_id"], format_data=False, **rp),
        ))
    else:
        LOGGER.warning("Skipping get_application_endpoints; no instance_id discovered.")

    if "instance_name" in discovered:
        results.append(await _safe_call(
            "get_instance_network_info",
            ads.get_instance_network_info(instance_name=discovered["instance_name"], format_data=False, **rp),
        ))
    else:
        LOGGER.warning("Skipping get_instance_network_info; no instance_name discovered.")

    if "datastore_id" in discovered:
        results.append(await _safe_call(
            "get_datastore",
            ads.get_datastore(datastore_id=discovered["datastore_id"], format_data=False, **rp),
        ))
    else:
        LOGGER.warning("Skipping get_datastore; no datastore_id discovered.")

    if "module_name" in discovered:
        results.append(await _safe_call(
            "get_provision_arguments",
            ads.get_provision_arguments(module_name=discovered["module_name"], format_data=False, **rp),
        ))
    else:
        LOGGER.warning("Skipping get_provision_arguments; no module_name discovered.")

    await ads.clean_up()
    return results


async def capture_instance_responses(section: str = "LIVE") -> list[EndpointResult]:
    """Call read-only Instance and Minecraft endpoints with ``to_file=True`` to generate JSON response files.

    Discovers a running Minecraft instance via ``ADSModule.get_instances()`` and captures
    file manager, backup, analytics and Minecraft-specific endpoints against it.

    Parameters
    ----------
    section: :class:`str`
        The local.ini section to use for credentials, by default "LIVE".

    Returns
    -------
    list[:class:`EndpointResult`]
        A list of results for each endpoint call. Empty if no running Minecraft instance is found.

    """
    bridge = Bridge(api_params=get_api_params(section=section), singleton=True)
    bridge.use_2fa = True
    ads = ADSModule(bridge=bridge)

    rp: dict[str, Any] = {"to_file": True, "path": _response_dir}
    results: list[EndpointResult] = []

    # Discover a running Minecraft instance.
    try:
        controllers = await ads.get_instances(include_self=True)
    except Exception as e:  # noqa: BLE001
        LOGGER.error("Failed to fetch instances: %s", e)
        await ads.clean_up()
        return [EndpointResult(endpoint="get_instances", error=e)]

    mc_instances: list[Any] = []
    for controller_entry in controllers:
        for inst in controller_entry.get("available_instances", []):
            if inst.get("module") == "Minecraft":
                mc_instances.append(inst)

    mc_data = next((inst for inst in mc_instances if inst.get("running")), None)
    if mc_data is None:
        LOGGER.warning("No running Minecraft instance found; skipping instance captures.")
        await ads.clean_up()
        return results

    LOGGER.info("Using Minecraft instance: %s (%s)", mc_data.get("friendly_name"), mc_data.get("instance_id"))
    mc = MinecraftInstance(data=mc_data, session=ads.session)
    mc._instance_id = mc_data["instance_id"]  # pyright: ignore[reportPrivateUsage]
    mc._endpoint_url = f"{bridge.url}/API/ADSModule/Servers/{mc._instance_id}"  # pyright: ignore[reportPrivateUsage]

    endpoints: dict[str, Any] = {
        "get_backups": lambda: mc.get_backups(format_data=False, **rp),
        "get_directory_listing": lambda: mc.get_directory_listing(format_data=False, **rp),
        "get_file_chunk": lambda: mc.get_file_chunk(
            file_path="server.properties", index=0, length=512,
            format_data=False, **rp),
        "mc_get_op_whitelist": lambda: mc.mc_get_op_whitelist(format_data=False, **rp),
        "mc_get_whitelist": lambda: mc.mc_get_whitelist(format_data=False, **rp),
        "mc_load_op_list": lambda: mc.mc_load_op_list(format_data=False, **rp),
        "mc_buk_get_installed_plugins": lambda: mc.mc_buk_get_installed_plugins(format_data=False, **rp),
        "mc_buk_get_popular_plugins": lambda: mc.mc_buk_get_popular_plugins(format_data=False, **rp),
        "get_analytics_summary": lambda: mc.get_analytics_summary(format_data=False, **rp),
    }

    for name, factory in endpoints.items():
        results.append(await _safe_call(name, factory()))

    await ads.clean_up()
    return results


async def capture_all_responses(section: str = "LIVE") -> dict[str, list[EndpointResult]]:
    """Run all capture functions and return results grouped by module.

    Calls :func:`capture_responses` (Core), :func:`capture_ads_responses` (ADSModule) and
    :func:`capture_instance_responses` (Instance/Minecraft) in sequence.

    Parameters
    ----------
    section: :class:`str`
        The local.ini section to use for credentials, by default "LIVE".

    Returns
    -------
    dict[:class:`str`, list[:class:`EndpointResult`]]
        Results keyed by ``"core"``, ``"ads"`` and ``"instance"``.

    """
    return {
        "core": await capture_responses(section=section),
        "ads": await capture_ads_responses(section=section),
        "instance": await capture_instance_responses(section=section),
    }


async def capture_all_and_report(section: str = "LIVE") -> None:
    """Run :func:`capture_all_responses` and print a summary report for each module."""
    all_results = await capture_all_responses(section=section)

    for module_name, results in all_results.items():
        success_count = sum(1 for r in results if r.success)
        fail_count = sum(1 for r in results if not r.success)
        LOGGER.info("--- %s Response Capture Report ---", module_name.upper())
        LOGGER.info("Total: %d | Success: %d | Failed: %d", len(results), success_count, fail_count)
        for r in results:
            if r.success:
                LOGGER.info("  OK:   %s", r.endpoint)
            else:
                LOGGER.error("  FAIL: %s -> %s", r.endpoint, r.error)


# endregion

# region Dataclass Unpack Tests — Saved Responses


class TestSessionUnpack:
    """Verify Session dataclass unpacks directly from JSON without cast."""

    def test_unpack_all_sessions(self) -> None:  # noqa: D102
        if not _response_exists("getactiveampsessions.json"):
            pytest.skip("Response file not captured yet — run capture_responses() first")
        data: list[Any] = _load_response("getactiveampsessions.json")  # pyright: ignore[reportAssignmentType]
        assert isinstance(data, list)
        for entry in data:
            session = Session(**entry)
            assert isinstance(session.source, str)
            assert isinstance(session.session_id, str)
            assert isinstance(session.username, str)
            assert isinstance(session.session_type, str)
            assert isinstance(session.start_time, datetime.datetime)
            assert isinstance(session.last_activity, datetime.datetime)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getactiveampsessions.json"):
            pytest.skip("Response file not captured yet")
        data: list[Any] = _load_response("getactiveampsessions.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(Session)}
        for entry in data:
            assert set(entry.keys()) == dc_field_names, (
                f"Key mismatch: JSON has {set(entry.keys())}, dataclass has {dc_field_names}"
            )


class TestUserInfoUnpack:
    """Verify UserInfo dataclass unpacks directly from JSON without cast."""

    def test_unpack_all_users(self) -> None:  # noqa: D102
        if not _response_exists("getallampuserinfo.json"):
            pytest.skip("Response file not captured yet")
        data: list[Any] = _load_response("getallampuserinfo.json")  # pyright: ignore[reportAssignmentType]
        assert isinstance(data, list)
        for entry in data:
            user = UserInfo(**entry)
            assert isinstance(user.id, str)
            assert isinstance(user.name, str)
            assert isinstance(user.is_super_user, bool)
            assert isinstance(user.roles, list)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getallampuserinfo.json"):
            pytest.skip("Response file not captured yet")
        data: list[Any] = _load_response("getallampuserinfo.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(UserInfo)}
        for entry in data:
            assert set(entry.keys()) == dc_field_names, (
                f"Key mismatch: JSON has {set(entry.keys())}, dataclass has {dc_field_names}"
            )


class TestScheduleDataUnpack:
    """Verify ScheduleData dataclass unpacks directly from JSON without cast."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("getscheduledata.json"):
            pytest.skip("Response file not captured yet")
        data: dict[str, Any] = _load_response("getscheduledata.json")  # pyright: ignore[reportAssignmentType]
        assert isinstance(data, dict)
        schedule = ScheduleData(**data)
        assert isinstance(schedule.available_methods, list)
        assert isinstance(schedule.available_triggers, list)
        assert isinstance(schedule.populated_triggers, list)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getscheduledata.json"):
            pytest.skip("Response file not captured yet")
        data: dict[str, Any] = _load_response("getscheduledata.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(ScheduleData)}
        assert set(data.keys()) == dc_field_names, (
            f"Key mismatch: JSON has {set(data.keys())}, dataclass has {dc_field_names}"
        )


class TestLoginResultsUnpack:
    """Verify LoginResults dataclass unpacks directly from JSON without cast."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("login.json"):
            pytest.skip("Response file not captured yet")
        data: dict[str, Any] = _load_response("login.json")  # pyright: ignore[reportAssignmentType]
        assert isinstance(data, dict)
        login = LoginResults(**data)
        assert isinstance(login.success, bool)
        assert isinstance(login.result, int)
        assert isinstance(login.session_id, str)

    def test_nested_user_info(self) -> None:  # noqa: D102
        if not _response_exists("login.json"):
            pytest.skip("Response file not captured yet")
        data: dict[str, Any] = _load_response("login.json")  # pyright: ignore[reportAssignmentType]
        login = LoginResults(**data)
        assert login.user_info is not None
        if isinstance(login.user_info, dict):
            user = LoginUserInfo(**login.user_info)
            assert isinstance(user.id, str)
            assert isinstance(user.username, str)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("login.json"):
            pytest.skip("Response file not captured yet")
        data: dict[str, Any] = _load_response("login.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(LoginResults)}
        assert set(data.keys()) == dc_field_names, (
            f"Key mismatch: JSON has {set(data.keys())}, dataclass has {dc_field_names}"
        )


class TestActionResultUnpack:
    """Verify ActionResult dataclass unpacks from a typical ActionResultResponse shape."""

    @pytest.mark.parametrize(
        "response",
        [
            {"status": True, "reason": "", "result": ""},
            {"status": False, "reason": "Permission denied", "result": ""},
            {"status": True, "reason": None, "result": None},
        ],
    )
    def test_unpack_variants(self, response: dict[str, Any]) -> None:  # noqa: D102
        action = ActionResult(**response)
        assert isinstance(action.status, bool)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        dc_field_names = {f.name for f in fields(ActionResult)}
        assert dc_field_names == {"status", "reason", "result"}


# endregion

# region Dataclass Unpack Tests — Captured Responses (require capture_responses)


class TestDiagnosticsUnpack:
    """Verify Diagnostics dataclass unpacks directly from JSON."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("getdiagnosticsinfo.json"):
            pytest.skip("Response file not captured yet — run capture_responses() first")
        data: dict[str, Any] = _load_response("getdiagnosticsinfo.json")  # pyright: ignore[reportAssignmentType]
        diag = Diagnostics(**data)
        assert isinstance(diag.application_name, str)
        assert isinstance(diag.module, str)
        assert isinstance(diag.instance_id, str)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getdiagnosticsinfo.json"):
            pytest.skip("Response file not captured yet")
        data: dict[str, Any] = _load_response("getdiagnosticsinfo.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(Diagnostics)}
        assert set(data.keys()) == dc_field_names, (
            f"Key mismatch: JSON has {set(data.keys())}, dataclass has {dc_field_names}"
        )


class TestModuleUnpack:
    """Verify Module dataclass unpacks directly from JSON."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("getmoduleinfo.json"):
            pytest.skip("Response file not captured yet — run capture_responses() first")
        data: dict[str, Any] = _load_response("getmoduleinfo.json")  # pyright: ignore[reportAssignmentType]
        mod = Module(**data)
        assert isinstance(mod.module_name, str)
        assert isinstance(mod.instance_id, str)
        assert isinstance(mod.amp_version, str)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getmoduleinfo.json"):
            pytest.skip("Response file not captured yet")
        data: dict[str, Any] = _load_response("getmoduleinfo.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(Module)}
        assert set(data.keys()) == dc_field_names, (
            f"Key mismatch: JSON has {set(data.keys())}, dataclass has {dc_field_names}"
        )


class TestPortUnpack:
    """Verify Port dataclass unpacks directly from JSON."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("getportsummaries.json"):
            pytest.skip("Response file not captured yet — run capture_responses() first")
        data: list[Any] = _load_response("getportsummaries.json")  # pyright: ignore[reportAssignmentType]
        assert isinstance(data, list)
        for entry in data:
            port = Port(**entry)
            assert isinstance(port.name, str)
            assert isinstance(port.port, int)
            assert isinstance(port.listening, bool)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getportsummaries.json"):
            pytest.skip("Response file not captured yet")
        data: list[Any] = _load_response("getportsummaries.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(Port)}
        for entry in data:
            extra = set(entry.keys()) - dc_field_names
            missing = dc_field_names - set(entry.keys())
            assert not extra, f"Extra keys in JSON: {extra}"
            # missing is OK if those fields have defaults
            for m in missing:
                assert any(f.name == m and f.default is not f.default_factory for f in fields(Port)), (  # noqa: B023  # pyright: ignore[reportFunctionMemberAccess]
                    f"Missing key {m!r} has no default"
                )


class TestRoleUnpack:
    """Verify Role dataclass unpacks directly from JSON."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("getroledata.json"):
            pytest.skip("Response file not captured yet — run capture_responses() first")
        data: list[Any] = _load_response("getroledata.json")  # pyright: ignore[reportAssignmentType]
        assert isinstance(data, list)
        for entry in data:
            role = Role(**entry)
            assert isinstance(role.id, str)
            assert isinstance(role.name, str)
            assert isinstance(role.permissions, list)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getroledata.json"):
            pytest.skip("Response file not captured yet")
        data: list[Any] = _load_response("getroledata.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(Role)}
        for entry in data:
            assert set(entry.keys()) == dc_field_names, (
                f"Key mismatch: JSON has {set(entry.keys())}, dataclass has {dc_field_names}"
            )


class TestRunningTaskUnpack:
    """Verify RunningTask dataclass unpacks directly from JSON."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("gettasks.json"):
            pytest.skip("Response file not captured yet — run capture_responses() first")
        data: list[Any] = _load_response("gettasks.json")  # pyright: ignore[reportAssignmentType]
        assert isinstance(data, list)
        for entry in data:
            task = RunningTask(**entry)
            assert isinstance(task.id, str)
            assert isinstance(task.name, str)
            assert isinstance(task.start_time, datetime.datetime)
            assert isinstance(task.last_update_pushed, datetime.datetime)


class TestStatusUnpack:
    """Verify Status dataclass unpacks directly from JSON."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("getstatus.json"):
            pytest.skip("Response file not captured yet — run capture_responses() first")
        data: dict[str, Any] = _load_response("getstatus.json")  # pyright: ignore[reportAssignmentType]
        status = Status(**data)
        assert isinstance(status.uptime, str)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getstatus.json"):
            pytest.skip("Response file not captured yet")
        data: dict[str, Any] = _load_response("getstatus.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(Status)}
        extra = set(data.keys()) - dc_field_names
        assert not extra, f"Extra keys in JSON: {extra}"


class TestUpdateInfoUnpack:
    """Verify UpdateInfo dataclass unpacks directly from JSON."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("getupdateinfo.json"):
            pytest.skip("Response file not captured yet — run capture_responses() first")
        data: dict[str, Any] = _load_response("getupdateinfo.json")  # pyright: ignore[reportAssignmentType]
        info = UpdateInfo(**data)
        assert isinstance(info.update_available, bool)
        assert isinstance(info.version, str)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getupdateinfo.json"):
            pytest.skip("Response file not captured yet")
        data: dict[str, Any] = _load_response("getupdateinfo.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(UpdateInfo)}
        extra = set(data.keys()) - dc_field_names
        assert not extra, f"Extra keys in JSON: {extra}"


class TestUpdatesUnpack:
    """Verify Updates dataclass unpacks directly from JSON."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("getupdates.json"):
            pytest.skip("Response file not captured yet — run capture_responses() first")
        data: dict[str, Any] = _load_response("getupdates.json")  # pyright: ignore[reportAssignmentType]
        updates = Updates(**data)
        assert isinstance(updates.console_entries, list)
        assert isinstance(updates.messages, list)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getupdates.json"):
            pytest.skip("Response file not captured yet")
        data: dict[str, Any] = _load_response("getupdates.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(Updates)}
        extra = set(data.keys()) - dc_field_names
        assert not extra, f"Extra keys in JSON: {extra}"


class TestAuditLogEntryUnpack:
    """Verify AuditLogEntry dataclass unpacks directly from JSON."""

    def test_unpack(self) -> None:  # noqa: D102
        if not _response_exists("getauditlogentries.json"):
            pytest.skip("Response file not captured yet — run capture_responses() first")
        data: list[Any] = _load_response("getauditlogentries.json")  # pyright: ignore[reportAssignmentType]
        assert isinstance(data, list)
        for entry in data:
            log = AuditLogEntry(**entry)
            assert isinstance(log.message, str)
            assert isinstance(log.user, str)
            assert isinstance(log.timestamp, datetime.datetime)

    def test_no_extra_keys(self) -> None:  # noqa: D102
        if not _response_exists("getauditlogentries.json"):
            pytest.skip("Response file not captured yet")
        data: list[Any] = _load_response("getauditlogentries.json")  # pyright: ignore[reportAssignmentType]
        dc_field_names = {f.name for f in fields(AuditLogEntry)}
        for entry in data:
            assert set(entry.keys()) == dc_field_names, (
                f"Key mismatch: JSON has {set(entry.keys())}, dataclass has {dc_field_names}"
            )


# endregion
