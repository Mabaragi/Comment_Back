import aiohttp, asyncio, logging
from .queries import COMMENT_QUERY, EPISODE_QUERY
from typing import List, Dict
from pprint import pprint


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NoCommentError(Exception):
    """크롤링 된 댓글이 없을때 발생하는 에러"""


class NoSeriesError(Exception):
    """시리즈가 없을때 발생하는 에러"""


class KakaoCommentCrawler:
    URL = "https://bff-page.kakao.com/graphql"
    HEADERS = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Referer": "https://page.kakao.com/",
        "accept": "*/*",
        "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
    }

    @classmethod
    async def _fetch(cls, session: aiohttp.ClientSession, body: Dict) -> Dict:
        try:
            async with session.post(
                cls.URL, headers=cls.HEADERS, json=body
            ) as response:
                response.raise_for_status()
                data = await response.json()
                # print(data)
                return data.get("data", {})
        except aiohttp.ClientError as err:
            logger.error(f"HTTP 요청 중 오류 발생: {err}")
            return {}

    @classmethod
    async def _crawl_episode_comments(
        cls,
        session: aiohttp.ClientSession,
        series_id: int,
        product_id: int,
        page: int,
        last_comment_uid: int = None,
    ) -> Dict:
        body = {
            "query": COMMENT_QUERY,
            "variables": {
                "commentListInput": {
                    "page": page,
                    "seriesId": series_id,
                    "productId": product_id,
                    "lastCommentUid": last_comment_uid,
                }
            },
        }
        return await cls._fetch(session, body)

    @classmethod
    async def get_comments_by_episode(
        cls, series_id: int, product_id: int
    ) -> List[Dict]:
        comments = []
        last_comment_uid = None
        page = 0

        async with aiohttp.ClientSession() as session:
            while True:
                await asyncio.sleep(0.5)  # 비동기 대기
                comment_data = await cls._crawl_episode_comments(
                    session, series_id, product_id, page, last_comment_uid
                )
                if page == 0:
                    comment_count = comment_data["commentList"][
                        "totalCount"
                    ]  # 첫번째 시도에서만 댓글 개수 셈
                    page_count = (comment_count - 1) // 25

                if not comment_data or "commentList" not in comment_data:
                    raise NoCommentError("댓글이 없습니다.")

                comment_list = comment_data["commentList"].get("commentList", [])
                if not comment_list:
                    raise NoCommentError("댓글이 없습니다.")

                comments.extend(comment_list)
                last_comment_uid = comment_list[-1]["commentUid"]
                logger.info(f"페이지 {page + 1} 댓글 {len(comments)}개 크롤링 완료.")
                page += 1

                if comment_data["commentList"].get("isEnd", False) or page > page_count:
                    break

        return comments

    @classmethod
    async def get_episode_by_series(cls, series_id: int, after: str = None) -> Dict:
        body = {
            "query": EPISODE_QUERY,
            "variables": {"seriesId": series_id, "after": after, "sortType": "asc"},
        }
        async with aiohttp.ClientSession() as session:
            data = await cls._fetch(session, body)
            if not data.get("contentHomeProductList"):
                raise NoSeriesError("해당 시리즈가 존재하지 않습니다.")
            return data.get("contentHomeProductList", {})

    async def get_all_episodes_by_series(cls, series_id: int) -> List[Dict]:
        episodes = await cls.get_episode_by_series(series_id)
        return episodes.get("edges", [])
