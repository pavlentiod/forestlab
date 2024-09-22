from datetime import datetime
from typing import Dict, List, Union
from uuid import UUID

from pydantic import BaseModel


class LegOutput(BaseModel):
    id: UUID
    start: int
    end: int

    @classmethod
    def convert_uuids_to_str(cls, obj):
        """Recursively converts UUID fields to strings."""
        if isinstance(obj, dict):  # If the object is a dictionary, iterate through items
            return {k: cls.convert_uuids_to_str(v) for k, v in obj.items()}
        elif isinstance(obj, list):  # If it's a list, apply conversion to each item
            return [cls.convert_uuids_to_str(i) for i in obj]
        elif isinstance(obj, UUID):  # Convert UUIDs to strings
            return str(obj)
        elif isinstance(obj, BaseModel):  # If it's a pydantic model, convert it to a dict first
            return cls.convert_uuids_to_str(obj.dict())
        else:
            return obj  # Return as is if no conversion is needed

    def to_str(self):
        """Convert all UUID fields to strings in this instance."""
        return self.convert_uuids_to_str(self.dict())


class CourseOutput(BaseModel):
    id: UUID
    points: Dict[int, Union[LegOutput, UUID]]

    @classmethod
    def convert_uuids_to_str(cls, obj):
        """Recursively converts UUID fields to strings."""
        if isinstance(obj, dict):  # If the object is a dictionary, iterate through items
            return {k: cls.convert_uuids_to_str(v) for k, v in obj.items()}
        elif isinstance(obj, list):  # If it's a list, apply conversion to each item
            return [cls.convert_uuids_to_str(i) for i in obj]
        elif isinstance(obj, UUID):  # Convert UUIDs to strings
            return str(obj)
        elif isinstance(obj, BaseModel):  # If it's a pydantic model, convert it to a dict first
            return cls.convert_uuids_to_str(obj.dict())
        else:
            return obj  # Return as is if no conversion is needed

    def to_str(self):
        """Convert all UUID fields to strings in this instance."""
        return self.convert_uuids_to_str(self.dict())


class RunnerOutput(BaseModel):
    id: UUID
    name: str
    surname: str
    result: int
    course: Union[CourseOutput, UUID]
    group: UUID

    @classmethod
    def convert_uuids_to_str(cls, obj):
        """Recursively converts UUID fields to strings."""
        if isinstance(obj, dict):  # If the object is a dictionary, iterate through items
            return {k: cls.convert_uuids_to_str(v) for k, v in obj.items()}
        elif isinstance(obj, list):  # If it's a list, apply conversion to each item
            return [cls.convert_uuids_to_str(i) for i in obj]
        elif isinstance(obj, UUID):  # Convert UUIDs to strings
            return str(obj)
        elif isinstance(obj, BaseModel):  # If it's a pydantic model, convert it to a dict first
            return cls.convert_uuids_to_str(obj.dict())
        else:
            return obj  # Return as is if no conversion is needed

    def to_str(self):
        """Convert all UUID fields to strings in this instance."""
        return self.convert_uuids_to_str(self.dict())


class GroupOutput(BaseModel):
    id: UUID
    name: str
    runners: List[Union[RunnerOutput, UUID]]
    courses: List[Union[CourseOutput, UUID]]

    @classmethod
    def convert_uuids_to_str(cls, obj):
        """Recursively converts UUID fields to strings."""
        if isinstance(obj, dict):  # If the object is a dictionary, iterate through items
            return {k: cls.convert_uuids_to_str(v) for k, v in obj.items()}
        elif isinstance(obj, list):  # If it's a list, apply conversion to each item
            return [cls.convert_uuids_to_str(i) for i in obj]
        elif isinstance(obj, UUID):  # Convert UUIDs to strings
            return str(obj)
        elif isinstance(obj, BaseModel):  # If it's a pydantic model, convert it to a dict first
            return cls.convert_uuids_to_str(obj.dict())
        else:
            return obj  # Return as is if no conversion is needed

    def to_str(self):
        """Convert all UUID fields to strings in this instance."""
        return self.convert_uuids_to_str(self.dict())


class EventOutput(BaseModel):
    id: UUID
    title: str
    count: int
    date: datetime
    source: str
    groups: List[GroupOutput]
    runners: List[RunnerOutput]
    courses: List[CourseOutput]
    legs: List[LegOutput]

    @classmethod
    def convert_uuids_to_str(cls, obj):
        """Recursively converts UUID fields to strings."""
        if isinstance(obj, dict):  # If the object is a dictionary, iterate through items
            return {k: cls.convert_uuids_to_str(v) for k, v in obj.items()}
        elif isinstance(obj, list):  # If it's a list, apply conversion to each item
            return [cls.convert_uuids_to_str(i) for i in obj]
        elif isinstance(obj, UUID):  # Convert UUIDs to strings
            return str(obj)
        elif isinstance(obj, BaseModel):  # If it's a pydantic model, convert it to a dict first
            return cls.convert_uuids_to_str(obj.dict())
        else:
            return obj  # Return as is if no conversion is needed

    def to_str(self):
        """Convert all UUID fields to strings in this instance."""
        return self.convert_uuids_to_str(self.dict())
