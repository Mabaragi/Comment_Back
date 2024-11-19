from typing import Optional
from pydantic import BaseModel, Field


class EpisodeCrawlRequest(BaseModel):
    series_id: int = Field(
        description="크롤링 하고자 하는 소설 또는 웹툰의 시리즈 id",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "series_id": 59071959,
            }
        }


class EpisodeCrawlResponse(BaseModel):
    series_id: int
    episode_count: int = 0
    duplicate_episodes: int = 0

    class Config:
        json_schema_extra = {
            "example": {
                "series_id": 65415225,
                "episode_count": 92,
                "duplicate_episodes": 0,
            }
        }
