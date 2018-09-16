import mock
import vcr

from pxf.backends.exceptions import WebsiteBackendException
from pxf.backends.website import WebsiteBackend
from tests.base import BaseTestCase


class TestWebsiteBackend(BaseTestCase):

    def test_create_website(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_create_website.yaml'):  # noqa
            website_backen = WebsiteBackend()
            response = website_backen.create_website("http://ibm.com.br")
            self.assertEqual(response, {})

    def test_create_website_without_200(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_create_website_without_200.yaml'):  # noqa
            with self.assertRaises(WebsiteBackendException):
                website_backen = WebsiteBackend()
                website_backen.create_website("http://ibm.com.br")

    @mock.patch('pxf.backends.website.requests.post')
    def test_create_website_with_exception(self, mock_request):
        mock_request.side_effect = mock.Mock(side_effect=Exception())
        with self.assertRaises(WebsiteBackendException):
            website_backen = WebsiteBackend()
            website_backen.create_website("http://ibm.com.br")

    def test_get_website(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_get_website.yaml'):  # noqa
            website_backen = WebsiteBackend()
            response = website_backen.get_website(1)
            self.assertEqual(response['urls'][0], "https://github.com/vtrmantovani")  # noqa
            self.assertEqual(response['urls'][1], "https://www.linkedin.com/in/vtrmantovani")  # noqa

    def test_get_website_without_200(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_get_website_without_200.yaml'):  # noqa
            with self.assertRaises(WebsiteBackendException):
                website_backen = WebsiteBackend()
                website_backen.get_website(1)

    @mock.patch('pxf.backends.website.requests.get')
    def test_get_website_with_exception(self, mock_request):
        mock_request.side_effect = mock.Mock(side_effect=Exception())
        with self.assertRaises(WebsiteBackendException):
            website_backen = WebsiteBackend()
            website_backen.get_website(1)

    def test_search(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_search.yaml'):  # noqa
            website_backen = WebsiteBackend()
            response = website_backen.search('NEW', 1, 0)
            self.assertEqual(response['websites'][0]['website'], "https://github.com/vtrmantovani")  # noqa
            self.assertEqual(response['total_itens'], 5)

    def test_search_without_200(self):
        with vcr.use_cassette('tests/fixtures/cassettes/test_search_without_200.yaml'):  # noqa
            with self.assertRaises(WebsiteBackendException):
                website_backen = WebsiteBackend()
                website_backen.search('NEW', 1, 0)

    @mock.patch('pxf.backends.website.requests.post')
    def test_search_with_exception(self, mock_request):
        mock_request.side_effect = mock.Mock(side_effect=Exception())
        with self.assertRaises(WebsiteBackendException):
            website_backen = WebsiteBackend()
            website_backen.search('NEW', 10, 0)
