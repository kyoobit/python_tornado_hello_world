import logging
import json

## python -m pip install --upgrade pip pytest
import pytest

## python -m pip install --upgrade pip tornado
from tornado import httpclient


## -----------------------------------------------------------------------------


def fetch(url:str, **kwargs):
    """HTTP Client
    See Also:
      * https://www.tornadoweb.org/en/stable/httpclient.html#http-client-interfaces
    """
    response = None
    http_client = httpclient.HTTPClient()
    try:
        response = http_client.fetch(url, **kwargs)
    except httpclient.HTTPError as err:
        response = err.response
    except Exception as err:
        response = err
    finally:
        http_client.close()
        print(f"response {type(response)}: {response!r}")
        if hasattr(response, 'request'):
            print(f"request: {response.request!r}")
            print(f"request.headers: {[h for h in response.request.headers.get_all()]!r}")
        if hasattr(response, 'code'):
            print(f"response.code: {response.code!r}")
            print(f"response.headers: {[h for h in response.headers.get_all()]!r}")
            print(f"response.body: {response.body!r}")
        return response


## -----------------------------------------------------------------------------


TEST_REQUESTS = [
    ## REQUEST: tuple = (path: str, options: dict, status_code: int),
    ('/foo', {'method': 'GET'}, 200),
    ('/bar', {'method': 'GET'}, 200),
    ('/blast', {'method': 'HEAD'}, 405),
    ('/blast', {'method': 'OPTIONS'}, 405),
    ('/blast', {'method': 'DELETE'}, 405),
    ]

## https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.Metafunc.parametrize
@pytest.mark.parametrize('path, options, status_code', TEST_REQUESTS, ids=[test[0] for test in TEST_REQUESTS])
def test_request(caplog, address, path, options, status_code):
    caplog.set_level(logging.DEBUG)
    print(f"path: {path!r}, options: {options!r}")

    ## Make the HTTP request
    response = fetch(f"http://{address}{path}", **options)

    ## Check response code for the expected value
    assert response.code == status_code

    ## Check response body for expected values
    if status_code == 200:
        assert response.body == b'Hello, World!\n'
