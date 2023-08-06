# Copyright 2017 Amazon.com, Inc. or its affiliates

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import datetime
import hashlib
import hmac
import logging
from requests import Request, Session

# Python 2/3 compatibility
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

logger = logging.getLogger(__name__)

_REGION = 'us-east-1'
_SERVICE = 'crowd'
_HOST = '{}.{}.amazonaws.com'.format(_SERVICE, _REGION)
_ENDPOINT = 'https://{}'.format(_HOST)

_TIMEOUT_SECONDS = 60


class MTurkCrowdClient(object):
    """A simple REST client to access the MTurk Crowd API.

    :param boto3_session: A boto3.session.Session constructed with the AWS
        credentials you wish to call the service with.
    """

    def __init__(self, boto3_session):
        self._session = boto3_session
        self._aws_account = _fetch_aws_account(self._session)

    def put_task(self, function_name, task_name, input):
        """Calls the given function to create a task with the given name and input.

        :param function_name: The name of the function to call.
        :param task_name: The task name to be used in creation.
        :param input: The input data to the function.

        :returns: Response object. See
            http://docs.python-requests.org/en/master/api/#requests.Response
        """
        return self._make_request(
            'PUT',
            function_name,
            task_name,
            {'input': input})

    def get_task(self, function_name, task_name):
        """Calls the given function to get the task with the given name.

        :param function_name: The name of the function to call.
        :param task_name: The name of the task to be created.

        :returns: Response object. See
            http://docs.python-requests.org/en/master/api/#requests.Response
        """
        return self._make_request(
            'GET',
            function_name,
            task_name)

    def delete_task(self, function_name, task_name):
        """Calls the given function to delete the task with the given name.

        :param function_name: The name of the function to call.
        :param task_name: The name of the task to be deleted.

        :returns: Response object. See
            http://docs.python-requests.org/en/master/api/#requests.Response
        """
        return self._make_request(
            'DELETE',
            function_name,
            task_name)

    def _make_request(self, method, function_name, task_name, body=None):
        uri_path = self._build_uri_path(function_name, task_name)
        headers = self._build_aws_sigv4_headers(method, uri_path, body)
        url = _ENDPOINT + uri_path

        request = Request(
            method,
            url,
            headers=headers,
            json=body).prepare()
        logger.debug('Invoking {} on URL {} with headers={}, body={}'.format(
            request.method,
            request.url,
            json.dumps(dict(request.headers)),
            request.body))
        response = Session().send(request, timeout=_TIMEOUT_SECONDS)
        return response

    def _build_aws_sigv4_headers(self, method, uri_path, body):
        # Generate HTTP headers for SigV4 signing which can be included in the
        # client's requests to authenticate its calls. See:
        # http://docs.aws.amazon.com/general/latest/gr/sigv4-signed-request-examples.html

        canonical_uri = quote(uri_path)

        # Get credentials containing AWS access key, secret key, and, if
        # present, session token
        credentials = self._session.get_credentials().get_frozen_credentials()

        # Create a date for headers and the credential string
        utcnow = datetime.datetime.utcnow()
        amzdate = utcnow.strftime('%Y%m%dT%H%M%SZ')
        # Date w/o time; used in credential scope
        datestamp = utcnow.strftime('%Y%m%d')

        # Create a canonical request
        # http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

        headers_to_sign = {
            'host': _HOST,
            'x-amz-date': amzdate
        }
        if credentials.token:
            headers_to_sign['x-amz-security-token'] = credentials.token

        sorted_header_names = sorted(set(headers_to_sign))
        canonical_headers = '\n'.join(['{}:{}'.format(k, headers_to_sign[k])
                                       for k in sorted_header_names])
        signed_headers = ';'.join(sorted_header_names)

        string_body = '' if body is None else json.dumps(body)
        payload_hash = hashlib.sha256(string_body.encode('utf-8')).hexdigest()
        canonical_request = method + '\n' \
            + canonical_uri + '\n\n' \
            + canonical_headers + '\n\n' \
            + signed_headers + '\n' \
            + payload_hash

        # Create the string to sign
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = datestamp + '/' \
            + _REGION + '/' \
            + _SERVICE + '/' \
            + 'aws4_request'
        string_to_sign = algorithm + '\n' \
            + amzdate + '\n' \
            + credential_scope + '\n' \
            + hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

        # Calculate the signature
        signing_key = _get_signature_key(
            credentials.secret_key,
            datestamp,
            _REGION,
            _SERVICE)
        signature = hmac.new(
            signing_key,
            (string_to_sign).encode('utf-8'),
            hashlib.sha256).hexdigest()

        # Add signing information to the request
        authorization_header = algorithm + ' ' + 'Credential=' \
            + credentials.access_key + '/' + credential_scope + ', ' + \
            'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

        headers = {
            'x-amz-date': amzdate,
            'Authorization': authorization_header
        }
        if 'x-amz-security-token' in headers_to_sign:
            headers['x-amz-security-token'] = (
                headers_to_sign['x-amz-security-token'])

        return headers

    def _build_uri_path(self, function_name, task_name):
        return '/{}/functions/{}/tasks/{}'.format(
            self._aws_account,
            quote(function_name, safe=''),
            quote(task_name, safe=''))


def _fetch_aws_account(session):
    sts_client = session.client('sts')
    return sts_client.get_caller_identity()['Account']


def _sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def _get_signature_key(key, date_stamp, region_name, service_name):
    k_date = _sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = _sign(k_date, region_name)
    k_service = _sign(k_region, service_name)
    k_signing = _sign(k_service, 'aws4_request')
    return k_signing
