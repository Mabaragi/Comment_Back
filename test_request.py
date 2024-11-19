from app.services.crawler import KakaoCommentCrawler
import asyncio
from pprint import pprint

SERIES_ID = 59071959


async def main():
    result = await KakaoCommentCrawler.get_all_episodes_by_series(series_id=SERIES_ID)
    # pprint(result)


if __name__ == "__main__":
    asyncio.run(main())
