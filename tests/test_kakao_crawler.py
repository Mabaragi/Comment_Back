import unittest, requests
from unittest.mock import patch, Mock
from src.crawler import (
    KakaoCommentCrawler,
    NoCommentError,
)  # Adjust the import as necessary


class TestKakaoCommentCrawler(unittest.TestCase):

    def setUp(self):
        self.crawler = KakaoCommentCrawler()
        self.series_id = 123456
        self.product_id = 654321

    @patch("crawler.requests.post")
    def test_crawl_episode_comments_success(self, mock_post):
        # Mock successful response with comments
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {
                "commentList": {
                    "isEnd": True,
                    "totalCount": 2,
                    "bestTotalCount": 0,
                    "selectedSortOpt": None,
                    "sortOptList": [],
                    "commentList": [
                        {
                            "commentUid": 1,
                            "comment": "Great episode!",
                            # ... other fields
                        },
                        {
                            "commentUid": 2,
                            "comment": "Looking forward to the next one.",
                            # ... other fields
                        },
                    ],
                }
            }
        }
        mock_post.return_value = mock_response

        result = self.crawler._crawl_episode_comments(
            series_id=self.series_id,
            product_id=self.product_id,
            page=0,
            sort_type="latest",
        )

        self.assertIn("commentList", result)
        self.assertEqual(result["commentList"]["totalCount"], 2)
        self.assertEqual(len(result["commentList"]["commentList"]), 2)
        mock_post.assert_called_once()

    @patch("crawler.requests.post")
    def test_crawl_episode_comments_no_comments(self, mock_post):
        # Mock response with no comments
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {
                "commentList": {
                    "totalCount": 0,
                    # ... other fields
                    "commentList:": {},
                }
            }
        }
        mock_post.return_value = mock_response

        with self.assertRaises(NoCommentError):
            self.crawler._crawl_episode_comments(
                series_id=self.series_id,
                product_id=self.product_id,
                page=0,
                sort_type="latest",
            )
        mock_post.assert_called_once()

    @patch("crawler.requests.post")
    def test_crawl_episode_comments_http_error(self, mock_post):
        # Mock an HTTP error
        mock_post.side_effect = requests.exceptions.HTTPError("500 Server Error")

        result = self.crawler._crawl_episode_comments(
            series_id=self.series_id,
            product_id=self.product_id,
            page=0,
            sort_type="latest",
        )

        self.assertEqual(result, {})
        mock_post.assert_called_once()

    @patch("crawler.requests.post")
    def test_get_comments_by_episode_multiple_pages(self, mock_post):
        # Mock responses for multiple pages
        mock_response_page1 = Mock()
        mock_response_page1.json.return_value = {
            "data": {
                "commentList": {
                    "isEnd": False,
                    "totalCount": 3,
                    "commentList": [
                        {"commentUid": 1, "comment": "First comment"},
                        {"commentUid": 2, "comment": "Second comment"},
                    ],
                }
            }
        }

        mock_response_page2 = Mock()
        mock_response_page2.json.return_value = {
            "data": {
                "commentList": {
                    "isEnd": True,
                    "totalCount": 3,
                    "commentList": [
                        {"commentUid": 3, "comment": "Third comment"},
                    ],
                }
            }
        }

        # Side effects for consecutive calls
        mock_post.side_effect = [mock_response_page1, mock_response_page2]

        comments = self.crawler.get_comments_by_episode(
            series_id=self.series_id, product_id=self.product_id
        )

        self.assertEqual(len(comments), 3)
        self.assertEqual(comments[0]["commentUid"], 1)
        self.assertEqual(comments[1]["commentUid"], 2)
        self.assertEqual(comments[2]["commentUid"], 3)
        self.assertEqual(mock_post.call_count, 2)

    @patch("crawler.requests.post")
    def test_get_comments_by_episode_no_comments(self, mock_post):
        # Mock response with no comments
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {"commentList": {"totalCount": 0, "commentList": []}}
        }
        mock_post.return_value = mock_response

        comments = self.crawler.get_comments_by_episode(
            series_id=self.series_id, product_id=self.product_id
        )

        self.assertEqual(comments, [])
        mock_post.assert_called_once()

    @patch("crawler.requests.post")
    def test_crawl_episode_comments_request_exception(self, mock_post):
        # Mock a generic request exception
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        result = self.crawler._crawl_episode_comments(
            series_id=self.series_id,
            product_id=self.product_id,
            page=0,
            sort_type="latest",
        )

        self.assertEqual(result, {})
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
