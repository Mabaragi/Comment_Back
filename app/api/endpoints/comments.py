from fastapi import APIRouter
from app.schemas.comment import *
from app.services.crawler import KakaoCommentCrawler

router = APIRouter()


@router.post("/crawl/")
async def crawl_comments(crawl_request: CommentCrawlRequest):    
    return
