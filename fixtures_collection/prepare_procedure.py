import copy

import allure
import pytest

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_ocds_orchestrator_operation_step_by_operation_id, \
    cleanup_table_of_services_for_expenditure_item
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_ei_process
from payloads_collection.budget.ei_payload import ExpenditureItemPayload


@pytest.fixture(scope="function")
def create_ei_tc_1(get_credits, connect_to_keyspace):
    bpe_host = get_credits[2]
    country = get_credits[4]
    language = get_credits[5]
    tender_classification_id = get_credits[9]
    connect_to_ocds = connect_to_keyspace[0]

    step_number = 1
    with allure.step(f"# {step_number}. Authorization platform one: Create EI process."):
        """
        Tender platform authorization for Create EI process.
        As result, get tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f"# {step_number}. Send a request to create a Create EI process."):
        """
        Send api request to BPE host to create a Create EI process.
        And save in variable cpid.
        """
        try:
            """
            Build payload for CreateEi process.
            """
            payload = copy.deepcopy(ExpenditureItemPayload(
                buyer_id=0,
                tender_classification_id=tender_classification_id)
            )

            # payload.delete_optional_fields(
            #     "tender.description",
            #     "tender.items",
            #     "planning.rationale",
            #     "buyer.identifier.uri",
            #     "buyer.address.postalCode",
            #     "buyer.additionalIdentifiers",
            #     "buyer.contactPoint.faxNumber",
            #     "buyer.contactPoint.url",
            #     "buyer.details"
            # )

            payload = payload.build_expenditure_item_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create EI process.")

        create_ei_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=operation_id,
            country=country,
            language=language,
            payload=payload,
            test_mode=True
        )
        message = get_message_for_platform(operation_id)
        cpid = message['data']['ocid']
        allure.attach(str(message), "Message for platform.")
        yield payload, cpid, message,
        try:
            """
            CLean up the database.
            """
            # Clean after Crate Ei process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
        except ValueError:
            raise ValueError("Impossible to cLean up the database.")
