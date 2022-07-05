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


@allure.step('# Prepared request: Update EI.')
def update_ei_process(host, access_token, x_operation_id, cpid, token, payload, test_mode=False):
    request = requests.post(
        url=f"{host}/do/ei/{cpid}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token
        },
        params={
            "testMode": test_mode
        },
        json=payload
    )
    allure.attach(f"{host}/do/ei/{cpid}", "URL")
    allure.attach(json.dumps(payload), "Prepared payload")
    return request


@allure.step('# Prepared request: Confirm EI.')
def confirm_ei_process(host, access_token, x_operation_id, cpid, token, test_mode=False):
    request = requests.post(
        url=f"{host}/do/confirmation/ei/{cpid}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token
        },
        params={
            "testMode": test_mode
        }
    )
    allure.attach(f"{host}/do/confirmation/ei/{cpid}", "URL")
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


@allure.step('# Prepared request: Outsourcing PN.')
def outsourcing_pn_process(host, access_token, x_operation_id, cpid, ocid, token, fa, ap, test_mode=False):
    request = requests.post(
        url=f"{host}/do/outsourcing/{cpid}/{ocid}",
        params={
            "testMode": test_mode,
            "FA": fa,
            "AP": ap
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token}
    )
    allure.attach(f"{host}/do/outsourcing/{cpid}/{ocid}", 'URL')
    return request


@allure.step('# Prepared request: Relation AP.')
def relation_ap_process(host, access_token, x_operation_id, cpid, ocid, token, cp, pn, test_mode=False):
    request = requests.post(
        url=f"{host}/do/relation/{cpid}/{ocid}",
        params={
            "testMode": test_mode,
            "CP": cp,
            "PN": pn
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token}
    )
    allure.attach(f"{host}/do/relation/{cpid}/{ocid}", 'URL')
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


@allure.step('# Prepared request: Create FE.')
def create_fe_process(host, access_token, x_operation_id, payload, cpid, ocid, token, test_mode=False):
    request = requests.post(
        url=f"{host}/do/fe/{cpid}/{ocid}",
        params={
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token},
        json=payload)
    allure.attach(f"{host}/do/fe/{cpid}/{ocid}", 'URL')
    allure.attach(json.dumps(payload), 'Prepared payload')
    return request


@allure.step('# Prepared request: Amend FE.')
def amend_fe_process(host, access_token, x_operation_id, payload, cpid, ocid, token, test_mode=False):
    request = requests.post(
        url=f"{host}/amend/fe/{cpid}/{ocid}",
        params={
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token},
        json=payload)
    allure.attach(f"{host}/amend/fe/{cpid}/{ocid}", 'URL')
    allure.attach(json.dumps(payload), 'Prepared payload')
    return request


@allure.step('# Prepared request: Create Submission.')
def create_submission_process(host, access_token, x_operation_id, payload, cpid, ocid, test_mode=False):
    request = requests.post(
        url=f"{host}/do/submission/{cpid}/{ocid}",
        params={
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json"},
        json=payload)
    allure.attach(f"{host}/do/submission/{cpid}/{ocid}", 'URL')
    allure.attach(json.dumps(payload), 'Prepared payload')
    return request


@allure.step('# Prepared request: Qualification Declare Non Conflict Interest.')
def qualification_declare_process(host, access_token, x_operation_id, payload, cpid, ocid, qualification_id,
                                  qualification_token, test_mode=False):
    request = requests.post(
        url=f"{host}/do/declaration/qualification/{cpid}/{ocid}/{qualification_id}",
        params={
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": qualification_token},
        json=payload)
    allure.attach(f"{host}/do/declaration/qualification/{cpid}/{ocid}/{qualification_id}", 'URL')
    allure.attach(json.dumps(payload), 'Prepared payload')
    return request


@allure.step('# Prepared request: Qualification Consideration.')
def qualification_consideration_process(host, access_token, x_operation_id, cpid, ocid, qualification_id,
                                        qualification_token, test_mode=False):
    request = requests.post(
        url=f"{host}/do/consideration/qualification/{cpid}/{ocid}/{qualification_id}",
        params={
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": qualification_token}
    )
    allure.attach(f"{host}/do/consideration/qualification/{cpid}/{ocid}/{qualification_id}", 'URL')
    return request


@allure.step('# Prepared request: Qualification.')
def qualification_process(host, access_token, x_operation_id, payload, cpid, ocid, qualification_id,
                          qualification_token, test_mode=False):
    request = requests.post(
        url=f"{host}/do/qualification/{cpid}/{ocid}/{qualification_id}",
        params={
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": qualification_token},
        json=payload)
    allure.attach(f"{host}/do/qualification/{cpid}/{ocid}/{qualification_id}", 'URL')
    allure.attach(json.dumps(payload), 'Prepared payload')
    return request


@allure.step('# Prepared request: Qualification Protocol.')
def qualification_protocol_process(host, access_token, x_operation_id, cpid, ocid, token, test_mode=False):
    request = requests.post(
        url=f"{host}/do/protocol/qualification/{cpid}/{ocid}/",
        params={
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token}
    )
    allure.attach(f"{host}/do/protocol/qualification/{cpid}/{ocid}/", 'URL')
    return request


@allure.step('# Prepared request: Complete Qualification.')
def complete_qualification_process(host, access_token, x_operation_id, cpid, ocid, token, test_mode=False):
    request = requests.post(
        url=f"{host}/complete/qualification/{cpid}/{ocid}/",
        params={
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token
        }
    )
    allure.attach(f"{host}/complete/qualification/{cpid}/{ocid}/", 'URL')
    return request


@allure.step('# Prepared request: Issuing Framework.')
def issuing_framework_process(host, access_token, x_operation_id, payload, cpid, ocid, contract_id,
                              token, test_mode=False):
    request = requests.post(
        url=f"{host}/issue/fc/{cpid}/{ocid}/{contract_id}",
        params={
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token},
        json=payload)
    allure.attach(f"{host}/issuing/fc/{cpid}/{ocid}/{contract_id}", 'URL')
    allure.attach(json.dumps(payload), 'Prepared payload')
    return request


@allure.step('# Prepared request: Create Confirmation Response.')
def create_confirmation_response_process(host, access_token, x_operation_id, payload, entity, cpid, ocid, entity_id,
                                         token, role, test_mode=False):
    request = requests.post(
        url=f"{host}/do/confirmation/{entity}/{cpid}/{ocid}/{entity_id}",
        params={
            "testMode": test_mode,
            "role": role
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": token},
        json=payload)
    allure.attach(f"{host}/do/confirmation/{entity}/{cpid}/{ocid}/{entity_id}", 'URL')
    allure.attach(json.dumps(payload), 'Prepared payload')
    return request


@allure.step('# Prepared request: Next Confirmation Step.')
def next_confirmation_step_process(host, access_token, x_operation_id, cpid, ocid, entity, entity_id,
                                   entity_token, role, test_mode=False):
    request = requests.post(
        url=f"{host}/complete/confirmationStage/{entity}/{cpid}/{ocid}/{entity_id}",
        params={
            "role": role,
            "testMode": test_mode
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "X-OPERATION-ID": x_operation_id,
            "Content-Type": "application/json",
            "X-TOKEN": entity_token}
    )
    allure.attach(f"{host}/complete/confirmationStage/{entity}/{cpid}/{ocid}/{entity_id}", 'URL')
    return request
