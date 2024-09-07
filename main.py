import datetime

import pandas as pd

from src.database import db_helper


async def main():
    async with db_helper.session_factory() as session:
        print(pd.read_csv('c.csv').memory_usage().sum())
        # event_service = EventService(session)
        # request = EventEndpoint(title='ZZ',
        #                         source="https://o-site.spb.ru/_races/240901ZZ/240901zz_split.htm",
        #                         date=datetime.datetime.now().date())
        # ev = await event_service.create(request)






if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

