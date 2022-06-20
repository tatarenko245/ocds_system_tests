import copy
import random
import time

import allure
import pytest

from class_collection.platform_authorization import PlatformAuthorization
from data_collection.data_constant import pmd_for_pn_framework_agreement
from functions_collection.cassandra_methods import get_max_duration_of_fa_from_access_rules, \
    cleanup_ocds_orchestrator_operation_step_by_operation_id, cleanup_table_of_services_for_expenditure_item, \
    cleanup_table_of_services_for_financial_source, cleanup_table_of_services_for_planning_notice, \
    cleanup_orchestrator_steps_by_cpid, cleanup_table_of_services_for_outsourcing_planning_notice, \
    cleanup_table_of_services_for_relation_aggregated_plan, cleanup_orchestrator_steps_by_cpid_and_operationid
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_ei_process, create_fs_process, create_pn_process, \
    create_ap_process, outsourcing_pn_process, relation_ap_process
from payloads_collection.budget.create_ei_payload import ExpenditureItemPayload
from payloads_collection.budget.create_fs_payload import FinancialSourcePayload
from payloads_collection.framework_agreement.create_ap_payload import AggregatedPlan
from payloads_collection.framework_agreement.create_pn_payload import PlanningNoticePayload


@pytest.fixture(scope="function")
# Create EI_1: full data model, create FS_1: full data model, create PN_1: full data model,
# create EI_2: required data model, create FS_2: required data model, create PN_2: required data model,
# create AP: full data model, outsource PN_1: payload isn't needed, outsource PN_2: payload isn't needed,
# relation AP: payload isn't needed.
def relation_ap_tc_1(get_parameters, prepare_currency, connect_to_keyspace):
    bpe_host = get_parameters[2]
    service_host = get_parameters[3]
    country = get_parameters[4]
    language = get_parameters[5]
    pmd = get_parameters[6]
    tender_classification_id = get_parameters[9]

    currency = prepare_currency

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_orchestrator = connect_to_keyspace[1]
    connect_to_access = connect_to_keyspace[2]

    # Create EI_1: full data model.
    step_number = 1
    with allure.step(f"# {step_number}. Authorization platform one: Create EI process."):
        """
        Tender platform authorization for Create EI process.
        As result, get tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        ei_1_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f"# {step_number}. Send a request to create a Create EI process."):
        """
        Send request to BPE host to create a Create EI process.
        And save in variable cpid.
        """
        try:
            """
            Build payload for Create EI process.
            """
            payload = copy.deepcopy(ExpenditureItemPayload(
                buyer_id=0,
                tender_classification_id=tender_classification_id)
            )

            payload.customize_tender_items(
                quantity_of_items=3,
                quantity_of_items_additional_classifications=3
            )
            ei_1_payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create EI process.")

        create_ei_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=ei_1_operation_id,
            country=country,
            language=language,
            payload=ei_1_payload,
            test_mode=True
        )
        message = get_message_for_platform(ei_1_operation_id)
        ei_1_cpid = message['data']['ocid']
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Create FS_1: full data model.
    fs_ocid_list = list()
    fs_payloads_list = list()
    fs_message_list = list()

    step_number += 1
    with allure.step(f"# {step_number}. Authorization platform one: Create FS process."):
        """
        Tender platform authorization for Create FS process.
        As result, get tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        fs_1_operation_id = platform_one.get_x_operation_id(access_token)

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
                ei_payload=ei_1_payload,
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
            fs_payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create Fs process.")

        create_fs_process(
            host=bpe_host,
            cpid=ei_1_cpid,
            access_token=access_token,
            x_operation_id=fs_1_operation_id,
            payload=fs_payload,
            test_mode=True
        )

        message = get_message_for_platform(fs_1_operation_id,)
        fs_ocid = message['data']['outcomes']['fs'][0]['id']
        fs_ocid_list.append(fs_ocid)
        fs_payloads_list.append(fs_payload)
        fs_message_list.append(message)
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Create PN_1: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Create PN process.'):
        """
        Tender platform authorization for Create PN process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        pn_1_operation_id = platform_one.get_x_operation_id(access_token)

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
                fs_id=fs_ocid,
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
            pn_1_payload = payload.build_payload()

        except ValueError:
            raise ValueError("Impossible to build payload for Create PN process.")

        create_pn_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=pn_1_operation_id,
            payload=pn_1_payload,
            test_mode=True,
            country=country,
            language=language,
            pmd=f"{random.choice(pmd_for_pn_framework_agreement)}"
        )
        message = get_message_for_platform(pn_1_operation_id)
        pn_1_cpid = message['data']['ocid']
        pn_1_ocid = message['data']['outcomes']['pn'][0]['id']
        pn_1_token = message['data']['outcomes']['pn'][0]['X-TOKEN']
        pn_1_url = f"{message['data']['url']}/{message['data']['outcomes']['pn'][0]['id']}"
        ms_1_url = f"{message['data']['url']}/{message['data']['ocid']}"
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Create EI_2: full data model.
    step_number += 1
    with allure.step(f"# {step_number}. Authorization platform one: Create EI process."):
        """
        Tender platform authorization for Create EI process.
        As result, get tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        ei_2_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f"# {step_number}. Send a request to create a Create EI process."):
        """
        Send request to BPE host to create a Create EI process.
        And save in variable cpid.
        """
        try:
            """
            Build payload for Create EI process.
            """
            payload = copy.deepcopy(ExpenditureItemPayload(
                buyer_id=0,
                tender_classification_id=tender_classification_id)
            )

            payload.customize_tender_items(
                quantity_of_items=3,
                quantity_of_items_additional_classifications=3
            )
            ei_2_payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create EI process.")

        create_ei_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=ei_2_operation_id,
            country=country,
            language=language,
            payload=ei_2_payload,
            test_mode=True
        )
        message = get_message_for_platform(ei_2_operation_id)
        ei_2_cpid = message['data']['ocid']
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Create FS_2: full data model.
    fs_ocid_list = list()
    fs_payloads_list = list()
    fs_message_list = list()

    step_number += 1
    with allure.step(f"# {step_number}. Authorization platform one: Create FS process."):
        """
        Tender platform authorization for Create FS process.
        As result, get tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        fs_2_operation_id = platform_one.get_x_operation_id(access_token)

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
                ei_payload=ei_2_payload,
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
            fs_payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create Fs process.")

        create_fs_process(
            host=bpe_host,
            cpid=ei_2_cpid,
            access_token=access_token,
            x_operation_id=fs_2_operation_id,
            payload=fs_payload,
            test_mode=True
        )

        message = get_message_for_platform(fs_2_operation_id)
        fs_ocid = message['data']['outcomes']['fs'][0]['id']
        fs_ocid_list.append(fs_ocid)
        fs_payloads_list.append(fs_payload)
        fs_message_list.append(message)
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Create PN_2: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Create PN process.'):
        """
        Tender platform authorization for Create PN process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        pn_2_operation_id = platform_one.get_x_operation_id(access_token)

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
                fs_id=fs_ocid,
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
            pn_2_payload = payload.build_payload()

        except ValueError:
            raise ValueError("Impossible to build payload for Create PN process.")

        create_pn_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=pn_2_operation_id,
            payload=pn_2_payload,
            test_mode=True,
            country=country,
            language=language,
            pmd=f"{random.choice(pmd_for_pn_framework_agreement)}"
        )
        message = get_message_for_platform(pn_2_operation_id)
        pn_2_cpid = message['data']['ocid']
        pn_2_ocid = message['data']['outcomes']['pn'][0]['id']
        pn_2_token = message['data']['outcomes']['pn'][0]['X-TOKEN']
        pn_2_url = f"{message['data']['url']}/{message['data']['outcomes']['pn'][0]['id']}"
        ms_2_url = f"{message['data']['url']}/{message['data']['ocid']}"
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Create AP: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Create AP process.'):
        """
        Tender platform authorization for Create AP process.
        As result get Tender platform's access ap_token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        ap_operation_id = platform_one.get_x_operation_id(access_token)

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

            ap_payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create AP process.")

        create_ap_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=ap_operation_id,
            payload=ap_payload,
            test_mode=True,
            country=country,
            language=language,
            pmd=pmd
        )

        message = get_message_for_platform(ap_operation_id)
        ap_cpid = message['data']['ocid']
        ap_ocid = message['data']['outcomes']['ap'][0]['id']
        ap_token = message['data']['outcomes']['ap'][0]['X-TOKEN']
        ap_url = f"{message['data']['url']}/{ap_ocid}"
        fa_url = f"{message['data']['url']}/{ap_cpid}"
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Outsource PN_1: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Outsourcing PN process.'):
        """
        Tender platform authorization for Outsourcing PN process.
        As result get Tender platform's access pn_token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        outsource_1_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Outsourcing PN process.'):
        """
        Send request to BPE host to create a Outsourcing PN process.
        """

        outsourcing_pn_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=outsource_1_operation_id,
            cpid=pn_1_cpid,
            ocid=pn_1_ocid,
            token=pn_1_token,
            fa=ap_cpid,
            ap=ap_ocid,
            test_mode=True
        )

        message = get_message_for_platform(outsource_1_operation_id)
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Outsource PN_2: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Outsourcing PN process.'):
        """
        Tender platform authorization for Outsourcing PN process.
        As result get Tender platform's access pn_token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        outsource_2_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Outsourcing PN process.'):
        """
        Send request to BPE host to create a Outsourcing PN process.
        """

        outsourcing_pn_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=outsource_2_operation_id,
            cpid=pn_2_cpid,
            ocid=pn_2_ocid,
            token=pn_2_token,
            fa=ap_cpid,
            ap=ap_ocid,
            test_mode=True
        )

        message = get_message_for_platform(outsource_2_operation_id)
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Relation AP for PN_1.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Relation AP process.'):
        """
        Tender platform authorization for Relation AP process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Relation AP process.'):
        """
        Send request to BPE host to create a Relation AP process.
        """

        relation_ap_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=operation_id,
            cpid=ap_cpid,
            ocid=ap_ocid,
            token=ap_token,
            cp=pn_1_cpid,
            pn=pn_1_ocid,
            test_mode=True
        )

        message = get_message_for_platform(operation_id)
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Relation AP for PN_2.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Relation AP process.'):
        """
        Tender platform authorization for Relation AP process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Relation AP process.'):
        """
        Send request to BPE host to create a Relation AP process.
        """

        relation_ap_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=operation_id,
            cpid=ap_cpid,
            ocid=ap_ocid,
            token=ap_token,
            cp=pn_2_cpid,
            pn=pn_2_ocid,
            test_mode=True
        )

        message = get_message_for_platform(operation_id)
        allure.attach(str(message), "Message for platform.")
    yield ap_cpid, ap_ocid, ap_token, ap_payload, ap_url, fa_url, pn_1_cpid, pn_1_ocid, pn_1_token, pn_1_payload,\
        pn_1_url, ms_1_url, pn_2_cpid, pn_2_ocid, pn_2_token, pn_2_payload, pn_2_url, ms_2_url, ei_1_payload,\
        ei_2_payload, currency, tender_classification_id

    try:
        """
        CLean up the database.
        """
        # Clean after Crate Ei_1 process:
        cleanup_orchestrator_steps_by_cpid_and_operationid(connect_to_orchestrator, ei_1_cpid, ei_1_operation_id)
        cleanup_table_of_services_for_expenditure_item(connect_to_ocds, ei_1_cpid)

        # Clean after Crate FS_1 process:
        cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, fs_1_operation_id)
        cleanup_table_of_services_for_financial_source(connect_to_ocds, ei_1_cpid)

        # Clean after Crate PN_1 process:
        cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, pn_1_operation_id)
        cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, pn_1_cpid)

        # Clean after Crate Ei_2 process:
        cleanup_orchestrator_steps_by_cpid_and_operationid(connect_to_orchestrator, ei_1_cpid, ei_1_operation_id)
        cleanup_table_of_services_for_expenditure_item(connect_to_ocds, ei_2_cpid)

        # Clean after Crate FS_2 process:
        cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, fs_2_operation_id)
        cleanup_table_of_services_for_financial_source(connect_to_ocds, ei_2_cpid)

        # Clean after Crate PN_2 process:
        cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, pn_2_operation_id)
        cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, pn_2_cpid)

        # Clean after Crate AP process:
        cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, ap_operation_id)
        cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, ap_cpid)

        # Clean after Outsourcing PN_1 process:
        cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, pn_1_cpid)
        cleanup_table_of_services_for_outsourcing_planning_notice(connect_to_ocds, connect_to_access, pn_1_cpid)

        # Clean after Outsourcing PN_2 process:
        cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, pn_2_cpid)
        cleanup_table_of_services_for_outsourcing_planning_notice(connect_to_ocds, connect_to_access, pn_2_cpid)

        # Clean after Relation AP process:
        cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ap_cpid)
        cleanup_table_of_services_for_relation_aggregated_plan(connect_to_ocds, connect_to_access, ap_cpid)
    except ValueError:
        raise ValueError("Impossible to cLean up the database.")
