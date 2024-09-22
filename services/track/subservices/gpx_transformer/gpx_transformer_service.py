import json
from datetime import datetime, timedelta
from typing import Optional, List, Tuple

import numpy as np
import pandas as pd
from lxml import etree

from src.schemas.track.track_schema import TrackInput, TrackData
from src.services.track.subservices.gpx_transformer.utils import haversine

METRE_IN_KM = 1000


class GPXTransformer:
    """
    A class for transforming GPX data to extract geographical and temporal data.
    """

    def __init__(self, file_content: bytes):
        """
        Initializes the GPXTransformer with a string of XML content.

        Args:
            file_content (str): A string containing GPX data.
        """
        self.file_content = file_content
        self.parser = etree.XMLParser(remove_blank_text=True)
        self.json_data = None
        self._name: Optional[str] = None
        self._time_list: Optional[List[datetime]] = None
        self._coordinates_list: Optional[List[float]] = None
        self._elevations_list: Optional[List[float]] = None
        self._total_distance: Optional[float] = None
        self._total_duration: Optional[float] = None
        self._total_elevation: Optional[int] = None
        self._starting_point: Optional[Tuple[float, float]] = None
        self._paired_data: Optional[List[List]] = None

    @property
    def root(self) -> etree._Element:
        """
        Returns the root element of the parsed XML tree.

        Returns:
            etree._Element: The root of the XML tree.
        """
        root = self.tree.getroot()
        return root

    @property
    def tree(self) -> etree._ElementTree:
        """
        Parses and returns the XML tree.

        Returns:
            etree._ElementTree: The parsed XML tree.
        """
        if not self.file_content:
            raise ValueError("The provided GPX data is empty or None.")

        # Ensure content is a string
        # if isinstance(self.file_content, bytes):
        #     self.file_content = self.file_content.decode('utf-8')

        try:
            tree = etree.fromstring(self.file_content, self.parser)
            tree = self.strip_ns_prefix(tree)
            return etree.ElementTree(tree)
        except etree.XMLSyntaxError as e:
            raise ValueError(f"Invalid XML content: {e}")

    def strip_ns_prefix(self, tree: etree._ElementTree) -> etree._ElementTree:
        """
        Removes XML namespace prefixes from all elements in the tree.

        Args:
            tree (etree._ElementTree): The XML tree.

        Returns:
            etree._ElementTree: The tree with namespace prefixes removed.
        """
        query = "descendant-or-self::*[namespace-uri()!='']"
        for element in tree.xpath(query):
            element.tag = etree.QName(element).localname
        return tree

    @property
    def coordinates_list(self) -> List[float]:
        """
        Returns a list of coordinates (longitude, latitude) from the GPX data.

        Returns:
            List[float]: List of alternating longitude and latitude values.
        """
        if self._coordinates_list:
            return self._coordinates_list

        coordinates_list = []
        elements = list(self.root.iter('trkpt')) or list(self.root.iter('rtept'))
        for element in elements:
            lon = float(element.attrib.get('lon'))
            lat = float(element.attrib.get('lat'))
            coordinates_list.extend([lon, lat])
        self._coordinates_list = coordinates_list
        return self._coordinates_list

    @property
    def time_list(self) -> List[datetime]:
        """
        Returns a list of time points from the GPX data.

        Returns:
            List[datetime]: List of datetime objects for each time point.
        """
        if self._time_list:
            return self._time_list

        time_list = []
        elements = list(self.root.iter('time'))
        for element in elements:
            time = datetime.strptime(element.text, '%Y-%m-%dT%H:%M:%SZ')
            time_list.append(time)
        self._time_list = time_list
        return self._time_list

    @property
    def elevation_list(self) -> List[float]:
        """
        Returns a list of elevation data from the GPX data.

        Returns:
            List[float]: List of elevation values.
        """
        if self._elevations_list:
            return self._elevations_list

        elevations_list = []
        for element in self.root.iter('trkpt'):
            ele = element.findtext('ele')
            if ele:
                elevations_list.append(float(ele))
        self._elevations_list = elevations_list
        return self._elevations_list

    @property
    def paired_data(self) -> List[List]:
        """
        Returns paired data containing time, latitude, longitude, and elevation.

        Returns:
            List[List]: Paired data of (time, lon, lat, elevation).
        """
        if self._paired_data:
            return self._paired_data

        time_list = self.time_list
        elevations_list = self.elevation_list
        coordinates_list = self.coordinates_list
        self._paired_data = [list(z) for z in
                             zip(time_list, coordinates_list[::2], coordinates_list[1::2], elevations_list)]
        return self._paired_data

    @property
    def total_elevation(self) -> int:
        """
        Returns the total positive gain in elevation.

        Returns:
            int: The total elevation gain.
        """
        if self._total_elevation:
            return self._total_elevation

        el = self.elevation_list
        total_elevation = sum(max(0, e1 - e0) for e0, e1 in zip(el, el[1:]))
        self._total_elevation = int(total_elevation)
        return self._total_elevation

    @property
    def total_duration(self):
        """
        Returns total time duration.
        """
        if self._total_duration:
            return self._total_duration

        total_duration = pd.Timestamp(self.time_list[-1]) - pd.Timestamp(self.time_list[0])
        self._total_duration = total_duration
        return self._total_duration

    @property
    def total_distance(self) -> float:
        """
        Returns the total distance between all coordinate points.

        Returns:
            float: The total distance in kilometers.
        """
        if self._total_distance:
            return self._total_distance

        cl = self.coordinates_list
        total_distance = sum(
            haversine(lon1, lat1, lon2, lat2) for lon1, lat1, lon2, lat2 in zip(cl[::2], cl[1::2], cl[2::2], cl[3::2]))
        self._total_distance = round(total_distance * METRE_IN_KM)
        return self._total_distance

    @property
    def starting_point(self) -> Tuple[float, float]:
        """
        Returns the first latitude and longitude pair from the GPX data.

        Returns:
            Tuple[float, float]: The first (lon, lat) coordinates.
        """
        if self._starting_point:
            return self._starting_point

        self._starting_point = (self.coordinates_list[0], self.coordinates_list[1])
        return self._starting_point

    def interp_points(self):
        paired_data = self.paired_data
        points = [
            {
                "time": entry[0],
                "lat": entry[2],
                "lon": entry[1],
                "elevation": entry[3]
            }
            for entry in paired_data
        ]
        time_range = int(round(self.total_duration.total_seconds()))
        start_time = points[0]['time']

        old_indexes = list(range(len(points)))
        time_indexes = list(range(time_range))
        lat_values = [i['lat'] for i in points]
        lon_values = [i['lon'] for i in points]
        ele_values = [i['elevation'] for i in points]

        interp_lat = np.interp(time_indexes, old_indexes, lat_values)
        interp_lon = np.interp(time_indexes, old_indexes, lon_values)
        interp_ele = np.interp(time_indexes, old_indexes, ele_values)
        interp_time = [(start_time + timedelta(seconds=i)).strftime('%Y-%m-%dT%H:%M:%SZ') for i, v in enumerate(time_indexes)]
        return [{
            "time": interp_time[i],
            "lat": interp_lat[i],
            "lon":interp_lon[i],
            "ele": interp_ele[i]
        } for i in time_indexes]


    def to_track_data(self) -> TrackData:
        """
        Converts the GPX data into a TrackData object.

        Returns:
            TrackData: A Pydantic model instance with track details.
        """
        points = self.interp_points()
        return TrackData(
            distance=self.total_distance,
            elevation=self.total_elevation,
            duration=self.total_duration.total_seconds(),
            points=points
        )
