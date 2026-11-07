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
from typing import TYPE_CHECKING, Optional

from .base import Base

if TYPE_CHECKING:
    from ._types import TemplateResponse, TemplateSourceResponse, TemplateSyncResponse

__all__ = ("TemplateModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class TemplateModule(Base):
    """The calls for game templates, the definitions a shard is made from, and the git repositories they come from.

    .. versionadded:: 6.0.0

    """

    async def get_template(self, template_slug: str) -> TemplateResponse:
        """Get one template.

        |coro|

        Endpoint: ``GET /api/templates/{template_slug}``

        Parameters
        ----------
        template_slug : :class:`str`
            The template's slug, eg. ``"minecraft-java"``.

        Returns
        -------
        :class:`TemplateResponse`
            The template, the same as its entry in :meth:`get_templates`.

        """
        return await self._request(method="GET", path=f"/api/templates/{template_slug}")

    async def get_templates(self, *, source_id: Optional[str] = None) -> list[TemplateResponse]:
        """Get every template, or one source's.

        |coro|

        Endpoint: ``GET /api/templates``, or ``GET /api/templates/sources/{source_id}``

        .. note::
            Each template is its whole definition, so the full list is large: 248 templates came to about 29 MB.

        Parameters
        ----------
        source_id : Union[:class:`str`, None], optional
            Only the templates from this source, eg. ``"amp3"``, by default None.
            See :meth:`get_template_sources`.

        Returns
        -------
        list[:class:`TemplateResponse`]
            The templates.

        Raises
        ------
        AMPAPIRequestError
            If there's no source with that ID (404, its `message` an English sentence).

        """
        path: str = "/api/templates" if source_id is None else f"/api/templates/sources/{source_id}"
        return await self._request(method="GET", path=path)

    async def get_template_sources(self) -> list[TemplateSourceResponse]:
        """Get the git repositories templates come from.

        |coro|

        Endpoint: ``GET /api/templates/sources``

        Returns
        -------
        list[:class:`TemplateSourceResponse`]
            The sources, eg. ``"official"`` and ``"amp3"``.

        """
        return await self._request(method="GET", path="/api/templates/sources")

    async def sync_template_source(self, source_id: str) -> TemplateSyncResponse:
        """Fetch the newest templates from one source.

        |coro|

        Endpoint: ``POST /api/templates/sources/{source_id}/sync``

        Parameters
        ----------
        source_id : :class:`str`
            The source's ID, eg. ``"amp3"``.

        Returns
        -------
        :class:`TemplateSyncResponse`
            The commit the source is now at, and if it changed.

        """
        return await self._request(method="POST", path=f"/api/templates/sources/{source_id}/sync")

    async def sync_template_sources(self) -> list[TemplateSyncResponse]:
        """Fetch the newest templates from every source.

        |coro|

        Endpoint: ``POST /api/templates/sources/sync``

        Returns
        -------
        list[:class:`TemplateSyncResponse`]
            One result for each source.

        """
        return await self._request(method="POST", path="/api/templates/sources/sync")
