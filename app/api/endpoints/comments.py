from fastapi import APIRouter, Depends
from app.schemas.comment import *
from app.services.crawler import KakaoCommentCrawler
from app.services.database import MongoDB
from ...dependencies import get_database

router = APIRouter()


@router.post("/crawl/")
async def crawl_comments(
    crawl_request: CommentCrawlRequest,
    mongo: dict[str, MongoDB] = Depends(get_database),
):
    series_id = crawl_request.series_id
    product_id = crawl_request.product_id
    database = mongo["mongo"].db
    collection = database.get_collection("comments")
    comments = await KakaoCommentCrawler.get_comments_by_episode(
        series_id=series_id, product_id=product_id
    )
    await collection.insert_many(documents=comments)
    comment_count = len(comments)
    return {"detail": f"{comment_count}개 댓글 크롤링 성공!"}