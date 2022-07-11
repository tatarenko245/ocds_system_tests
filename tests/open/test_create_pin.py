import copy
import json
import os

import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from payloads_collection.open.create_pin_payload import PriorInformationNoticePayload


@allure.parent_suite("Plan")
@allure.suite("Prior Planning Notice")
@allure.severity("Critical")
@allure.testcase(url="https://docs.google.com/spreadsheets/d/1-I_7nLopu_q2wAyWzfTyscHMBL4GA1sIL6IpwBk-QCw/"
                     "edit#gid=159118352",
                 name="Test Suite")
class TestCreatePIN:

    country = os.getenv("COUNTRY")
    if country == "MD":
        @allure.title("Повна модель, якщо країна Молдова")
        def test_case_1(self, get_parameters, connect_to_keyspace, create_fs_tc_1_new):

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

            currency = create_fs_tc_1_new[0]
            ei_cpid = create_fs_tc_1_new[2]
            ei_url = create_fs_tc_1_new[4]
            fs_ocid = create_fs_tc_1_new[7]
            fs_url = create_fs_tc_1_new[9]

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
                        ))

                    list_of_classifications = [
                        {
                            "ei": ei_cpid,
                            "fs": fs_ocid
                        },
                        {
                            'ei': 'test-t1s2t3-MD-1657278051706',
                            'fs': 'test-t1s2t3-MD-1657278051706-FS-1657278059193'
                        }
                    ]
                    payload.customize_planning_budget_budgetbreakdown(list_of_classifications)

                    payload.customize_tender_lots(
                        quantity_of_lots=1,
                        quantity_of_options=1,
                        quantity_of_recurrence_dates=1,
                        quantity_of_renewal=1
                        )

                    payload.customize_tender_items(
                        quantity_of_items=1,
                        quantity_of_items_additionalclassifications=1
                    )

                    payload.customize_tender_electronicauctions_object()

                    payload.customize_tender_documents(
                        quantity_of_documents=1
                    )

                    payload.customize_tender_procuringentity_additionalidentifiers(
                        quantity_of_tender_procuring_entity_additional_identifiers=1
                    )

                    payload.customize_tender_procuringentity_bf_persones_array(
                        quantity_of_persones_objects=1,
                        quantity_of_bf_objects=1,
                        quantity_of_documents_objects=1
                    )
                    exclusion_criteria_array = payload.prepare_exclusion_criteria(
                        "criteria.relatedItem",
                        "criteria.requirementGroups.requirements.minValue",
                        "criteria.requirementGroups.requirements.maxValue",
                        language=language,
                        environment=environment
                    )

                    selection_criteria_array = payload.prepare_selection_criteria(
                        "criteria.relatedItem",
                        "criteria.requirementGroups.requirements.expectedValue",
                        language=language,
                        environment=environment
                    )

                    payload.customize_tender_criteria(
                        exclusion_criteria_array, selection_criteria_array
                    )

                    payload = payload.build_payload()
                except ValueError:
                    raise ValueError("Impossible to build payload for Create PIN process.")

                print("\n PIN payload")
                print(json.dumps(payload))

            #     synchronous_result = create_pin_process(
            #         host=bpe_host,
            #         access_token=access_token,
            #         x_operation_id=operation_id,
            #         country=country,
            #         language=language,
            #         pmd=pmd,
            #         payload=payload,
            #         test_mode=True
            #     )
            #     message = get_message_for_platform(operation_id)
            #     allure.attach(str(message), "Message for platform.")
            #
            # step_number += 1
            # with allure.step(f"# {step_number}. See result"):
            #     """
            #     Check the results of TestCase.
            #     """
            #
            #     with allure.step(f"# {step_number}.1. Check status code"):
            #         """
            #         Check the status code of sending the request.
            #         """
            #         with allure.step('Compare actual status code and expected status code of sending request.'):
            #             allure.attach(str(synchronous_result.status_code), "Actual status code.")
            #             allure.attach(str(202), "Expected status code.")
            #             assert synchronous_result.status_code == 202
            #
            #     with allure.step(f'# {step_number}.2. Check the message for the platform, the Confirm EI process.'):
            #         """
            #         Check the message for platform.
            #         """
            #         actual_message = message
            #
            #         try:
            #             """
            #             Build expected message for platform.
            #             """
            #             expected_message = copy.deepcopy(ConfirmExpenditureItemMessage(
            #                 environment=environment,
            #                 country=country,
            #                 actual_message=actual_message,
            #                 test_mode=True)
            #             )
            #
            #             expected_message = expected_message.build_expected_success_message()
            #         except ValueError:
            #             ValueError("Impossible to build expected message for platform.")
            #
            #         with allure.step('Compare actual and expected message for platform.'):
            #             allure.attach(json.dumps(actual_message), "Actual message.")
            #             allure.attach(json.dumps(expected_message), "Expected message.")
            #
            #             assert actual_message == expected_message, \
            #                 allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
            #                               f"cpid = '{cpid}' and operation_id = '{operation_id}' "
            #                               f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
            #
            #     with allure.step(f'# {step_number}.3. Check EI release.'):
            #         """
            #         Compare actual EI release and expected EI release.
            #         """
            #         url = f"{actual_message['data']['url']}/{cpid}"
            #         actual_release = requests.get(url=url).json()
            #
            #         try:
            #             """
            #             Build expected EI release.
            #             """
            #             expected_release = copy.deepcopy(ConfirmExpenditureItemRelease(
            #                 environment, language, tender_classification_id
            #             ))
            #             expected_release = expected_release.build_expected_ei_release(
            #                 actual_message, actual_release, previous_ei_release
            #             )
            #         except ValueError:
            #             ValueError("Impossible to build expected EI release.")
            #
            #         with allure.step("Compare actual and expected releases."):
            #             allure.attach(json.dumps(actual_release), "Actual release.")
            #             allure.attach(json.dumps(expected_release), "Expected release.")
            #
            #             assert actual_release == expected_release, \
            #                 allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
            #                               f"cpid = '{cpid}' and operation_id = '{operation_id}' "
            #                               f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
            # if clean_up_database is True:
            #     try:
            #         """
            #         CLean up the database.
            #         """
            #         # Clean after Update EI process:
            #         cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
            #         cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            #     except ValueError:
            #         ValueError("Impossible to cLean up the database.")
            # else:
            #     with allure.step("The steps of process."):
            #         allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
            #                       f"cpid = '{cpid}' and operation_id = '{operation_id}' "
            #                       f"ALLOW FILTERING;",    "Cassandra DataBase: steps of process.")
