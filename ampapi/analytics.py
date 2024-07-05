from __future__ import annotations

from datetime import timedelta
from typing import Any, Union

from .base import Base
from .types import *

__all__ = ("AnalyticsPlugin",)


class AnalyticsPlugin(Base):
    """
    Contains the base functions for any `/API/AnalyticsPlugin/` AMP API endpoints.

    """
    # AnalyticsPlugin: GetAnalyticsSummary: Parameters: {'Name': 'PeriodDays', 'TypeName': 'Int32', 'Description': '', 'Optional': True} {'Name': 'StartDate', 'TypeName': 'Nullable<DateTime>', 'Description': '', 'Optional': True} {'Name': 'Filters', 'TypeName': 'Dictionary<String, String>', 'Description': '', 'Optional': True} ReturnTypeName: Object IsComplexType: False

    async def get_analytics_summary(self, period_days: int = 30, start_date: datetime = datetime.now(), filters: Union[Analytics_Filter, None] = None, format_data: Union[bool, None] = None) -> Analytics_Summary:
        """

        Retrieves the Analytics data for the Instance. \n
        See data such as how many people are playing, how long they've been playing, and where they are from.


        Args:
            period_days (int, optional): How far back in days to go. Defaults to 30.
            start_date (datetime, optional): From what date to go back from. Defaults to Current Date/Time. 
            filters (Union[Analytics_Filter, None], optional): Filters results based upon the supplied dataclass values. Defaults to None.\n
                See `types.py -> Analytics_Filter` for more information.
            format_data (Union[bool, None], optional): Format the JSON response data. Defaults to None. (Uses `FORMAT_DATA` global constant if None)

        Returns:
            Analytics_Summary: On success returns an Analytics_Summary dataclass.
                See `types.py -> Analytics_Summary`
        """

        await self._connect()
        if isinstance(start_date, datetime):
            date: float = start_date.timestamp()

        if filters is not None:
            if isinstance(filters, Analytics_Filter):
                data: dict[Any, Any] = self.dataclass_to_dict(dataclass=filters)
        else:
            data: dict[Any, Any] = {}

        parameters: dict[str, Any] = {
            "PeriodDays": period_days,
            "StartDate": date,
            "Filters": data,
        }
        result = await self._call_api(api="AnalyticsPlugin/GetAnalyticsSummary", parameters=parameters, format_data=format_data, format=Analytics_Summary)
        return result
