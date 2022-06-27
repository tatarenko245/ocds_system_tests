import copy
import random

import allure
import pytest

from class_collection.platform_authorization import PlatformAuthorization
from data_collection.data_constant import pmd_for_pn_framework_agreement
from functions_collection.cassandra_methods import cleanup_ocds_orchestrator_operation_step_by_operation_id, \
    cleanup_table_of_services_for_financial_source, \
    cleanup_table_of_services_for_planning_notice, get_max_duration_of_fa_from_access_rules
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_fs_process, create_pn_process, \
    create_ap_process
from payloads_collection.budget.create_fs_payload import FinancialSourcePayload
from payloads_collection.framework_agreement.create_ap_payload import AggregatedPlan
from payloads_collection.framework_agreement.create_pn_payload import PlanningNoticePayload


@pytest.fixture(scope="function")
# Create EI: full data model, create FS: full data model.
def create_fs_tc_1(get_parameters, connect_to_keyspace, prepare_currency, create_ei_tc_1):
    bpe_host = get_parameters[2]
    connect_to_ocds = connect_to_keyspace[0]
    ei_payload = create_ei_tc_1[0]
    cpid = create_ei_tc_1[1]
    ei_message = create_ei_tc_1[2]
    currency = prepare_currency

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
            payload = copy.deepcopy(FinancialSourcePayload(
                ei_payload=ei_payload,
                amount=89999.89,
                currency=currency,
                payer_id=1,
                funder_id=2
            ))

            payload.customize_buyer_additional_identifiers(
                quantity_of_buyer_additional_identifiers=3
            )
            payload.customize_tender_procuring_entity_additional_identifiers(
                quantity_of_tender_procuring_entity_additional_identifiers=3
            )
            payload = payload.build_payload()
        except ValueError:
            ValueError("Impossible to build payload for Create Fs process.")

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
        yield payload, ocid, message, currency, ei_payload, ei_message
        try:
            """
            CLean up the database.
            """
            # Clean after Crate FS process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_financial_source(connect_to_ocds, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")


@pytest.fixture(scope="function")
# Create EI: required data model, create FS: required data model.
def create_fs_tc_2(get_parameters, connect_to_keyspace, prepare_currency, create_ei_tc_2):
    bpe_host = get_parameters[2]
    connect_to_ocds = connect_to_keyspace[0]
    ei_payload = create_ei_tc_2[0]
    cpid = create_ei_tc_2[1]
    ei_message = create_ei_tc_2[2]
    currency = prepare_currency

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
            payload = copy.deepcopy(FinancialSourcePayload(
                ei_payload=ei_payload,
                amount=89999.89,
                currency=currency,
                payer_id=1
            ))
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
            payload = payload.build_payload()
        except ValueError:
            ValueError("Impossible to build payload for Create Fs process.")

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
        yield payload, ocid, message, currency, ei_payload, ei_message
        try:
            """
            CLean up the database.
            """
            # Clean after Crate FS process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_financial_source(connect_to_ocds, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")


@pytest.fixture(scope="function")
# Create EI: required data model, create FS: required data model.
def create_fs_tc_3(get_parameters, connect_to_keyspace, prepare_currency, create_ei_tc_2, ):
    bpe_host = get_parameters[2]
    connect_to_ocds = connect_to_keyspace[0]
    ei_payload = create_ei_tc_2[0]
    cpid = create_ei_tc_2[1]
    ei_message = create_ei_tc_2[2]
    currency = prepare_currency

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
            payload = copy.deepcopy(FinancialSourcePayload(
                ei_payload=ei_payload,
                amount=89999.89,
                currency=currency,
                payer_id=0
            ))
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
            payload = payload.build_payload()
        except ValueError:
            ValueError("Impossible to build payload for Create Fs process.")

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
        yield payload, ocid, message, currency, ei_payload, ei_message
        try:
            """
            CLean up the database.
            """
            # Clean after Crate FS process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_financial_source(connect_to_ocds, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")


@pytest.fixture(scope="function")
# Create EI: full data model, create FS: full data model, create PN: full data model.
def create_pn_tc_1(get_parameters, connect_to_keyspace, create_fs_tc_1):
    bpe_host = get_parameters[2]
    service_host = get_parameters[3]
    country = get_parameters[4]
    language = get_parameters[5]
    pmd = f"{random.choice(pmd_for_pn_framework_agreement)}"
    tender_classification_id = get_parameters[9]

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_access = connect_to_keyspace[2]

    fs_ocid_list = list()
    fs_payloads_list = list()
    fs_message_list = list()

    fs_1_payload = create_fs_tc_1[0]
    ocid = create_fs_tc_1[1]
    fs_1_message = create_fs_tc_1[2]
    currency = create_fs_tc_1[3]
    fs_ocid_list.append(ocid)
    fs_payloads_list.append(fs_1_payload)
    fs_message_list.append(fs_1_message)

    step_number = 1
    with allure.step(f'# {step_number}. Authorization platform one: Create PN process.'):
        """
        Tender platform authorization for Create PN process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Create PN process.'):
        """
        Send request to BPE host to create a Create PN process.
        And save in variable ocid and token..
        """
        try:
            """
            Build payload for Create PN process.
            """
            payload = copy.deepcopy(PlanningNoticePayload(
                fs_id=ocid,
                amount=910.00,
                currency=currency,
                tender_classification_id=tender_classification_id,
                host_to_service=service_host)
            )

            payload.customize_planning_budget_budget_breakdown(fs_ocid_list)

            payload.customize_tender_lots(
                quantity_of_lots=5
            )

            lot_id_list = payload.get_lots_id_from_payload()

            payload.customize_tender_items(
                lot_id_list=lot_id_list,
                quantity_of_items=5,
                quantity_of_items_additional_classifications=3
            )

            payload.customize_tender_documents(
                lot_id_list=lot_id_list,
                quantity_of_documents=5
            )
            payload = payload.build_payload()

        except ValueError:
            ValueError("Impossible to build payload for Create PN process.")

        create_pn_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=operation_id,
            payload=payload,
            test_mode=True,
            country=country,
            language=language,
            pmd=pmd
        )
        message = get_message_for_platform(operation_id)
        cpid = message['data']['ocid']
        ocid = message['data']['outcomes']['pn'][0]['id']
        token = message['data']['outcomes']['pn'][0]['X-TOKEN']
        allure.attach(str(message), "Message for platform.")
        yield payload, cpid, ocid, token, message, currency, tender_classification_id
        try:
            """
            CLean up the database.
            """
            # Clean after Crate PN process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")


@pytest.fixture(scope="function")
# Create EI: required data model, create FS: required data model, create PN: required data model.
def create_pn_tc_2(get_parameters, connect_to_keyspace, create_fs_tc_2, create_fs_tc_3):
    bpe_host = get_parameters[2]
    service_host = get_parameters[3]
    country = get_parameters[4]
    language = get_parameters[5]
    pmd = f"{random.choice(pmd_for_pn_framework_agreement)}"
    tender_classification_id = get_parameters[9]

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_access = connect_to_keyspace[2]

    fs_ocid_list = list()
    fs_payloads_list = list()
    fs_message_list = list()

    fs_1_payload = create_fs_tc_2[0]
    ocid = create_fs_tc_2[1]
    fs_1_message = create_fs_tc_2[2]
    currency = create_fs_tc_2[3]
    fs_ocid_list.append(ocid)
    fs_payloads_list.append(fs_1_payload)
    fs_message_list.append(fs_1_message)

    fs_2_payload = create_fs_tc_3[0]
    ocid = create_fs_tc_3[1]
    fs_2_message = create_fs_tc_3[2]
    fs_ocid_list.append(ocid)
    fs_payloads_list.append(fs_2_payload)
    fs_message_list.append(fs_2_message)

    step_number = 1
    with allure.step(f'# {step_number}. Authorization platform one: Create PN process.'):
        """
        Tender platform authorization for Create PN process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Create PN process.'):
        """
        Send request to BPE host to create a Create PN process.
        And save in variable ocid and token..
        """
        try:
            """
            Build payload for Create PN process.
            """
            payload = copy.deepcopy(PlanningNoticePayload(
                fs_id=ocid,
                amount=909.99,
                currency=currency,
                tender_classification_id=tender_classification_id,
                host_to_service=service_host)
            )

            payload.customize_planning_budget_budget_breakdown(fs_ocid_list)

            payload.delete_optional_fields(
                "planning.rationale",
                "planning.budget.description",
                "tender.procurementMethodRationale",
                "tender.procurementMethodAdditionalInfo",
                "tender.lots",
                "tender.items",
                "tender.documents"
            )
            payload = payload.build_payload()

        except ValueError:
            ValueError("Impossible to build payload for Create PN process.")

        create_pn_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=operation_id,
            payload=payload,
            test_mode=True,
            country=country,
            language=language,
            pmd=pmd
        )
        message = get_message_for_platform(operation_id)
        cpid = message['data']['ocid']
        ocid = message['data']['outcomes']['pn'][0]['id']
        token = message['data']['outcomes']['pn'][0]['X-TOKEN']
        allure.attach(str(message), "Message for platform.")
        yield payload, cpid, ocid, token, message, currency, tender_classification_id
        try:
            """
            CLean up the database.
            """
            # Clean after Crate PN process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")


@pytest.fixture(scope="function")
# Create EI: full data model, create FS: full data model, create PN: full data model,
# create AP: full data model.
def create_ap_tc_1(get_parameters, connect_to_keyspace, create_pn_tc_1):
    bpe_host = get_parameters[2]
    service_host = get_parameters[3]
    country = get_parameters[4]
    language = get_parameters[5]
    pmd = get_parameters[6]

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_access = connect_to_keyspace[2]

    pn_payload = create_pn_tc_1[0]
    pn_cpid = create_pn_tc_1[1]
    pn_ocid = create_pn_tc_1[2]
    pn_token = create_pn_tc_1[3]
    pn_message = create_pn_tc_1[4]
    currency = create_pn_tc_1[5]
    tender_classification_id = create_pn_tc_1[6]

    pn_url = f"{pn_message['data']['url']}/{pn_message['data']['outcomes']['pn'][0]['id']}"
    ms_url = f"{pn_message['data']['url']}/{pn_message['data']['ocid']}"

    step_number = 1
    with allure.step(f'# {step_number}. Authorization platform one: Create AP process.'):
        """
        Tender platform authorization for Create AP process.
        As result get Tender platform's access ap_token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Create AP process.'):
        """
        Send request to BPE host to create a Create AP process.
        And save in variable ap_cpid and ap_token..
        """
        try:
            """
            Build payload for Create AP process.
            """
            max_duration_of_fa = get_max_duration_of_fa_from_access_rules(
                connect_to_access,
                country,
                pmd
            )

            payload = copy.deepcopy(AggregatedPlan(
                central_purchasing_body_id=55,
                host_to_service=service_host,
                max_duration_of_fa=max_duration_of_fa,
                tender_classification_id=tender_classification_id,
                currency=currency
            ))

            payload.customize_tender_procuring_entity_additional_identifiers(
                quantity_of_tender_procuring_entity_additional_identifiers=3
            )

            payload.customize_tender_documents(
                quantity_of_documents=3
            )
            tender_classification_id = payload.get_tender_classification_id()
            payload = payload.build_payload()
        except ValueError:
            ValueError("Impossible to build payload for Create AP process.")

        create_ap_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=operation_id,
            payload=payload,
            test_mode=True,
            country=country,
            language=language,
            pmd=pmd
        )

        message = get_message_for_platform(operation_id)
        ap_cpid = message['data']['ocid']
        ap_ocid = message['data']['outcomes']['ap'][0]['id']
        ap_token = message['data']['outcomes']['ap'][0]['X-TOKEN']
        ap_url = f"{message['data']['url']}/{ap_ocid}"
        fa_url = f"{message['data']['url']}/{ap_cpid}"
        allure.attach(str(message), "Message for platform.")

        yield payload, ap_cpid, ap_ocid, ap_token, message, currency, tender_classification_id, ap_url, fa_url, \
            pn_cpid, pn_ocid, pn_token, pn_url, ms_url, pn_payload
        try:
            """
            CLean up the database.
            """
            # Clean after Crate AP process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, ap_cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")


@pytest.fixture(scope="function")
# Create EI: required data model, create FS: required data model, create PN: required data model,
# create AP: required data model.
def create_ap_tc_2(get_parameters, connect_to_keyspace, create_pn_tc_2):
    bpe_host = get_parameters[2]
    service_host = get_parameters[3]
    country = get_parameters[4]
    language = get_parameters[5]
    pmd = get_parameters[6]

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_access = connect_to_keyspace[2]

    pn_payload = create_pn_tc_2[0]
    pn_cpid = create_pn_tc_2[1]
    pn_ocid = create_pn_tc_2[2]
    pn_token = create_pn_tc_2[3]
    pn_message = create_pn_tc_2[4]
    currency = create_pn_tc_2[5]
    tender_classification_id = create_pn_tc_2[6]

    pn_url = f"{pn_message['data']['url']}/{pn_message['data']['outcomes']['pn'][0]['id']}"
    ms_url = f"{pn_message['data']['url']}/{pn_message['data']['ocid']}"

    step_number = 1
    with allure.step(f'# {step_number}. Authorization platform one: Create AP process.'):
        """
        Tender platform authorization for Create AP process.
        As result get Tender platform's access ap_token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Create AP process.'):
        """
        Send request to BPE host to create a Create AP process.
        And save in variable ap_cpid and ap_token..
        """
        try:
            """
            Build payload for Create AP process.
            """
            max_duration_of_fa = get_max_duration_of_fa_from_access_rules(
                connect_to_access,
                country,
                pmd
            )

            payload = copy.deepcopy(AggregatedPlan(
                central_purchasing_body_id=55,
                host_to_service=service_host,
                max_duration_of_fa=max_duration_of_fa,
                tender_classification_id=tender_classification_id,
                currency=currency
            ))

            payload.delete_optional_fields(
                "tender.procurementMethodRationale",
                "tender.procuringEntity.additionalIdentifiers",
                "tender.procuringEntity.address.postalCode",
                "tender.procuringEntity.contactPoint.faxNumber",
                "tender.procuringEntity.contactPoint.url",
                "tender.documents"
            )
            tender_classification_id = payload.get_tender_classification_id()
            payload = payload.build_payload()
        except ValueError:
            ValueError("Impossible to build payload for Create AP process.")

        create_ap_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=operation_id,
            payload=payload,
            test_mode=True,
            country=country,
            language=language,
            pmd=pmd
        )

        message = get_message_for_platform(operation_id)
        ap_cpid = message['data']['ocid']
        ap_ocid = message['data']['outcomes']['ap'][0]['id']
        ap_token = message['data']['outcomes']['ap'][0]['X-TOKEN']
        ap_url = f"{message['data']['url']}/{ap_ocid}"
        fa_url = f"{message['data']['url']}/{ap_cpid}"
        allure.attach(str(message), "Message for platform.")

        yield payload, ap_cpid, ap_ocid, ap_token, message, currency, tender_classification_id, ap_url, fa_url, \
            pn_cpid, pn_ocid, pn_token, pn_url, ms_url, pn_payload
        try:
            """
            CLean up the database.
            """
            # Clean after Crate AP process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, ap_cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")
