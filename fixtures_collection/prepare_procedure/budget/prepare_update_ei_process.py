import copy

import allure
import pytest
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid, \
    cleanup_table_of_services_for_expenditure_item
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import update_ei_process
from payloads_collection.budget.update_ei_payload import UpdateExpenditureItemPayload


@pytest.fixture(scope="function")
# Create Ei full data model -> Confirm EI -> Withdraw EI -> Update EI full data model.
def update_ei_tc_1(get_parameters, connect_to_keyspace, withdraw_ei_tc_1):
    bpe_host = get_parameters[2]
    country = get_parameters[4]
    tender_classification_id = get_parameters[9]
    clean_up_database = get_parameters[10]

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_orchestrator = connect_to_keyspace[1]

    ei_cpid = withdraw_ei_tc_1[0]
    ei_token = withdraw_ei_tc_1[1]
    ei_url = withdraw_ei_tc_1[3]
    currency = withdraw_ei_tc_1[4]
    buyer_id = withdraw_ei_tc_1[5]
    buyer_scheme = withdraw_ei_tc_1[6]

    previous_ei_release = requests.get(ei_url).json()

    """
    VR.COM-14.9.2: Check EI state.
    """
    if previous_ei_release['releases'][0]['tender']['status'] == "planning":
        pass
    else:
        raise ValueError(f"The EI release has invalid state: "
                         f"{previous_ei_release['releases'][0]['tender']['status']}.")

    step_number = 1
    with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
        """
        Tender platform authorization for Update EI process.
        As result, get tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
        """
        Send api request to BPE host to create a Update EI process.
        """
        try:
            """
            Build payload for Update EI process.
            """
            payload = copy.deepcopy(UpdateExpenditureItemPayload(
                connect_to_ocds=connect_to_ocds,
                country=country,
                tender_classification_id=tender_classification_id,
                amount=0.99)
            )

            payload.update_old_tender_items(
                previous_ei_release['releases'][0]['tender']['items'][0]['id'],
                previous_items_list=previous_ei_release['releases'][0]['tender']['items'],
                quantity_of_new_additional_classifications=1
            )
            payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Update EI process.")

        update_ei_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=operation_id,
            cpid=ei_cpid,
            token=ei_token,
            payload=payload,
            test_mode=True
        )
        message = get_message_for_platform(operation_id)
        allure.attach(str(message), "Message for platform.")

        yield ei_cpid, ei_token, message, ei_url, currency, buyer_id, buyer_scheme

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Update EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ei_cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, ei_cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
