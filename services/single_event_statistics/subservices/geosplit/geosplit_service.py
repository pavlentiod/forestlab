from matplotlib import pyplot as plt
from pandas import DataFrame
import matplotlib
from pandas import DataFrame

matplotlib.use('TkAgg')
from src.schemas.single_event_statistics.single_event_statistics_schema import RunnerLegStatistics, RunnerStatistics, \
    RunnerLegGEOStatistics
from src.schemas.track.track_schema import TrackInDB
from src.services.track.subservices.gpx_transformer.utils import haversine

METRE_IN_KM = 1000


class GeoSplitService:

    def __init__(self, track: TrackInDB):
        self.distance: float = track.distance
        self.elevation: float = track.elevation
        self.duration: float = track.duration
        self.points: DataFrame = DataFrame(track.points).astype({"time": "datetime64[ns, UTC]"})

    def get_runner_leg_stat(self, leg_stat: RunnerLegStatistics) -> RunnerLegGEOStatistics:
        leg_start_point = leg_stat.gen_time - leg_stat.split

        leg_points: DataFrame = self.points.loc[leg_start_point:leg_stat.gen_time]

        leg_length = haversine(leg_points['lon'].iloc[0], leg_points['lat'].iloc[0],
                               leg_points['lon'].iloc[leg_stat.split],
                               leg_points['lat'].iloc[leg_stat.split])
        path_length = sum(
            [haversine(leg_points['lon'].iloc[i], leg_points['lat'].iloc[i], leg_points['lon'].iloc[i + 1],
                       leg_points['lat'].iloc[i + 1]) for i
             in range(len(leg_points) - 1)])
        el = leg_points['ele'].to_list()
        total_elevation = sum(max(0, e1 - e0) for e0, e1 in zip(el, el[1:]))

        leg_geo_stats = {
            "ele": int(total_elevation),
            "length": int(leg_length * METRE_IN_KM),
            "path": int(path_length * METRE_IN_KM)
        }
        return RunnerLegGEOStatistics(**leg_geo_stats)

    def get_runner_legs_stat(self, stat: RunnerStatistics, course_start: str):
        start_index = self.points[self.points['time'] == course_start].index[0]
        self.points = self.points.loc[start_index:, :].reset_index(drop=True)
        geo_course_statistics = []
        for leg in stat.course_stat:
            if leg.gen_time <= self.duration - start_index:
                leg.geo_stat = self.get_runner_leg_stat(leg)
            geo_course_statistics.append(leg)
        stat.course_stat = geo_course_statistics
        return stat
