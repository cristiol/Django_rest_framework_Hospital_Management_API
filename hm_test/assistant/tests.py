import pytest
import requests
pytest_mark = pytest.mark.django_db


base_url = "http://127.0.0.1:8000/api/assistant/"
url_create_assistant = f"{base_url}registration/"
url_assistant_detail = f"{base_url}assistant-profile/2/"

good_token_assistant = {"Authorization": "Token 9163342dd2f98f45e71bef9ae17aa258658b123b"}
bad_token_assistant = {"Authorization": "Token 43b1edc8a7e7f3bdf8211a72c0acef96f2d54dd2"}

payload_create_assistant = {
  "user_data": {
    "username": "test_user_assistant_12",
    "first_name": "TestAssistant",
    "last_name": "Smith",
    "password": "Parola456test",
    "password2": "Parola456test"
  },
  "profile_data": {
    "user": 5
  }
}
payload_update_assistant = {
  "user_data": {

    "first_name": "Alex",
    "last_name": "Smith",
  },
  "profile_data": {
    "user": 5
  }
}


def test_get_assistant_good_token():
    response = requests.get(url=url_assistant_detail, headers=good_token_assistant)
    assert response.status_code == 200


def test_get_assistant_bad_token():
    response = requests.get(url=url_assistant_detail, headers=bad_token_assistant)
    assert response.status_code == 403


def test_update_assistant_good_token():
    response = requests.put(url=url_assistant_detail, json=payload_update_assistant,
                            headers=good_token_assistant)
    assert response.status_code == 200


def test_update_assistant_bad_token():
    response = requests.put(url=url_assistant_detail, json=payload_update_assistant,
                            headers=bad_token_assistant)
    assert response.status_code == 403


def test_create_assistant_good_token():
    response = requests.post(url=url_create_assistant, json=payload_create_assistant,
                             headers=good_token_assistant)
    assert response.status_code == 201


def test_create_assistant_bad_token():
    response = requests.post(url=url_create_assistant, json=payload_create_assistant,
                             headers=bad_token_assistant)
    assert response.status_code == 403


