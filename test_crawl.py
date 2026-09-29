import unittest
from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_urls = ["https://www.boot.dev/blog/path/","https://www.boot.dev/blog/path","http://www.boot.dev/blog/path/","http://www.boot.dev/blog/path"]
        actual = list(map(normalize_url,input_urls))
        expected = "www.boot.dev/blog/path"
        for url in actual:
            self.assertEqual(url, expected)


if __name__ == "__main__":
    unittest.main()