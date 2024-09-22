from pandas import Series

from src.services.single_event_data.single_event_data_service import SingleEventDataService


class StatCourse:
    """
    Class for one runner on certain event. Can calculate personal statistics on event
    """

    def __init__(self, course_id: str, service: SingleEventDataService):
        self.service: SingleEventDataService = service
        self.data = self.service.get_course(course_id).to_str()

    def get_leaderboard(self, group_id: str = None) -> Series:
        all_runners = self.service.runners

        if group_id:
            course_runners = [i for i, v in all_runners.items() if [v['course'], v['group']] == [self.data['id'], group_id]]
        else:
            course_runners = [i for i, v in all_runners.items() if v['course'] == self.data['id']]

        return self.service.results.loc[course_runners].sort_values()