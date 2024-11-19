from typing import Optional
from pydantic import BaseModel, Field


class CommentRequest(BaseModel):
    product_id: int
    comment_id: Optional[int] = None


class CommentCrawlRequest(BaseModel):
    series_id: int = Field(
        description="크롤링 하고자 하는 소설 또는 웹툰의 시리즈 id",
    )
    product_id: int = Field(
        description="크롤링 하고자 하는 에피소드 id",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "series_id": 65404339,
                "product_id": 65415225,
            }
        }


class CommentCrawlResponse(BaseModel):
    series_id: int
    product_id: int
    comment_count: int
    duplicate_comments: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "series_id": 65415225,
                "product_id": 65415225,
                "comment_count": 12,
                "duplicate_comments": 0,
            }
        }
