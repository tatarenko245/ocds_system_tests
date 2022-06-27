import copy
import json
import allure
import requests


from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid, \
    cleanup_table_of_services_for_outsourcing_planning_notice
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import outsourcing_pn_process
from messages_collection.framework_agreement.outsourcing_pn_message import OutsourcingPnMessage
from releases_collection.framework_agreement.outsourcing_pn_release import OutsourcingPlanningNoticeRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Outsourcing PN")
@allure.severity("Critical")
@allure.testcase(url="")
class TestOutsourcingPN:
    @allure.title("Check records: based on full data model from previous processes.")
    def test_case_1(self, get_parameters, connect_to_keyspace, create_ap_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]

        ap_cpid = create_ap_tc_1[1]
        ap_ocid = create_ap_tc_1[2]
        ap_url = create_ap_tc_1[7]
        fa_url = create_ap_tc_1[8]
        pn_cpid = create_ap_tc_1[9]
        pn_ocid = create_ap_tc_1[10]
        pn_token = create_ap_tc_1[11]
        pn_url = create_ap_tc_1[12]
        ms_url = create_ap_tc_1[13]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_pn_release = requests.get(url=pn_url).json()
        previous_ms_release = requests.get(url=ms_url).json()

        step_number = 1
        with allure.step(f'# {step_number}. Authorization platform one: Outsourcing PN process.'):
            """
            Tender platform authorization for Outsourcing PN process.
            As result get Tender platform's access pn_token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f'# {step_number}. Send a request to create a Outsourcing PN process.'):
            """
            Send request to BPE host to create a Outsourcing PN process.
            """

            synchronous_result = outsourcing_pn_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=pn_cpid,
                ocid=pn_ocid,
                token=pn_token,
                fa=ap_cpid,
                ap=ap_ocid,
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Outsourcing PN process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(OutsourcingPnMessage(
                        environment=environment,
                        actual_message=actual_message,
                        cpid=pn_cpid,
                        ocid=pn_ocid
                    ))

                    expected_message = expected_message.build_expected_message()
                except ValueError:
                    raise ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"ap_cpid = '{pn_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.3. Check PN release.'):
                """
                Compare actual PN release and expected PN release.
                """
                actual_pn_release = requests.get(url=pn_url).json()
                actual_ms_release = requests.get(url=ms_url).json()
                actual_ap_release = requests.get(url=ap_url).json()
                actual_fa_release = requests.get(url=fa_url).json()

                try:
                    """
                    Build expected PN release.
                    """
                    expected_release = copy.deepcopy(OutsourcingPlanningNoticeRelease(
                        environment,
                        actual_message,
                        pn_cpid,
                        pn_ocid,
                        ap_cpid,
                        ap_ocid,
                        actual_pn_release,
                        previous_pn_release,
                        actual_ms_release,
                        previous_ms_release,
                        actual_ap_release,
                        previous_ap_release,
                        actual_fa_release,
                        previous_fa_release
                    ))

                    expected_pn_release = expected_release.build_expected_pn_release()
                except ValueError:
                    raise ValueError("Impossible to build expected PN release.")

                with allure.step('Compare actual and expected PN release.'):
                    allure.attach(json.dumps(actual_pn_release), "Actual release.")
                    allure.attach(json.dumps(expected_pn_release), "Expected release.")

                    assert actual_pn_release == expected_pn_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"ap_cpid = '{pn_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check MS release.'):
                """
                Compare actual MS release and expected MS release.
                """
                try:
                    """
                    Build expected MS release.
                    """
                    expected_ms_release = expected_release.build_expected_ms_release()
                except ValueError:
                    raise ValueError("Impossible to build expected MS release.")

                with allure.step("Compare actual and expected MS release."):
                    allure.attach(json.dumps(actual_ms_release), "Actual release.")
                    allure.attach(json.dumps(expected_ms_release), "Expected release.")

                    assert actual_ms_release == expected_ms_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"ap_cpid = '{pn_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
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
                    raise ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected release.")

                    assert actual_ap_release == expected_ap_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"ap_cpid = '{pn_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
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
                    raise ValueError("Impossible to build expected FA release.")

                with allure.step("Compare actual and expected FA release."):
                    allure.attach(json.dumps(actual_fa_release), "Actual release.")
                    allure.attach(json.dumps(expected_fa_release), "Expected release.")

                    assert actual_fa_release == expected_fa_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"ap_cpid = '{pn_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

        try:
            """
            CLean up the database.
            """
            # Clean after Outsourcing PN process:
            cleanup_orchestrator_steps_by_cpid(
                connect_to_orchestrator,
                pn_cpid
            )

            cleanup_table_of_services_for_outsourcing_planning_notice(
                connect_to_ocds,
                connect_to_access,
                pn_cpid
            )
        except ValueError:
            raise ValueError("Impossible to cLean up the database.")

    @allure.title("Check records: based on required data model from previous processes.")
    def test_case_2(self, get_parameters, connect_to_keyspace, create_ap_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]

        ap_cpid = create_ap_tc_2[1]
        ap_ocid = create_ap_tc_2[2]
        ap_url = create_ap_tc_2[7]
        fa_url = create_ap_tc_2[8]
        pn_cpid = create_ap_tc_2[9]
        pn_ocid = create_ap_tc_2[10]
        pn_token = create_ap_tc_2[11]
        pn_url = create_ap_tc_2[12]
        ms_url = create_ap_tc_2[13]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_pn_release = requests.get(url=pn_url).json()
        previous_ms_release = requests.get(url=ms_url).json()

        step_number = 1
        with allure.step(f'# {step_number}. Authorization platform one: Outsourcing PN process.'):
            """
            Tender platform authorization for Outsourcing PN process.
            As result get Tender platform's access pn_token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f'# {step_number}. Send a request to create a Outsourcing PN process.'):
            """
            Send request to BPE host to create a Outsourcing PN process.
            """

            synchronous_result = outsourcing_pn_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=pn_cpid,
                ocid=pn_ocid,
                token=pn_token,
                fa=ap_cpid,
                ap=ap_ocid,
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Outsourcing PN process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(OutsourcingPnMessage(
                        environment=environment,
                        actual_message=actual_message,
                        cpid=pn_cpid,
                        ocid=pn_ocid
                    ))

                    expected_message = expected_message.build_expected_message()
                except ValueError:
                    raise ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"ap_cpid = '{pn_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.3. Check PN release.'):
                """
                Compare actual PN release and expected PN release.
                """
                actual_pn_release = requests.get(url=pn_url).json()
                actual_ms_release = requests.get(url=ms_url).json()
                actual_ap_release = requests.get(url=ap_url).json()
                actual_fa_release = requests.get(url=fa_url).json()

                try:
                    """
                    Build expected PN release.
                    """
                    expected_release = copy.deepcopy(OutsourcingPlanningNoticeRelease(
                        environment,
                        actual_message,
                        pn_cpid,
                        pn_ocid,
                        ap_cpid,
                        ap_ocid,
                        actual_pn_release,
                        previous_pn_release,
                        actual_ms_release,
                        previous_ms_release,
                        actual_ap_release,
                        previous_ap_release,
                        actual_fa_release,
                        previous_fa_release
                    ))

                    expected_pn_release = expected_release.build_expected_pn_release()
                except ValueError:
                    raise ValueError("Impossible to build expected PN release.")

                with allure.step('Compare actual and expected PN release.'):
                    allure.attach(json.dumps(actual_pn_release), "Actual release.")
                    allure.attach(json.dumps(expected_pn_release), "Expected release.")

                    assert actual_pn_release == expected_pn_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"ap_cpid = '{pn_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check MS release.'):
                """
                Compare actual MS release and expected MS release.
                """
                try:
                    """
                    Build expected MS release.
                    """
                    expected_ms_release = expected_release.build_expected_ms_release()
                except ValueError:
                    raise ValueError("Impossible to build expected MS release.")

                with allure.step("Compare actual and expected MS release."):
                    allure.attach(json.dumps(actual_ms_release), "Actual release.")
                    allure.attach(json.dumps(expected_ms_release), "Expected release.")

                    assert actual_ms_release == expected_ms_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"ap_cpid = '{pn_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
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
                    raise ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected release.")

                    assert actual_ap_release == expected_ap_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"ap_cpid = '{pn_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
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
                    raise ValueError("Impossible to build expected FA release.")

                with allure.step("Compare actual and expected FA release."):
                    allure.attach(json.dumps(actual_fa_release), "Actual release.")
                    allure.attach(json.dumps(expected_fa_release), "Expected release.")

                    assert actual_fa_release == expected_fa_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"ap_cpid = '{pn_cpid}' AND operation_id={operation_id} ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

        try:
            """
            CLean up the database.
            """
            # Clean after Outsourcing PN process:
            cleanup_orchestrator_steps_by_cpid(
                connect_to_orchestrator,
                pn_cpid
            )

            cleanup_table_of_services_for_outsourcing_planning_notice(
                connect_to_ocds,
                connect_to_access,
                pn_cpid
            )
        except ValueError:
            raise ValueError("Impossible to cLean up the database.")
