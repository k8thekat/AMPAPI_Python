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

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from ._enums import TaskState
from .base import Base

if TYPE_CHECKING:
    from ._types import RunningTaskResponse

__all__ = ("TaskModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class TaskModule(Base):
    """The calls for running tasks, the long jobs such as a shard update or an import.

    .. versionadded:: 6.0.0

    """

    # TODO: A `Task` object, once the tasks hub gives live progress (#47.2).

    # TODO: Type the reply once AMP is seen cancelling a task live (#47.11).
    # Every task seen had `isCancellable` set to `False`, so only the 409 refusal was captured.
    async def cancel_running_task(self, task_id: str) -> Any:
        """Ask AMP to stop a running task.

        |coro|

        Endpoint: ``POST /api/running-tasks/{task_id}/cancel``

        Parameters
        ----------
        task_id : :class:`str`
            The task's ID.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        Raises
        ------
        AMPAPIRequestError
            If the task can't be cancelled or has finished (409).

        """
        return await self._request(method="POST", path=f"/api/running-tasks/{task_id}/cancel", data={})

    async def delete_running_task(self, task_id: str) -> None:
        """Dismiss a finished task, so it leaves the list at once.

        |coro|

        Endpoint: ``DELETE /api/running-tasks/{task_id}``

        Parameters
        ----------
        task_id : :class:`str`
            The task's ID.

        Raises
        ------
        AMPAPIRequestError
            If the task is still running (409).

        """
        await self._request(method="DELETE", path=f"/api/running-tasks/{task_id}")

    async def get_running_tasks(self) -> list[RunningTaskResponse]:
        """Get the tasks running now, and those that finished in the last few seconds.

        |coro|

        Endpoint: ``GET /api/running-tasks``

        Returns
        -------
        list[:class:`RunningTaskResponse`]
            The tasks, each `state` a :class:`TaskState`.

        """
        result: list[RunningTaskResponse] = await self._request(method="GET", path="/api/running-tasks")
        for task in result:
            task["state"] = self._to_enum(TaskState, task["state"])
        return result
