import pytest
from my_sdk import Client, SDKException

def test_client_initialization():
    client = Client(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.base_url == "https://api.example.com"

def test_invalid_request():
    client = Client(api_key="test_key")
    with pytest.raises(SDKException):
        client._request("GET", "/invalid-endpoint") 