from tools.api_test import api_test
import json

def test_api_test_get():
    payload = json.dumps({
        "method": "GET",
        "url": "https://reqres.in/api/users/2"
    })

    response = api_test(payload)
    assert "status_code" in response