import copy
import json
import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import get_process_id_by_operation_id, \
    cleanup_ocds_orchestrator_operation_step_by_operation_id, cleanup_table_of_services_for_planning_notice
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_pn_process
from messages_collection.open.create_pn_message import PlanningNoticeMessage
from payloads_collection.open.create_pn_payload import PlanningNoticePayload

from releases_collection.open.create_pn_release import PlanningNoticeRelease


@allure.parent_suite("Open")
@allure.suite("Planning Notice")
@allure.severity("Critical")
@allure.testcase(url="")
class TestCreatePN:
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace, create_fs_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]
        pmd = get_parameters[6]
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
        ei_payload = create_fs_tc_1[4]
        ei_message = create_fs_tc_1[5]
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

                payload.customize_tender_procuring_entity_additional_identifiers(
                    quantity_of_tender_procuring_entity_additional_identifiers=3
                )

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
                ValueError("Impossible to build payload for CreatePlanningNotice process.")

            synchronous_result = create_pn_process(
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
            cpid = message['data']['outcomes']['pn'][0]['id']
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create PN process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(PlanningNoticeMessage(
                        environment=environment,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_message()
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    process_id = get_process_id_by_operation_id(connect_to_ocds, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.3. Check PN release.'):
                """
                Compare actual PN release and expected PN release.
                """
                pn_url = f"{actual_message['data']['url']}/{actual_message['data']['outcomes']['pn'][0]['id']}"
                actual_pn_release = requests.get(url=pn_url).json()

                try:
                    """
                    Build expected PN release.
                    """
                    expected_release = copy.deepcopy(PlanningNoticeRelease(
                        environment, language, pmd, payload, actual_message
                    ))

                    expected_pn_release = expected_release.build_expected_pn_release(actual_pn_release)
                except ValueError:
                    ValueError("Impossible to build expected PN release.")

                print("\n Actual PN release")
                print(json.dumps(actual_pn_release))
                print("\n Expected PN release")
                print(json.dumps(expected_pn_release))

                with allure.step('Compare actual and expected PN release.'):
                    allure.attach(json.dumps(actual_pn_release), "Actual PN release.")
                    allure.attach(json.dumps(expected_pn_release), "Expected PN release.")

                    assert actual_pn_release == expected_pn_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check MS release.'):
                """
                Compare actual MS release and expected MS release.
                """
                ms_url = f"{actual_message['data']['url']}/{actual_message['data']['ocid']}"
                actual_ms_release = requests.get(url=ms_url).json()

                try:
                    """
                    Build expected MS release.
                    """
                    expected_ms_release = expected_release.build_expected_ms_release(
                        ei_payload, ei_message, fs_payloads_list, fs_message_list,
                        tender_classification_id, actual_ms_release
                    )
                except ValueError:
                    ValueError("Impossible to build expected MS release.")

                print("\n Actual MS release")
                print(json.dumps(actual_ms_release))
                print("\n Expected MS release")
                print(json.dumps(expected_ms_release))

                with allure.step('Compare actual and expected MS release.'):
                    allure.attach(json.dumps(actual_ms_release), "Actual MS release.")
                    allure.attach(json.dumps(expected_ms_release), "Expected MS release.")

                    assert actual_pn_release == expected_pn_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")
        # try:
        #     """
        #     CLean up the database.
        #     """
        #     # Clean after Crate PN process:
        #     cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
        #     cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, cpid)
        # except ValueError:
        #     ValueError("Impossible to cLean up the database.")

    # @allure.title("Check records: based on required data model.")
    # def test_case_2(self, get_parameters, connect_to_keyspace, create_fs_tc_2, create_fs_tc_3, ):
    #
    #     environment = get_parameters[0]
    #     bpe_host = get_parameters[2]
    #     service_host = get_parameters[3]
    #     country = get_parameters[4]
    #     language = get_parameters[5]
    #     pmd = get_parameters[6]
    #     tender_classification_id = get_parameters[9]
    #
    #     connect_to_ocds = connect_to_keyspace[0]
    #     connect_to_access = connect_to_keyspace[2]
    #
    #     fs_ocid_list = list()
    #     fs_payloads_list = list()
    #     fs_message_list = list()
    #
    #     fs_1_payload = create_fs_tc_2[0]
    #     ocid = create_fs_tc_2[1]
    #     fs_1_message = create_fs_tc_2[2]
    #     currency = create_fs_tc_2[3]
    #     ei_payload = create_fs_tc_2[4]
    #     ei_message = create_fs_tc_2[5]
    #     fs_ocid_list.append(ocid)
    #     fs_payloads_list.append(fs_1_payload)
    #     fs_message_list.append(fs_1_message)
    #
    #     fs_2_payload = create_fs_tc_3[0]
    #     ocid = create_fs_tc_3[1]
    #     fs_2_message = create_fs_tc_3[2]
    #     fs_ocid_list.append(ocid)
    #     fs_payloads_list.append(fs_2_payload)
    #     fs_message_list.append(fs_2_message)
    #
    #     step_number = 1
    #     with allure.step(f'# {step_number}. Authorization platform one: Create PN process.'):
    #         """
    #         Tender platform authorization for Create PN process.
    #         As result get Tender platform's access token and process operation-id.
    #         """
    #         platform_one = PlatformAuthorization(bpe_host)
    #         access_token = platform_one.get_access_token_for_platform_one()
    #         operation_id = platform_one.get_x_operation_id(access_token)
    #
    #     step_number += 1
    #     with allure.step(f'# {step_number}. Send a request to create a Create PN process.'):
    #         """
    #         Send request to BPE host to create a Create PN process.
    #         And save in variable ocid and token..
    #         """
    #         try:
    #             """
    #             Build payload for Create PN process.
    #             """
    #             payload = copy.deepcopy(PlanningNoticePayload(
    #                 fs_id=ocid,
    #                 amount=909.99,
    #                 currency=currency,
    #                 tender_classification_id=tender_classification_id,
    #                 host_to_service=service_host)
    #             )
    #
    #             payload.customize_planning_budget_budget_breakdown(fs_ocid_list)
    #
    #             payload.delete_optional_fields(
    #                 "planning.rationale",
    #                 "planning.budget.description",
    #                 "tender.procurementMethodRationale",
    #                 "tender.procurementMethodAdditionalInfo",
    #                 "tender.lots",
    #                 "tender.items",
    #                 "tender.documents"
    #             )
    #             payload = payload.build_payload()
    #
    #         except ValueError:
    #             ValueError("Impossible to build payload for CreatePlanningNotice process.")
    #
    #         synchronous_result = create_pn_process(
    #             host=bpe_host,
    #             access_token=access_token,
    #             x_operation_id=operation_id,
    #             payload=payload,
    #             test_mode=True,
    #             country=country,
    #             language=language,
    #             pmd=pmd
    #         )
    #
    #         message = get_message_for_platform(operation_id)
    #         cpid = message['data']['outcomes']['pn'][0]['id']
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
    #         with allure.step(f'# {step_number}.2. Check the message for the platform, the Create PN process.'):
    #             """
    #             Check the message for platform.
    #             """
    #             actual_message = message
    #
    #             try:
    #                 """
    #                 Build expected message for platform.
    #                 """
    #                 expected_message = copy.deepcopy(PlanningNoticeMessage(
    #                     environment=environment,
    #                     actual_message=actual_message,
    #                     test_mode=True)
    #                 )
    #
    #                 expected_message = expected_message.build_expected_message()
    #             except ValueError:
    #                 ValueError("Impossible to build expected message for platform.")
    #
    #             with allure.step('Compare actual and expected message for platform.'):
    #                 allure.attach(json.dumps(actual_message), "Actual message.")
    #                 allure.attach(json.dumps(expected_message), "Expected message.")
    #
    #                 process_id = get_process_id_by_operation_id(connect_to_ocds, operation_id)
    #
    #                 assert actual_message == expected_message, \
    #                     allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
    #                                   f"process_id = '{process_id}' ALLOW FILTERING;",
    #                                   "Cassandra DataBase: steps of process.")
    #
    #         with allure.step(f'# {step_number}.3. Check PN release.'):
    #             """
    #             Compare actual PN release and expected PN release.
    #             """
    #             pn_url = f"{actual_message['data']['url']}/{actual_message['data']['outcomes']['pn'][0]['id']}"
    #             actual_pn_release = requests.get(url=pn_url).json()
    #
    #             ms_url = f"{actual_message['data']['url']}/{actual_message['data']['ocid']}"
    #             actual_ms_release = requests.get(url=ms_url).json()
    #
    #             try:
    #                 """
    #                 Build expected PN release.
    #                 """
    #                 expected_release = copy.deepcopy(PlanningNoticeRelease(
    #                     environment=environment,
    #                     host_to_service=service_host,
    #                     language=language,
    #                     pmd=pmd,
    #                     pn_payload=payload,
    #                     pn_message=actual_message,
    #                     actual_pn_release=actual_pn_release,
    #                     actual_ms_release=actual_ms_release
    #                 ))
    #
    #                 expected_pn_release = expected_release.build_expected_pn_release()
    #             except ValueError:
    #                 ValueError("Impossible to build expected PN release.")
    #
    #             with allure.step('Compare actual and expected PN release.'):
    #                 allure.attach(json.dumps(actual_pn_release), "Actual PN release.")
    #                 allure.attach(json.dumps(expected_pn_release), "Expected PN release.")
    #
    #                 assert actual_pn_release == expected_pn_release, \
    #                     allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
    #                                   f"process_id = '{process_id}' ALLOW FILTERING;",
    #                                   "Cassandra DataBase: steps of process.")
    #
    #         with allure.step(f'# {step_number}.4. Check MS release.'):
    #             """
    #             Compare actual MS release and expected MS release.
    #             """
    #             try:
    #                 """
    #                 Build expected MS release.
    #                 """
    #                 expected_ms_release = expected_release.build_expected_ms_release(
    #                     ei_payload,
    #                     ei_message,
    #                     fs_payloads_list,
    #                     fs_message_list,
    #                     tender_classification_id
    #                 )
    #             except ValueError:
    #                 ValueError("Impossible to build expected MS release.")
    #
    #             with allure.step('Compare actual and expected MS release.'):
    #                 allure.attach(json.dumps(actual_ms_release), "Actual MS release.")
    #                 allure.attach(json.dumps(expected_ms_release), "Expected MS release.")
    #
    #                 assert actual_pn_release == expected_pn_release, \
    #                     allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
    #                                   f"process_id = '{process_id}' ALLOW FILTERING;",
    #                                   "Cassandra DataBase: steps of process.")
    #     try:
    #         """
    #         CLean up the database.
    #         """
    #         # Clean after Crate PN process:
    #         cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
    #         cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, cpid)
    #     except ValueError:
    #         ValueError("Impossible to cLean up the database.")
