from pprint import pprint
from typing import Union

from ampapi import *
from ampapi.dataclass import AnalyticsFilter, AnalyticsSummary, APIParams, Players
from ampapi.enums import *
from ampapi.instance import AMPADSInstance, AMPInstance, AMPMinecraftInstance

_params = APIParams(url="http://192.168.13.130:8080", user="bot_username", password="bot_password")


async def Sample_API() -> None:
    """
    Example API Function to call Endpoints.
    """
    _bridge = Bridge(api_params=_params)
    ADS: AMPControllerInstance = AMPControllerInstance()
    # By default all API calls will be formatted into Dataclasses if possible.
    # You can toggle format_data off with ANY of the API classes that inherit Base().
    ADS.format_data = False

    # This would populate the ADS class property .instances and .available_instances
    await ADS.get_instances(format_data=True)
    # We convert the ADS.instances attribute to a list for easier iteration.
    # The data is a set to prevent duplicates.
    ADSinstances = list(ADS.instances)
    arkinstance: Union[AMPInstance, None] = None
    mcinstance: Union[AMPInstance, AMPMinecraftInstance, None] = None
    # We can break out all our instances into their own attributes.
    for instance in ADSinstances:
        # Pre populated from the dataclass and has the API endpoints too!
        if isinstance(instance, (AMPADSInstance, AMPInstance, AMPMinecraftInstance)):
            if instance.friendly_name == "ArkInstance":
                arkinstance = instance
            elif instance.friendly_name == "Minecraft_PVP":
                mcinstance = instance

    if arkinstance is None or mcinstance is None or not isinstance(mcinstance, AMPMinecraftInstance):
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
    # Can be checked via `AMPInstance.Running`.
    # To keep this updated simply check.
    if mcinstance.running is True:
        print(f"{mcinstance.friendly_name} is Running Nyao~")

    elif mcinstance.running is False:
        print(f"{mcinstance.friendly_name} is Starting Nyao~")
        await mcinstance.start_instance()

    # You can also restart and stop the Instance too.
    await mcinstance.restart_instance()
    await mcinstance.stop_instance()

    # The State of the Application. eg. Running, Offline, Restarting, etc. See `types.py -> State_enum
    # This is NOT updated constantly. See about using `get_status()` to keep it current.
    if mcinstance.app_state == AMPInstanceState.stopped:
        await mcinstance.start_application()

    # You can also stop and update the application via
    await mcinstance.stop_application()
    await mcinstance.update_application()

    # To get more current Instance State check out.
    mcinstance.status.state
    mcinstance.app_state
    # To keep the `AMPInstance.State` property current; simply call the function below.
    await mcinstance.get_status()
    # You can also check Metrics of an Instance easily.
    mcinstance.status.metrics

    # Want to kick a random person? Here ya go~
    players: list[Players] = await mcinstance.get_user_list()
    await mcinstance.mc_kick_user_by_id(user_id=players[0].uuid)

    # Analytics Introduction -
    # Simply call the below method.
    # By default it will use current day and time and go back 30 days into the past from now.
    stats: AnalyticsSummary = await mcinstance.get_analytics_summary()
    pprint(stats)

    # Let's say you ONLY want US players.
    # First you create a filter, then pass the filter into the function call.
    filter_: AnalyticsFilter = AnalyticsFilter(country="US")
    await mcinstance.get_analytics_summary(filters=filter_)
