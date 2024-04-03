import pytest
import requests
pytest_mark = pytest.mark.django_db


base_url = "http://127.0.0.1:8000/api/doctor/"
url_create_doctor = f"{base_url}registration/"
url_doctor_detail = f"{base_url}doctor-profile/5/"

good_token_doctor = {"Authorization": "Token 9163342dd2f98f45e71bef9ae17aa258658b123b"}
bad_token_doctor = {"Authorization": "Token 43b1edc8a7e7f3bdf8211a72c0acef96f2d54dd2"}

payload_create_doctor = {
  "user_data": {
    "username": "test_user_doctor_12",
    "first_name": "TestDoctor",
    "last_name": "Allen",
    "password": "passsecure124",
    "password2": "passsecure124"
  },
  "profile_data": {
    "user": 5
  }
}
payload_update_doctor = {
  "user_data": {

    "first_name": "Joe",
    "last_name": "Di Marco",
  },
  "profile_data": {
    "user": 5
  }
}


def test_get_doctor_good_token():
    response = requests.get(url=url_doctor_detail, headers=good_token_doctor)
    assert response.status_code == 200


def test_get_assistant_bad_token():
    response = requests.get(url=url_doctor_detail, headers=bad_token_doctor)
    assert response.status_code == 403


def test_update_doctor_good_token():
    response = requests.put(url=url_doctor_detail, json=payload_update_doctor,
                            headers=good_token_doctor)
    assert response.status_code == 200


def test_update_doctor_bad_token():
    response = requests.put(url=url_doctor_detail, json=payload_update_doctor,
                            headers=bad_token_doctor)
    assert response.status_code == 403


def test_create_doctor_good_token():
    response = requests.post(url=url_create_doctor, json=payload_create_doctor,
                             headers=good_token_doctor)
    assert response.status_code == 201


def test_create_assistant_bad_token():
    response = requests.post(url=url_create_doctor, json=payload_create_doctor,
                            headers=bad_token_doctor)
    assert response.status_code == 403




