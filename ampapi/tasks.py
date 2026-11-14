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

from .base import Base
from .objects import RunningTask

if TYPE_CHECKING:
    from ._types import TaskResponse

__all__ = ("TaskModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class TaskModule(Base):
    """The calls for tasks, the long jobs such as a shard update or an import.

    .. versionadded:: 6.0.0

    """

    # TODO: A `Task` object, once the tasks hub gives live progress (#3-47.2).

    # TODO: Remove the warning once AMP honours a clone's cancel (U25).
    # AMP 3.0.0.6 answers it with 202, and the clone carries on copying.
    async def cancel_running_task(self, task_id: str) -> None:
        """Ask AMP to stop a running task.

        |coro|

        Endpoint: ``POST /api/running-tasks/{task_id}/cancel``

        Clone and move tasks (``"ShardClone"``, ``"ShardMigration"``) have `isCancellable` set and an update task
        doesn't, so cancelling an update is refused; :meth:`ShardModule.stop_shard` ends an update. To stop a shard
        move, use :meth:`ShardModule.cancel_shard_migration`.

        .. warning::
            Cancelling a clone is answered 202 and the clone's task reads `TaskState.cancelling`, then the clone carries
            on copying and completes.

        Parameters
        ----------
        task_id : :class:`str`
            The task's ID.

        Raises
        ------
        AMPAPIRequestError
            **404** - If the task has left the list.\n
            **409** - If the task can't be cancelled.

        """
        await self._request(method="POST", path=f"/api/running-tasks/{task_id}/cancel", data={})

    # TODO: Reword the warning once AMP's update honours the cancel (U33).
    # AMP 3.0.0.6 answers 202 and records the cancel, and the update carries on as if it hadn't been sent.
    async def cancel_task(self, task_id: str, *, tenant_id: str = "_root") -> None:
        """Ask AMP to stop a task, through the task's own record.

        |coro|

        Endpoint: ``POST /api/tasks/{tenant_id}/{task_id}/cancel``

        AMP answers at once (202) and passes the cancel to the shard the task works on, which stops the task at its next
        check. :meth:`get_task` shows the request as `cancellationRequestedAt`. A second cancel before the task finishes
        is answered 202 too.

        .. warning::
            AMP 3.0.0.6's shard update ignores the cancel: the task's record reads status 4 (cancel asked for) while the
            update carries on, whether the update was downloading, between steps or starting its container.
            :meth:`ShardModule.stop_shard` is what ends an update.

        Parameters
        ----------
        task_id : :class:`str`
            The task's ID, eg. the `taskId` from :meth:`ShardModule.update_shard`.
        tenant_id : :class:`str`, optional
            The task's tenant, its `tenantId`, by default ``"_root"``, the only tenant seen live.

        Raises
        ------
        AMPAPIRequestError
            **403** - If the logged in user may see the task but not stop it.\n
            **404** - If the logged in user can see no task with that ID.\n
            **409** - If the task has finished `tasks.error.alreadyComplete`.\n
            **409** - If the task works on no shard.

        """
        await self._request(method="POST", path=f"/api/tasks/{tenant_id}/{task_id}/cancel", data={})

    async def delete_running_task(self, task_id: str) -> None:
        """Dismiss a finished task, so the task leaves the list at once.

        |coro|

        Endpoint: ``DELETE /api/running-tasks/{task_id}``

        A failed task otherwise stays for about 30 minutes, through :meth:`ShardModule.delete_shard_migration` and, for
        a failed move, even the shard's purge.

        Parameters
        ----------
        task_id : :class:`str`
            The task's ID.

        Raises
        ------
        AMPAPIRequestError
            **409** - If the task is still running. A task still marked running can be dismissed once the task has
            stopped reporting for a couple of minutes.

        """
        await self._request(method="DELETE", path=f"/api/running-tasks/{task_id}")

    async def get_running_tasks(self) -> list[RunningTask]:
        """Get the logged in user's tasks running now, and their tasks that finished in the last few seconds, oldest first.

        |coro|

        Endpoint: ``GET /api/running-tasks``

        A failed task stays for about 30 minutes, unless :meth:`delete_running_task` dismisses the task or a later task of
        the same type on the same target ends. Nothing in the list says when a failed task will go.

        Returns
        -------
        list[:class:`RunningTask`]
            The tasks, each `state` a :class:`TaskState`.

        """
        result: list[dict[str, Any]] = await self._request(method="GET", path="/api/running-tasks")
        return [RunningTask(data=entry) for entry in result]

    async def get_task(self, task_id: str, *, tenant_id: str = "_root") -> TaskResponse:
        """Get AMP's record of one task, with each of its steps.

        |coro|

        Endpoint: ``GET /api/tasks/{tenant_id}/{task_id}``

        Unlike :meth:`get_running_tasks`, this call isn't limited to the logged in user's own tasks, and the record stays
        after the task leaves that list. A shard move's task has no record here (404), only an entry in
        :meth:`get_running_tasks`.

        Parameters
        ----------
        task_id : :class:`str`
            The task's ID, eg. the `taskId` from :meth:`ShardModule.update_shard`.
        tenant_id : :class:`str`, optional
            The task's tenant, its `tenantId`, by default ``"_root"``, the only tenant seen live.

        Returns
        -------
        :class:`TaskResponse`
            The task and its steps; not the same shape as a :class:`RunningTask`.

        Raises
        ------
        AMPAPIRequestError
            **404** - If the logged in user can see no task with that ID.\n
            **404** - If the task belongs to a shard move.

        """
        return await self._request(method="GET", path=f"/api/tasks/{tenant_id}/{task_id}")
