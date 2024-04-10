import unittest
from unittest.mock import patch
from newsappflask import newsappflask, get_articles_from_source

class TestGetArticlesFromSource(unittest.TestCase):
    def test_get_articles_from_source(self):
        sample_response = {
            'status': 'ok',
            'articles': [
                {'title': 'Article 1', 'description': 'Description 1', 'urlToImage': 'Image 1'},
                {'title': 'Article 2', 'description': 'Description 2', 'urlToImage': 'Image 2'},
            ]
        }
        with patch('newsapi.NewsApiClient.get_top_headlines') as mock_get_top_headlines:
            mock_get_top_headlines.return_value = sample_response
            articles, desc, img = get_articles_from_source('source_id')
            self.assertEqual(len(articles), 2)
            self.assertEqual(len(desc), 2)
            self.assertEqual(len(img), 2)

class TestBBCRoute(unittest.TestCase):
    def setUp(self):
        self.client = newsappflask.test_client()

    def test_bbc_route(self):
        with patch('newsappflask.get_articles_from_source') as mock_get_articles_from_source:
            mock_get_articles_from_source.return_value = (['Article 1'], ['Description 1'], ['Image 1'])
            response = self.client.get('/bbc')
            self.assertIn(b'Article 1', response.data)

if __name__ == '__main__':
    unittest.main()
