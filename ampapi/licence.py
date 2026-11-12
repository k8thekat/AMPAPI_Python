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
from typing import TYPE_CHECKING, Any, Optional, Union

from .base import Base

if TYPE_CHECKING:
    from ._types import (
        LicenceAgreementResponse,
        LicenceQueryResponse,
        LicenceResponse,
        LicenceStatusResponse,
        LicenceTermsAcceptance,
        LicenceTermsRequest,
    )

__all__ = ("LicenceModule",)

LOGGER: logging.Logger = logging.getLogger(__name__)


class LicenceModule(Base):
    """The calls for the panel's licences: checking a key, activating it, its terms and removing it.

    .. versionadded:: 6.0.0

    """

    # TODO: Type the reply once AMP is seen answering it live (#3-47.10).
    # Only refusals are known; the reply to accepted terms isn't.
    async def accept_licence_terms(self, spire_id: str, grade_id: str, key: str, terms: LicenceTermsAcceptance) -> Any:
        """Accept the terms for a licence that is already active, eg. one whose `standing` is ``"TermsRequired"``.

        |coro|

        Endpoint: ``POST /api/licence/{spire_id}/{grade_id}/terms``

        Parameters
        ----------
        spire_id : :class:`str`
            The licence's `spireId`.
        grade_id : :class:`str`
            The licence's `gradeId`.
        key : :class:`str`
            The licence key.
        terms : :class:`LicenceTermsAcceptance`
            The terms acceptance, filled from :meth:`get_licence_agreement`.

        Returns
        -------
        Any
            AMP's reply as it came, `None` for an empty one.

        Raises
        ------
        AMPAPIRequestError
            If the licence needs no terms (400, ``"licence.error.termsNotApplicable"``), which is the case when
            :meth:`query_licence` reads `termsRequired` as `False`. A wrong `key` gets 502
            (``"licence.error.termsUnavailable"``), as AMP asks the licensing service before it checks the key.

        """
        data: LicenceTermsRequest = {**terms, "key": key}
        return await self._request(method="POST", path=f"/api/licence/{spire_id}/{grade_id}/terms", data=data)

    # TODO: Drop the note once AMP answers with the whole licence (U19b).
    # AMP 3.0.0.6 answers before the licence service does, with the limit, totals, issue date and terms all `None`.
    async def activate_licence(self, key: str, *, terms: Optional[LicenceTermsAcceptance] = None) -> LicenceResponse:
        """Activate a licence key on this panel.

        |coro|

        Endpoint: ``POST /api/licence``

        .. note::
            The reply comes back before the licence service answers, so its `shardLimit`, `keyShardsTotal`, `issuedAt`
            and terms versions are `None` and `limitKnown` is `False`. :meth:`get_licence_status` has them a few
            seconds later.

        The panel can restart once licensed: :meth:`PlatformModule.get_health_status` reads ``"starting"`` until it is
        ``"ready"`` again, and a setting read before then can look unapplied.

        Parameters
        ----------
        key : :class:`str`
            The licence key.
        terms : Union[:class:`LicenceTermsAcceptance`, None], optional
            The licence terms acceptance, by default None.
            Only a key whose `LicenceQueryResponse.termsRequired` is `True` needs one, see :meth:`query_licence`.

        Returns
        -------
        :class:`LicenceResponse`
            The licence AMP activated (201).

        """
        return await self._request(method="POST", path="/api/licence", data={"key": key, "terms": terms})

    async def delete_licence(self, spire_id: str, grade_id: str) -> None:
        """Remove a licence from the panel.

        |coro|

        Endpoint: ``DELETE /api/licence/{spire_id}/{grade_id}``

        With no licence left, :meth:`PlatformModule.get_health_status` reads ``"preview-licence"`` until one is
        activated again.

        Parameters
        ----------
        spire_id : :class:`str`
            The licence's `spireId`.
        grade_id : :class:`str`
            The licence's `gradeId`.

        Raises
        ------
        AMPAPIRequestError
            If the panel has no such licence, eg. it was removed already (404).

        """
        await self._request(method="DELETE", path=f"/api/licence/{spire_id}/{grade_id}")

    async def get_licence_agreement(self, version: int, *, language: Optional[str] = None) -> LicenceAgreementResponse:
        """Get the licence terms a key may need accepted.

        |coro|

        Endpoint: ``GET /api/licence/terms/agreement``

        Parameters
        ----------
        version : :class:`int`
            The terms version, a licence's `requiredTermsVersion`. An unknown one gets 404
            (``"licence.error.termsUnknownVersion"``).
        language : Union[:class:`str`, None], optional
            The language to read them in, eg. ``"fr"``, by default None.
            AMP sends English when it has no copy in that language.

        Returns
        -------
        :class:`LicenceAgreementResponse`
            The terms, with the hash and attestation a :class:`LicenceTermsAcceptance` sends back.

        """
        parameters: dict[str, Union[str, int]] = self._without_none(mapping={"version": version, "lang": language})
        return await self._request(method="GET", path="/api/licence/terms/agreement", parameters=parameters)

    async def get_licence_status(self) -> LicenceStatusResponse:
        """Get the panel's licences and how many shards they allow.

        |coro|

        Endpoint: ``GET /api/licence``

        Returns
        -------
        :class:`LicenceStatusResponse`
            The licences, with the shard count and limit.

        """
        return await self._request(method="GET", path="/api/licence")

    async def query_licence(self, key: str) -> LicenceQueryResponse:
        """Check what a licence key gives, without activating it.

        |coro|

        Endpoint: ``POST /api/licence/query``

        Parameters
        ----------
        key : :class:`str`
            The licence key.

        Returns
        -------
        :class:`LicenceQueryResponse`
            The key's product, grade and expiry, and if this panel can use it.

        """
        return await self._request(method="POST", path="/api/licence/query", data={"key": key})
