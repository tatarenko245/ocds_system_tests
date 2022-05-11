import copy
import json
import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import get_process_id_by_operation_id, \
    get_max_duration_of_fa_from_access_rules
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import update_ap_process
from messages_collection.framework_agreement.update_ap_message import UpdateApMessage
from payloads_collection.framework_agreement.update_ap_payload import UpdateAggregatedPlan
from releases_collection.framework_agreement.update_ap_release import UpdateAggregatedPlanRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Aggregated Plan")
@allure.severity("Critical")
@allure.testcase(url="")
class TestUpdateAP:
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace, relation_ap_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]
        pmd = get_parameters[6]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_access = connect_to_keyspace[2]

        cpid = relation_ap_tc_1[0]
        ocid = relation_ap_tc_1[1]
        token = relation_ap_tc_1[2]
        create_ap_payload = relation_ap_tc_1[3]
        ap_url = relation_ap_tc_1[4]
        fa_url = relation_ap_tc_1[5]
        currency = relation_ap_tc_1[20]
        tender_classification_id = relation_ap_tc_1[21]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()

        step_number = 1
        with allure.step(f'# {step_number}. Authorization platform one: Update AP process.'):
            """
            Tender platform authorization for Update AP process.
            As result get Tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f'# {step_number}. Send a request to create a Update AP process.'):
            """
            Send api request to BPE host to create a Update AP process.
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
                    create_ap_payload=create_ap_payload,
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
                # Forbiden change currency, even if actual currency == previous currency.
                payload.delete_optional_fields(
                    "tender.value"
                )
                payload = payload.build_payload()
            except ValueError:
                raise ValueError("Impossible to build payload for Update AP process.")

            synchronous_result = update_ap_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                payload=payload,
                test_mode=True,
                cpid=cpid,
                ocid=ocid,
                token=token
            )

            message = get_message_for_platform(operation_id)
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Update AP process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(UpdateApMessage(
                        environment=environment,
                        actual_message=actual_message,
                        cpid=cpid,
                        ocid=ocid,
                        test_mode=True
                    ))

                    expected_message = expected_message.build_expected_message()
                except ValueError:
                    raise ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    process_id = get_process_id_by_operation_id(connect_to_ocds, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.3. Check AP release.'):
                """
                Compare previous AP release and actual AP release.
                """
                actual_ap_release = requests.get(url=ap_url).json()
                actual_fa_release = requests.get(url=fa_url).json()

                try:
                    """
                    Build expected AP release.
                    """
                    expected_release = copy.deepcopy(UpdateAggregatedPlanRelease(
                        environment,
                        language,
                        cpid,
                        ocid,
                        payload,
                        actual_message,
                        actual_ap_release,
                        previous_ap_release,
                        actual_fa_release,
                        previous_fa_release,
                    ))

                    expected_ap_release = expected_release.build_expected_ap_release()
                except ValueError:
                    raise ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    assert actual_ap_release == expected_ap_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FA release.'):
                """
                Compare previous MS release and actual MS release.
                """
                try:
                    """
                    Build expected MS release.
                    """
                    expected_fa_release = expected_release.build_expected_fa_release()
                except ValueError:
                    raise ValueError("Impossible to build expected MS release.")

                with allure.step("Compare actual and expected MS release."):
                    allure.attach(json.dumps(actual_fa_release), "Actual MS release.")
                    allure.attach(json.dumps(expected_fa_release), "Expected MS release.")

                    assert actual_fa_release == expected_fa_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")




        # try:
        #     """
        #     CLean up the database.
        #     """
        #     # Clean after Update AP process:
        #     cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
        #     cleanup_table_of_services_for_aggregated_plan(connect_to_ocds, connect_to_access, cpid)
        # except ValueError:
        #     raise ValueError("Impossible to cLean up the database.")
