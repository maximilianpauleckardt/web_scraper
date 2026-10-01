import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_urls = ["https://www.boot.dev/blog/path/","https://www.boot.dev/blog/path","http://www.boot.dev/blog/path/","http://www.boot.dev/blog/path"]
        actual = list(map(normalize_url,input_urls))
        expected = "www.boot.dev/blog/path"
        for url in actual:
            self.assertEqual(url, expected)
    
    def test_get_heading_from_html(self):
        example_html_1 = "<html><body><h1>Welcome to Boot.dev</h1></body></html>"
        example_html_2 = "<html><body><h2>Hello from Boot.dev</h2></body></html>"
        example_html_3 = "<html><body></body></html>"
        test_1 = get_heading_from_html(example_html_1)
        test_2 = get_heading_from_html(example_html_2)
        test_3 = get_heading_from_html(example_html_3)
        expected = {"<h1>":"Welcome to Boot.dev","<h2>":"Hello from Boot.dev","empty":""}
        self.assertEqual(test_1, expected["<h1>"])
        self.assertEqual(test_2, expected["<h2>"])
        self.assertEqual(test_3, expected["empty"])
    
    def test_get_first_paragraph_from_html(self):
        example_html_1 = "<html><body><p>Learn to code by building real projects.</p><main></main></body></html>"
        example_html_2 = "<html><body><main><p>This is the second paragraph.</p></main></body></html>"
        example_html_3 = "<html><body></body></html>"
        test_1 = get_first_paragraph_from_html(example_html_1)
        test_2 = get_first_paragraph_from_html(example_html_2)
        test_3 = get_first_paragraph_from_html(example_html_3)
        expected = {"<body><p>":"Learn to code by building real projects.","<main><p>":"This is the second paragraph.","empty":""}
        self.assertEqual(test_1, expected["<body><p>"])
        self.assertEqual(test_2, expected["<main><p>"])
        self.assertEqual(test_3, expected["empty"])

    def test_get_urls_from_htmll(self):
        example_html = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        example_base_url = 'https://crawler-test.com'
        actual = get_urls_from_html(example_html, example_base_url)
        expected = ['https://crawler-test.com']
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()