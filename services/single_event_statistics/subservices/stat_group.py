from typing import List
from pandas import Series

from src.schemas.event.event_schema import EventInDB
from src.services.single_event_data.single_event_data_service import SingleEventDataService


class StatGroup:
    """
    Class representing a specific group in a certain event.
    This class provides methods to retrieve group-specific statistics such as the leaderboard.
    """

    def __init__(self, group_id: str, service: SingleEventDataService):
        """
        Initializes a StatGroup object with the group's ID and the event data service.

        Args:
            group_id (str): The ID of the group.
            service (SingleEventDataService): The service providing access to event data.
        """
        self.service: SingleEventDataService = service
        self.data: dict = self.service.get_group(group_id).to_str()  # Group data from the service

    def get_leaderboard(self) -> Series:
        """
        Retrieves the leaderboard for the group based on the runner's results.

        Returns:
            Series: A pandas Series containing the sorted results (times) of the group's runners.
        """
        # Retrieve the list of runner IDs in the group
        names: List[str] = self.data['runners']
        # Fetch the results for the runners in the group and sort them to generate the leaderboard
        return self.service.results.loc[names].sort_values()
