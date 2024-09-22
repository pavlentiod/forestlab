from pandas import Series

from src.services.single_event_data.single_event_data_service import SingleEventDataService


class StatLeg:
    """
    Class representing a specific leg in a certain event.
    This class provides methods to retrieve leg-specific statistics such as the leaderboard for that leg.
    """

    def __init__(self, leg_id: str, service: SingleEventDataService):
        """
        Initializes a StatLeg object with the leg's ID and the event data service.

        Args:
            leg_id (str): The ID of the leg.
            service (SingleEventDataService): The service providing access to event data.
        """
        self.service: SingleEventDataService = service
        self.data: dict = self.service.get_leg(leg_id).to_str()  # Leg data from the service

    def get_leaderboard(self, group_id: str = None) -> Series:
        """
        Retrieves the leaderboard for the leg, either for a specific group or for all participants.

        Args:
            group_id (str, optional): The ID of the group to filter the leaderboard by.
                                      If None, returns the leaderboard for all participants.

        Returns:
            Series: A pandas Series containing the sorted results (split times) for the leg.
                    Missing values are dropped.
        """
        if group_id:
            # If group_id is provided, retrieve runners in that group and get their splits for the leg
            group_runners = self.service.get_group(group_id).to_str()['runners']
            return self.service.splits.loc[group_runners, self.data['id']].sort_values().dropna(how='all')
        else:
            # Otherwise, get splits for all runners in the leg
            return self.service.splits.loc[:, self.data['id']].sort_values().dropna(how='all')
