# Copyright 2016 - StackStorm, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import base64
import copy

import mock
from oslotest import base
import requests

from oslo_utils import uuidutils
from osprofiler import _utils as osprofiler_utils
import osprofiler.profiler

from mistralclient.api import httpclient

API_BASE_URL = 'http://localhost:8989/v2'
API_URL = '/executions'

EXPECTED_URL = API_BASE_URL + API_URL

AUTH_TOKEN = uuidutils.generate_uuid()
PROJECT_ID = uuidutils.generate_uuid()
USER_ID = uuidutils.generate_uuid()
PROFILER_HMAC_KEY = 'SECRET_HMAC_KEY'
PROFILER_TRACE_ID = uuidutils.generate_uuid()

EXPECTED_AUTH_HEADERS = {
    'x-auth-token': AUTH_TOKEN,
    'X-Project-Id': PROJECT_ID,
    'X-User-Id': USER_ID
}

EXPECTED_REQ_OPTIONS = {
    'headers': EXPECTED_AUTH_HEADERS
}

EXPECTED_BODY = {
    'k1': 'abc',
    'k2': 123,
    'k3': True
}


class FakeRequest(object):

    def __init__(self, method):
        self.method = method


class FakeResponse(object):

    def __init__(self, method, url, status_code):
        self.request = FakeRequest(method)
        self.url = url
        self.status_code = status_code


class HTTPClientTest(base.BaseTestCase):

    def setUp(self):
        super(HTTPClientTest, self).setUp()
        osprofiler.profiler.init(None)
        self.client = httpclient.HTTPClient(
            API_BASE_URL,
            auth_token=AUTH_TOKEN,
            project_id=PROJECT_ID,
            user_id=USER_ID
        )

    @mock.patch.object(
        requests,
        'get',
        mock.MagicMock(return_value=FakeResponse('get', EXPECTED_URL, 200))
    )
    def test_get_request_options(self):
        self.client.get(API_URL)

        requests.get.assert_called_with(
            EXPECTED_URL,
            **EXPECTED_REQ_OPTIONS
        )

    @mock.patch.object(
        osprofiler.profiler._Profiler,
        'get_base_id',
        mock.MagicMock(return_value=PROFILER_TRACE_ID)
    )
    @mock.patch.object(
        osprofiler.profiler._Profiler,
        'get_id',
        mock.MagicMock(return_value=PROFILER_TRACE_ID)
    )
    @mock.patch.object(
        requests,
        'get',
        mock.MagicMock(return_value=FakeResponse('get', EXPECTED_URL, 200))
    )
    def test_get_request_options_with_profile_enabled(self):
        osprofiler.profiler.init(PROFILER_HMAC_KEY)

        data = {'base_id': PROFILER_TRACE_ID, 'parent_id': PROFILER_TRACE_ID}
        signed_data = osprofiler_utils.signed_pack(data, PROFILER_HMAC_KEY)

        headers = {
            'X-Trace-Info': signed_data[0],
            'X-Trace-HMAC': signed_data[1]
        }

        self.client.get(API_URL)

        expected_options = copy.deepcopy(EXPECTED_REQ_OPTIONS)
        expected_options['headers'].update(headers)

        requests.get.assert_called_with(
            EXPECTED_URL,
            **expected_options
        )

    @mock.patch.object(
        requests,
        'get',
        mock.MagicMock(return_value=FakeResponse('get', EXPECTED_URL, 200))
    )
    def test_get_request_options_with_headers_for_get(self):
        target_auth_url = uuidutils.generate_uuid()
        target_auth_token = uuidutils.generate_uuid()
        target_user_id = 'target_user'
        target_project_id = 'target_project'
        target_service_catalog = 'this should be there'
        target_insecure = 'target insecure'
        target_region = 'target region name'
        target_user_domain_name = 'target user domain name'
        target_project_domain_name = 'target project domain name'

        target_client = httpclient.HTTPClient(
            API_BASE_URL,
            auth_token=AUTH_TOKEN,
            project_id=PROJECT_ID,
            user_id=USER_ID,
            target_auth_url=target_auth_url,
            target_auth_token=target_auth_token,
            target_project_id=target_project_id,
            target_user_id=target_user_id,
            target_service_catalog=target_service_catalog,
            target_region_name=target_region,
            target_user_domain_name=target_user_domain_name,
            target_project_domain_name=target_project_domain_name,
            target_insecure=target_insecure
        )

        target_client.get(API_URL)

        expected_options = copy.deepcopy(EXPECTED_REQ_OPTIONS)

        headers = expected_options["headers"]

        headers["X-Target-Auth-Uri"] = target_auth_url
        headers["X-Target-Auth-Token"] = target_auth_token
        headers["X-Target-Insecure"] = target_insecure
        headers["X-Target-User-Id"] = target_user_id
        headers["X-Target-Project-Id"] = target_project_id
        headers["X-Target-Region-Name"] = target_region
        headers["X-Target-User-Domain-Name"] = target_user_domain_name
        headers["X-Target-Project-Domain-Name"] = target_project_domain_name

        catalog = base64.b64encode(target_service_catalog.encode('utf-8'))
        headers["X-Target-Service-Catalog"] = catalog

        requests.get.assert_called_with(EXPECTED_URL, **expected_options)

    @mock.patch.object(
        requests,
        'post',
        mock.MagicMock(return_value=FakeResponse('post', EXPECTED_URL, 201))
    )
    def test_get_request_options_with_headers_for_post(self):
        headers = {'foo': 'bar'}

        self.client.post(API_URL, EXPECTED_BODY, headers=headers)

        expected_options = copy.deepcopy(EXPECTED_REQ_OPTIONS)
        expected_options['headers'].update(headers)
        expected_options['headers']['content-type'] = 'application/json'

        requests.post.assert_called_with(
            EXPECTED_URL,
            EXPECTED_BODY,
            **expected_options
        )

    @mock.patch.object(
        requests,
        'put',
        mock.MagicMock(return_value=FakeResponse('put', EXPECTED_URL, 200))
    )
    def test_get_request_options_with_headers_for_put(self):
        headers = {'foo': 'bar'}

        self.client.put(API_URL, EXPECTED_BODY, headers=headers)

        expected_options = copy.deepcopy(EXPECTED_REQ_OPTIONS)
        expected_options['headers'].update(headers)
        expected_options['headers']['content-type'] = 'application/json'

        requests.put.assert_called_with(
            EXPECTED_URL,
            EXPECTED_BODY,
            **expected_options
        )

    @mock.patch.object(
        requests,
        'delete',
        mock.MagicMock(return_value=FakeResponse('delete', EXPECTED_URL, 200))
    )
    def test_get_request_options_with_headers_for_delete(self):
        headers = {'foo': 'bar'}

        self.client.delete(API_URL, headers=headers)

        expected_options = copy.deepcopy(EXPECTED_REQ_OPTIONS)
        expected_options['headers'].update(headers)

        requests.delete.assert_called_with(
            EXPECTED_URL,
            **expected_options
        )

    @mock.patch.object(
        httpclient.HTTPClient,
        '_get_request_options',
        mock.MagicMock(return_value=copy.deepcopy(EXPECTED_REQ_OPTIONS))
    )
    @mock.patch.object(
        requests,
        'get',
        mock.MagicMock(return_value=FakeResponse('get', EXPECTED_URL, 200))
    )
    def test_http_get(self):
        self.client.get(API_URL)

        httpclient.HTTPClient._get_request_options.assert_called_with(
            'get',
            None
        )

        requests.get.assert_called_with(
            EXPECTED_URL,
            **EXPECTED_REQ_OPTIONS
        )

    @mock.patch.object(
        httpclient.HTTPClient,
        '_get_request_options',
        mock.MagicMock(return_value=copy.deepcopy(EXPECTED_REQ_OPTIONS))
    )
    @mock.patch.object(
        requests,
        'post',
        mock.MagicMock(return_value=FakeResponse('post', EXPECTED_URL, 201))
    )
    def test_http_post(self):
        self.client.post(API_URL, EXPECTED_BODY)

        httpclient.HTTPClient._get_request_options.assert_called_with(
            'post',
            None
        )

        requests.post.assert_called_with(
            EXPECTED_URL,
            EXPECTED_BODY,
            **EXPECTED_REQ_OPTIONS
        )

    @mock.patch.object(
        httpclient.HTTPClient,
        '_get_request_options',
        mock.MagicMock(return_value=copy.deepcopy(EXPECTED_REQ_OPTIONS))
    )
    @mock.patch.object(
        requests,
        'put',
        mock.MagicMock(return_value=FakeResponse('put', EXPECTED_URL, 200))
    )
    def test_http_put(self):
        self.client.put(API_URL, EXPECTED_BODY)

        httpclient.HTTPClient._get_request_options.assert_called_with(
            'put',
            None
        )

        requests.put.assert_called_with(
            EXPECTED_URL,
            EXPECTED_BODY,
            **EXPECTED_REQ_OPTIONS
        )

    @mock.patch.object(
        httpclient.HTTPClient,
        '_get_request_options',
        mock.MagicMock(return_value=copy.deepcopy(EXPECTED_REQ_OPTIONS))
    )
    @mock.patch.object(
        requests,
        'delete',
        mock.MagicMock(return_value=FakeResponse('delete', EXPECTED_URL, 200))
    )
    def test_http_delete(self):
        self.client.delete(API_URL)

        httpclient.HTTPClient._get_request_options.assert_called_with(
            'delete',
            None
        )

        requests.delete.assert_called_with(
            EXPECTED_URL,
            **EXPECTED_REQ_OPTIONS
        )
