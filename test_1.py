import json
import requests
import time

from secrets import secrets
BASE_URL = secrets.get('BASE_URL')
USER = secrets.get('USER')
PASS = secrets.get('PASS')


def test_get_token_check_status_code_equals_200():
    response = requests.post(BASE_URL + '/token', auth=(USER, PASS))
    assert response.status_code == 200, 'Checking status code for correct credentials'


def test_get_token_check_status_code_equals_400():
    response = requests.post(BASE_URL + '/token', auth=('usr', PASS))
    assert response.status_code == 400, 'Checking status code for incorrect credentials'


def test_get_token_check_message_incorrect_credentials():
    response = requests.post(BASE_URL + '/token', auth=('usr', PASS))
    assert response.json()['message'] == 'invalid username or password', 'Checking message for incorrect credentials'


def test_get_clients_list_check_status_code_equals_200():
    head = getting_token()
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    print(response.json())
    assert response.status_code == 200, 'Checking status code for getting clients list'


def test_get_clients_list_check_length():
    head = getting_token()
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    assert len(response.json()['clients']) == 2, 'Checking length of list'


def test_get_clients_list_check_payload():
    head = getting_token()
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    json_data = [{'firstName': 'Dawe',
                  'id': '35757ac79306',
                  'lastName': 'Awe',
                  'phone': '123456789'},
                 {'firstName': 'Ricky',
                  'id': 'c368d6b09c3e',
                  'lastName': 'Deckard',
                  'phone': '+48 800 190 590'}
                 ]
    assert response.json()['clients'] == json_data


def test_get_clients_list_check_status_code_equals_403():
    head = {'X-API-KEY': '8IWVmOhZGDwyuf_GEFXllB_Wv0v2uCJ62jKZO2AHoHU'}
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    assert response.status_code == 403, 'Checking status code for getting clients list'


def test_get_clients_list_check_message_incorrect_apikey():
    head = {'X-API-KEY': '8IWVmOhZGDwyuf_GEFXllB_Wv0v2uCJ62jKZO2AHoHU'}
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    assert response.json()['message'] == 'invalid or missing api key', 'Checking message for incorrect api key'


def test_get_client_id():
    head = getting_token()
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    assert response.json()['clients'][0]['id'] == '35757ac79306', 'Checking id for client'


def test_get_client_details_status_code_equals_200():
    head = getting_token()
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    url_id = 'https://qa-interview-api.migo.money/client/{}'.format(response.json()['clients'][0]['id'])
    response_details = requests.get(url_id, headers=head)
    assert response_details.status_code == 200, 'Checking status code for getting client details'


def test_get_client_details():
    head = getting_token()
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    url_id = 'https://qa-interview-api.migo.money/client/{}'.format(response.json()['clients'][0]['id'])
    resp = requests.get(url_id, headers=head)
    print(resp.json())


def test_get_clients_list_invalid_apikey_status_code_equals_403():
    head = {'X-API-KEY': '8IWVmOhZGDwyuf_GEFXllB_Wv0v2uCJ62jKZO2AHoHU'}
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    assert response.status_code == 403, 'Checking status code for getting clients list with invalid api key'


def test_get_clients_list_invalid_apikey_message_invalid_or_missing_api_key():
    head = {'X-API-KEY': '8IWVmOhZGDwyuf_GEFXllB_Wv0v2uCJ62jKZO2AHoHU'}
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    assert response.json()['message'] == 'invalid or missing api key', 'Checking message for getting clients list with invalid api key'


def test_get_client_details_status_code_equals_404():
    head = getting_token()
    url = BASE_URL + '/clients'
    url_id = 'https://qa-interview-api.migo.money/client/123'
    response_details = requests.get(url_id, headers=head)
    assert response_details.status_code == 404, 'Checking status code for getting client details'


def test_get_client_details_message_equals_client_not_found():
    head = getting_token()
    url = BASE_URL + '/clients'
    url_id = 'https://qa-interview-api.migo.money/client/123'
    response_details = requests.get(url_id, headers=head)
    assert response_details.json()['message'] == 'client not found', 'Checking message for getting client details'


def test_put_invalid_body_checking_status_code_400():
    data = {"lastName": "Deckard",
            "phone": "+48 800 190 591"
            }
    head = getting_token()
    url = BASE_URL + '/clients'
    response = requests.get(url, headers=head)
    url_id = 'https://qa-interview-api.migo.money/client/{}'.format(response.json()['clients'][0]['id'])
    response_put = requests.put(url_id, data=data, headers=head)
    assert response_put.status_code == 400


def test_post_add_new_client_check_status_code_200():
    ts = time.time()
    payload = {"firstName": f"Katherina {ts}",
                "lastName": f"Deckard {ts}",
                "phone": "+48 800 190 590"}
    response = requests.post(BASE_URL + '/token', auth=(USER, PASS))
    token = response.json()['key']
    url = BASE_URL + '/client'

    headers = {
            'X-API-KEY': token,
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': token
            }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    global id_new_client
    id_new_client = response.json()['id']

    assert response.status_code == 200, 'Checking status code for adding new client'


def test_delete_client_check_status_code_200():
    head = getting_token()
    url = BASE_URL + f'/client/{id_new_client}'

    response = requests.delete(url, headers=head)
    assert response.status_code == 200, 'Checking status code for deleting new client'


def getting_token():
    response = requests.post(BASE_URL + '/token', auth=(USER, PASS))
    token = response.json()['key']
    head = {'X-API-KEY': token}
    return head
