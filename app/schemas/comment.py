from pydantic import BaseModel, Field


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
                "series_id": 59071959,
                "product_id": 59124625,
            }
        }
