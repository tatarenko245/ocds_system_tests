import copy
import random

import allure
import pytest

from class_collection.platform_authorization import PlatformAuthorization
from data_collection.data_constant import currency_tuple
from functions_collection.cassandra_methods import cleanup_ocds_orchestrator_operation_step_by_operation_id, \
    cleanup_table_of_services_for_expenditure_item, cleanup_table_of_services_for_financial_source
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_ei_process, create_fs_process
from payloads_collection.budget.ei_payload import ExpenditureItemPayload
from payloads_collection.budget.fs_payload import FinancialSourcePayload


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

            payload.delete_optional_fields(
                "tender.description",
                "tender.items",
                "planning.rationale",
                "buyer.identifier.uri",
                "buyer.address.postalCode",
                "buyer.additionalIdentifiers",
                "buyer.contactPoint.faxNumber",
                "buyer.contactPoint.url",
                "buyer.details"
            )

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


@pytest.fixture(scope="function")
def create_fs_tc_1(create_ei_tc_1, get_credits, connect_to_keyspace):
    bpe_host = get_credits[2]
    connect_to_ocds = connect_to_keyspace[0]
    ei_payload = create_ei_tc_1[0]
    cpid = create_ei_tc_1[1]
    currency = f"{random.choice(currency_tuple)}"

    step_number = 1
    with allure.step(f"# {step_number}. Authorization platform one: Create FS process."):
        """
        Tender platform authorization for Create FS process.
        As result, get tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f"# {step_number}. Send a request to create a Create FS process."):
        """
        Send api request to BPE host to create a Create FS process.
        """
        try:
            """
            Build payload for Create FS process.
            """
            payload = copy.deepcopy(FinancialSourcePayload(
                ei_payload=ei_payload,
                amount=89999.89,
                currency=currency,
                payer_id=1,
                funder_id=2)
            )
            payload.delete_optional_fields(
                "tender.procuringEntity.identifier.uri",
                "tender.procuringEntity.address.postalCode",
                "tender.procuringEntity.additionalIdentifiers",
                "tender.procuringEntity.contactPoint.faxNumber",
                "tender.procuringEntity.contactPoint.url",
                "planning.budget.id",
                "planning.budget.description",
                "planning.budget.europeanUnionFunding",
                "planning.budget.project",
                "planning.budget.projectID",
                "planning.budget.uri",
                "planning.rationale",
                "buyer"
            )
            payload = payload.build_financial_source_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create Fs process.")

        create_fs_process(
            host=bpe_host,
            cpid=cpid,
            access_token=access_token,
            x_operation_id=operation_id,
            payload=payload,
            test_mode=True
        )

        message = get_message_for_platform(operation_id)
        ocid = message['data']['outcomes']['fs'][0]['id']
        allure.attach(str(message), "Message for platform.")
        yield payload, ocid, message
        try:
            """
            CLean up the database.
            """
            # Clean after Crate FS process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_financial_source(connect_to_ocds, cpid)
        except ValueError:
            raise ValueError("Impossible to cLean up the database.")
