from fastapi import UploadFile

from src.schemas.event.event_schema import EventInput
from src.services.event.parser.src.utils import get_source, parse_event


class Parser:

    def parse(self, source_link: str = None, source_file: UploadFile = None) -> EventInput:
        page = get_source(source_link, source_file)
        try:
            event_df, courses = parse_event(page)
            # init_entities_by_id
        except Exception as e:
            raise ValueError(f"Cant parse {source_link if source_link else source_file.filename}")
        event = EventInput(
            count=event_df.shape[0],
            source=source_link,
            status=True,
            splits=event_df.to_json(),
            courses=courses.to_json()
        )
        return event
