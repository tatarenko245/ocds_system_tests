import json

import allure
import requests


@allure.step('# Prepared request: create EI.')
def create_ei_process(host, access_token, x_operation_id, country, language, payload, test_mode=False):
    request = requests.post(
        url=f"{host}/do/ei",
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json"},
        params={
            "country": country,
            "lang": language,
            "testMode": test_mode
        },
        json=payload
    )
    allure.attach(f"{host}/do/ei", "URL")
    allure.attach(json.dumps(payload), "Prepared payload")
    return request
