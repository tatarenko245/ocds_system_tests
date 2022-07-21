import copy
import json
import os

import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid, \
    cleanup_table_of_services_for_prior_information_notice
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_pin_process
from messages_collection.open.create_pin_message import CreatePriorInformationNoticeMessage
from payloads_collection.open.create_pin_payload import PriorInformationNoticePayload
from releases_collection.open.create_pin_release import CreatePriorInformationNoticeRelease


@allure.parent_suite("Plan")
@allure.suite("Prior Planning Notice")
@allure.severity("Critical")
@allure.testcase(url="https://docs.google.com/spreadsheets/d/1-I_7nLopu_q2wAyWzfTyscHMBL4GA1sIL6IpwBk-QCw/"
                     "edit#gid=159118352",
                 name="Test Suite")
class TestCreatePIN:
    country = os.getenv("COUNTRY")
    if country == "MD":
        # @allure.title("Створити PIN, повна модель, для Молдови.")
        # def test_case_1(self, get_parameters, connect_to_keyspace, create_fs_tc_1_new):
        #
        #     environment = get_parameters[0]
        #     bpe_host = get_parameters[2]
        #     service_host = get_parameters[3]
        #     country = get_parameters[4]
        #     language = get_parameters[5]
        #     pmd = get_parameters[6]
        #     tender_classification_id = get_parameters[9]
        #     clean_up_database = get_parameters[10]
        #
        #     connect_to_ocds = connect_to_keyspace[0]
        #     connect_to_orchestrator = connect_to_keyspace[1]
        #     connect_to_access = connect_to_keyspace[2]
        #     connect_to_clarification = connect_to_keyspace[3]
        #     connect_to_auctions = connect_to_keyspace[8]
        #
        #     currency = create_fs_tc_1_new[0]
        #     ei_cpid = create_fs_tc_1_new[2]
        #     ei_url = create_fs_tc_1_new[4]
        #     fs_ocid = create_fs_tc_1_new[7]
        #     fs_url = create_fs_tc_1_new[9]
        #     buyer_id = create_fs_tc_1_new[11]
        #     buyer_scheme = create_fs_tc_1_new[12]
        #
        #     previous_ei_release = requests.get(ei_url).json()
        #     previous_fs_release = requests.get(fs_url).json()
        #
        #     """
        #     VR.COM-14.4.3 Check EI state.
        #     """
        #     if previous_ei_release['releases'][0]['tender']['status'] == "planning":
        #         pass
        #     else:
        #         raise ValueError(f"The EI release has invalid state: "
        #                          f"{previous_ei_release['releases'][0]['tender']['status']}.")
        #
        #     """
        #     VR.COM-14.4.4 Check FS state.
        #     """
        #     if previous_fs_release['releases'][0]['tender']['status'] == "active":
        #         pass
        #     else:
        #         raise ValueError(f"The FS release has invalid state: "
        #                          f"{previous_fs_release['releases'][0]['tender']['status']}.")
        #
        #     step_number = 1
        #     with allure.step(f"# {step_number}. Authorization platform one: Create PIN process."):
        #         """
        #         Tender platform authorization for Create PIN process.
        #         As result, get tender platform's access token and process operation-id.
        #         """
        #         platform_one = PlatformAuthorization(bpe_host)
        #         access_token = platform_one.get_access_token_for_platform_one()
        #         operation_id = platform_one.get_x_operation_id(access_token)
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. Send a request to create a Create PIN process."):
        #         """
        #         Send api request to BPE host to create a Create PIN process.
        #         """
        #
        #         try:
        #             """
        #             Build payload for Create PIN process.
        #             """
        #             payload = copy.deepcopy(PriorInformationNoticePayload(
        #                 environment=environment,
        #                 language=language,
        #                 host_to_service=service_host,
        #                 country=country,
        #                 amount=5000.00,
        #                 currency=currency,
        #                 tender_classification_id=tender_classification_id,
        #                 procurinentity_id=buyer_id,
        #                 procurinentity_scheme=buyer_scheme
        #             ))
        #
        #             list_of_classifications = [
        #                 {
        #                     "ei": ei_cpid,
        #                     "fs": fs_ocid
        #                 }
        #             ]
        #             payload.customize_planning_budget_budgetbreakdown(connect_to_ocds, list_of_classifications)
        #
        #             payload.customize_tender_lots(
        #                 quantity_of_lots=1,
        #                 quantity_of_options=1,
        #                 quantity_of_recurrence_dates=1,
        #                 quantity_of_renewal=1
        #             )
        #
        #             lots_id = payload.get_lots_id_from_payload()
        #
        #             payload.customize_tender_items(
        #                 quantity_of_items=1,
        #                 quantity_of_items_additionalclassifications=1
        #             )
        #
        #             payload.customize_tender_electronicauctions_object(connect_to_auctions, pmd)
        #
        #             payload.customize_tender_procuringentity_additionalidentifiers(
        #                 quantity_of_tender_procuring_entity_additional_identifiers=1
        #             )
        #
        #             payload.customize_tender_procuringentity_bf_persones_array(
        #                 quantity_of_persones_objects=1,
        #                 quantity_of_bf_objects=1,
        #                 quantity_of_documents_objects=1
        #             )
        #             exclusion_criteria_array = payload.prepare_exclusion_criteria(
        #                 "criteria.relatedItem",
        #                 "criteria.requirementGroups.requirements.minValue",
        #                 "criteria.requirementGroups.requirements.maxValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="tenderer"
        #             )
        #
        #             selection_criteria_array = payload.prepare_selection_criteria(
        #                 "criteria.relatedItem",
        #                 "criteria.requirementGroups.requirements.expectedValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="tenderer"
        #             )
        #
        #             other_criteria_array = payload.prepare_other_criteria(
        #                 "criteria.requirementGroups.requirements.minValue",
        #                 "criteria.requirementGroups.requirements.maxValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="lot",
        #                 criteria_related_item=lots_id[0]
        #             )
        #
        #             payload.customize_tender_criteria(
        #                 exclusion_criteria_array, selection_criteria_array, other_criteria_array
        #             )
        #
        #             selection_conversions_array = payload.prepare_selection_conversions(selection_criteria_array)
        #             other_conversions_array = payload.prepare_other_conversions(other_criteria_array)
        #             payload.customize_tender_conversions(selection_conversions_array, other_conversions_array)
        #
        #             relates_to = {
        #                 "relatesTo": "lot",
        #                 "relatedItems": lots_id
        #             }
        #
        #             payload.customize_tender_targets(
        #                 targets_dict=relates_to
        #             )
        #
        #             payload.customize_tender_documents(
        #                 quantity_of_documents=1
        #             )
        #
        #             payload = payload.build_payload()
        #         except ValueError:
        #             raise ValueError("Impossible to build payload for Create PIN process.")
        #
        #         synchronous_result = create_pin_process(
        #             host=bpe_host,
        #             access_token=access_token,
        #             x_operation_id=operation_id,
        #             country=country,
        #             language=language,
        #             pmd=pmd,
        #             payload=payload,
        #             test_mode=True
        #         )
        #         message = get_message_for_platform(operation_id)
        #         cpid = message['data']['ocid'][:28]
        #         ocid = message['data']['outcomes']['pin'][0]['id']
        #         allure.attach(str(message), "Message for platform.")
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. See result"):
        #         """
        #         Check the results of TestCase.
        #         """
        #
        #         with allure.step(f"# {step_number}.1. Check status code"):
        #             """
        #             Check the status code of sending the request.
        #             """
        #             with allure.step('Compare actual status code and expected status code of sending request.'):
        #                 allure.attach(str(synchronous_result.status_code), "Actual status code.")
        #                 allure.attach(str(202), "Expected status code.")
        #                 assert synchronous_result.status_code == 202
        #
        #         with allure.step(f'# {step_number}.2. Check the message for the platform, the Create PIN process.'):
        #             """
        #             Check the message for platform.
        #             """
        #             actual_message = message
        #
        #             try:
        #                 """
        #                 Build expected message for platform.
        #                 """
        #                 expected_message = copy.deepcopy(CreatePriorInformationNoticeMessage(
        #                     environment=environment,
        #                     country=country,
        #                     actual_message=actual_message,
        #                     test_mode=True)
        #                 )
        #
        #                 expected_message = expected_message.build_expected_success_message()
        #             except ValueError:
        #                 ValueError("Impossible to build expected message for platform.")
        #
        #             with allure.step('Compare actual and expected message for platform.'):
        #                 allure.attach(json.dumps(actual_message), "Actual message.")
        #                 allure.attach(json.dumps(expected_message), "Expected message.")
        #
        #                 assert actual_message == expected_message, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.3. Check PI release.'):
        #             """
        #             Compare actual PI release and expected PI release.
        #             """
        #             url = f"{actual_message['data']['url']}/{ocid}"
        #             actual_pi_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected PI release.
        #                 """
        #                 expected_release = copy.deepcopy(CreatePriorInformationNoticeRelease(
        #                     environment, country, language, tender_classification_id, payload, actual_message
        #                 ))
        #                 expected_pi_release = expected_release.build_expected_pi_release(actual_pi_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected PI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_pi_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_pi_release), "Expected release.")
        #
        #                 assert actual_pi_release == expected_pi_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.4. Check MS release.'):
        #             """
        #             Compare actual MS release and expected MS release.
        #             """
        #             url = f"{actual_message['data']['url']}/{cpid}"
        #             actual_ms_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected MS release.
        #                 """
        #                 expected_ms_release = expected_release.build_expected_ms_release(
        #                     actual_ms_release, pmd, need_fs=True
        #                 )
        #             except ValueError:
        #                 ValueError("Impossible to build expected MS release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ms_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ms_release), "Expected release.")
        #
        #                 assert actual_ms_release == expected_ms_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.5. Check EI release.'):
        #             """
        #             Compare actual EI release and expected EI release.
        #             """
        #             actual_ei_release = requests.get(url=ei_url).json()
        #
        #             try:
        #                 """
        #                 Build expected EI release.
        #                 """
        #                 expected_ei_release = expected_release.build_expected_ei_release(actual_ei_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected EI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ei_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ei_release), "Expected release.")
        #
        #                 assert actual_ei_release == expected_ei_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.6. Check FS release.'):
        #             """
        #             Compare actual FS release and expected FS release.
        #             """
        #             actual_fs_release = requests.get(url=fs_url).json()
        #
        #             try:
        #                 """
        #                 Build expected FS release.
        #                 """
        #                 expected_fs_release = expected_release.build_expected_fs_release(actual_fs_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected FS release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_fs_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_fs_release), "Expected release.")
        #
        #                 assert actual_fs_release == expected_fs_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #     if clean_up_database is True:
        #         try:
        #             """
        #             CLean up the database.
        #             """
        #             # Clean after Create PIN process:
        #             cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
        #             cleanup_table_of_services_for_prior_information_notice(
        #                 connect_to_ocds, connect_to_auctions, connect_to_clarification, connect_to_access, cpid
        #             )
        #         except ValueError:
        #             ValueError("Impossible to cLean up the database.")
        #     else:
        #         with allure.step("The steps of process."):
        #             allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                           f"operation_id = '{operation_id}' ALLOW FILTERING;",
        #                           "Cassandra DataBase: steps of process.")
        #
        # @allure.title("Створити PIN повна модель, без опціональних атрибутів на другому рівні, для Молдови.")
        # def test_case_2(self, get_parameters, connect_to_keyspace, create_fs_tc_1_new):
        #
        #     environment = get_parameters[0]
        #     bpe_host = get_parameters[2]
        #     service_host = get_parameters[3]
        #     country = get_parameters[4]
        #     language = get_parameters[5]
        #     pmd = get_parameters[6]
        #     tender_classification_id = get_parameters[9]
        #     clean_up_database = get_parameters[10]
        #
        #     connect_to_ocds = connect_to_keyspace[0]
        #     connect_to_orchestrator = connect_to_keyspace[1]
        #     connect_to_access = connect_to_keyspace[2]
        #     connect_to_clarification = connect_to_keyspace[3]
        #     connect_to_auctions = connect_to_keyspace[8]
        #
        #     currency = create_fs_tc_1_new[0]
        #     ei_cpid = create_fs_tc_1_new[2]
        #     ei_url = create_fs_tc_1_new[4]
        #     fs_ocid = create_fs_tc_1_new[7]
        #     fs_url = create_fs_tc_1_new[9]
        #     buyer_id = create_fs_tc_1_new[11]
        #     buyer_scheme = create_fs_tc_1_new[12]
        #
        #     previous_ei_release = requests.get(ei_url).json()
        #     previous_fs_release = requests.get(fs_url).json()
        #
        #     """
        #     VR.COM-14.4.3 Check EI state.
        #     """
        #     if previous_ei_release['releases'][0]['tender']['status'] == "planning":
        #         pass
        #     else:
        #         raise ValueError(f"The EI release has invalid state: "
        #                          f"{previous_ei_release['releases'][0]['tender']['status']}.")
        #
        #     """
        #     VR.COM-14.4.4 Check FS state.
        #     """
        #     if previous_fs_release['releases'][0]['tender']['status'] == "active":
        #         pass
        #     else:
        #         raise ValueError(f"The FS release has invalid state: "
        #                          f"{previous_fs_release['releases'][0]['tender']['status']}.")
        #
        #     step_number = 1
        #     with allure.step(f"# {step_number}. Authorization platform one: Create PIN process."):
        #         """
        #         Tender platform authorization for Create PIN process.
        #         As result, get tender platform's access token and process operation-id.
        #         """
        #         platform_one = PlatformAuthorization(bpe_host)
        #         access_token = platform_one.get_access_token_for_platform_one()
        #         operation_id = platform_one.get_x_operation_id(access_token)
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. Send a request to create a Create PIN process."):
        #         """
        #         Send api request to BPE host to create a Create PIN process.
        #         """
        #
        #         try:
        #             """
        #             Build payload for Create PIN process.
        #             """
        #             payload = copy.deepcopy(PriorInformationNoticePayload(
        #                 environment=environment,
        #                 language=language,
        #                 host_to_service=service_host,
        #                 country=country,
        #                 amount=5000.00,
        #                 currency=currency,
        #                 tender_classification_id=tender_classification_id,
        #                 procurinentity_id=buyer_id,
        #                 procurinentity_scheme=buyer_scheme
        #             ))
        #
        #             list_of_classifications = [
        #                 {
        #                     "ei": ei_cpid,
        #                     "fs": fs_ocid
        #                 }
        #             ]
        #             payload.customize_planning_budget_budgetbreakdown(connect_to_ocds, list_of_classifications)
        #
        #             payload.customize_tender_lots(
        #                 quantity_of_lots=1,
        #                 quantity_of_options=1,
        #                 quantity_of_recurrence_dates=1,
        #                 quantity_of_renewal=1
        #             )
        #
        #             payload.customize_tender_items(
        #                 quantity_of_items=1,
        #                 quantity_of_items_additionalclassifications=1
        #             )
        #
        #             payload.customize_tender_procuringentity_additionalidentifiers(
        #                 quantity_of_tender_procuring_entity_additional_identifiers=1
        #             )
        #
        #             payload.customize_tender_procuringentity_bf_persones_array(
        #                 quantity_of_persones_objects=1,
        #                 quantity_of_bf_objects=1,
        #                 quantity_of_documents_objects=1
        #             )
        #
        #             payload.delete_optional_fields(
        #                 "planning.rationale",
        #                 "tender.procurementMethodRationale",
        #                 "tender.enquiryPeriod",
        #                 "tender.procurementMethodModalities",
        #                 "tender.electronicAuctions",
        #                 "tender.criteria",
        #                 "tender.conversions",
        #                 "tender.targets",
        #                 "tender.documents"
        #             )
        #             payload = payload.build_payload()
        #             payload['tender']['awardCriteria'] = "priceOnly"
        #             payload['tender']['awardCriteriaDetails'] = "automated"
        #         except ValueError:
        #             raise ValueError("Impossible to build payload for Create PIN process.")
        #
        #         synchronous_result = create_pin_process(
        #             host=bpe_host,
        #             access_token=access_token,
        #             x_operation_id=operation_id,
        #             country=country,
        #             language=language,
        #             pmd=pmd,
        #             payload=payload,
        #             test_mode=True
        #         )
        #         message = get_message_for_platform(operation_id)
        #         cpid = message['data']['ocid'][:28]
        #         ocid = message['data']['outcomes']['pin'][0]['id']
        #         allure.attach(str(message), "Message for platform.")
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. See result"):
        #         """
        #         Check the results of TestCase.
        #         """
        #
        #         with allure.step(f"# {step_number}.1. Check status code"):
        #             """
        #             Check the status code of sending the request.
        #             """
        #             with allure.step('Compare actual status code and expected status code of sending request.'):
        #                 allure.attach(str(synchronous_result.status_code), "Actual status code.")
        #                 allure.attach(str(202), "Expected status code.")
        #                 assert synchronous_result.status_code == 202
        #
        #         with allure.step(f'# {step_number}.2. Check the message for the platform, the Create PIN process.'):
        #             """
        #             Check the message for platform.
        #             """
        #             actual_message = message
        #
        #             try:
        #                 """
        #                 Build expected message for platform.
        #                 """
        #                 expected_message = copy.deepcopy(CreatePriorInformationNoticeMessage(
        #                     environment=environment,
        #                     country=country,
        #                     actual_message=actual_message,
        #                     test_mode=True)
        #                 )
        #
        #                 expected_message = expected_message.build_expected_success_message()
        #             except ValueError:
        #                 ValueError("Impossible to build expected message for platform.")
        #
        #             with allure.step('Compare actual and expected message for platform.'):
        #                 allure.attach(json.dumps(actual_message), "Actual message.")
        #                 allure.attach(json.dumps(expected_message), "Expected message.")
        #
        #                 assert actual_message == expected_message, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.3. Check PI release.'):
        #             """
        #             Compare actual PI release and expected PI release.
        #             """
        #             url = f"{actual_message['data']['url']}/{ocid}"
        #             actual_pi_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected PI release.
        #                 """
        #                 expected_release = copy.deepcopy(CreatePriorInformationNoticeRelease(
        #                     environment, country, language, tender_classification_id, payload, actual_message
        #                 ))
        #                 expected_pi_release = expected_release.build_expected_pi_release(actual_pi_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected PI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_pi_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_pi_release), "Expected release.")
        #
        #                 assert actual_pi_release == expected_pi_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.4. Check MS release.'):
        #             """
        #             Compare actual MS release and expected MS release.
        #             """
        #             url = f"{actual_message['data']['url']}/{cpid}"
        #             actual_ms_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected MS release.
        #                 """
        #                 expected_ms_release = expected_release.build_expected_ms_release(
        #                     actual_ms_release, pmd, need_fs=True
        #                 )
        #             except ValueError:
        #                 ValueError("Impossible to build expected MS release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ms_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ms_release), "Expected release.")
        #
        #                 assert actual_ms_release == expected_ms_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.5. Check EI release.'):
        #             """
        #             Compare actual EI release and expected EI release.
        #             """
        #             actual_ei_release = requests.get(url=ei_url).json()
        #
        #             try:
        #                 """
        #                 Build expected EI release.
        #                 """
        #                 expected_ei_release = expected_release.build_expected_ei_release(actual_ei_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected EI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ei_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ei_release), "Expected release.")
        #
        #                 assert actual_ei_release == expected_ei_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.6. Check FS release.'):
        #             """
        #             Compare actual FS release and expected FS release.
        #             """
        #             actual_fs_release = requests.get(url=fs_url).json()
        #
        #             try:
        #                 """
        #                 Build expected FS release.
        #                 """
        #                 expected_fs_release = expected_release.build_expected_fs_release(actual_fs_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected FS release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_fs_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_fs_release), "Expected release.")
        #
        #                 assert actual_fs_release == expected_fs_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #     if clean_up_database is True:
        #         try:
        #             """
        #             CLean up the database.
        #             """
        #             # Clean after Create PIN process:
        #             cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
        #             cleanup_table_of_services_for_prior_information_notice(
        #                 connect_to_ocds, connect_to_auctions, connect_to_clarification, connect_to_access, cpid
        #             )
        #         except ValueError:
        #             ValueError("Impossible to cLean up the database.")
        #     else:
        #         with allure.step("The steps of process."):
        #             allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                           f"operation_id = '{operation_id}' ALLOW FILTERING;",
        #                           "Cassandra DataBase: steps of process.")
        #
        # @allure.title("Створити PIN повна модель, без опціональних атрибутів на третьому рівні, для Молдови.")
        # def test_case_3(self, get_parameters, connect_to_keyspace, create_fs_tc_1_new):
        #
        #     environment = get_parameters[0]
        #     bpe_host = get_parameters[2]
        #     service_host = get_parameters[3]
        #     country = get_parameters[4]
        #     language = get_parameters[5]
        #     pmd = get_parameters[6]
        #     tender_classification_id = get_parameters[9]
        #     clean_up_database = get_parameters[10]
        #
        #     connect_to_ocds = connect_to_keyspace[0]
        #     connect_to_orchestrator = connect_to_keyspace[1]
        #     connect_to_access = connect_to_keyspace[2]
        #     connect_to_clarification = connect_to_keyspace[3]
        #     connect_to_auctions = connect_to_keyspace[8]
        #
        #     currency = create_fs_tc_1_new[0]
        #     ei_cpid = create_fs_tc_1_new[2]
        #     ei_url = create_fs_tc_1_new[4]
        #     fs_ocid = create_fs_tc_1_new[7]
        #     fs_url = create_fs_tc_1_new[9]
        #     buyer_id = create_fs_tc_1_new[11]
        #     buyer_scheme = create_fs_tc_1_new[12]
        #
        #     previous_ei_release = requests.get(ei_url).json()
        #     previous_fs_release = requests.get(fs_url).json()
        #
        #     """
        #     VR.COM-14.4.3 Check EI state.
        #     """
        #     if previous_ei_release['releases'][0]['tender']['status'] == "planning":
        #         pass
        #     else:
        #         raise ValueError(f"The EI release has invalid state: "
        #                          f"{previous_ei_release['releases'][0]['tender']['status']}.")
        #
        #     """
        #     VR.COM-14.4.4 Check FS state.
        #     """
        #     if previous_fs_release['releases'][0]['tender']['status'] == "active":
        #         pass
        #     else:
        #         raise ValueError(f"The FS release has invalid state: "
        #                          f"{previous_fs_release['releases'][0]['tender']['status']}.")
        #
        #     step_number = 1
        #     with allure.step(f"# {step_number}. Authorization platform one: Create PIN process."):
        #         """
        #         Tender platform authorization for Create PIN process.
        #         As result, get tender platform's access token and process operation-id.
        #         """
        #         platform_one = PlatformAuthorization(bpe_host)
        #         access_token = platform_one.get_access_token_for_platform_one()
        #         operation_id = platform_one.get_x_operation_id(access_token)
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. Send a request to create a Create PIN process."):
        #         """
        #         Send api request to BPE host to create a Create PIN process.
        #         """
        #
        #         try:
        #             """
        #             Build payload for Create PIN process.
        #             """
        #             payload = copy.deepcopy(PriorInformationNoticePayload(
        #                 environment=environment,
        #                 language=language,
        #                 host_to_service=service_host,
        #                 country=country,
        #                 amount=5000.00,
        #                 currency=currency,
        #                 tender_classification_id=tender_classification_id,
        #                 procurinentity_id=buyer_id,
        #                 procurinentity_scheme=buyer_scheme
        #             ))
        #
        #             list_of_classifications = [
        #                 {
        #                     "ei": ei_cpid,
        #                     "fs": fs_ocid
        #                 }
        #             ]
        #             payload.customize_planning_budget_budgetbreakdown(connect_to_ocds, list_of_classifications)
        #
        #             payload.customize_tender_lots(
        #                 quantity_of_lots=1,
        #                 quantity_of_options=0,
        #                 quantity_of_recurrence_dates=0,
        #                 quantity_of_renewal=0
        #             )
        #
        #             lots_id = payload.get_lots_id_from_payload()
        #
        #             payload.customize_tender_items(
        #                 quantity_of_items=1,
        #                 quantity_of_items_additionalclassifications=1
        #             )
        #
        #             payload.customize_tender_electronicauctions_object(connect_to_auctions, pmd)
        #
        #             payload.customize_tender_procuringentity_additionalidentifiers(
        #                 quantity_of_tender_procuring_entity_additional_identifiers=1
        #             )
        #
        #             payload.customize_tender_procuringentity_bf_persones_array(
        #                 quantity_of_persones_objects=1,
        #                 quantity_of_bf_objects=1,
        #                 quantity_of_documents_objects=1
        #             )
        #             exclusion_criteria_array = payload.prepare_exclusion_criteria(
        #                 "criteria.classification",
        #                 "criteria.description",
        #                 "criteria.relatedItem",
        #                 "criteria.requirementGroups.requirements.minValue",
        #                 "criteria.requirementGroups.requirements.maxValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="tenderer"
        #             )
        #
        #             selection_criteria_array = payload.prepare_selection_criteria(
        #                 "criteria.classification",
        #                 "criteria.description",
        #                 "criteria.relatedItem",
        #                 "criteria.requirementGroups.requirements.expectedValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="tenderer"
        #             )
        #
        #             other_criteria_array = payload.prepare_other_criteria(
        #                 "criteria.classification",
        #                 "criteria.description",
        #                 "criteria.relatedItem",
        #                 "criteria.requirementGroups.requirements.minValue",
        #                 "criteria.requirementGroups.requirements.maxValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="lot",
        #                 criteria_related_item=lots_id[0]
        #             )
        #
        #             payload.customize_tender_criteria(
        #                 exclusion_criteria_array, selection_criteria_array, other_criteria_array
        #             )
        #
        #             # Attributes 'tender.lots[0].options', 'tender.lots[0].recurrence', 'tender.lots[0].renewal'
        #             # had been deleted in 'customize_tender_lots' method.
        #             payload.delete_optional_fields(
        #                 "planning.budget.description",
        #                 "tender.procuringEntity.additionalIdentifiers",
        #                 "tender.procuringEntity.persones",
        #                 "tender.conversions[?].description",
        #                 "tender.targets[?].relatedItem",
        #                 "tender.lots[?].internalId",
        #                 "tender.lots[?].hasOptions",
        #                 "tender.lots[?].hasRecurrence",
        #                 "tender.lots[?].hasRenewal",
        #                 "tender.items[?].internalId",
        #                 "tender.items[?].additionalClassifications",
        #                 "tender.documents[?].description",
        #                 "tender.documents[?].relatedLots",
        #                 conversion_position=0,
        #                 target_position=0,
        #                 lot_position=0,
        #                 item_position=0,
        #                 document_position=0
        #             )
        #
        #             selection_conversions_array = payload.prepare_selection_conversions(selection_criteria_array)
        #             other_conversions_array = payload.prepare_other_conversions(other_criteria_array)
        #             payload.customize_tender_conversions(selection_conversions_array, other_conversions_array)
        #
        #             relates_to = {
        #                 "relatesTo": "lot",
        #                 "relatedItems": lots_id
        #             }
        #
        #             payload.customize_tender_targets(
        #                 targets_dict=relates_to
        #             )
        #
        #             payload.customize_tender_documents(
        #                 quantity_of_documents=1
        #             )
        #
        #             payload = payload.build_payload()
        #         except ValueError:
        #             raise ValueError("Impossible to build payload for Create PIN process.")
        #
        #         synchronous_result = create_pin_process(
        #             host=bpe_host,
        #             access_token=access_token,
        #             x_operation_id=operation_id,
        #             country=country,
        #             language=language,
        #             pmd=pmd,
        #             payload=payload,
        #             test_mode=True
        #         )
        #         message = get_message_for_platform(operation_id)
        #         cpid = message['data']['ocid'][:28]
        #         ocid = message['data']['outcomes']['pin'][0]['id']
        #         allure.attach(str(message), "Message for platform.")
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. See result"):
        #         """
        #         Check the results of TestCase.
        #         """
        #
        #         with allure.step(f"# {step_number}.1. Check status code"):
        #             """
        #             Check the status code of sending the request.
        #             """
        #             with allure.step('Compare actual status code and expected status code of sending request.'):
        #                 allure.attach(str(synchronous_result.status_code), "Actual status code.")
        #                 allure.attach(str(202), "Expected status code.")
        #                 assert synchronous_result.status_code == 202
        #
        #         with allure.step(f'# {step_number}.2. Check the message for the platform, the Create PIN process.'):
        #             """
        #             Check the message for platform.
        #             """
        #             actual_message = message
        #
        #             try:
        #                 """
        #                 Build expected message for platform.
        #                 """
        #                 expected_message = copy.deepcopy(CreatePriorInformationNoticeMessage(
        #                     environment=environment,
        #                     country=country,
        #                     actual_message=actual_message,
        #                     test_mode=True)
        #                 )
        #
        #                 expected_message = expected_message.build_expected_success_message()
        #             except ValueError:
        #                 ValueError("Impossible to build expected message for platform.")
        #
        #             with allure.step('Compare actual and expected message for platform.'):
        #                 allure.attach(json.dumps(actual_message), "Actual message.")
        #                 allure.attach(json.dumps(expected_message), "Expected message.")
        #
        #                 assert actual_message == expected_message, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.3. Check PI release.'):
        #             """
        #             Compare actual PI release and expected PI release.
        #             """
        #             url = f"{actual_message['data']['url']}/{ocid}"
        #             actual_pi_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected PI release.
        #                 """
        #                 expected_release = copy.deepcopy(CreatePriorInformationNoticeRelease(
        #                     environment, country, language, tender_classification_id, payload, actual_message
        #                 ))
        #                 expected_pi_release = expected_release.build_expected_pi_release(actual_pi_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected PI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_pi_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_pi_release), "Expected release.")
        #
        #                 assert actual_pi_release == expected_pi_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.4. Check MS release.'):
        #             """
        #             Compare actual MS release and expected MS release.
        #             """
        #             url = f"{actual_message['data']['url']}/{cpid}"
        #             actual_ms_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected MS release.
        #                 """
        #                 expected_ms_release = expected_release.build_expected_ms_release(
        #                     actual_ms_release, pmd, need_fs=True
        #                 )
        #             except ValueError:
        #                 ValueError("Impossible to build expected MS release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ms_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ms_release), "Expected release.")
        #
        #                 assert actual_ms_release == expected_ms_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.5. Check EI release.'):
        #             """
        #             Compare actual EI release and expected EI release.
        #             """
        #             actual_ei_release = requests.get(url=ei_url).json()
        #
        #             try:
        #                 """
        #                 Build expected EI release.
        #                 """
        #                 expected_ei_release = expected_release.build_expected_ei_release(actual_ei_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected EI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ei_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ei_release), "Expected release.")
        #
        #                 assert actual_ei_release == expected_ei_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.6. Check FS release.'):
        #             """
        #             Compare actual FS release and expected FS release.
        #             """
        #             actual_fs_release = requests.get(url=fs_url).json()
        #
        #             try:
        #                 """
        #                 Build expected FS release.
        #                 """
        #                 expected_fs_release = expected_release.build_expected_fs_release(actual_fs_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected FS release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_fs_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_fs_release), "Expected release.")
        #
        #                 assert actual_fs_release == expected_fs_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #     if clean_up_database is True:
        #         try:
        #             """
        #             CLean up the database.
        #             """
        #             # Clean after Create PIN process:
        #             cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
        #             cleanup_table_of_services_for_prior_information_notice(
        #                 connect_to_ocds, connect_to_auctions, connect_to_clarification, connect_to_access, cpid
        #             )
        #         except ValueError:
        #             ValueError("Impossible to cLean up the database.")
        #     else:
        #         with allure.step("The steps of process."):
        #             allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                           f"operation_id = '{operation_id}' ALLOW FILTERING;",
        #                           "Cassandra DataBase: steps of process.")

        @allure.title("Створити PIN повна модель, без опціональних атрибутів на четвертому рівні, для Молдови.")
        def test_case_4(self, get_parameters, connect_to_keyspace, create_fs_tc_1_new):

            environment = get_parameters[0]
            bpe_host = get_parameters[2]
            service_host = get_parameters[3]
            country = get_parameters[4]
            language = get_parameters[5]
            pmd = get_parameters[6]
            tender_classification_id = get_parameters[9]
            clean_up_database = get_parameters[10]

            connect_to_ocds = connect_to_keyspace[0]
            connect_to_orchestrator = connect_to_keyspace[1]
            connect_to_access = connect_to_keyspace[2]
            connect_to_clarification = connect_to_keyspace[3]
            connect_to_auctions = connect_to_keyspace[8]

            currency = create_fs_tc_1_new[0]
            ei_cpid = create_fs_tc_1_new[2]
            ei_url = create_fs_tc_1_new[4]
            fs_ocid = create_fs_tc_1_new[7]
            fs_url = create_fs_tc_1_new[9]
            buyer_id = create_fs_tc_1_new[11]
            buyer_scheme = create_fs_tc_1_new[12]

            previous_ei_release = requests.get(ei_url).json()
            previous_fs_release = requests.get(fs_url).json()

            """
            VR.COM-14.4.3 Check EI state.
            """
            if previous_ei_release['releases'][0]['tender']['status'] == "planning":
                pass
            else:
                raise ValueError(f"The EI release has invalid state: "
                                 f"{previous_ei_release['releases'][0]['tender']['status']}.")

            """
            VR.COM-14.4.4 Check FS state.
            """
            if previous_fs_release['releases'][0]['tender']['status'] == "active":
                pass
            else:
                raise ValueError(f"The FS release has invalid state: "
                                 f"{previous_fs_release['releases'][0]['tender']['status']}.")

            step_number = 1
            with allure.step(f"# {step_number}. Authorization platform one: Create PIN process."):
                """
                Tender platform authorization for Create PIN process.
                As result, get tender platform's access token and process operation-id.
                """
                platform_one = PlatformAuthorization(bpe_host)
                access_token = platform_one.get_access_token_for_platform_one()
                operation_id = platform_one.get_x_operation_id(access_token)

            step_number += 1
            with allure.step(f"# {step_number}. Send a request to create a Create PIN process."):
                """
                Send api request to BPE host to create a Create PIN process.
                """

                try:
                    """
                    Build payload for Create PIN process.
                    """
                    payload = copy.deepcopy(PriorInformationNoticePayload(
                        environment=environment,
                        language=language,
                        host_to_service=service_host,
                        country=country,
                        amount=5000.00,
                        currency=currency,
                        tender_classification_id=tender_classification_id,
                        procurinentity_id=buyer_id,
                        procurinentity_scheme=buyer_scheme
                    ))

                    list_of_classifications = [
                        {
                            "ei": ei_cpid,
                            "fs": fs_ocid
                        }
                    ]
                    payload.customize_planning_budget_budgetbreakdown(connect_to_ocds, list_of_classifications)

                    payload.customize_tender_lots(
                        quantity_of_lots=1,
                        quantity_of_options=1,
                        quantity_of_recurrence_dates=1,
                        quantity_of_renewal=1
                    )

                    lots_id = payload.get_lots_id_from_payload()

                    payload.customize_tender_items(
                        quantity_of_items=1,
                        quantity_of_items_additionalclassifications=1
                    )

                    items_id = payload.get_items_id_from_payload()

                    payload.customize_tender_electronicauctions_object(connect_to_auctions, pmd)

                    payload.customize_tender_procuringentity_additionalidentifiers(
                        quantity_of_tender_procuring_entity_additional_identifiers=1
                    )

                    payload.customize_tender_procuringentity_bf_persones_array(
                        quantity_of_persones_objects=1,
                        quantity_of_bf_objects=1,
                        quantity_of_documents_objects=1
                    )
                    exclusion_criteria_array = payload.prepare_exclusion_criteria(
                        "criteria.requirementGroups.description",
                        "criteria.requirementGroups.requirements.minValue",
                        "criteria.requirementGroups.requirements.maxValue",
                        language=language,
                        environment=environment,
                        criteria_relates_to="item",
                        criteria_related_item=items_id[0]
                    )

                    selection_criteria_array = payload.prepare_selection_criteria(
                        "criteria.requirementGroups.description",
                        "criteria.requirementGroups.requirements.expectedValue",
                        language=language,
                        environment=environment,
                        criteria_relates_to="item",
                        criteria_related_item=items_id[0]
                    )

                    other_criteria_array = payload.prepare_other_criteria(
                        "criteria.requirementGroups.description",
                        "criteria.requirementGroups.requirements.minValue",
                        "criteria.requirementGroups.requirements.maxValue",
                        language=language,
                        environment=environment,
                        criteria_relates_to="item",
                        criteria_related_item=items_id[0]
                    )

                    payload.customize_tender_criteria(
                        exclusion_criteria_array, selection_criteria_array, other_criteria_array
                    )

                    payload.delete_optional_fields(
                        "tender.procuringEntity.identifier.uri",
                        "tender.procuringEntity.additionalIdentifiers[?].uri",
                        "tender.procuringEntity.address.postalCode",
                        "tender.procuringEntity.contactPoint.faxNumber",
                        "tender.procuringEntity.contactPoint.url",
                        "tender.targets[?].observations[?].period",
                        "tender.lots[?].placeOfPerformance.description",
                        "tender.lots[?].options[?].period",
                        "tender.lots[?].recurrence.dates",
                        "tender.lots[?].renewal.period",
                        "tender.lots[?].renewal.minimumRenewals",
                        "tender.lots[?].renewal.maximumRenewals",
                        pe_additionalidentifiers_position=0,
                        target_position=0,
                        lot_position=0,
                        lot_options_position=0
                    )

                    selection_conversions_array = payload.prepare_selection_conversions(selection_criteria_array)
                    other_conversions_array = payload.prepare_other_conversions(other_criteria_array)
                    payload.customize_tender_conversions(selection_conversions_array, other_conversions_array)

                    relates_to = {
                        "relatesTo": "lot",
                        "relatedItems": lots_id
                    }

                    payload.customize_tender_targets(
                        targets_dict=relates_to
                    )

                    payload.customize_tender_documents(
                        quantity_of_documents=1
                    )

                    payload = payload.build_payload()
                except ValueError:
                    raise ValueError("Impossible to build payload for Create PIN process.")

                synchronous_result = create_pin_process(
                    host=bpe_host,
                    access_token=access_token,
                    x_operation_id=operation_id,
                    country=country,
                    language=language,
                    pmd=pmd,
                    payload=payload,
                    test_mode=True
                )
                message = get_message_for_platform(operation_id)
                cpid = message['data']['ocid'][:28]
                ocid = message['data']['outcomes']['pin'][0]['id']
                allure.attach(str(message), "Message for platform.")

            step_number += 1
            with allure.step(f"# {step_number}. See result"):
                """
                Check the results of TestCase.
                """

                with allure.step(f"# {step_number}.1. Check status code"):
                    """
                    Check the status code of sending the request.
                    """
                    with allure.step('Compare actual status code and expected status code of sending request.'):
                        allure.attach(str(synchronous_result.status_code), "Actual status code.")
                        allure.attach(str(202), "Expected status code.")
                        assert synchronous_result.status_code == 202

                with allure.step(f'# {step_number}.2. Check the message for the platform, the Create PIN process.'):
                    """
                    Check the message for platform.
                    """
                    actual_message = message

                    try:
                        """
                        Build expected message for platform.
                        """
                        expected_message = copy.deepcopy(CreatePriorInformationNoticeMessage(
                            environment=environment,
                            country=country,
                            actual_message=actual_message,
                            test_mode=True)
                        )

                        expected_message = expected_message.build_expected_success_message()
                    except ValueError:
                        ValueError("Impossible to build expected message for platform.")

                    with allure.step('Compare actual and expected message for platform.'):
                        allure.attach(json.dumps(actual_message), "Actual message.")
                        allure.attach(json.dumps(expected_message), "Expected message.")

                        assert actual_message == expected_message, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

                with allure.step(f'# {step_number}.3. Check PI release.'):
                    """
                    Compare actual PI release and expected PI release.
                    """
                    url = f"{actual_message['data']['url']}/{ocid}"
                    actual_pi_release = requests.get(url=url).json()

                    try:
                        """
                        Build expected PI release.
                        """
                        expected_release = copy.deepcopy(CreatePriorInformationNoticeRelease(
                            environment, country, language, tender_classification_id, payload, actual_message
                        ))
                        expected_pi_release = expected_release.build_expected_pi_release(actual_pi_release)
                    except ValueError:
                        ValueError("Impossible to build expected PI release.")

                    with allure.step("Compare actual and expected releases."):
                        allure.attach(json.dumps(actual_pi_release), "Actual release.")
                        allure.attach(json.dumps(expected_pi_release), "Expected release.")

                        assert actual_pi_release == expected_pi_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

                with allure.step(f'# {step_number}.4. Check MS release.'):
                    """
                    Compare actual MS release and expected MS release.
                    """
                    url = f"{actual_message['data']['url']}/{cpid}"
                    actual_ms_release = requests.get(url=url).json()

                    try:
                        """
                        Build expected MS release.
                        """
                        expected_ms_release = expected_release.build_expected_ms_release(
                            actual_ms_release, pmd, need_fs=True
                        )
                    except ValueError:
                        ValueError("Impossible to build expected MS release.")

                    with allure.step("Compare actual and expected releases."):
                        allure.attach(json.dumps(actual_ms_release), "Actual release.")
                        allure.attach(json.dumps(expected_ms_release), "Expected release.")

                        assert actual_ms_release == expected_ms_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

                with allure.step(f'# {step_number}.5. Check EI release.'):
                    """
                    Compare actual EI release and expected EI release.
                    """
                    actual_ei_release = requests.get(url=ei_url).json()

                    try:
                        """
                        Build expected EI release.
                        """
                        expected_ei_release = expected_release.build_expected_ei_release(actual_ei_release)
                    except ValueError:
                        ValueError("Impossible to build expected EI release.")

                    with allure.step("Compare actual and expected releases."):
                        allure.attach(json.dumps(actual_ei_release), "Actual release.")
                        allure.attach(json.dumps(expected_ei_release), "Expected release.")

                        assert actual_ei_release == expected_ei_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

                with allure.step(f'# {step_number}.6. Check FS release.'):
                    """
                    Compare actual FS release and expected FS release.
                    """
                    actual_fs_release = requests.get(url=fs_url).json()

                    try:
                        """
                        Build expected FS release.
                        """
                        expected_fs_release = expected_release.build_expected_fs_release(actual_fs_release)
                    except ValueError:
                        ValueError("Impossible to build expected FS release.")

                    with allure.step("Compare actual and expected releases."):
                        allure.attach(json.dumps(actual_fs_release), "Actual release.")
                        allure.attach(json.dumps(expected_fs_release), "Expected release.")

                        assert actual_fs_release == expected_fs_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            if clean_up_database is True:
                try:
                    """
                    CLean up the database.
                    """
                    # Clean after Create PIN process:
                    cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                    cleanup_table_of_services_for_prior_information_notice(
                        connect_to_ocds, connect_to_auctions, connect_to_clarification, connect_to_access, cpid
                    )
                except ValueError:
                    ValueError("Impossible to cLean up the database.")
            else:
                with allure.step("The steps of process."):
                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                  f"operation_id = '{operation_id}' ALLOW FILTERING;",
                                  "Cassandra DataBase: steps of process.")

    elif country == "LT":
        # @allure.title("Створити PIN, повна модель, для Литви.")
        # def test_case_1(self, get_parameters, connect_to_keyspace, confirm_ei_tc_1):
        #
        #     environment = get_parameters[0]
        #     bpe_host = get_parameters[2]
        #     service_host = get_parameters[3]
        #     country = get_parameters[4]
        #     language = get_parameters[5]
        #     pmd = get_parameters[6]
        #     tender_classification_id = get_parameters[9]
        #     clean_up_database = get_parameters[10]
        #
        #     connect_to_ocds = connect_to_keyspace[0]
        #     connect_to_orchestrator = connect_to_keyspace[1]
        #     connect_to_access = connect_to_keyspace[2]
        #     connect_to_clarification = connect_to_keyspace[3]
        #     connect_to_auctions = connect_to_keyspace[8]
        #
        #     ei_cpid = confirm_ei_tc_1[0]
        #     ei_url = confirm_ei_tc_1[3]
        #     currency = confirm_ei_tc_1[4]
        #     buyer_id = confirm_ei_tc_1[5]
        #     buyer_scheme = confirm_ei_tc_1[6]
        #
        #     previous_ei_release = requests.get(ei_url).json()
        #
        #     """
        #     VR.COM-14.4.3 Check EI state.
        #     """
        #     if previous_ei_release['releases'][0]['tender']['status'] == "planned":
        #         pass
        #     else:
        #         raise ValueError(f"The EI release has invalid state: "
        #                          f"{previous_ei_release['releases'][0]['tender']['status']}.")
        #
        #     step_number = 1
        #     with allure.step(f"# {step_number}. Authorization platform one: Create PIN process."):
        #         """
        #         Tender platform authorization for Create PIN process.
        #         As result, get tender platform's access token and process operation-id.
        #         """
        #         platform_one = PlatformAuthorization(bpe_host)
        #         access_token = platform_one.get_access_token_for_platform_one()
        #         operation_id = platform_one.get_x_operation_id(access_token)
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. Send a request to create a Create PIN process."):
        #         """
        #         Send api request to BPE host to create a Create PIN process.
        #         """
        #
        #         try:
        #             """
        #             Build payload for Create PIN process.
        #             """
        #             payload = copy.deepcopy(PriorInformationNoticePayload(
        #                 environment=environment,
        #                 language=language,
        #                 host_to_service=service_host,
        #                 country=country,
        #                 amount=5000.00,
        #                 currency=currency,
        #                 tender_classification_id=tender_classification_id,
        #                 procurinentity_id=buyer_id,
        #                 procurinentity_scheme=buyer_scheme
        #             ))
        #
        #             list_of_classifications = [
        #                 {
        #                     "ei": ei_cpid
        #                 }
        #             ]
        #             payload.customize_planning_budget_budgetbreakdown(connect_to_ocds, list_of_classifications)
        #
        #             payload.customize_tender_lots(
        #                 quantity_of_lots=1,
        #                 quantity_of_options=1,
        #                 quantity_of_recurrence_dates=1,
        #                 quantity_of_renewal=1
        #             )
        #
        #             lots_id = payload.get_lots_id_from_payload()
        #
        #             payload.customize_tender_items(
        #                 quantity_of_items=1,
        #                 quantity_of_items_additionalclassifications=1
        #             )
        #
        #             payload.customize_tender_electronicauctions_object(connect_to_auctions, pmd)
        #
        #             payload.customize_tender_procuringentity_additionalidentifiers(
        #                 quantity_of_tender_procuring_entity_additional_identifiers=1
        #             )
        #
        #             payload.customize_tender_procuringentity_bf_persones_array(
        #                 quantity_of_persones_objects=1,
        #                 quantity_of_bf_objects=1,
        #                 quantity_of_documents_objects=1
        #             )
        #             exclusion_criteria_array = payload.prepare_exclusion_criteria(
        #                 "criteria.relatedItem",
        #                 "criteria.requirementGroups.requirements.minValue",
        #                 "criteria.requirementGroups.requirements.maxValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="tenderer"
        #             )
        #
        #             selection_criteria_array = payload.prepare_selection_criteria(
        #                 "criteria.relatedItem",
        #                 "criteria.requirementGroups.requirements.expectedValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="tenderer"
        #             )
        #
        #             other_criteria_array = payload.prepare_other_criteria(
        #                 "criteria.requirementGroups.requirements.minValue",
        #                 "criteria.requirementGroups.requirements.maxValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="lot",
        #                 criteria_related_item=lots_id[0]
        #             )
        #
        #             payload.customize_tender_criteria(
        #                 exclusion_criteria_array, selection_criteria_array, other_criteria_array
        #             )
        #
        #             selection_conversions_array = payload.prepare_selection_conversions(selection_criteria_array)
        #             other_conversions_array = payload.prepare_other_conversions(other_criteria_array)
        #             payload.customize_tender_conversions(selection_conversions_array, other_conversions_array)
        #
        #             relates_to = {
        #                 "relatesTo": "lot",
        #                 "relatedItems": lots_id
        #             }
        #
        #             payload.customize_tender_targets(
        #                 targets_dict=relates_to
        #             )
        #
        #             payload.customize_tender_documents(
        #                 quantity_of_documents=1
        #             )
        #
        #             payload = payload.build_payload()
        #         except ValueError:
        #             raise ValueError("Impossible to build payload for Create PIN process.")
        #
        #         synchronous_result = create_pin_process(
        #             host=bpe_host,
        #             access_token=access_token,
        #             x_operation_id=operation_id,
        #             country=country,
        #             language=language,
        #             pmd=pmd,
        #             payload=payload,
        #             test_mode=True
        #         )
        #         message = get_message_for_platform(operation_id)
        #         cpid = message['data']['ocid'][:28]
        #         ocid = message['data']['outcomes']['pin'][0]['id']
        #         allure.attach(str(message), "Message for platform.")
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. See result"):
        #         """
        #         Check the results of TestCase.
        #         """
        #
        #         with allure.step(f"# {step_number}.1. Check status code"):
        #             """
        #             Check the status code of sending the request.
        #             """
        #             with allure.step('Compare actual status code and expected status code of sending request.'):
        #                 allure.attach(str(synchronous_result.status_code), "Actual status code.")
        #                 allure.attach(str(202), "Expected status code.")
        #                 assert synchronous_result.status_code == 202
        #
        #         with allure.step(f'# {step_number}.2. Check the message for the platform, the Create PIN process.'):
        #             """
        #             Check the message for platform.
        #             """
        #             actual_message = message
        #
        #             try:
        #                 """
        #                 Build expected message for platform.
        #                 """
        #                 expected_message = copy.deepcopy(CreatePriorInformationNoticeMessage(
        #                     environment=environment,
        #                     country=country,
        #                     actual_message=actual_message,
        #                     test_mode=True)
        #                 )
        #
        #                 expected_message = expected_message.build_expected_success_message()
        #             except ValueError:
        #                 ValueError("Impossible to build expected message for platform.")
        #
        #             with allure.step('Compare actual and expected message for platform.'):
        #                 allure.attach(json.dumps(actual_message), "Actual message.")
        #                 allure.attach(json.dumps(expected_message), "Expected message.")
        #
        #                 assert actual_message == expected_message, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.3. Check PI release.'):
        #             """
        #             Compare actual PI release and expected PI release.
        #             """
        #             url = f"{actual_message['data']['url']}/{ocid}"
        #             actual_pi_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected PI release.
        #                 """
        #                 expected_release = copy.deepcopy(CreatePriorInformationNoticeRelease(
        #                     environment, country, language, tender_classification_id, payload, actual_message
        #                 ))
        #                 expected_pi_release = expected_release.build_expected_pi_release(actual_pi_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected PI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_pi_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_pi_release), "Expected release.")
        #
        #                 assert actual_pi_release == expected_pi_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.4. Check MS release.'):
        #             """
        #             Compare actual MS release and expected MS release.
        #             """
        #             url = f"{actual_message['data']['url']}/{cpid}"
        #             actual_ms_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected MS release.
        #                 """
        #                 expected_ms_release = expected_release.build_expected_ms_release(
        #                     actual_ms_release, pmd, need_fs=False
        #                 )
        #             except ValueError:
        #                 ValueError("Impossible to build expected MS release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ms_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ms_release), "Expected release.")
        #
        #                 assert actual_ms_release == expected_ms_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.5. Check EI release.'):
        #             """
        #             Compare actual EI release and expected EI release.
        #             """
        #             actual_ei_release = requests.get(url=ei_url).json()
        #
        #             try:
        #                 """
        #                 Build expected EI release.
        #                 """
        #                 expected_ei_release = expected_release.build_expected_ei_release(actual_ei_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected EI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ei_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ei_release), "Expected release.")
        #
        #                 assert actual_ei_release == expected_ei_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #     if clean_up_database is True:
        #         try:
        #             """
        #             CLean up the database.
        #             """
        #             # Clean after Create PIN process:
        #             cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
        #             cleanup_table_of_services_for_prior_information_notice(
        #                 connect_to_ocds, connect_to_auctions, connect_to_clarification, connect_to_access, cpid
        #             )
        #         except ValueError:
        #             ValueError("Impossible to cLean up the database.")
        #     else:
        #         with allure.step("The steps of process."):
        #             allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                           f"operation_id = '{operation_id}' ALLOW FILTERING;",
        #                           "Cassandra DataBase: steps of process.")
        #
        # @allure.title("Створити PIN повна модель, без опціональних атрибутів на другому рівні, для Литви.")
        # def test_case_2(self, get_parameters, connect_to_keyspace, confirm_ei_tc_1):
        #
        #     environment = get_parameters[0]
        #     bpe_host = get_parameters[2]
        #     service_host = get_parameters[3]
        #     country = get_parameters[4]
        #     language = get_parameters[5]
        #     pmd = get_parameters[6]
        #     tender_classification_id = get_parameters[9]
        #     clean_up_database = get_parameters[10]
        #
        #     connect_to_ocds = connect_to_keyspace[0]
        #     connect_to_orchestrator = connect_to_keyspace[1]
        #     connect_to_access = connect_to_keyspace[2]
        #     connect_to_clarification = connect_to_keyspace[3]
        #     connect_to_auctions = connect_to_keyspace[8]
        #
        #     ei_cpid = confirm_ei_tc_1[0]
        #     ei_url = confirm_ei_tc_1[3]
        #     currency = confirm_ei_tc_1[4]
        #     buyer_id = confirm_ei_tc_1[5]
        #     buyer_scheme = confirm_ei_tc_1[6]
        #
        #     previous_ei_release = requests.get(ei_url).json()
        #
        #     """
        #     VR.COM-14.4.3 Check EI state.
        #     """
        #     if previous_ei_release['releases'][0]['tender']['status'] == "planned":
        #         pass
        #     else:
        #         raise ValueError(f"The EI release has invalid state: "
        #                          f"{previous_ei_release['releases'][0]['tender']['status']}.")
        #
        #     step_number = 1
        #     with allure.step(f"# {step_number}. Authorization platform one: Create PIN process."):
        #         """
        #         Tender platform authorization for Create PIN process.
        #         As result, get tender platform's access token and process operation-id.
        #         """
        #         platform_one = PlatformAuthorization(bpe_host)
        #         access_token = platform_one.get_access_token_for_platform_one()
        #         operation_id = platform_one.get_x_operation_id(access_token)
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. Send a request to create a Create PIN process."):
        #         """
        #         Send api request to BPE host to create a Create PIN process.
        #         """
        #
        #         try:
        #             """
        #             Build payload for Create PIN process.
        #             """
        #             payload = copy.deepcopy(PriorInformationNoticePayload(
        #                 environment=environment,
        #                 language=language,
        #                 host_to_service=service_host,
        #                 country=country,
        #                 amount=5000.00,
        #                 currency=currency,
        #                 tender_classification_id=tender_classification_id,
        #                 procurinentity_id=buyer_id,
        #                 procurinentity_scheme=buyer_scheme
        #             ))
        #
        #             list_of_classifications = [
        #                 {
        #                     "ei": ei_cpid
        #                 }
        #             ]
        #             payload.customize_planning_budget_budgetbreakdown(connect_to_ocds, list_of_classifications)
        #
        #             payload.customize_tender_lots(
        #                 quantity_of_lots=1,
        #                 quantity_of_options=1,
        #                 quantity_of_recurrence_dates=1,
        #                 quantity_of_renewal=1
        #             )
        #
        #             payload.customize_tender_items(
        #                 quantity_of_items=1,
        #                 quantity_of_items_additionalclassifications=1
        #             )
        #
        #             payload.customize_tender_procuringentity_additionalidentifiers(
        #                 quantity_of_tender_procuring_entity_additional_identifiers=1
        #             )
        #
        #             payload.customize_tender_procuringentity_bf_persones_array(
        #                 quantity_of_persones_objects=1,
        #                 quantity_of_bf_objects=1,
        #                 quantity_of_documents_objects=1
        #             )
        #
        #             payload.delete_optional_fields(
        #                 "planning.rationale",
        #                 "tender.procurementMethodRationale",
        #                 "tender.enquiryPeriod",
        #                 "tender.procurementMethodModalities",
        #                 "tender.electronicAuctions",
        #                 "tender.criteria",
        #                 "tender.conversions",
        #                 "tender.targets",
        #                 "tender.documents"
        #             )
        #             payload = payload.build_payload()
        #             payload['tender']['awardCriteria'] = "priceOnly"
        #             payload['tender']['awardCriteriaDetails'] = "automated"
        #         except ValueError:
        #             raise ValueError("Impossible to build payload for Create PIN process.")
        #
        #         synchronous_result = create_pin_process(
        #             host=bpe_host,
        #             access_token=access_token,
        #             x_operation_id=operation_id,
        #             country=country,
        #             language=language,
        #             pmd=pmd,
        #             payload=payload,
        #             test_mode=True
        #         )
        #         message = get_message_for_platform(operation_id)
        #         cpid = message['data']['ocid'][:28]
        #         ocid = message['data']['outcomes']['pin'][0]['id']
        #         allure.attach(str(message), "Message for platform.")
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. See result"):
        #         """
        #         Check the results of TestCase.
        #         """
        #
        #         with allure.step(f"# {step_number}.1. Check status code"):
        #             """
        #             Check the status code of sending the request.
        #             """
        #             with allure.step('Compare actual status code and expected status code of sending request.'):
        #                 allure.attach(str(synchronous_result.status_code), "Actual status code.")
        #                 allure.attach(str(202), "Expected status code.")
        #                 assert synchronous_result.status_code == 202
        #
        #         with allure.step(f'# {step_number}.2. Check the message for the platform, the Create PIN process.'):
        #             """
        #             Check the message for platform.
        #             """
        #             actual_message = message
        #
        #             try:
        #                 """
        #                 Build expected message for platform.
        #                 """
        #                 expected_message = copy.deepcopy(CreatePriorInformationNoticeMessage(
        #                     environment=environment,
        #                     country=country,
        #                     actual_message=actual_message,
        #                     test_mode=True)
        #                 )
        #
        #                 expected_message = expected_message.build_expected_success_message()
        #             except ValueError:
        #                 ValueError("Impossible to build expected message for platform.")
        #
        #             with allure.step('Compare actual and expected message for platform.'):
        #                 allure.attach(json.dumps(actual_message), "Actual message.")
        #                 allure.attach(json.dumps(expected_message), "Expected message.")
        #
        #                 assert actual_message == expected_message, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.3. Check PI release.'):
        #             """
        #             Compare actual PI release and expected PI release.
        #             """
        #             url = f"{actual_message['data']['url']}/{ocid}"
        #             actual_pi_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected PI release.
        #                 """
        #                 expected_release = copy.deepcopy(CreatePriorInformationNoticeRelease(
        #                     environment, country, language, tender_classification_id, payload, actual_message
        #                 ))
        #                 expected_pi_release = expected_release.build_expected_pi_release(actual_pi_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected PI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_pi_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_pi_release), "Expected release.")
        #
        #                 assert actual_pi_release == expected_pi_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.4. Check MS release.'):
        #             """
        #             Compare actual MS release and expected MS release.
        #             """
        #             url = f"{actual_message['data']['url']}/{cpid}"
        #             actual_ms_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected MS release.
        #                 """
        #                 expected_ms_release = expected_release.build_expected_ms_release(
        #                     actual_ms_release, pmd, need_fs=False
        #                 )
        #             except ValueError:
        #                 ValueError("Impossible to build expected MS release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ms_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ms_release), "Expected release.")
        #
        #                 assert actual_ms_release == expected_ms_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.5. Check EI release.'):
        #             """
        #             Compare actual EI release and expected EI release.
        #             """
        #             actual_ei_release = requests.get(url=ei_url).json()
        #
        #             try:
        #                 """
        #                 Build expected EI release.
        #                 """
        #                 expected_ei_release = expected_release.build_expected_ei_release(actual_ei_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected EI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ei_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ei_release), "Expected release.")
        #
        #                 assert actual_ei_release == expected_ei_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #     if clean_up_database is True:
        #         try:
        #             """
        #             CLean up the database.
        #             """
        #             # Clean after Create PIN process:
        #             cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
        #             cleanup_table_of_services_for_prior_information_notice(
        #                 connect_to_ocds, connect_to_auctions, connect_to_clarification, connect_to_access, cpid
        #             )
        #         except ValueError:
        #             ValueError("Impossible to cLean up the database.")
        #     else:
        #         with allure.step("The steps of process."):
        #             allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                           f"operation_id = '{operation_id}' ALLOW FILTERING;",
        #                           "Cassandra DataBase: steps of process.")
        #
        # @allure.title("Створити PIN повна модель, без опціональних атрибутів на третьому рівні, для Литви.")
        # def test_case_3(self, get_parameters, connect_to_keyspace, confirm_ei_tc_1):
        #
        #     environment = get_parameters[0]
        #     bpe_host = get_parameters[2]
        #     service_host = get_parameters[3]
        #     country = get_parameters[4]
        #     language = get_parameters[5]
        #     pmd = get_parameters[6]
        #     tender_classification_id = get_parameters[9]
        #     clean_up_database = get_parameters[10]
        #
        #     connect_to_ocds = connect_to_keyspace[0]
        #     connect_to_orchestrator = connect_to_keyspace[1]
        #     connect_to_access = connect_to_keyspace[2]
        #     connect_to_clarification = connect_to_keyspace[3]
        #     connect_to_auctions = connect_to_keyspace[8]
        #
        #     ei_cpid = confirm_ei_tc_1[0]
        #     ei_url = confirm_ei_tc_1[3]
        #     currency = confirm_ei_tc_1[4]
        #     buyer_id = confirm_ei_tc_1[5]
        #     buyer_scheme = confirm_ei_tc_1[6]
        #
        #     previous_ei_release = requests.get(ei_url).json()
        #
        #     """
        #     VR.COM-14.4.3 Check EI state.
        #     """
        #     if previous_ei_release['releases'][0]['tender']['status'] == "planned":
        #         pass
        #     else:
        #         raise ValueError(f"The EI release has invalid state: "
        #                          f"{previous_ei_release['releases'][0]['tender']['status']}.")
        #
        #     step_number = 1
        #     with allure.step(f"# {step_number}. Authorization platform one: Create PIN process."):
        #         """
        #         Tender platform authorization for Create PIN process.
        #         As result, get tender platform's access token and process operation-id.
        #         """
        #         platform_one = PlatformAuthorization(bpe_host)
        #         access_token = platform_one.get_access_token_for_platform_one()
        #         operation_id = platform_one.get_x_operation_id(access_token)
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. Send a request to create a Create PIN process."):
        #         """
        #         Send api request to BPE host to create a Create PIN process.
        #         """
        #
        #         try:
        #             """
        #             Build payload for Create PIN process.
        #             """
        #             payload = copy.deepcopy(PriorInformationNoticePayload(
        #                 environment=environment,
        #                 language=language,
        #                 host_to_service=service_host,
        #                 country=country,
        #                 amount=5000.00,
        #                 currency=currency,
        #                 tender_classification_id=tender_classification_id,
        #                 procurinentity_id=buyer_id,
        #                 procurinentity_scheme=buyer_scheme
        #             ))
        #
        #             list_of_classifications = [
        #                 {
        #                     "ei": ei_cpid
        #                 }
        #             ]
        #             payload.customize_planning_budget_budgetbreakdown(connect_to_ocds, list_of_classifications)
        #
        #             payload.customize_tender_lots(
        #                 quantity_of_lots=1,
        #                 quantity_of_options=0,
        #                 quantity_of_recurrence_dates=0,
        #                 quantity_of_renewal=0
        #             )
        #
        #             lots_id = payload.get_lots_id_from_payload()
        #
        #             payload.customize_tender_items(
        #                 quantity_of_items=1,
        #                 quantity_of_items_additionalclassifications=1
        #             )
        #
        #             payload.customize_tender_electronicauctions_object(connect_to_auctions, pmd)
        #
        #             payload.customize_tender_procuringentity_additionalidentifiers(
        #                 quantity_of_tender_procuring_entity_additional_identifiers=1
        #             )
        #
        #             payload.customize_tender_procuringentity_bf_persones_array(
        #                 quantity_of_persones_objects=1,
        #                 quantity_of_bf_objects=1,
        #                 quantity_of_documents_objects=1
        #             )
        #             exclusion_criteria_array = payload.prepare_exclusion_criteria(
        #                 "criteria.classification",
        #                 "criteria.description",
        #                 "criteria.relatedItem",
        #                 "criteria.requirementGroups.requirements.minValue",
        #                 "criteria.requirementGroups.requirements.maxValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="tenderer"
        #             )
        #
        #             selection_criteria_array = payload.prepare_selection_criteria(
        #                 "criteria.classification",
        #                 "criteria.description",
        #                 "criteria.relatedItem",
        #                 "criteria.requirementGroups.requirements.expectedValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="tenderer"
        #             )
        #
        #             other_criteria_array = payload.prepare_other_criteria(
        #                 "criteria.classification",
        #                 "criteria.description",
        #                 "criteria.relatedItem",
        #                 "criteria.requirementGroups.requirements.minValue",
        #                 "criteria.requirementGroups.requirements.maxValue",
        #                 language=language,
        #                 environment=environment,
        #                 criteria_relates_to="lot",
        #                 criteria_related_item=lots_id[0]
        #             )
        #
        #             payload.customize_tender_criteria(
        #                 exclusion_criteria_array, selection_criteria_array, other_criteria_array
        #             )
        #
        #             # Attributes 'tender.lots[0].options', 'tender.lots[0].recurrence', 'tender.lots[0].renewal'
        #             # had been deleted in 'customize_tender_lots' method.
        #             payload.delete_optional_fields(
        #                 "planning.budget.description",
        #                 "tender.procuringEntity.additionalIdentifiers",
        #                 "tender.procuringEntity.persones",
        #                 "tender.conversions[?].description",
        #                 "tender.targets[?].relatedItem",
        #                 "tender.lots[?].internalId",
        #                 "tender.lots[?].hasOptions",
        #                 "tender.lots[?].hasRecurrence",
        #                 "tender.lots[?].hasRenewal",
        #                 "tender.items[?].internalId",
        #                 "tender.items[?].additionalClassifications",
        #                 "tender.documents[?].description",
        #                 "tender.documents[?].relatedLots",
        #                 conversion_position=0,
        #                 target_position=0,
        #                 lot_position=0,
        #                 item_position=0,
        #                 document_position=0
        #             )
        #
        #             selection_conversions_array = payload.prepare_selection_conversions(selection_criteria_array)
        #             other_conversions_array = payload.prepare_other_conversions(other_criteria_array)
        #             payload.customize_tender_conversions(selection_conversions_array, other_conversions_array)
        #
        #             relates_to = {
        #                 "relatesTo": "lot",
        #                 "relatedItems": lots_id
        #             }
        #
        #             payload.customize_tender_targets(
        #                 targets_dict=relates_to
        #             )
        #
        #             payload.customize_tender_documents(
        #                 quantity_of_documents=1
        #             )
        #
        #             payload = payload.build_payload()
        #         except ValueError:
        #             raise ValueError("Impossible to build payload for Create PIN process.")
        #         print("\n Payload PIN")
        #         print(json.dumps(payload))
        #         synchronous_result = create_pin_process(
        #             host=bpe_host,
        #             access_token=access_token,
        #             x_operation_id=operation_id,
        #             country=country,
        #             language=language,
        #             pmd=pmd,
        #             payload=payload,
        #             test_mode=True
        #         )
        #         message = get_message_for_platform(operation_id)
        #         cpid = message['data']['ocid'][:28]
        #         ocid = message['data']['outcomes']['pin'][0]['id']
        #         allure.attach(str(message), "Message for platform.")
        #
        #     step_number += 1
        #     with allure.step(f"# {step_number}. See result"):
        #         """
        #         Check the results of TestCase.
        #         """
        #
        #         with allure.step(f"# {step_number}.1. Check status code"):
        #             """
        #             Check the status code of sending the request.
        #             """
        #             with allure.step('Compare actual status code and expected status code of sending request.'):
        #                 allure.attach(str(synchronous_result.status_code), "Actual status code.")
        #                 allure.attach(str(202), "Expected status code.")
        #                 assert synchronous_result.status_code == 202
        #
        #         with allure.step(f'# {step_number}.2. Check the message for the platform, the Create PIN process.'):
        #             """
        #             Check the message for platform.
        #             """
        #             actual_message = message
        #
        #             try:
        #                 """
        #                 Build expected message for platform.
        #                 """
        #                 expected_message = copy.deepcopy(CreatePriorInformationNoticeMessage(
        #                     environment=environment,
        #                     country=country,
        #                     actual_message=actual_message,
        #                     test_mode=True)
        #                 )
        #
        #                 expected_message = expected_message.build_expected_success_message()
        #             except ValueError:
        #                 ValueError("Impossible to build expected message for platform.")
        #
        #             with allure.step('Compare actual and expected message for platform.'):
        #                 allure.attach(json.dumps(actual_message), "Actual message.")
        #                 allure.attach(json.dumps(expected_message), "Expected message.")
        #
        #                 assert actual_message == expected_message, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.3. Check PI release.'):
        #             """
        #             Compare actual PI release and expected PI release.
        #             """
        #             url = f"{actual_message['data']['url']}/{ocid}"
        #             actual_pi_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected PI release.
        #                 """
        #                 expected_release = copy.deepcopy(CreatePriorInformationNoticeRelease(
        #                     environment, country, language, tender_classification_id, payload, actual_message
        #                 ))
        #                 expected_pi_release = expected_release.build_expected_pi_release(actual_pi_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected PI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_pi_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_pi_release), "Expected release.")
        #
        #                 assert actual_pi_release == expected_pi_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.4. Check MS release.'):
        #             """
        #             Compare actual MS release and expected MS release.
        #             """
        #             url = f"{actual_message['data']['url']}/{cpid}"
        #             actual_ms_release = requests.get(url=url).json()
        #
        #             try:
        #                 """
        #                 Build expected MS release.
        #                 """
        #                 expected_ms_release = expected_release.build_expected_ms_release(
        #                     actual_ms_release, pmd, need_fs=False
        #                 )
        #             except ValueError:
        #                 ValueError("Impossible to build expected MS release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ms_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ms_release), "Expected release.")
        #
        #                 assert actual_ms_release == expected_ms_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #         with allure.step(f'# {step_number}.5. Check EI release.'):
        #             """
        #             Compare actual EI release and expected EI release.
        #             """
        #             actual_ei_release = requests.get(url=ei_url).json()
        #
        #             try:
        #                 """
        #                 Build expected EI release.
        #                 """
        #                 expected_ei_release = expected_release.build_expected_ei_release(actual_ei_release)
        #             except ValueError:
        #                 ValueError("Impossible to build expected EI release.")
        #
        #             with allure.step("Compare actual and expected releases."):
        #                 allure.attach(json.dumps(actual_ei_release), "Actual release.")
        #                 allure.attach(json.dumps(expected_ei_release), "Expected release.")
        #
        #                 assert actual_ei_release == expected_ei_release, \
        #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                                   f"operation_id = '{operation_id}' "
        #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        #
        #     if clean_up_database is True:
        #         try:
        #             """
        #             CLean up the database.
        #             """
        #             # Clean after Create PIN process:
        #             cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
        #             cleanup_table_of_services_for_prior_information_notice(
        #                 connect_to_ocds, connect_to_auctions, connect_to_clarification, connect_to_access, cpid
        #             )
        #         except ValueError:
        #             ValueError("Impossible to cLean up the database.")
        #     else:
        #         with allure.step("The steps of process."):
        #             allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                           f"operation_id = '{operation_id}' ALLOW FILTERING;",
        #                           "Cassandra DataBase: steps of process.")

        @allure.title("Створити PIN повна модель, без опціональних атрибутів на четвертому рівні, для Литви.")
        def test_case_4(self, get_parameters, connect_to_keyspace, confirm_ei_tc_1):

            environment = get_parameters[0]
            bpe_host = get_parameters[2]
            service_host = get_parameters[3]
            country = get_parameters[4]
            language = get_parameters[5]
            pmd = get_parameters[6]
            tender_classification_id = get_parameters[9]
            clean_up_database = get_parameters[10]

            connect_to_ocds = connect_to_keyspace[0]
            connect_to_orchestrator = connect_to_keyspace[1]
            connect_to_access = connect_to_keyspace[2]
            connect_to_clarification = connect_to_keyspace[3]
            connect_to_auctions = connect_to_keyspace[8]

            ei_cpid = confirm_ei_tc_1[0]
            ei_url = confirm_ei_tc_1[3]
            currency = confirm_ei_tc_1[4]
            buyer_id = confirm_ei_tc_1[5]
            buyer_scheme = confirm_ei_tc_1[6]

            previous_ei_release = requests.get(ei_url).json()

            """
            VR.COM-14.4.3 Check EI state.
            """
            if previous_ei_release['releases'][0]['tender']['status'] == "planned":
                pass
            else:
                raise ValueError(f"The EI release has invalid state: "
                                 f"{previous_ei_release['releases'][0]['tender']['status']}.")

            step_number = 1
            with allure.step(f"# {step_number}. Authorization platform one: Create PIN process."):
                """
                Tender platform authorization for Create PIN process.
                As result, get tender platform's access token and process operation-id.
                """
                platform_one = PlatformAuthorization(bpe_host)
                access_token = platform_one.get_access_token_for_platform_one()
                operation_id = platform_one.get_x_operation_id(access_token)

            step_number += 1
            with allure.step(f"# {step_number}. Send a request to create a Create PIN process."):
                """
                Send api request to BPE host to create a Create PIN process.
                """

                try:
                    """
                    Build payload for Create PIN process.
                    """
                    payload = copy.deepcopy(PriorInformationNoticePayload(
                        environment=environment,
                        language=language,
                        host_to_service=service_host,
                        country=country,
                        amount=5000.00,
                        currency=currency,
                        tender_classification_id=tender_classification_id,
                        procurinentity_id=buyer_id,
                        procurinentity_scheme=buyer_scheme
                    ))

                    list_of_classifications = [
                        {
                            "ei": ei_cpid
                        }
                    ]
                    payload.customize_planning_budget_budgetbreakdown(connect_to_ocds, list_of_classifications)

                    payload.customize_tender_lots(
                        quantity_of_lots=1,
                        quantity_of_options=1,
                        quantity_of_recurrence_dates=1,
                        quantity_of_renewal=1
                    )

                    lots_id = payload.get_lots_id_from_payload()

                    payload.customize_tender_items(
                        quantity_of_items=1,
                        quantity_of_items_additionalclassifications=1
                    )

                    payload.customize_tender_electronicauctions_object(connect_to_auctions, pmd)

                    payload.customize_tender_procuringentity_additionalidentifiers(
                        quantity_of_tender_procuring_entity_additional_identifiers=1
                    )

                    payload.customize_tender_procuringentity_bf_persones_array(
                        quantity_of_persones_objects=1,
                        quantity_of_bf_objects=1,
                        quantity_of_documents_objects=1
                    )
                    exclusion_criteria_array = payload.prepare_exclusion_criteria(
                        "criteria.requirementGroups.description",
                        "criteria.requirementGroups.requirements.minValue",
                        "criteria.requirementGroups.requirements.maxValue",
                        language=language,
                        environment=environment,
                        criteria_relates_to="lot",
                        criteria_related_item=lots_id[0]
                    )

                    selection_criteria_array = payload.prepare_selection_criteria(
                        "criteria.requirementGroups.description",
                        "criteria.requirementGroups.requirements.expectedValue",
                        language=language,
                        environment=environment,
                        criteria_relates_to="lot",
                        criteria_related_item=lots_id[0]
                    )

                    other_criteria_array = payload.prepare_other_criteria(
                        "criteria.requirementGroups.description",
                        "criteria.requirementGroups.requirements.minValue",
                        "criteria.requirementGroups.requirements.maxValue",
                        language=language,
                        environment=environment,
                        criteria_relates_to="lot",
                        criteria_related_item=lots_id[0]
                    )

                    payload.customize_tender_criteria(
                        exclusion_criteria_array, selection_criteria_array, other_criteria_array
                    )

                    payload.delete_optional_fields(
                        "tender.procuringEntity.identifier.uri",
                        "tender.procuringEntity.additionalIdentifiers[?].uri",
                        "tender.procuringEntity.address.postalCode",
                        "tender.procuringEntity.contactPoint.faxNumber",
                        "tender.procuringEntity.contactPoint.url",
                        "tender.targets[?].observations[?].period",
                        "tender.lots[?].placeOfPerformance.description",
                        "tender.lots[?].options[?].description",
                        "tender.lots[?].recurrence.description",
                        "tender.lots[?].renewal.description",
                        "tender.lots[?].renewal.minimumRenewals",
                        "tender.lots[?].renewal.maximumRenewals",
                        pe_additionalidentifiers_position=0,
                        target_position=0,
                        lot_position=0,
                        lot_options_position=0
                    )

                    selection_conversions_array = payload.prepare_selection_conversions(selection_criteria_array)
                    other_conversions_array = payload.prepare_other_conversions(other_criteria_array)
                    payload.customize_tender_conversions(selection_conversions_array, other_conversions_array)

                    relates_to = {
                        "relatesTo": "lot",
                        "relatedItems": lots_id
                    }

                    payload.customize_tender_targets(
                        targets_dict=relates_to
                    )

                    payload.customize_tender_documents(
                        quantity_of_documents=1
                    )

                    payload = payload.build_payload()
                except ValueError:
                    raise ValueError("Impossible to build payload for Create PIN process.")
                print("\n Payload PIN")
                print(json.dumps(payload))
                synchronous_result = create_pin_process(
                    host=bpe_host,
                    access_token=access_token,
                    x_operation_id=operation_id,
                    country=country,
                    language=language,
                    pmd=pmd,
                    payload=payload,
                    test_mode=True
                )
                message = get_message_for_platform(operation_id)
                cpid = message['data']['ocid'][:28]
                ocid = message['data']['outcomes']['pin'][0]['id']
                allure.attach(str(message), "Message for platform.")

            step_number += 1
            with allure.step(f"# {step_number}. See result"):
                """
                Check the results of TestCase.
                """

                with allure.step(f"# {step_number}.1. Check status code"):
                    """
                    Check the status code of sending the request.
                    """
                    with allure.step('Compare actual status code and expected status code of sending request.'):
                        allure.attach(str(synchronous_result.status_code), "Actual status code.")
                        allure.attach(str(202), "Expected status code.")
                        assert synchronous_result.status_code == 202

                with allure.step(f'# {step_number}.2. Check the message for the platform, the Create PIN process.'):
                    """
                    Check the message for platform.
                    """
                    actual_message = message

                    try:
                        """
                        Build expected message for platform.
                        """
                        expected_message = copy.deepcopy(CreatePriorInformationNoticeMessage(
                            environment=environment,
                            country=country,
                            actual_message=actual_message,
                            test_mode=True)
                        )

                        expected_message = expected_message.build_expected_success_message()
                    except ValueError:
                        ValueError("Impossible to build expected message for platform.")

                    with allure.step('Compare actual and expected message for platform.'):
                        allure.attach(json.dumps(actual_message), "Actual message.")
                        allure.attach(json.dumps(expected_message), "Expected message.")

                        assert actual_message == expected_message, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

                with allure.step(f'# {step_number}.3. Check PI release.'):
                    """
                    Compare actual PI release and expected PI release.
                    """
                    url = f"{actual_message['data']['url']}/{ocid}"
                    actual_pi_release = requests.get(url=url).json()

                    try:
                        """
                        Build expected PI release.
                        """
                        expected_release = copy.deepcopy(CreatePriorInformationNoticeRelease(
                            environment, country, language, tender_classification_id, payload, actual_message
                        ))
                        expected_pi_release = expected_release.build_expected_pi_release(actual_pi_release)
                    except ValueError:
                        ValueError("Impossible to build expected PI release.")

                    with allure.step("Compare actual and expected releases."):
                        allure.attach(json.dumps(actual_pi_release), "Actual release.")
                        allure.attach(json.dumps(expected_pi_release), "Expected release.")

                        assert actual_pi_release == expected_pi_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

                with allure.step(f'# {step_number}.4. Check MS release.'):
                    """
                    Compare actual MS release and expected MS release.
                    """
                    url = f"{actual_message['data']['url']}/{cpid}"
                    actual_ms_release = requests.get(url=url).json()

                    try:
                        """
                        Build expected MS release.
                        """
                        expected_ms_release = expected_release.build_expected_ms_release(
                            actual_ms_release, pmd, need_fs=False
                        )
                    except ValueError:
                        ValueError("Impossible to build expected MS release.")

                    with allure.step("Compare actual and expected releases."):
                        allure.attach(json.dumps(actual_ms_release), "Actual release.")
                        allure.attach(json.dumps(expected_ms_release), "Expected release.")

                        assert actual_ms_release == expected_ms_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

                with allure.step(f'# {step_number}.5. Check EI release.'):
                    """
                    Compare actual EI release and expected EI release.
                    """
                    actual_ei_release = requests.get(url=ei_url).json()

                    try:
                        """
                        Build expected EI release.
                        """
                        expected_ei_release = expected_release.build_expected_ei_release(actual_ei_release)
                    except ValueError:
                        ValueError("Impossible to build expected EI release.")

                    with allure.step("Compare actual and expected releases."):
                        allure.attach(json.dumps(actual_ei_release), "Actual release.")
                        allure.attach(json.dumps(expected_ei_release), "Expected release.")

                        assert actual_ei_release == expected_ei_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            if clean_up_database is True:
                try:
                    """
                    CLean up the database.
                    """
                    # Clean after Create PIN process:
                    cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                    cleanup_table_of_services_for_prior_information_notice(
                        connect_to_ocds, connect_to_auctions, connect_to_clarification, connect_to_access, cpid
                    )
                except ValueError:
                    ValueError("Impossible to cLean up the database.")
            else:
                with allure.step("The steps of process."):
                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                  f"operation_id = '{operation_id}' ALLOW FILTERING;",
                                  "Cassandra DataBase: steps of process.")