"""Copyright (C) 2021-2026 Katelynn Cadwallader.

This file is part of AMPAPI_Python.

AMPAPI_Python is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3, or (at your option)
any later version.

AMPAPI_Python is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with AMPAPI_Python; see the file COPYING.  If not, write to the Free
Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
02110-1301, USA.
"""

# This is a sample script, not a module of a package
# ruff: noqa: INP001

import logging
from typing import Union

import aiohttp

from ampapi import (
    AnalyticsFilter,
    AnalyticsSummary,
    APIParams,
    Bridge,
    Controller,
    Instance,
    InstanceState,
    MinecraftInstance,
    Players,
    Status,
)
from ampapi.errors import AMPAPIError

# These are placeholders, fill in your own
_params = APIParams(url="http://192.168.13.130:8080", user="bot_username", password="bot_password")  # noqa: S106


async def sample_api() -> None:
    """Example API Function to call Endpoints."""
    # The API also supports the ability to have an existing `aiohttp.ClientSession`;
    # Simply supply your existing session to the Bridge, and every API class made with it uses that session
    # Make sure to close your session after running any code, the API never closes one you passed in. (If needed)
    logger = logging.getLogger(__name__)
    # _bridge = Bridge(api_params=_params)
    session: aiohttp.ClientSession = aiohttp.ClientSession()
    _bridge = Bridge(api_params=_params, session=session)
    # ADS: Controller = Controller(session=session)
    ads: Controller = Controller()
    # By default all API calls will be formatted into Dataclasses if possible.
    # You can toggle format_data off with ANY of the API classes that inherit Base().
    ads.format_data = False

    # This would populate the ads class property .instances
    await ads.get_instances(format_data=True)
    # We convert the ads.instances attribute to a list for easier iteration.
    # The data is a set to prevent duplicates.
    ads_instances = list(ads.instances)
    arkinstance: Union[Instance, None] = None
    mcinstance: Union[Instance, MinecraftInstance, None] = None
    # We can break out all our instances into their own attributes.
    for instance in ads_instances:
        # Pre populated from the dataclass and has the API endpoints too!
        # if isinstance(instance, Instance):
        # Every converted Instance is already an `Instance`, so there is nothing to check
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
    # await mcinstance.mc_add_to_whitelist(user_or_uuid="k8_thekat")
    # AMP 2.6.5.0 removed the whitelist endpoints, so we send the server's own console command instead
    await mcinstance.send_console_message(msg="whitelist add k8_thekat")

    # You can also check attributes and other fields of the instance for easy logic.
    if mcinstance.instance_name == "Test_Server":
        # do code here
        ...

    # The State of the Instance.
    # Can be checked via `Instance.running`.
    # This is cached, call `ads.get_instances()` again to refresh it.
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
    # status = await mcinstance.get_status()
    # print(status.state)
    # A call gives the raw dict when `format_data` is off, so we ask for the dataclass and check we got it
    status = await mcinstance.get_status(format_data=True)
    if isinstance(status, Status):
        print(status.state)
        # You can also check Metrics of an Instance easily.
        print(status.metrics)

    # Errors are raised, not returned. Everything we raise inherits from `AMPAPIError` (see `ampapi.errors`).
    # Want to kick a random person? Here ya go~
    try:
        # players: Players = await mcinstance.get_user_list()
        players = await mcinstance.get_user_list(format_data=True)
    except AMPAPIError:
        logger.error("Failed to retrieve Players")
        return
    if isinstance(players, Players) and len(players.sorted) > 0:
        await mcinstance.mc_kick_user_by_id(user_id=players.sorted[0].uuid)

    # Analytics Introduction -
    # Simply call the below method.
    # By default it will use current day and time and go back 30 days into the past from now.
    try:
        # stats: AnalyticsSummary = await mcinstance.get_analytics_summary()
        stats = await mcinstance.get_analytics_summary(format_data=True)
    except AMPAPIError:
        logger.error("Failed to retrieve Stats")
        return
    # pprint(stats)
    if isinstance(stats, AnalyticsSummary):
        print(stats)

    # Let's say you ONLY want US players.
    # First you create a filter, then pass the filter into the function call.
    filter_: AnalyticsFilter = AnalyticsFilter(country="US")
    await mcinstance.get_analytics_summary(filters=filter_)

    # Session closing..
    await session.close()
