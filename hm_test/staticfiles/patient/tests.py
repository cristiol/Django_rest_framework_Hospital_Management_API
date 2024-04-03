import pytest
import requests
pytest_mark = pytest.mark.django_db


url = "http://127.0.0.1:8000/api/patient/patient-profile/16/"
url_applied_treatment = "http://127.0.0.1:8000/api/patient/update-applied-treatment/16/"
url_recommended_treatment = "http://127.0.0.1:8000/api/patient/update-recommended-treatment/16/"
url_assign_assistants = "http://127.0.0.1:8000/api/patient/assign-assistants/16/"
url_create_patient = "http://127.0.0.1:8000/api/patient/registration/"


good_token_applied_treatment = {
        "Authorization": "Token a0c116a8e11d399a7f9d4b5f17a57ced418c57ef"
    }
bad_token_applied_treatment = {
        "Authorization": "Token 43b1edc8a7e7f3bdf8211a72c0acef96f2d54dd2"
    }
good_token_recommended_treatment = {
        "Authorization": "Token f8e2e0968bb94581ad7f80797c6fbb26568af65d"
    }
bad_token_recommended_treatment = {
        "Authorization": "Token 79ac608a9a91d9e675c1e4343ecc84e9c76b9dd0"
    }
good_token_assign_assistants = {
        "Authorization": "Token f8e2e0968bb94581ad7f80797c6fbb26568af65d"
    }
bad_token_assign_assistants = {
        "Authorization": "Token 79ac608a9a91d9e675c1e4343ecc84e9c76b9dd0"
    }

good_credentials_header = {
        "Authorization": "Token 9163342dd2f98f45e71bef9ae17aa258658b123b"
    }
bad_credentials_header = {
        "Authorization": "Token a2798555da4766b9d520034d650d18deb9a70842"
    }

good_token_create_patient = {
        "Authorization": "Token 9163342dd2f98f45e71bef9ae17aa258658b123b"
    }
bad_token_create_patient = {
        "Authorization": "Token a2798555da4766b9d520034d650d18deb9a70842"
    }


payload_put_profile_patient = {"profile data": {"name": "Pierre Dupont Francois"}}
payload_recommended_treatment = {"recommended_treatment": 11}
payload_assign_assistants = {"assistants": [2,3]}
payload_applied_treatment = {"applied_treatment": 11}

payload_create_patient = {"user_data": {
    "username": "test_user_12",
    "first_name": "Test",
    "last_name": "User",
    "password": "MotDePasse456test",
    "password2": "MotDePasse456test"
  },
  "profile_data": {
    "user": 4,
    "doctors": [4],
    "assistants": [3,7],
    "recommended_treatment": 11,
    "applied_treatment": 11,
    "name": "Test User"
  }
}


def test_get_good_credentials():
    response = requests.get(url, headers=good_credentials_header)
    assert response.status_code == 200


def test_get_without_token():
    response = requests.get(url)
    assert response.status_code == 401


def test_get_invalid_credentials():
    response = requests.get(url,headers=bad_credentials_header)
    assert response.status_code == 403


def test_put_good_credentials():
    response = requests.put(url, json=payload_put_profile_patient, headers=good_credentials_header)
    assert response.status_code == 200


def test_put_without_token():
    response = requests.put(url, json=payload_put_profile_patient)
    assert response.status_code == 401


def test_put_invalid_credentials():
    response = requests.get(url, json=payload_put_profile_patient, headers=bad_credentials_header)
    assert response.status_code == 403


def test_good_token_applied_treatment():
    response = requests.put(url=url_applied_treatment, json=payload_applied_treatment,
                            headers=good_token_applied_treatment)
    assert response.status_code == 200


def test_bad_token_applied_treatment():
    response = requests.put(url=url_applied_treatment, json=payload_applied_treatment,
                            headers=bad_token_applied_treatment)
    assert response.status_code == 403


def test_good_token_recommended_treatment():
    response = requests.put(url=url_recommended_treatment, json=payload_recommended_treatment,
                            headers=good_token_recommended_treatment)
    assert response.status_code == 200


def test_bad_token_recommended_treatment():
    response = requests.put(url=url_recommended_treatment, json=payload_recommended_treatment,
                            headers=bad_token_recommended_treatment)
    assert response.status_code == 403


def test_good_token_assign_assistants():
    response = requests.put(url=url_assign_assistants, json=payload_assign_assistants,
                            headers=good_token_assign_assistants)
    assert response.status_code == 200


def test_bad_token_assign_assistants():
    response = requests.put(url=url_assign_assistants, json=payload_assign_assistants,
                            headers=bad_token_assign_assistants)
    assert response.status_code == 403


def test_bad_token_create_patient():
    response = requests.post(url=url_create_patient, json=payload_create_patient,
                             headers=bad_token_create_patient)
    assert response.status_code == 403


def test_good_token_create_patient():
    response = requests.post(url=url_create_patient, json=payload_create_patient,
                             headers=good_token_create_patient)
    assert response.status_code == 201












