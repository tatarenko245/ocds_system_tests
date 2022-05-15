import copy
import json
import allure
import requests


from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid, \
    cleanup_table_of_services_for_relation_aggregated_plan
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import relation_ap_process
from messages_collection.framework_agreement.relation_ap_message import RelationApMessage
from releases_collection.framework_agreement.relation_ap_release import RelationAggregatedPlanRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Relation AP")
@allure.severity("Critical")
class TestRelationAP:
    @allure.title("Check records: based on full data model from previous processes.")
    @allure.testcase(
        url="https://docs.google.com/spreadsheets/d/1taw-E-4lryj80XYGdVwi1G-C2U6SQyilBuziGjXGyME/edit#gid=0",
        name="Why this test case was fall down?")
    def test_case_1(self, get_parameters, connect_to_keyspace, outsource_pn_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        language = get_parameters[5]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]

        ap_cpid = outsource_pn_tc_1[0]
        ap_ocid = outsource_pn_tc_1[1]
        ap_token = outsource_pn_tc_1[2]

        ap_url = outsource_pn_tc_1[4]
        fa_url = outsource_pn_tc_1[5]
        pn_1_cpid = outsource_pn_tc_1[6]
        pn_1_ocid = outsource_pn_tc_1[7]
        pn_1_payload = outsource_pn_tc_1[9]
        pn_1_url = outsource_pn_tc_1[10]
        ms_1_url = outsource_pn_tc_1[11]
        pn_2_cpid = outsource_pn_tc_1[12]
        pn_2_ocid = outsource_pn_tc_1[13]
        pn_2_payload = outsource_pn_tc_1[15]
        pn_2_url = outsource_pn_tc_1[16]
        ms_2_url = outsource_pn_tc_1[17]
        ei_1_payload = outsource_pn_tc_1[18]
        ei_2_payload = outsource_pn_tc_1[19]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_pn_1_release = requests.get(url=pn_1_url).json()
        previous_ms_1_release = requests.get(url=ms_1_url).json()
        previous_pn_2_release = requests.get(url=pn_2_url).json()
        previous_ms_2_release = requests.get(url=ms_2_url).json()

        step_number = 1
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

            synchronous_result = relation_ap_process(
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Relation AP process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(RelationApMessage(
                        environment=environment,
                        actual_message=actual_message,
                        cpid=ap_cpid,
                        ocid=ap_ocid
                    ))

                    expected_message = expected_message.build_expected_message()
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"fa = '{ap_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.3. Check PN release.'):
                """
                Compare actual PN release and expected PN release.
                """
                actual_pn_1_release = requests.get(url=pn_1_url).json()
                actual_ms_1_release = requests.get(url=ms_1_url).json()
                actual_ap_release = requests.get(url=ap_url).json()
                actual_fa_release = requests.get(url=fa_url).json()

                try:
                    """
                    Build expected PN release.
                    """
                    expected_release = copy.deepcopy(RelationAggregatedPlanRelease(
                        environment,
                        language,
                        actual_message,
                        ap_cpid,
                        ap_ocid,
                        pn_1_cpid,
                        pn_1_ocid,
                        actual_pn_1_release,
                        previous_pn_1_release,
                        actual_ms_1_release,
                        previous_ms_1_release,
                        actual_ap_release,
                        previous_ap_release,
                        actual_fa_release,
                        previous_fa_release,
                        [pn_1_payload],
                        [ei_1_payload]
                    ))

                    expected_pn_1_release = expected_release.build_expected_pn_release()
                except ValueError:
                    ValueError("Impossible to build expected PN release.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_pn_1_release), "Actual message.")
                    allure.attach(json.dumps(expected_pn_1_release), "Expected message.")

                    assert actual_pn_1_release == expected_pn_1_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"fa = '{ap_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check MS release.'):
                """
                Compare actual MS release and expected MS release.
                """
                try:
                    """
                    Build expected MS release.
                    """
                    expected_ms_1_release = expected_release.build_expected_ms_release()
                except ValueError:
                    ValueError("Impossible to build expected MS release.")

                with allure.step("Compare actual and expected MS release."):
                    allure.attach(json.dumps(actual_ms_1_release), "Actual MS release.")
                    allure.attach(json.dumps(expected_ms_1_release), "Expected MS release.")

                    assert actual_ms_1_release == expected_ms_1_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"fa = '{ap_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.5. Check AP release.'):
                """
                Compare actual AP release and expected AP release.
                """
                try:
                    """
                    Build expected AP release.
                    """
                    expected_ap_release = expected_release.build_expected_ap_release()
                except ValueError:
                    ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    assert actual_ap_release == expected_ap_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"fa = '{ap_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.6. Check FA release.'):
                """
                Compare actual FA release and expected FA release.
                """
                try:
                    """
                    Build expected FA release.
                    """
                    expected_fa_release = expected_release.build_expected_fa_release()
                except ValueError:
                    ValueError("Impossible to build expected FA release.")

                with allure.step("Compare actual and expected FA release."):
                    allure.attach(json.dumps(actual_fa_release), "Actual FA release.")
                    allure.attach(json.dumps(expected_fa_release), "Expected FA release.")

                    assert actual_fa_release == expected_fa_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"fa = '{ap_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()

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

            synchronous_result = relation_ap_process(
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Relation AP process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(RelationApMessage(
                        environment=environment,
                        actual_message=actual_message,
                        cpid=ap_cpid,
                        ocid=ap_ocid
                    ))

                    expected_message = expected_message.build_expected_message()
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"fa = '{ap_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.3. Check PN release.'):
                """
                Compare actual PN release and expected PN release.
                """
                actual_pn_2_release = requests.get(url=pn_2_url).json()
                actual_ms_2_release = requests.get(url=ms_2_url).json()
                actual_ap_release = requests.get(url=ap_url).json()
                actual_fa_release = requests.get(url=fa_url).json()

                try:
                    """
                    Build expected PN release.
                    """
                    expected_release = copy.deepcopy(RelationAggregatedPlanRelease(
                        environment,
                        language,
                        actual_message,
                        ap_cpid,
                        ap_ocid,
                        pn_2_cpid,
                        pn_2_ocid,
                        actual_pn_2_release,
                        previous_pn_2_release,
                        actual_ms_2_release,
                        previous_ms_2_release,
                        actual_ap_release,
                        previous_ap_release,
                        actual_fa_release,
                        previous_fa_release,
                        [pn_2_payload],
                        [ei_2_payload]
                    ))

                    expected_pn_2_release = expected_release.build_expected_pn_release()
                except ValueError:
                    ValueError("Impossible to build expected PN release.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_pn_2_release), "Actual message.")
                    allure.attach(json.dumps(expected_pn_2_release), "Expected message.")

                    assert actual_pn_2_release == expected_pn_2_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"fa = '{ap_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check MS release.'):
                """
                Compare actual MS release and expected MS release.
                """
                try:
                    """
                    Build expected MS release.
                    """
                    expected_ms_2_release = expected_release.build_expected_ms_release()
                except ValueError:
                    ValueError("Impossible to build expected MS release.")

                with allure.step("Compare actual and expected MS release."):
                    allure.attach(json.dumps(actual_ms_2_release), "Actual MS release.")
                    allure.attach(json.dumps(expected_ms_2_release), "Expected MS release.")

                    assert actual_ms_2_release == expected_ms_2_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"fa = '{ap_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.5. Check AP release.'):
                """
                Compare actual AP release and expected AP release.
                """
                try:
                    """
                    Build expected AP release.
                    """
                    expected_ap_release = expected_release.build_expected_ap_release()
                except ValueError:
                    ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    assert actual_ap_release == expected_ap_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"fa = '{ap_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.6. Check FA release.'):
                """
                Compare actual FA release and expected FA release.
                """
                try:
                    """
                    Build expected FA release.
                    """
                    expected_fa_release = expected_release.build_expected_fa_release()
                except ValueError:
                    ValueError("Impossible to build expected FA release.")

                with allure.step("Compare actual and expected FA release."):
                    allure.attach(json.dumps(actual_fa_release), "Actual FA release.")
                    allure.attach(json.dumps(expected_fa_release), "Expected FA release.")

                    assert actual_fa_release == expected_fa_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"fa = '{ap_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

        try:
            """
            CLean up the database.
            """
            # Clean after Relation AP process:
            cleanup_orchestrator_steps_by_cpid(
                connect_to_orchestrator,
                ap_cpid
            )

            cleanup_table_of_services_for_relation_aggregated_plan(
                connect_to_ocds,
                connect_to_access,
                ap_cpid
            )
        except ValueError:
            ValueError("Impossible to cLean up the database.")
