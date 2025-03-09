import unittest
from url import URL, show
from io import StringIO

class TestURL(unittest.TestCase):
    def test_scheme(self):
        url = URL("http://example.org")
        self.assertEqual(url.scheme, "http")

        url = URL("https://example.org")
        self.assertEqual(url.scheme, "https")

        url = URL("file://some/path")
        self.assertEqual(url.scheme, "file")

        # with self.assertRaises(AssertionError):
        #     URL("data:text/html,Hello world!")

        with self.assertRaises(AssertionError):
            URL("view-source:https://example.org")

    def test_host(self):
        url = URL("https://example.org")
        self.assertEqual(url.host, "example.org")

        url = URL("https://example.org/index.html")
        self.assertEqual(url.host, "example.org")

        url = URL("https://sub.example.org")
        self.assertEqual(url.host, "sub.example.org")

    def test_path(self):
        url = URL("https://example.org")
        self.assertEqual(url.path, "/")

        url = URL("https://example.org/index.html")
        self.assertEqual(url.path, "/index.html")

        url = URL("https://example.org/some/path")
        self.assertEqual(url.path, "/some/path")

    def test_ports(self):
        url = URL("http://example.org")
        self.assertEqual(url.port, 80)

        url = URL("https://example.org")
        self.assertEqual(url.port, 443)

        url = URL("http://example.org:8443")
        self.assertEqual(url.port, 8443)

        url = URL("https://example.org:8443")
        self.assertEqual(url.port, 8443)

    def test_url_parsing(self):
        test_cases = [
            ("https://example.org:8443/test/path", "https", "example.org", 8443, "/test/path"),
            ("http://example.org", "http", "example.org", 80, "/"),
            ("https://example.org/abc/def", "https", "example.org", 443, "/abc/def"),
            ("http://example.org:8080", "http", "example.org", 8080, "/"),
            ("https://sub.domain.org:9000/some/path", "https", "sub.domain.org", 9000, "/some/path"),
        ]

        for url_str, scheme, host, port, path in test_cases:
            url = URL(url_str)
            self.assertEqual(url.scheme, scheme)
            self.assertEqual(url.host, host)
            self.assertEqual(url.port, port)
            self.assertEqual(url.path, path)

    def test_show_function(self):
        test_cases = [
            ("<html><body>Hello World</body></html>", "Hello World"),
            ("<p>Test</p><br><div>More text</div>", "TestMore text"),
            ("No tags here", "No tags here"),
            ("<h1>Title</h1>\n<p>Paragraph</p>", "Title\nParagraph"),
            ("<script>alert('hi')</script>Visible text", "alert('hi')Visible text"),
        ]

        for html, expected in test_cases:
            with self.subTest(html=html):
                output = StringIO()
                import sys
                sys.stdout = output
                show(html)
                sys.stdout = sys.__stdout__
                self.assertEqual(output.getvalue(), expected)

if __name__ == "__main__":
    unittest.main()
