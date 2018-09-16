import json

import requests
from flask import current_app

from pxf import logger
from pxf.backends.exceptions import WebsiteBackendException


class WebsiteBackend:

    def _header_authorization(self):
        return 'PXaLogin apikey="{0}"'.format(current_app.config['PXA_URL_API_KEY'])  # noqa

    def _url(self, endpoint, **kwargs):
        return current_app.config['PXA_URL'] + endpoint.format(**kwargs)

    def create_website(self, url):
        params = {
            "url": url,
        }

        try:
            response = requests.post(self._url('/api/website'),
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': self._header_authorization()  # noqa
                                     },
                                     data=json.dumps(params),
                                     timeout=current_app.config['PXA_TIMEOUT']
                                     )
        except Exception as e:
            logger.error("WebsiteBackend Exception createa_website erro:{}".format(str(e)))  # noqa
            raise WebsiteBackendException(str(e))

        if response.status_code != 201:
            logger.error("WebsiteBackend createa_website erro:{}".format(str(response.text)))  # noqa
            raise WebsiteBackendException('[{0}] {1}'.format(response.status_code, response.content))  # noqa

        return response.json()

    def get_website(self, website_id):
        try:
            response = requests.get(self._url('/api/website/{website_id}', website_id=website_id),  # noqa
                                    headers={'Authorization': self._header_authorization()},  # noqa
                                    timeout=current_app.config['PXA_TIMEOUT'])
        except Exception as e:
            logger.error("WebsiteBackend Exception get_website erro:{}".format(str(e)))  # noqa
            raise WebsiteBackendException(str(e))

        if response.status_code != 200:
            logger.error("WebsiteBackend get_website erro:{}".format(str(response.text)))  # noqa
            raise WebsiteBackendException('[{0}] {1}'.format(response.status_code, response.content))  # noqa

        return response.json()

    def search(self, status, limit, offset):
        params = {
            "status": status,
            "limit": limit,
            "offset": offset
        }

        try:
            response = requests.post(self._url('/api/search'),
                                     headers={
                                         'Content-Type': 'application/json',
                                         'Authorization': self._header_authorization()  # noqa
                                     },
                                     data=json.dumps(params),
                                     timeout=current_app.config['PXA_TIMEOUT']
                                     )
        except Exception as e:
            logger.error("WebsiteBackend Exception search erro:{}".format(str(e)))  # noqa
            raise WebsiteBackendException(str(e))

        if response.status_code != 200:
            logger.error("WebsiteBackend search erro:{}".format(str(response.text)))  # noqa
            raise WebsiteBackendException('[{0}] {1}'.format(response.status_code, response.content))  # noqa

        return response.json()
