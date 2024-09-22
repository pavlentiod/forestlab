from fastapi import UploadFile

from src.schemas.event.event_schema import EventInput
from src.services.event.subservices.parser.src.init_db_entities import init_event_entities
from src.services.event.subservices.parser.src.web_parse import parse_event, get_source


class Parser:
    """
    Parser class to process event data from a source link or uploaded file
    and generate an EventInput schema.
    """

    def parse(self, source_link: str = None, source_file: UploadFile = None) -> EventInput:
        """
        Parse the event data from the provided source link or file.

        Args:
            source_link (str): URL link to the event source.
            source_file (UploadFile): Uploaded file containing the event data.

        Returns:
            EventInput: Parsed event data encapsulated in the EventInput schema.
        """
        # Fetch the source data from link or file
        page = get_source(source_link, source_file)
        try:
            # Parse the event data into a DataFrame and list of courses
            event_df, courses = parse_event(page)
        except Exception as e:
            raise ValueError(f"Can't parse {source_link if source_link else source_file.filename}")

        # Initialize event entities and return the result
        event = init_event_entities(event_df, courses)
        return event
