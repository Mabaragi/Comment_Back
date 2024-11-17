from pydantic import BaseModel, Field


class CommentCrawlRequest(BaseModel):
    episode_id: int = Field(
        description="크롤링 하고자 하는 소설 또는 웹툰의 시리즈 id",
        examples=[3123, 123],
    )
    series_id: int = Field(
        description="크롤링 하고자 하는 회차의 에피소드 id", examples=[123, 12333]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "episode_id": 59071959,
                "series_id": 59114404,
            }
        }
