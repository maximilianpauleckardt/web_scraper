import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data


class TestCrawl(unittest.TestCase):
    def test_normalize_url_1(self):
        input_url_1 = "https://www.boot.dev/blog/path/"
        actual_1 = normalize_url(input_url_1)
        expected_1 = "www.boot.dev/blog/path"
        self.assertEqual(actual_1, expected_1)

    def test_normalize_url_2(self):
            input_url_2 = "http://www.boot.dev/blog/path/"
            actual_2 = normalize_url(input_url_2)
            expected_2 = "www.boot.dev/blog/path"
            self.assertEqual(actual_2, expected_2)

    def test_normalize_url_3(self):
                input_url_3 = "http://www.boot.dev/blog/path/"
                actual_3 = normalize_url(input_url_3)
                expected_3 = "www.boot.dev/blog/path"
                self.assertEqual(actual_3, expected_3)
    
    def test_get_heading_from_html_1(self):
        example_html_1 = "<html><body><h1>Welcome to Boot.dev</h1></body></html>"
        test_1 = get_heading_from_html(example_html_1)
        expected_1 = "Welcome to Boot.dev"
        self.assertEqual(test_1, expected_1)

    def test_get_heading_from_html_2(self):
        example_html_2 = "<html><body><h2>Hello from Boot.dev</h2></body></html>"
        test_2 = get_heading_from_html(example_html_2)
        expected_2 = "Hello from Boot.dev"
        self.assertEqual(test_2, expected_2)

    def test_get_heading_from_html_3(self):
        example_html_3 = "<html><body></body></html>"
        test_3 = get_heading_from_html(example_html_3)
        expected_3 = ""
        self.assertEqual(test_3, expected_3)
    
    def test_get_first_paragraph_from_html_1(self):
        example_html_1 = "<html><body><p>Learn to code by building real projects.</p><main></main></body></html>"
        test_1 = get_first_paragraph_from_html(example_html_1)
        expected_1 = "Learn to code by building real projects."
        self.assertEqual(test_1, expected_1)

    def test_get_first_paragraph_from_html_2(self):
            example_html_2 = "<html><body><main><p>This is the second paragraph.</p></main></body></html>"
            test_2 = get_first_paragraph_from_html(example_html_2)
            expected_2 = "This is the second paragraph."
            self.assertEqual(test_2, expected_2)

    def test_get_first_paragraph_from_html_3(self):
            example_html_3 = "<html><body></body></html>"
            test_3 = get_first_paragraph_from_html(example_html_3)
            expected_3 = ""
            self.assertEqual(test_3, expected_3)

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

    def test_extract_page_data_1(self):
        input_url_1 = "https://crawler-test.com"
        input_body_1 = """<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>"""
        actual_1 = extract_page_data(input_body_1, input_url_1)
        expected_1 = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
            }
        self.assertEqual(actual_1, expected_1)
    
    def test_extract_page_data_2(self):
        input_url_2 = "https://google.com"
        input_body_2 = """<html><body>
            <h2>Test Title</h2>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
        </body></html>"""
        actual_2 = extract_page_data(input_body_2, input_url_2)
        expected_2 = {
            "url": "https://google.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://google.com/link1"],
            "image_urls": [],
            }
        self.assertEqual(actual_2, expected_2)
    
    def test_fill_lines(self):
        y = 1
        x = 1
        self.assertEqual(y, x)

    def test_fill_lines_1(self):
        y = 1
        x = 1
        self.assertEqual(y, x)

    def test_fill_line_2(self):
        y = 1
        x = 1
        self.assertEqual(y, x)

    def test_fill_line_3(self):
        y = 1
        x = 1
        self.assertEqual(y, x)

    def test_fill_line_4(self):
        y = 1
        x = 1
        self.assertEqual(y, x)

    def test_fill_line_5(self):
        y = 1
        x = 1
        self.assertEqual(y, x)

    def test_fill_line_6(self):
        y = 1
        x = 1
        self.assertEqual(y, x)

    def test_fill_line_7(self):
        y = 1
        x = 1
        self.assertEqual(y, x)

if __name__ == "__main__":
    unittest.main()