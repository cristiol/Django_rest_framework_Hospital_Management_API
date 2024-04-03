import pytest
import requests
pytest_mark = pytest.mark.django_db


base_url = "http://127.0.0.1:8000/api/treatment/"
url_create_treatment = f"{base_url}creation/"
url_treatment_detail = f"{base_url}treatment-detail/1/"

good_token_create_treatment = {"Authorization": "Token 9163342dd2f98f45e71bef9ae17aa258658b123b"}
bad_token_create_treatment = {"Authorization": "Token 43b1edc8a7e7f3bdf8211a72c0acef96f2d54dd2"}

payload_creation_treatment = {
    "name": "Chiropractic Care",
    "description": "Chiropractic care is a healthcare profession that focuses on the diagnosis, treatment, and prevention of mechanical disorders of the musculoskeletal system, particularly the spine. Chiropractors use hands-on manipulation and other alternative treatments to align the body's structure and promote natural healing."
}

payload_modify_treatment = {
    "name":	"Chemotherapy",
    "description": "Chemotherapy is a cancer treatment that uses drugs to target and kill rapidly dividing cancer cells."
}


def test_get_treatment_good_token():
    response = requests.get(url=url_treatment_detail, headers=good_token_create_treatment)
    assert response.status_code == 200


def test_get_treatment_bad_token():
    response = requests.get(url=url_create_treatment, headers=bad_token_create_treatment)
    assert response.status_code == 403


def test_update_treatment_good_token():
    response = requests.put(url=url_treatment_detail, json=payload_modify_treatment,
                            headers=good_token_create_treatment)
    assert response.status_code == 200


def test_update_treatment_bad_token():
    response = requests.put(url=url_create_treatment, json=payload_modify_treatment,
                            headers=bad_token_create_treatment)
    assert response.status_code == 403


def test_create_treatment_good_token():
    response = requests.post(url=url_create_treatment, json=payload_creation_treatment,
                             headers=good_token_create_treatment)
    assert response.status_code == 201


def test_create_treatment_bad_token():
    response = requests.post(url=url_create_treatment, json=payload_creation_treatment,
                             headers=bad_token_create_treatment)
    assert response.status_code == 403



