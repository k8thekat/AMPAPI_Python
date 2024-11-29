from datetime import datetime
from typing import Any, Union

from .base import Base
from .dataclass import AnalyticsFilter, AnalyticsSummary

# from .enums import *

__all__ = ("AnalyticsPlugin",)


class AnalyticsPlugin(Base):
    """
    Contains the base functions for any `/API/AnalyticsPlugin/` AMP API endpoints.

    .. note::
        If the ``format_data`` parameter is None on any function; the global ``FORMAT_DATA`` will be used instead.


    """

    async def get_analytics_summary(
        self,
        period_days: int = 30,
        start_date: datetime = datetime.now(),
        filters: Union[AnalyticsFilter, None] = None,
        format_data: Union[bool, None] = None,
    ) -> AnalyticsSummary:
        """|coro|
        Retrieves the Analytics data for the Instance. \n
        See data such as how many people are playing, how long they've been playing, and where they are from.

        Parameters
        -----------
        period_days: :class:`int`, optional
            How far back in days to go, by default 30
        start_date: :class:`datetime.datetime`, optional
            The date to start from, by default :meth:`~datetime.datetime.now`
        filters: Union[:class:`AnalyticsFilter`, None], optional
            Filters results based upon the supplied dataclass values. See :class:`Analytics_Filter`, by default None
        format_data: Union[:class:`bool`, None], optional
            Format the JSON response data, by default None.

        Returns
        --------
        :class:`AnalyticsSummary`
            On success returns an :class:`AnalyticsSummary` dataclass.
        """
        await self._connect()
        if isinstance(start_date, datetime):
            date: float = start_date.timestamp()

        if filters is not None:
            if isinstance(filters, AnalyticsFilter):
                data: dict[Any, Any] = self.dataclass_to_dict(dataclass_=filters)
        else:
            data: dict[Any, Any] = {}

        parameters: dict[str, Any] = {
            "PeriodDays": period_days,
            "StartDate": date,
            "Filters": data,
        }
        result: Any = await self._call_api(
            api="AnalyticsPlugin/GetAnalyticsSummary",
            parameters=parameters,
            format_data=format_data,
            format_=AnalyticsSummary,
        )
        return result
