import logging
from pprint import pprint
from typing import Union

import aiohttp

from ampapi import AnalyticsFilter, AnalyticsSummary, APIParams, Bridge, Controller, Instance, InstanceState, MinecraftInstance, Players
from ampapi.errors import AMPAPIError

_params = APIParams(url="http://192.168.13.130:8080", user="bot_username", password="bot_password")


async def Sample_API() -> None:
    """Example API Function to call Endpoints."""
    # The API also supports the ability to have an existing `aiohttp.ClientSession`;
    # Simply supply your existing session to the Controller
    # Make sure to close your session after running any code. (If needed)
    logger = logging.getLogger(__name__)
    _bridge = Bridge(api_params=_params)
    session: aiohttp.ClientSession = aiohttp.ClientSession()
    ADS: Controller = Controller(session=session)
    # By default all API calls will be formatted into Dataclasses if possible.
    # You can toggle format_data off with ANY of the API classes that inherit Base().
    ADS.format_data = False

    # This would populate the ADS class property .instances
    await ADS.get_instances(format_data=True)
    # We convert the ADS.instances attribute to a list for easier iteration.
    # The data is a set to prevent duplicates.
    ADSinstances = list(ADS.instances)
    arkinstance: Union[Instance, None] = None
    mcinstance: Union[Instance, MinecraftInstance, None] = None
    # We can break out all our instances into their own attributes.
    for instance in ADSinstances:
        # Pre populated from the dataclass and has the API endpoints too!
        if isinstance(instance, Instance):
            if instance.friendly_name == "ArkInstance":
                arkinstance = instance
            elif instance.friendly_name == "Minecraft_PVP":
                mcinstance = instance

    if arkinstance is None or mcinstance is None or not isinstance(mcinstance, MinecraftInstance):
        return
    # This turns back on data formatting Globally.
    arkinstance.format_data = True

    # You can take a backup really easily.
    await arkinstance.take_backup(name="ARK1_backup", description="This is an ARK backup", sticky=True)

    # Then you can call instance type specific API endpoints.
    await mcinstance.mc_add_to_whitelist(user_or_uuid="k8_thekat")

    # You can also check attributes and other fields of the instance for easy logic.
    if mcinstance.instance_name == "Test_Server":
        # do code here
        ...

    # The State of the Instance.
    # Can be checked via `Instance.running`.
    # This is cached, call `ADS.get_instances()` again to refresh it.
    if mcinstance.running is True:
        print(f"{mcinstance.friendly_name} is Running Nyao~")

    elif mcinstance.running is False:
        print(f"{mcinstance.friendly_name} is Starting Nyao~")
        await mcinstance.start_instance()

    # You can also restart and stop the Instance too.
    await mcinstance.restart_instance()
    await mcinstance.stop_instance()

    # The State of the Application. eg. ready, stopped, restarting, etc. See `_enums.py -> InstanceState`
    # This is NOT updated constantly. See about using `get_status()` to get it current.
    if mcinstance.app_state == InstanceState.stopped:
        await mcinstance.start_application()

    # You can also stop and update the application via
    await mcinstance.stop_application()
    await mcinstance.update_application()

    # To get the current Instance State call the function below, it returns a `Status` dataclass.
    status = await mcinstance.get_status()
    print(status.state)
    # You can also check Metrics of an Instance easily.
    print(status.metrics)

    # Errors are raised, not returned. Everything we raise inherits from `AMPAPIError` (see `ampapi.errors`).
    # Want to kick a random person? Here ya go~
    try:
        players: Players = await mcinstance.get_user_list()
    except AMPAPIError:
        logger.exception("Failed to retrieve Players")
        return
    await mcinstance.mc_kick_user_by_id(user_id=players.sorted[0].uuid)

    # Analytics Introduction -
    # Simply call the below method.
    # By default it will use current day and time and go back 30 days into the past from now.
    try:
        stats: AnalyticsSummary = await mcinstance.get_analytics_summary()
    except AMPAPIError:
        logger.exception("Failed to retrieve Stats")
        return
    pprint(stats)

    # Let's say you ONLY want US players.
    # First you create a filter, then pass the filter into the function call.
    filter_: AnalyticsFilter = AnalyticsFilter(country="US")
    await mcinstance.get_analytics_summary(filters=filter_)

    # Session closing..
    await session.close()
