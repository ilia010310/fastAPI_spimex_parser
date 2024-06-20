import asyncio
import time
from src.parser.collector_links import collector_links
from src.parser.core import async_inset_data
from src.parser.parser import parser_xls


async def main():
    links = await collector_links()
    for link, date in links:
        data_from_page = await parser_xls(link, date)
        await async_inset_data(data_from_page)


if __name__ == "__main__":
    start = time.monotonic()
    asyncio.run(main())
    end = time.monotonic()
    work_time = end - start
    print(f'Время выполнения программы: {int(work_time // 60)}мин. {int(work_time % 60)} сек.')
