from fastapi import APIRouter, Depends, HTTPException
from app.schemas.comment import *
from app.services.crawler import KakaoCommentCrawler
from app.services.database import MongoDB
from ...dependencies import get_database
from typing import Optional
from pprint import pprint
from pymongo.errors import BulkWriteError

router = APIRouter()


@router.get("/products/{product_id}/comments/")
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


@router.post("/crawl/")
async def crawl_comments(
    crawl_request: CommentCrawlRequest,
    mongo: MongoDB = Depends(get_database),
) -> CommentCrawlResponse:
    series_id = crawl_request.series_id
    product_id = crawl_request.product_id
    collection = mongo.db.get_collection("comments")
    comments = await KakaoCommentCrawler.get_comments_by_episode(
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
        pass
    return CommentCrawlResponse(
        series_id=series_id, product_id=product_id, comment_count=comment_count
    )
