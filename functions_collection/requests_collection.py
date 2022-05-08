import json

import allure
import requests


@allure.step('# Prepared request: Create EI.')
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


@allure.step('# Prepared request: Create FS.')
def create_fs_process(host, cpid, access_token, x_operation_id, payload, test_mode=False):
    request = requests.post(
        url=f"{host}/do/fs/{cpid}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json"},
        params={
            "testMode": test_mode
        },
        json=payload
    )
    allure.attach(f"{host}/do/fs/{cpid}", "URL")
    allure.attach(json.dumps(payload), "Prepared payload")
    return request


@allure.step('# Prepared request: Create PN.')
def create_pn_process(host, access_token, x_operation_id, payload, country, language, pmd, test_mode=False):
    request = requests.post(
        url=f"{host}/do/pn",
        params={
            "testMode": test_mode,
            "country": country,
            "lang": language,
            "pmd": pmd
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json"},
        json=payload)
    allure.attach(f"{host}/do/pn", 'URL')
    allure.attach(json.dumps(payload), 'Prepared payload')
    return request


@allure.step('# Prepared request: Create AP.')
def create_ap_process(host, access_token, x_operation_id, payload, country, language, pmd, test_mode=False):
    request = requests.post(
        url=f"{host}/do/ap",
        params={
            "testMode": test_mode,
            "country": country,
            "lang": language,
            "pmd": pmd
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json"},
        json=payload)
    allure.attach(f"{host}/do/ap", 'URL')
    allure.attach(json.dumps(payload), 'Prepared payload')
    return request


@allure.step('# Prepared request: Update AP.')
def update_ap_process(host, access_token, x_operation_id, payload, cpid, ocid, token, test_mode=False):
    request = requests.post(
        url=f"{host}/do/ap/{cpid}/{ocid}",
        params={
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token},
        json=payload)
    allure.attach(f"{host}/do/ap/{cpid}/{ocid}", 'URL')
    allure.attach(json.dumps(payload), 'Prepared payload')
    return request
