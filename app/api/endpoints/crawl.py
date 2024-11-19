from fastapi import APIRouter, Depends, HTTPException
from app.schemas.comment import *
from app.schemas.episodes import *
from app.services.crawler import KakaoPageCrawler
from app.services.database import MongoDB
from ...dependencies import get_database
from typing import Optional
from pprint import pprint
from pymongo.errors import BulkWriteError

router = APIRouter()


@router.get("/products/{product_id}/")
async def get_comments(
    product_id: int = 59124625,
    comment_id: Optional[int] = None,  # comment_id는 선택적
    mongo: MongoDB = Depends(get_database),
):
    product_id = product_id
    comment_id = comment_id
    collection = mongo.db.get_collection("comments")
    if comment_id == None:  # 프로덕트의 모든 댓글 반환
        comments_cursor = collection.find({"productId": product_id})
        comments = await comments_cursor.to_list(length=None)  # 결과를 리스트로 변환
        if not comments:  # 결과가 없는 경우
            raise HTTPException(status_code=404, detail="댓글이 존재하지 않습니다.")
        return {"comments": comments}


@router.post("/comments/")
async def crawl_comments(
    crawl_request: CommentCrawlRequest,
    mongo: MongoDB = Depends(get_database),
) -> CommentCrawlResponse:
    series_id = crawl_request.series_id
    product_id = crawl_request.product_id
    collection = mongo.db.get_collection("comments")
    comments = await KakaoPageCrawler.get_comments_by_episode(
        series_id=series_id, product_id=product_id
    )
    comment_count = len(comments)
    try:
        await collection.insert_many(documents=comments, ordered=False)  # 중복 무시
    except Exception as e:
        # 중복된 commentUid로 인해 발생하는 오류를 처리
        if isinstance(e, BulkWriteError):
            duplicate_num = len(e.details.get("writeErrors", []))
            return CommentCrawlResponse(
                series_id=series_id,
                product_id=product_id,
                comment_count=comment_count,
                duplicate_comments=duplicate_num,
            )
    return CommentCrawlResponse(
        series_id=series_id, product_id=product_id, comment_count=comment_count
    )


@router.post("/episodes/")
async def crawl_episodes(
    crawl_request: EpisodeCrawlRequest,
    mongo: MongoDB = Depends(get_database),
) -> EpisodeCrawlResponse:
    series_id = crawl_request.series_id
    collection = mongo.db.get_collection("episodes")
    episode_datas = await KakaoPageCrawler.get_all_episodes_by_series(
        series_id=series_id
    )
    episodes = [
        {**episode_data.get("node", {}).get("single", {}), "seriesId": series_id}
        for episode_data in episode_datas
    ]
    episode_count = len(episodes)
    try:
        await collection.insert_many(documents=episodes, ordered=False)  # 중복 무시
    except Exception as e:
        # 중복된 productId로 인해 발생하는 오류를 처리
        if isinstance(e, BulkWriteError):
            print(e)
            duplicate_num = len(e.details.get("writeErrors", []))
            return EpisodeCrawlResponse(
                series_id=series_id,
                episode_count=episode_count,
                duplicate_episodes=duplicate_num,
            )
        pass
    return EpisodeCrawlResponse(series_id=series_id, episode_count=episode_count)
