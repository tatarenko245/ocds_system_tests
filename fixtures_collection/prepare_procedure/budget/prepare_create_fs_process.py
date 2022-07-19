import copy

import allure
import pytest

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_ocds_orchestrator_operation_step_by_operation_id, \
    cleanup_table_of_services_for_financial_source
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_fs_process
from payloads_collection.budget.create_fs_payload import FinancialSourcePayload


@pytest.fixture(scope="function")
# Create EI: full data model, create FS: full data model.
def create_fs_tc_1_new(get_parameters, connect_to_keyspace, create_ei_tc_1):
    bpe_host = get_parameters[2]
    country = get_parameters[4]
    connect_to_ocds = connect_to_keyspace[0]

    ei_payload = create_ei_tc_1[0]
    ei_cpid = create_ei_tc_1[1]
    ei_message = create_ei_tc_1[2]
    ei_url = create_ei_tc_1[3]
    ei_token = create_ei_tc_1[4]
    currency = create_ei_tc_1[5]
    buyer_id = create_ei_tc_1[6]
    buyer_scheme = create_ei_tc_1[7]

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
        Send request to BPE host to create a Create FS process.
        """
        try:
            """
            Build payload for Create FS process.
            """
            payer_id = 1
            payer_scheme = "MD-IDNO"
            funder_id = 2
            funder_scheme = "MD-IDNO"

            fs_payload = copy.deepcopy(FinancialSourcePayload(
                country=country,
                ei_payload=ei_payload,
                amount=89999.89,
                currency=currency,
                payer_id=payer_id,
                payer_scheme=payer_scheme,
                funder_id=funder_id,
                funder_scheme=funder_scheme
            ))

            fs_payload.customize_buyer_additional_identifiers(
                quantity_of_buyer_additional_identifiers=3
            )
            fs_payload.customize_tender_procuring_entity_additional_identifiers(
                quantity_of_tender_procuring_entity_additional_identifiers=3
            )
            fs_payload = fs_payload.build_payload()
        except ValueError:
            ValueError("Impossible to build payload for Create Fs process.")

        create_fs_process(
            host=bpe_host,
            cpid=ei_cpid,
            access_token=access_token,
            x_operation_id=operation_id,
            payload=fs_payload,
            test_mode=True
        )

        fs_message = get_message_for_platform(operation_id)
        fs_ocid = fs_message['data']['outcomes']['fs'][0]['id']
        fs_token = fs_message['data']['outcomes']['fs'][0]['X-TOKEN']
        fs_url = f"{fs_message['data']['url']}/{fs_ocid}"
        allure.attach(str(fs_message), "Message for platform.")
        yield currency, ei_payload, ei_cpid, ei_token, ei_url, ei_message, fs_payload, fs_ocid, fs_token, fs_url, \
            fs_message, buyer_id, buyer_scheme, payer_id, payer_scheme, funder_id, funder_scheme

        try:
            """
            CLean up the database.
            """
            # Clean after Crate FS process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_financial_source(connect_to_ocds, ei_cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")
