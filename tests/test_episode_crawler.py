import pytest, logging
from pprint import pprint
from app.services.crawler import KakaoCommentCrawler, NoSeriesError


# @pytest.fixture
# def crawler():
#     """KakaoCommentCrawler 인스턴스를 생성하는 fixture."""
#     return KakaoCommentCrawler()


# @pytest.mark.skip
@pytest.mark.asyncio
async def test_no_comments_raise_error():
    series_id = 5907195912  # 없는 시리즈 아이디
    # with pytest.raises(NoSeriesError):
    #     crawler.get_episode_by_series(series_id=series_id)
    with pytest.raises(NoSeriesError):
        await KakaoCommentCrawler.get_episode_by_series(series_id=series_id)


episode_test_cases = [
    pytest.param(59071959, None, 59114404, id="시리즈 id, 시작화수 첫번째 에피소드 id"),
    pytest.param(
        59071959,
        None,
        59114401,
        marks=pytest.mark.xfail,
        id="시리즈 id, 시작 화수, 틀린 첫번째 에피소드 id",
    ),
    pytest.param(59071959, "6", 59124633, id="6화이후 25개 크롤링, 7번째 에피소드 id"),
    pytest.param(
        59071959,
        "6",
        59114404,
        marks=pytest.mark.xfail,
        id="6화이후 25개 크롤링, 1번째 에피소드 id",
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("series_id, after, first_episode", episode_test_cases)
async def test_episode_crawling(series_id: int, after: str, first_episode: int):
    episode_list = await KakaoCommentCrawler.get_episode_by_series(
        series_id=series_id, after=after
    )
    assert episode_list["edges"][0]["node"]["single"]["productId"] == first_episode


all_episode_test_cases = [pytest.param(59071959, id="시리즈 id")]


@pytest.mark.asyncio
@pytest.mark.parametrize("series_id", all_episode_test_cases)
async def test_all_episode_crawling(series_id):
    pass
