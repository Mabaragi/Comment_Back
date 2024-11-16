import asyncio, aiohttp
from src.crawler import KakaoCommentCrawler, NoSeriesError

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


async def _fetch(session: aiohttp.ClientSession, body):
    headers = HEADERS
    url = URL
    try:
        async with session.post(url=url, headers=headers, json=body) as response:
            response.raise_for_status()
            data = response.json().get("data", {})
            return data
    except aiohttp.ClientError as err:
        print(err)
        return {}
    pass


async def main():
    body = {
        "query": """
            query contentHomeProductList($seriesId: Long!) {
                contentHomeProductList(seriesId: $seriesId) {
                    totalCount
                    edges {
                        node {
                            id
                            title
                        }
                    }
                }
            }""",
        "variables": {"seriesId": 59071959},
    }
    result = await _fetch(aiohttp.ClientSession(), body=body)
    print(result)
    # crawler = KakaoCommentCrawler()
    # try:
    #     result = await crawler.get_episode_by_series(59071559)
    #     print(result)
    # except NoSeriesError as e:
    #     print(f"시리즈 오류 발생: {e}")
    # except Exception as e:
    #     print(f"예상치 못한 오류 발생: {e}")


if __name__ == "__main__":
    asyncio.run(main())

# fetch("https://bff-page.kakao.com/graphql", {
#   "headers": {
#     "accept": "*/*",
#     "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
#     "content-type": "application/json",
#     "priority": "u=1, i",
#     "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-site"
#   },
#   "referrer": "https://page.kakao.com/",
#   "referrerPolicy": "strict-origin-when-cross-origin",
#   "body": "{\"query\":\"\\n    query contentHomeProductList($after: String, $before: String, $first: Int, $last: Int, $seriesId: Long!, $boughtOnly: Boolean, $sortType: String) {\\n  contentHomeProductList(\\n    seriesId: $seriesId\\n    after: $after\\n    before: $before\\n    first: $first\\n    last: $last\\n    boughtOnly: $boughtOnly\\n    sortType: $sortType\\n  ) {\\n    totalCount\\n    pageInfo {\\n      hasNextPage\\n      endCursor\\n      hasPreviousPage\\n      startCursor\\n    }\\n    selectedSortOption {\\n      id\\n      name\\n      param\\n    }\\n    sortOptionList {\\n      id\\n      name\\n      param\\n    }\\n    edges {\\n      cursor\\n      node {\\n        ...SingleListViewItem\\n      }\\n    }\\n  }\\n}\\n    \\n    fragment SingleListViewItem on SingleListViewItem {\\n  id\\n  type\\n  thumbnail\\n  showPlayerIcon\\n  isCheckMode\\n  isChecked\\n  scheme\\n  row1\\n  row2\\n  row3 {\\n    badgeList\\n    text\\n    priceList\\n  }\\n  single {\\n    productId\\n    ageGrade\\n    id\\n    isFree\\n    thumbnail\\n    title\\n    slideType\\n    operatorProperty {\\n      isTextViewer\\n    }\\n  }\\n  isViewed\\n  eventLog {\\n    ...EventLogFragment\\n  }\\n  discountRate\\n  discountRateText\\n}\\n    \\n\\n    fragment EventLogFragment on EventLog {\\n  fromGraphql\\n  click {\\n    layer1\\n    layer2\\n    setnum\\n    ordnum\\n    copy\\n    imp_id\\n    imp_provider\\n  }\\n  eventMeta {\\n    id\\n    name\\n    subcategory\\n    category\\n    series\\n    provider\\n    series_id\\n    type\\n  }\\n  viewimp_contents {\\n    type\\n    name\\n    id\\n    imp_area_ordnum\\n    imp_id\\n    imp_provider\\n    imp_type\\n    layer1\\n    layer2\\n  }\\n  customProps {\\n    landing_path\\n    view_type\\n    helix_id\\n    helix_yn\\n    helix_seed\\n    content_cnt\\n    event_series_id\\n    event_ticket_type\\n    play_url\\n    banner_uid\\n  }\\n}\\n    \",\"variables\":{\"seriesId\":59071959,\"boughtOnly\":false,\"sortType\":\"asc\",\"after\":\"6\"}}",
#   "method": "POST",
#   "mode": "cors",
#   "credentials": "include"
# });
