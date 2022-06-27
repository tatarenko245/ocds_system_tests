import copy
import random
import time

import allure
import pytest
import requests

from class_collection.platform_authorization import PlatformAuthorization
from class_collection.prepare_criteria_array import CriteriaArray
from data_collection.data_constant import pmd_for_pn_framework_agreement
from functions_collection.cassandra_methods import get_max_duration_of_fa_from_access_rules, \
    cleanup_ocds_orchestrator_operation_step_by_operation_id, cleanup_table_of_services_for_expenditure_item, \
    cleanup_table_of_services_for_financial_source, cleanup_table_of_services_for_planning_notice, \
    cleanup_orchestrator_steps_by_cpid, cleanup_table_of_services_for_outsourcing_planning_notice, \
    cleanup_table_of_services_for_relation_aggregated_plan, cleanup_table_of_services_for_aggregated_plan, \
    cleanup_table_of_services_for_framework_establishment, cleanup_table_of_services_for_create_submission, \
    cleanup_table_of_services_for_submission_period_end, cleanup_table_of_services_for_qualification_declare
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.mdm_methods import get_standard_criteria
from functions_collection.requests_collection import create_ei_process, create_fs_process, create_pn_process, \
    create_ap_process, outsourcing_pn_process, relation_ap_process, update_ap_process, create_fe_process, \
    amend_fe_process, create_submission_process, qualification_declare_process
from functions_collection.some_functions import time_bot, get_id_token_of_qualification_in_pending_awaiting_state
from payloads_collection.budget.create_ei_payload import ExpenditureItemPayload
from payloads_collection.budget.create_fs_payload import FinancialSourcePayload
from payloads_collection.framework_agreement.amend_fe_payload import AmendFrameworkEstablishmentPayload
from payloads_collection.framework_agreement.create_ap_payload import AggregatedPlan
from payloads_collection.framework_agreement.create_fe_payload import FrameworkEstablishmentPayload
from payloads_collection.framework_agreement.create_pn_payload import PlanningNoticePayload
from payloads_collection.framework_agreement.create_submission_payload import CreateSubmissionPayload
from payloads_collection.framework_agreement.qualification_declare_payload import \
    QualificationDeclareNonConflictOfInterestPayload
from payloads_collection.framework_agreement.update_ap_payload import UpdateAggregatedPlan


@pytest.fixture(scope="function")
# Create EI_1: full data model, create FS_1: full data model, create PN_1: full data model,
# create EI_2: full data model, create FS_2: full data model, create PN_2: full data model,
# create AP: full data model, outsource PN_1: payload isn't needed, outsource PN_2: payload isn't needed,
# relation AP: payload isn't needed, update ap: full data model, create FE: full data model, amend FE: full data model,
# create first Submission: full data model, create second Submission: full data model,
# create third Submission: full data model, Submission Period End: payload isn't needed,
# Qualification Declare: full data model.
def qualification_declare_tc_1(get_parameters, prepare_currency, connect_to_keyspace):
    environment = get_parameters[0]
    bpe_host = get_parameters[2]
    service_host = get_parameters[3]
    country = get_parameters[4]
    language = get_parameters[5]
    pmd = get_parameters[6]
    tender_classification_id = get_parameters[9]
    clean_up_database = get_parameters[10]

    currency = prepare_currency

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_orchestrator = connect_to_keyspace[1]
    connect_to_access = connect_to_keyspace[2]
    connect_to_clarification = connect_to_keyspace[3]
    connect_to_dossier = connect_to_keyspace[4]
    connect_to_qualification = connect_to_keyspace[5]

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
                country=country,
                buyer_id=0,
                tender_classification_id=tender_classification_id,
                amount=100000.00,
                currency=currency)
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
                country=country,
                buyer_id=10,
                tender_classification_id=tender_classification_id,
                amount=100000.00,
                currency=currency)
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
    time.sleep(5)

    # Update AP.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Update AP process.'):
        """
        Tender platform authorization for Update AP process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        update_ap_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Update AP process.'):
        """
        Send request to BPE host to create a Update AP process.
        """
        try:
            """
            Build payload for Update AP process.
            """
            max_duration_of_fa = get_max_duration_of_fa_from_access_rules(
                connect_to_access,
                country,
                pmd
            )

            payload = copy.deepcopy(UpdateAggregatedPlan(
                host_to_service=service_host,
                currency=currency,
                create_ap_payload=ap_payload,
                max_duration_of_fa=max_duration_of_fa,
                tender_classification_id=tender_classification_id
            ))

            payload.customize_tender_lots(quantity_of_lots=3)
            lot_id_list = payload.get_lots_id_from_payload()

            payload.customize_tender_items(
                lot_id_list=lot_id_list,
                quantity_of_items=3,
                quantity_of_items_additional_classifications=3
            )

            payload.customize_tender_documents(
                lot_id_list=lot_id_list,
                quantity_of_new_documents=3
            )
            # Forbidden change currency, even if actual currency == previous currency.
            payload.delete_optional_fields(
                "tender.value"
            )
            payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Update AP process.")

        update_ap_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=update_ap_operation_id,
            payload=payload,
            test_mode=True,
            cpid=ap_cpid,
            ocid=ap_ocid,
            token=ap_token
        )

        message = get_message_for_platform(update_ap_operation_id)
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Create FE: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Create FE process.'):
        """
        Tender platform authorization for Create FE process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        create_fe_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Create FE process.'):
        """
        Send request to BPE host to create a Create FE process.
        """
        try:
            """
            Build payload for Create FE process.
            """
            payload = copy.deepcopy(FrameworkEstablishmentPayload(
                ap_payload=ap_payload,
                host_to_service=service_host,
                country=country,
                language=language,
                environment=environment,
                person_title="Mr.",
                business_functions_type="chairman",
                tender_documents_type="tenderNotice",
                pre_qualification_sec=121
            ))

            payload.customize_tender_pe_persones(
                quantity_of_persones_objects=3,
                quantity_of_bf_objects=3,
                quantity_of_bf_documents_objects=3
            )

            # Get all 'standard' criteria from eMDM service.
            standard_criteria = get_standard_criteria(environment, country, language)

            # Prepare 'exclusion' criteria for payload.
            some_criteria = CriteriaArray(
                host_to_service=service_host,
                country=country,
                language=language,
                environment=environment,
                quantity_of_criteria_objects=len(standard_criteria[1]),
                quantity_of_requirement_groups_objects=1,
                quantity_of_requirements_objects=2,
                quantity_of_eligible_evidences_objects=2,
                type_of_standard_criteria=1
            )
            # Delete redundant attributes: 'minValue', 'maxValue', because attribute ' expectedValue' will be used.
            some_criteria.delete_optional_fields(
                "criteria.requirementGroups.requirements.minValue",
                "criteria.requirementGroups.requirements.maxValue",
                # "criteria.description",
                # "criteria.requirementGroups.description",
                # "criteria.requirementGroups.requirements.description",
                # "criteria.requirementGroups.requirements.period",
                # "criteria.requirementGroups.requirements.eligibleEvidences"
            )

            some_criteria.prepare_criteria_array(criteria_relates_to="tenderer")
            some_criteria.set_unique_temporary_id_for_eligible_evidences()
            some_criteria.set_unique_temporary_id_for_criteria()
            exclusion_criteria_array = some_criteria.build_criteria_array()

            # Prepare 'selection' criteria for payload.
            some_criteria = CriteriaArray(
                host_to_service=service_host,
                country=country,
                language=language,
                environment=environment,
                quantity_of_criteria_objects=len(standard_criteria[2]),
                quantity_of_requirement_groups_objects=2,
                quantity_of_requirements_objects=2,
                quantity_of_eligible_evidences_objects=2,
                type_of_standard_criteria=2
            )
            #  Delete redundant attribute: 'expectedValue', because attributes 'maxValue' and
            #  'minValue' will be used.
            some_criteria.delete_optional_fields(
                "criteria.requirementGroups.requirements.expectedValue",
                # "criteria.description",
                # "criteria.requirementGroups.description",
                # "criteria.requirementGroups.requirements.description",
                # "criteria.requirementGroups.requirements.period",
                # "criteria.requirementGroups.requirements.eligibleEvidences"
            )

            some_criteria.prepare_criteria_array(criteria_relates_to="tenderer")
            some_criteria.set_unique_temporary_id_for_eligible_evidences()
            some_criteria.set_unique_temporary_id_for_criteria()
            selection_criteria_array = some_criteria.build_criteria_array()

            payload.customize_tender_criteria(exclusion_criteria_array, selection_criteria_array)
            payload.customize_tender_documents(quantity_of_new_documents=3)

            create_fe_payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create FE process.")

        create_fe_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=create_fe_operation_id,
            payload=create_fe_payload,
            test_mode=True,
            cpid=ap_cpid,
            ocid=ap_ocid,
            token=ap_token
        )

        message = get_message_for_platform(create_fe_operation_id)
        fe_ocid = message['data']['outcomes']['fe'][0]['id']
        fe_url = f"{message['data']['url']}/{fe_ocid}"
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    previous_fe_release = requests.get(url=fe_url).json()
    # Amend FE: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Amend FE process.'):
        """
        Tender platform authorization for Amend FE process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        amend_fe_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Amend FE process.'):
        """
        Send request to BPE host to create a Amend FE process.
        """
        try:
            """
            Build payload for Amend FE process.
            """
            payload = copy.deepcopy(AmendFrameworkEstablishmentPayload(
                ap_payload=ap_payload,
                create_fe_payload=create_fe_payload,
                previous_fe_release=previous_fe_release,
                host_to_service=service_host,
                country=country,
                language=language,
                environment=environment,
                person_title="Ms.",
                business_functions_type="contactPoint",
                tender_documents_type="complaints",
                pre_qualification_sec=500
            ))

            payload.customize_old_persones(
                "MD-IDNO-create fe: tender.procuringEntity.persones[0].id",
                "MD-IDNO-create fe: tender.procuringEntity.persones[1].id",
                "MD-IDNO-create fe: tender.procuringEntity.persones[2].id",
                need_to_add_new_bf=True,
                quantity_of_new_bf_objects=3,
                need_to_add_new_document=True,
                quantity_of_new_documents_objects=3
            )
            payload.add_new_persones(
                quantity_of_persones_objects=3,
                quantity_of_bf_objects=3,
                quantity_of_documents_objects=3
            )
            payload.customize_old_tender_documents(
                previous_fe_release['releases'][0]['tender']['documents'][0]['id'],
                previous_fe_release['releases'][0]['tender']['documents'][1]['id']
            )
            payload.add_new_tender_documents(quantity_of_new_documents=3)
            payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Amend FE process.")

        amend_fe_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=amend_fe_operation_id,
            payload=payload,
            test_mode=True,
            cpid=ap_cpid,
            ocid=fe_ocid,
            token=ap_token
        )

        message = get_message_for_platform(amend_fe_operation_id)
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Create First Submission: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Create Submission process.'):
        """
        Tender platform authorization for Create Submission process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        create_submission_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Create Submission process.'):
        """
        Send request to BPE host to create a Create Submission process.
        """
        try:
            """
            Build payload for Create Submission process.
            """
            payload = copy.deepcopy(CreateSubmissionPayload(
                service_host,
                previous_fe_release
            ))

            payload.prepare_submission_object(
                submission_position=0,
                quantity_of_candidates=3,
                quantity_of_additional_identifiers=3,
                quantity_of_persones=3,
                quantity_of_evidences=3,
                quantity_of_business_functions=3,
                quantity_of_bf_documents=3,
                quantity_of_main_economic_activities=3,
                quantity_of_bank_accounts=3,
                quantity_of_additional_account_identifiers=3,
                quantity_of_documents=3
            )
            payload.prepare_submission_object(
                submission_position=1,
                quantity_of_candidates=3,
                quantity_of_additional_identifiers=3,
                quantity_of_persones=3,
                quantity_of_evidences=3,
                quantity_of_business_functions=3,
                quantity_of_bf_documents=3,
                quantity_of_main_economic_activities=3,
                quantity_of_bank_accounts=3,
                quantity_of_additional_account_identifiers=3,
                quantity_of_documents=3
            )
            create_1_submission_payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create Submisison process.")

        create_submission_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=create_submission_operation_id,
            payload=create_1_submission_payload,
            test_mode=True,
            cpid=ap_cpid,
            ocid=fe_ocid
        )

        create_1_submission_message = get_message_for_platform(create_submission_operation_id)
        allure.attach(str(create_1_submission_message), "Message for platform.")
    time.sleep(5)

    # Create Second Submission: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Create Submission process.'):
        """
        Tender platform authorization for Create Submission process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        create_submission_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Create Submission process.'):
        """
        Send request to BPE host to create a Create Submission process.
        """
        try:
            """
            Build payload for Create Submission process.
            """
            payload = copy.deepcopy(CreateSubmissionPayload(
                service_host,
                previous_fe_release
            ))

            payload.prepare_submission_object(
                submission_position=2,
                quantity_of_candidates=3,
                quantity_of_additional_identifiers=3,
                quantity_of_persones=3,
                quantity_of_evidences=3,
                quantity_of_business_functions=3,
                quantity_of_bf_documents=3,
                quantity_of_main_economic_activities=3,
                quantity_of_bank_accounts=3,
                quantity_of_additional_account_identifiers=3,
                quantity_of_documents=3
            )
            payload.prepare_submission_object(
                submission_position=3,
                quantity_of_candidates=3,
                quantity_of_additional_identifiers=3,
                quantity_of_persones=3,
                quantity_of_evidences=3,
                quantity_of_business_functions=3,
                quantity_of_bf_documents=3,
                quantity_of_main_economic_activities=3,
                quantity_of_bank_accounts=3,
                quantity_of_additional_account_identifiers=3,
                quantity_of_documents=3
            )
            create_2_submission_payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create Submission process.")

        create_submission_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=create_submission_operation_id,
            payload=create_2_submission_payload,
            test_mode=True,
            cpid=ap_cpid,
            ocid=fe_ocid
        )

        create_2_submission_message = get_message_for_platform(create_submission_operation_id)
        allure.attach(str(create_2_submission_message), "Message for platform.")
    time.sleep(5)

    # Create Third Submission: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Create Submission process.'):
        """
        Tender platform authorization for Create Submission process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        create_submission_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Create Submission process.'):
        """
        Send request to BPE host to create a Create Submission process.
        """
        try:
            """
            Build payload for Create Submission process.
            """
            payload = copy.deepcopy(CreateSubmissionPayload(
                service_host,
                previous_fe_release
            ))

            payload.prepare_submission_object(
                submission_position=4,
                quantity_of_candidates=3,
                quantity_of_additional_identifiers=3,
                quantity_of_persones=3,
                quantity_of_evidences=3,
                quantity_of_business_functions=3,
                quantity_of_bf_documents=3,
                quantity_of_main_economic_activities=3,
                quantity_of_bank_accounts=3,
                quantity_of_additional_account_identifiers=3,
                quantity_of_documents=3
            )
            payload.prepare_submission_object(
                submission_position=5,
                quantity_of_candidates=3,
                quantity_of_additional_identifiers=3,
                quantity_of_persones=3,
                quantity_of_evidences=3,
                quantity_of_business_functions=3,
                quantity_of_bf_documents=3,
                quantity_of_main_economic_activities=3,
                quantity_of_bank_accounts=3,
                quantity_of_additional_account_identifiers=3,
                quantity_of_documents=3
            )
            create_3_submission_payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create Submisison process.")

        create_submission_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=create_submission_operation_id,
            payload=create_3_submission_payload,
            test_mode=True,
            cpid=ap_cpid,
            ocid=fe_ocid
        )

        create_3_submission_message = get_message_for_platform(create_submission_operation_id)
        allure.attach(str(create_3_submission_message), "Message for platform.")
    time.sleep(5)

    # Submission Period End: payload isn't needed.
    previous_fe_release = requests.get(url=fe_url).json()
    step_number += 1
    with allure.step(f"# {step_number}. Get message for platform."):
        time_bot(previous_fe_release['releases'][0]['preQualification']['period']['endDate'])
        message = get_message_for_platform(ocid=fe_ocid, initiator="bpe")
        submission_period_end_message = message[0]
        allure.attach(str(submission_period_end_message), "Message for platform.")
    time.sleep(5)

    # Qualification Declare: full data model.
    previous_fe_release = requests.get(url=fe_url).json()

    """Get requirements for Qualification Declare"""
    if "criteria" in previous_fe_release['releases'][0]['tender']:
        requirements_list = list()
        for c in previous_fe_release['releases'][0]['tender']['criteria']:
            for c_1 in c:
                if c_1 == "source":
                    if c['source'] == "procuringEntity":
                        requirement_groups_list = list()
                        for rg in c['requirementGroups']:
                            for rg_1 in rg:
                                if rg_1 == "id":
                                    requirement_groups_list.append(rg['id'])

                        for x in range(len(requirement_groups_list)):
                            for rr in c['requirementGroups'][x]['requirements']:
                                for rr_1 in rr:
                                    if rr_1 == "id":
                                        requirements_list.append(rr['id'])
    else:
        raise KeyError("The 'criteria' array is missed into FE release.")

    """Get candidates for Qualification Declare"""
    if "qualifications" in previous_fe_release['releases'][0]:
        candidates_list = list()
        for qu in previous_fe_release['releases'][0]['qualifications']:
            if qu['status'] == "pending":
                if "statusDetails" in qu:
                    if qu['statusDetails'] == "awaiting":
                        if 'submissions' in previous_fe_release['releases'][0]:
                            for s in previous_fe_release['releases'][0]['submissions']['details']:
                                if s['id'] == qu['relatedSubmission']:
                                    for cand in range(len(s['candidates'])):
                                        candidate_dictionary = {
                                            "qualification_id": qu['id'],
                                            "candidates": s['candidates'][cand]
                                        }
                                        candidates_list.append(candidate_dictionary)
                        else:
                            raise KeyError("The 'submissions' object is missed into FE release.")
    else:
        raise KeyError("The 'qualifications' array is missed into FE release.")

    """Get qualification.id and qualification.token for Qualification Declare"""
    qualifications_from_message = get_id_token_of_qualification_in_pending_awaiting_state(
        actual_qualifications_array=previous_fe_release['releases'][0]['qualifications'],
        feed_point_message=submission_period_end_message
    )
    qualification_list = list()
    for q in qualifications_from_message:
        qualification_list.append(q)

    """ Depends on quantity of requirements into criteria and
    depends on quantity of candidates into Create Submission payload and
    depends on quantity of qualifications into FE release, send requests"""
    step_number += 1
    for x in range(len(requirements_list)):
        for y in range(len(candidates_list)):
            for q in range(len(qualification_list)):
                if qualification_list[q][0] == candidates_list[y]['qualification_id']:

                    step_number += x + y + q
                    with allure.step(f'# {step_number}. Authorization platform one: Qualification Declare '
                                     f'Non Conflict Of Interest process.'):
                        """
                        Tender platform authorization for Qualification Declare Non Conflict Of Interest process.
                        As result get Tender platform's access token and process operation-id.
                        """
                        platform_one = PlatformAuthorization(bpe_host)
                        access_token = platform_one.get_access_token_for_platform_one()
                        operation_id = platform_one.get_x_operation_id(access_token)

                    step_number += 1
                    with allure.step(f'# {step_number}. Send a request to create '
                                     f'a Qualification Declare  Non Conflict Of Interest process.'):
                        """
                        Send request to BPE host to create a Qualification Declare  Non Conflict Interest process.
                        """
                        try:
                            """
                            Build payload for Qualification Declare Non Conflict Interest process.
                            """
                            payload = copy.deepcopy(QualificationDeclareNonConflictOfInterestPayload(
                                service_host=service_host,
                                requirement_id=requirements_list[x],
                                tenderer_id=candidates_list[y]['candidates']['id'],
                                value=True
                            ))

                            payload.customize_business_functions(
                                quantity_of_bf=3,
                                quantity_of_bf_documents=3
                            )

                            payload = payload.build_payload()
                        except ValueError:
                            raise ValueError("Impossible to build payload for"
                                             "Qualification Declare Non Conflict Interest process.")

                        qualification_declare_process(
                            host=bpe_host,
                            access_token=access_token,
                            x_operation_id=operation_id,
                            payload=payload,
                            test_mode=True,
                            cpid=ap_cpid,
                            ocid=fe_ocid,
                            qualification_id=qualification_list[q][0],
                            qualification_token=qualification_list[q][1]
                        )

                        message = get_message_for_platform(operation_id)
                        allure.attach(str(message), "Message for platform.")

    yield ap_cpid, ap_ocid, ap_token, ap_payload, ap_url, fa_url, pn_1_cpid, pn_1_ocid, pn_1_token, pn_1_payload,\
        pn_1_url, ms_1_url, pn_2_cpid, pn_2_ocid, pn_2_token, pn_2_payload, pn_2_url, ms_2_url, ei_1_payload,\
        ei_2_payload, currency, tender_classification_id, create_fe_payload, fe_ocid, fe_url,\
        create_1_submission_payload, create_1_submission_message, \
        create_2_submission_payload, create_2_submission_message,\
        create_3_submission_payload, create_3_submission_message, submission_period_end_message

    if bool(clean_up_database) is True:
        try:
            """
            CLean up the database.
            """
            # Clean after Crate Ei_1 process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ei_1_cpid)
            cleanup_table_of_services_for_expenditure_item(connect_to_ocds, ei_1_cpid)

            # Clean after Crate FS_1 process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, fs_1_operation_id)
            cleanup_table_of_services_for_financial_source(connect_to_ocds, ei_1_cpid)

            # Clean after Crate PN_1 process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, pn_1_operation_id)
            cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, pn_1_cpid)

            # Clean after Crate Ei_2 process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ei_2_cpid)
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

            # Clean after Update AP process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, update_ap_operation_id)
            cleanup_table_of_services_for_aggregated_plan(connect_to_ocds, connect_to_access, ap_cpid)

            # Clean after Create Framework Establishment process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, create_fe_operation_id)

            cleanup_table_of_services_for_framework_establishment(
                connect_to_ocds, connect_to_access, connect_to_clarification, connect_to_dossier, ap_cpid
            )

            # Clean after Amend Framework Establishment process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, amend_fe_operation_id)

            cleanup_table_of_services_for_framework_establishment(
                connect_to_ocds, connect_to_access, connect_to_clarification, connect_to_dossier, ap_cpid
            )

            # Clean after Create Submission process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ap_cpid)

            cleanup_table_of_services_for_create_submission(
                connect_to_ocds, connect_to_access, connect_to_dossier, ap_cpid)

            # Clean after Create Submission process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ap_cpid)

            cleanup_table_of_services_for_submission_period_end(
                connect_to_ocds, connect_to_access, connect_to_dossier, connect_to_clarification,
                connect_to_qualification, ap_cpid
            )

            # Clean after Qualification Declare Non Conflict Of Interest process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ap_cpid)

            cleanup_table_of_services_for_qualification_declare(
                connect_to_ocds, connect_to_access, connect_to_qualification, ap_cpid)

        except ValueError:
            raise ValueError("Impossible to cLean up the database.")


@pytest.fixture(scope="function")
# Create EI_1: required data model, create FS_1: required data model, create PN_1: required data model,
# create EI_2: required data model, create FS_2: required data model, create PN_2: required data model,
# create AP: required data model, outsource PN_1: payload isn't needed, outsource PN_2: payload isn't needed,
# relation AP: payload isn't needed, update ap: required data model, create FE: required data model,
# amend FE: required data model, create Submission: required data model, Submission Period End: payload isn't needed,
# Qualification Declare: required data model.
def qualification_declare_tc_2(get_parameters, prepare_currency, connect_to_keyspace):
    environment = get_parameters[0]
    bpe_host = get_parameters[2]
    service_host = get_parameters[3]
    country = get_parameters[4]
    language = get_parameters[5]
    pmd = get_parameters[6]
    tender_classification_id = get_parameters[9]
    clean_up_database = get_parameters[10]

    currency = prepare_currency

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_orchestrator = connect_to_keyspace[1]
    connect_to_access = connect_to_keyspace[2]
    connect_to_clarification = connect_to_keyspace[3]
    connect_to_dossier = connect_to_keyspace[4]
    connect_to_qualification = connect_to_keyspace[5]

    # Create EI_1: required data model.
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
                country=country,
                buyer_id=0,
                tender_classification_id=tender_classification_id,
                amount=100000.00,
                currency=currency)
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

    # Create FS_1: required data model.
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

    # Create PN_1: required data model.
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

            payload.delete_optional_fields(
                "planning.rationale",
                "planning.budget.description",
                "tender.procurementMethodRationale",
                "tender.procurementMethodAdditionalInfo",
                "tender.lots",
                "tender.items",
                "tender.documents"
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

    # Create EI_2: required data model.
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
                country=country,
                buyer_id=10,
                tender_classification_id=tender_classification_id,
                amount=100000.00,
                currency=currency)
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

    # Create FS_2: required data model.
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

    # Create PN_2: required data model.
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

            payload.delete_optional_fields(
                "planning.rationale",
                "planning.budget.description",
                "tender.procurementMethodRationale",
                "tender.procurementMethodAdditionalInfo",
                "tender.lots",
                "tender.items",
                "tender.documents"
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

    # Create AP: required data model.
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

            payload.delete_optional_fields(
                "tender.procurementMethodRationale",
                "tender.procuringEntity.additionalIdentifiers",
                "tender.procuringEntity.address.postalCode",
                "tender.procuringEntity.contactPoint.faxNumber",
                "tender.procuringEntity.contactPoint.url",
                "tender.documents"
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

    # Outsource PN_1: required data model.
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

    # Outsource PN_2: required data model.
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
    time.sleep(5)

    # Update AP: required data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Update AP process.'):
        """
        Tender platform authorization for Update AP process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        update_ap_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Update AP process.'):
        """
        Send request to BPE host to create a Update AP process.
        """
        try:
            """
            Build payload for Update AP process.
            """
            max_duration_of_fa = get_max_duration_of_fa_from_access_rules(
                connect_to_access,
                country,
                pmd
            )

            payload = copy.deepcopy(UpdateAggregatedPlan(
                host_to_service=service_host,
                currency=currency,
                create_ap_payload=ap_payload,
                max_duration_of_fa=max_duration_of_fa,
                tender_classification_id=tender_classification_id
            ))

            # Forbidden change currency, even if actual currency == previous currency.
            # Read the rule VR.COM-1.26.14.
            payload.delete_optional_fields(
                "tender.value",
                "tender.procurementMethodRationale",
                "tender.lots.internalId",
                # "tender.lots.placeOfPerformance",
                "tender.items.internalId",
                "tender.items.additionalClassifications",
                "tender.items.deliveryAddress",
                "tender.documents"
            )
            payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Update AP process.")

        update_ap_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=update_ap_operation_id,
            payload=payload,
            test_mode=True,
            cpid=ap_cpid,
            ocid=ap_ocid,
            token=ap_token
        )

        message = get_message_for_platform(update_ap_operation_id)
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Create FE: required data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Create FE process.'):
        """
        Tender platform authorization for Create FE process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        create_fe_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Create FE process.'):
        """
        Send request to BPE host to create a Create FE process.
        """
        try:
            """
            Build payload for Create FE process.
            """
            payload = copy.deepcopy(FrameworkEstablishmentPayload(
                ap_payload=ap_payload,
                host_to_service=service_host,
                country=country,
                language=language,
                environment=environment,
                person_title="Mr.",
                business_functions_type="chairman",
                tender_documents_type="tenderNotice",
                pre_qualification_sec=121
            ))
            payload.delete_optional_fields(
                "tender.secondStage",
                "tender.procurementMethodModalities",
                "tender.procurementMethodRationale",
                "tender.procuringEntity",
                "tender.criteria",
                "tender.documents"
            )
            create_fe_payload = payload.build_payload()

        except ValueError:
            raise ValueError("Impossible to build payload for Create FE process.")

        create_fe_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=create_fe_operation_id,
            payload=create_fe_payload,
            test_mode=True,
            cpid=ap_cpid,
            ocid=ap_ocid,
            token=ap_token
        )

        message = get_message_for_platform(create_fe_operation_id)
        fe_ocid = message['data']['outcomes']['fe'][0]['id']
        fe_url = f"{message['data']['url']}/{fe_ocid}"
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    previous_fe_release = requests.get(url=fe_url).json()
    # Amend FE: full data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Amend FE process.'):
        """
        Tender platform authorization for Amend FE process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        amend_fe_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Amend FE process.'):
        """
        Send request to BPE host to create a Amend FE process.
        """
        try:
            """
            Build payload for Amend FE process.
            """
            payload = copy.deepcopy(AmendFrameworkEstablishmentPayload(
                ap_payload=ap_payload,
                create_fe_payload=create_fe_payload,
                previous_fe_release=previous_fe_release,
                host_to_service=service_host,
                country=country,
                language=language,
                environment=environment,
                person_title="Ms.",
                business_functions_type="contactPoint",
                tender_documents_type="complaints",
                pre_qualification_sec=200
            ))

            payload.delete_optional_fields(
                "tender.procuringEntity",
                "tender.documents",
                "tender.procurementMethodRationale"
            )
            payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Amend FE process.")

        amend_fe_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=amend_fe_operation_id,
            payload=payload,
            test_mode=True,
            cpid=ap_cpid,
            ocid=fe_ocid,
            token=ap_token
        )

        message = get_message_for_platform(amend_fe_operation_id)
        allure.attach(str(message), "Message for platform.")
    time.sleep(5)

    # Create Submission: required data model.
    step_number += 1
    with allure.step(f'# {step_number}. Authorization platform one: Create Submission process.'):
        """
        Tender platform authorization for Create Submission process.
        As result get Tender platform's access token and process operation-id.
        """
        platform_one = PlatformAuthorization(bpe_host)
        access_token = platform_one.get_access_token_for_platform_one()
        create_submission_operation_id = platform_one.get_x_operation_id(access_token)

    step_number += 1
    with allure.step(f'# {step_number}. Send a request to create a Create Submission process.'):
        """
        Send request to BPE host to create a Create Submission process.
        """
        try:
            """
            Build payload for Create Submission process.
            """
            payload = copy.deepcopy(CreateSubmissionPayload(
                service_host,
                previous_fe_release
            ))

            payload.delete_optional_fields(
                "submission.requirementResponses",
                "submission.candidates.identifier.uri",
                "submission.candidates.additionalIdentifiers",
                "submission.candidates.address.postalCode",
                "submission.candidates.contactPoint.faxNumber",
                "submission.candidates.contactPoint.url",
                "submission.candidates.persones",
                "submission.candidates.details.typeOfSupplier",
                "submission.candidates.details.mainEconomicActivities",
                "submission.candidates.details.bankAccounts",
                "submission.candidates.details.legalForm.uri",
                "submission.documents"
            )
            payload.prepare_submission_object(submission_position=0)
            create_submission_payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create Submission process.")

        create_submission_process(
            host=bpe_host,
            access_token=access_token,
            x_operation_id=create_submission_operation_id,
            payload=create_submission_payload,
            test_mode=True,
            cpid=ap_cpid,
            ocid=fe_ocid
        )

        create_submission_message = get_message_for_platform(create_submission_operation_id)
        allure.attach(str(create_submission_message), "Message for platform.")
    time.sleep(5)

    # Submission Period End: payload isn't needed.
    previous_fe_release = requests.get(url=fe_url).json()
    step_number += 1
    with allure.step(f"# {step_number}. Get message for platform."):
        time_bot(previous_fe_release['releases'][0]['preQualification']['period']['endDate'])
        message = get_message_for_platform(ocid=fe_ocid, initiator="bpe")
        submission_period_end_message = message[0]
        allure.attach(str(submission_period_end_message), "Message for platform.")
    time.sleep(5)

    # Qualification Declare: required data model.
    previous_fe_release = requests.get(url=fe_url).json()

    """Get requirements for Qualification Declare"""
    if "criteria" in previous_fe_release['releases'][0]['tender']:
        requirements_list = list()
        for c in previous_fe_release['releases'][0]['tender']['criteria']:
            for c_1 in c:
                if c_1 == "source":
                    if c['source'] == "procuringEntity":
                        requirement_groups_list = list()
                        for rg in c['requirementGroups']:
                            for rg_1 in rg:
                                if rg_1 == "id":
                                    requirement_groups_list.append(rg['id'])

                        for x in range(len(requirement_groups_list)):
                            for rr in c['requirementGroups'][x]['requirements']:
                                for rr_1 in rr:
                                    if rr_1 == "id":
                                        requirements_list.append(rr['id'])
    else:
        raise KeyError("The 'criteria' array is missed into FE release.")

    """Get candidates for Qualification Declare"""
    if "qualifications" in previous_fe_release['releases'][0]:
        candidates_list = list()
        for qu in previous_fe_release['releases'][0]['qualifications']:
            if qu['status'] == "pending":
                if qu['statusDetails'] == "awaiting":
                    if 'submissions' in previous_fe_release['releases'][0]:
                        for s in previous_fe_release['releases'][0]['submissions']['details']:
                            if s['id'] == qu['relatedSubmission']:
                                for cand in range(len(s['candidates'])):
                                    candidate_dictionary = {
                                        "qualification_id": qu['id'],
                                        "candidates": s['candidates'][cand]
                                    }
                                    candidates_list.append(candidate_dictionary)
                    else:
                        raise KeyError("The 'submissions' object is missed into FE release.")
    else:
        raise KeyError("The 'qualifications' array is missed into FE release.")

    """Get qualification.id and qualification.token for Qualification Declare"""
    qualifications_from_message = get_id_token_of_qualification_in_pending_awaiting_state(
        actual_qualifications_array=previous_fe_release['releases'][0]['qualifications'],
        feed_point_message=submission_period_end_message
    )
    qualification_list = list()
    for q in qualifications_from_message:
        qualification_list.append(q)

    """ Depends on quantity of requirements into criteria and
    depends on quantity of candidates into Create Submission payload and
    depends on quantity of qualifications into FE release, send requests"""
    step_number += 1
    for x in range(len(requirements_list)):
        for y in range(len(candidates_list)):
            for q in range(len(qualification_list)):
                if qualification_list[q][0] == candidates_list[y]['qualification_id']:

                    step_number += x + y + q
                    with allure.step(f'# {step_number}. Authorization platform one: Qualification Declare '
                                     f'Non Conflict Interest process.'):
                        """
                        Tender platform authorization for Qualification Declare  Non Conflict Interest process.
                        As result get Tender platform's access token and process operation-id.
                        """
                        platform_one = PlatformAuthorization(bpe_host)
                        access_token = platform_one.get_access_token_for_platform_one()
                        operation_id = platform_one.get_x_operation_id(access_token)

                    step_number += 1
                    with allure.step(f'# {step_number}. Send a request to create '
                                     f'a Qualification Declare  Non Conflict Interest process.'):
                        """
                        Send request to BPE host to create a Qualification Declare  Non Conflict Interest process.
                        """
                        try:
                            """
                            Build payload for Qualification Declare Non Conflict Interest process.
                            """
                            payload = copy.deepcopy(QualificationDeclareNonConflictOfInterestPayload(
                                service_host=service_host,
                                requirement_id=requirements_list[x],
                                tenderer_id=candidates_list[y]['candidates']['id'],
                                value=True
                            ))

                            payload.customize_business_functions(
                                quantity_of_bf=1,
                                quantity_of_bf_documents=0
                            )
                            payload.delete_optional_fields(
                                "requirementResponse.responder.identifier.uri",
                                "requirementResponse.responder.businessFunctions.documents",
                                bf_position=0
                            )
                            payload = payload.build_payload()
                        except ValueError:
                            raise ValueError("Impossible to build payload for"
                                             "Qualification Declare Non Conflict Interest process.")

                        qualification_declare_process(
                            host=bpe_host,
                            access_token=access_token,
                            x_operation_id=operation_id,
                            payload=payload,
                            test_mode=True,
                            cpid=ap_cpid,
                            ocid=fe_ocid,
                            qualification_id=qualification_list[q][0],
                            qualification_token=qualification_list[q][1]
                        )

                        message = get_message_for_platform(operation_id)
                        allure.attach(str(message), "Message for platform.")

    yield ap_cpid, ap_ocid, ap_token, ap_payload, ap_url, fa_url, pn_1_cpid, pn_1_ocid, pn_1_token, pn_1_payload,\
        pn_1_url, ms_1_url, pn_2_cpid, pn_2_ocid, pn_2_token, pn_2_payload, pn_2_url, ms_2_url, ei_1_payload,\
        ei_2_payload, currency, tender_classification_id, create_fe_payload, fe_ocid, fe_url,\
        create_submission_payload, create_submission_message, submission_period_end_message

    if bool(clean_up_database) is True:
        try:
            """
            CLean up the database.
            """
            # Clean after Crate Ei_1 process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ei_1_cpid)
            cleanup_table_of_services_for_expenditure_item(connect_to_ocds, ei_1_cpid)

            # Clean after Crate FS_1 process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, fs_1_operation_id)
            cleanup_table_of_services_for_financial_source(connect_to_ocds, ei_1_cpid)

            # Clean after Crate PN_1 process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, pn_1_operation_id)
            cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, pn_1_cpid)

            # Clean after Crate Ei_2 process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ei_2_cpid)
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

            # Clean after Update AP process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, update_ap_operation_id)
            cleanup_table_of_services_for_aggregated_plan(connect_to_ocds, connect_to_access, ap_cpid)

            # Clean after Create Framework Establishment process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, create_fe_operation_id)

            cleanup_table_of_services_for_framework_establishment(
                connect_to_ocds, connect_to_access, connect_to_clarification, connect_to_dossier, ap_cpid
            )

            # Clean after Amend Framework Establishment process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, amend_fe_operation_id)

            cleanup_table_of_services_for_framework_establishment(
                connect_to_ocds, connect_to_access, connect_to_clarification, connect_to_dossier, ap_cpid
            )

            # Clean after Create Submission process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ap_cpid)

            cleanup_table_of_services_for_create_submission(
                connect_to_ocds, connect_to_access, connect_to_dossier, ap_cpid)

            # Clean after Create Submission process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ap_cpid)

            cleanup_table_of_services_for_submission_period_end(
                connect_to_ocds, connect_to_access, connect_to_dossier, connect_to_clarification,
                connect_to_qualification, ap_cpid
            )

            # Clean after Qualification Declare Non Conflict Of Interest process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, ap_cpid)

            cleanup_table_of_services_for_qualification_declare(
                connect_to_ocds, connect_to_access, connect_to_qualification, ap_cpid)
        except ValueError:
            raise ValueError("Impossible to cLean up the database.")
