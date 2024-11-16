import requests

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
    "Referrer-Policy": "strict-origin-when-cross-origin",
}
body = {
    "query": """
    query contentHomeProductList($after: String, $before: String, $first: Int, $last: Int, $seriesId: Long!, $boughtOnly: Boolean, $sortType: String) {
      contentHomeProductList(
        seriesId: $seriesId
        after: $after
        before: $before
        first: $first
        last: $last
        boughtOnly: $boughtOnly
        sortType: $sortType
      ) {
        totalCount
        pageInfo {
          hasNextPage
          endCursor
          hasPreviousPage
          startCursor
        }
        selectedSortOption {
          id
          name
          param
        }
        sortOptionList {
          id
          name
          param
        }
        edges {
          cursor
          node {
            ...SingleListViewItem
          }
        }
      }
    }
    
    fragment SingleListViewItem on SingleListViewItem {
      id
      type
      thumbnail
      showPlayerIcon
      isCheckMode
      isChecked
      scheme
      row1
      row2
      row3 {
        badgeList
        text
        priceList
      }
      single {
        productId
        ageGrade
        id
        isFree
        thumbnail
        title
        slideType
        operatorProperty {
          isTextViewer
        }
      }
      isViewed
      eventLog {
        ...EventLogFragment
      }
      discountRate
      discountRateText
    }
    
    
    fragment EventLogFragment on EventLog {
      fromGraphql
      click {
        layer1
        layer2
        setnum
        ordnum
        copy
        imp_id
        imp_provider
      }
      eventMeta {
        id
        name
        subcategory
        category
        series
        provider
        series_id
        type
      }
      viewimp_contents {
        type
        name
        id
        imp_area_ordnum
        imp_id
        imp_provider
        imp_type
        layer1
        layer2
      }
      customProps {
        landing_path
        view_type
        helix_id
        helix_yn
        helix_seed
        content_cnt
        event_series_id
        event_ticket_type
        play_url
        banner_uid
      }
    }
    """,
    "variables": {
        "seriesId": 59071959,
    },
}

response = requests.post(url=URL, headers=HEADERS, json=body).json()["data"][
    "contentHomeProductList"
]["edges"][0]["node"]["single"]["productId"]

print(response)
