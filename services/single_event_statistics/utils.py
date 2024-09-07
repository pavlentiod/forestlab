from typing import Dict
from uuid import uuid4, UUID

from pandas import DataFrame

from src.schemas.single_event_statistics.single_event_schema import LegOutput, CourseOutput


def create_legs_id(legs: list) -> Dict[UUID]:
    return {leg: uuid4() for leg in legs}


def create_courses_list(df: DataFrame, legs: Dict[UUID]):
    uniq_courses = df.drop_duplicates(subset=df.columns)
    courses = []
    for row in uniq_courses.iterrows():
        sorted_course = row[1].sort_values()
        course = {n: LegOutput(id=uuid4(), start=legs[leg][0], end=legs[leg[1]]) for n, leg in
                  enumerate(sorted_course.index)}
        courses.append(CourseOutput(id=uuid4(), points=course))
    return courses
