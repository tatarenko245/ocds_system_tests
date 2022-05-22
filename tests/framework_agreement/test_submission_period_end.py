import copy
import json
import allure
import requests

from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid, \
     cleanup_table_of_services_for_submission_period_end
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.some_functions import time_bot
from messages_collection.framework_agreement.submission_period_end_message import SubmissionPeriodEndMessage
from releases_collection.framework_agreement.submission_period_end_release import SubmissionPeriodEndRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Submission")
@allure.severity("Critical")
class TestSubmissionPeriodEnd:
    @allure.title("Check records: based on full data model.")
    @allure.testcase(url="")
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace, create_submission_tc_1):

        environment = get_parameters[0]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]
        pmd = get_parameters[6]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]
        connect_to_clarification = connect_to_keyspace[3]
        connect_to_dossier = connect_to_keyspace[4]
        connect_to_qualification = connect_to_keyspace[5]

        cpid = create_submission_tc_1[0]
        ap_url = create_submission_tc_1[4]
        fa_url = create_submission_tc_1[5]
        ocid = create_submission_tc_1[23]
        fe_url = create_submission_tc_1[24]
        list_of_submission_payloads = [
            create_submission_tc_1[25],
            create_submission_tc_1[27],
            create_submission_tc_1[29]
        ]
        list_of_submission_messages = [
            create_submission_tc_1[26],
            create_submission_tc_1[28],
            create_submission_tc_1[30]
        ]
        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_fe_release = requests.get(url=fe_url).json()

        step_number = 1
        with allure.step(f"# {step_number}. Get message for platform."):
            time_bot(previous_fe_release['releases'][0]['preQualification']['period']['endDate'])
            message = get_message_for_platform(ocid=ocid, initiator="bpe")
            allure.attach(str(message), "Message for platform.")

        step_number += 1
        with allure.step(f"# {step_number}. See result"):
            """
            Check the results of TestCase.
            """

            with allure.step(f'# {step_number}.1. Check the message for the platform,'
                             f'the Submission Period End process.'):
                """
                Check the message for platform.
                """
                actual_message = message[0]

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(SubmissionPeriodEndMessage(
                        environment=environment,
                        actual_message=actual_message,
                        cpid=cpid,
                        ocid=ocid,
                        test_mode=True,
                        expected_quantity_of_outcomes_submission=3
                    ))

                    expected_message = expected_message.build_expected_message()
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{actual_message['X-OPERATION-ID']}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.3. Check AP release.'):
                """
                Compare previous AP release and actual AP release.
                """
                actual_ap_release = requests.get(url=ap_url).json()
                try:
                    """
                    Build expected AP release.
                    """
                    expected_release = copy.deepcopy(SubmissionPeriodEndRelease(
                        environment, country, language, pmd, actual_message, service_host, ocid
                    ))
                    expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
                except ValueError:
                    ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                  f"cpid = '{cpid}' and operation_id = '{actual_message['X-OPERATION-ID']}' "
                                  f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FE release.'):
                """
                Compare previous FE release and actual FE release.
                """
                actual_fe_release = requests.get(url=fe_url).json()
                try:
                    """
                    Build expected FE release.
                    """
                    expected_fe_release = expected_release.build_expected_fe_release(
                        previous_fe_release, list_of_submission_payloads, list_of_submission_messages,
                        actual_fe_release
                    )
                except ValueError:
                    ValueError("Impossible to build expected FE release.")

                with allure.step("Compare actual and expected FE release."):
                    allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                    allure.attach(json.dumps(expected_fe_release), "Expected FE release.")

                    assert actual_fe_release == expected_fe_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{actual_message['X-OPERATION-ID']}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FA release.'):
                """
                Compare previous FA release and actual FA release.
                """
                actual_fa_release = requests.get(url=fa_url).json()
                try:
                    """
                    Build expected FA release.
                    """
                    expected_fa_release = expected_release.build_expected_fa_release(previous_fa_release)
                except ValueError:
                    ValueError("Impossible to build expected FA release.")

                with allure.step("Compare actual and expected FA release."):
                    allure.attach(json.dumps(actual_fa_release), "Actual Fa release.")
                    allure.attach(json.dumps(expected_fa_release), "Expected Fa release.")

                    assert actual_fa_release == expected_fa_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{actual_message['X-OPERATION-ID']}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        try:
            """
            CLean up the database.
            """
            # Clean after Create Submission process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)

            cleanup_table_of_services_for_submission_period_end(
                connect_to_ocds, connect_to_access, connect_to_dossier, connect_to_clarification,
                connect_to_qualification, cpid
            )
        except ValueError:
            ValueError("Impossible to cLean up the database.")

    @allure.title("Check records: based on required data model.")
    def test_case_2(self, get_parameters, connect_to_keyspace, create_submission_tc_2):

        environment = get_parameters[0]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]
        pmd = get_parameters[6]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]
        connect_to_clarification = connect_to_keyspace[3]
        connect_to_dossier = connect_to_keyspace[4]
        connect_to_qualification = connect_to_keyspace[5]

        cpid = create_submission_tc_2[0]
        ap_url = create_submission_tc_2[4]
        fa_url = create_submission_tc_2[5]
        ocid = create_submission_tc_2[23]
        fe_url = create_submission_tc_2[24]
        list_of_submission_payloads = [create_submission_tc_2[25]]
        list_of_submission_messages = [create_submission_tc_2[26]]
        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_fe_release = requests.get(url=fe_url).json()

        step_number = 1
        with allure.step(f"# {step_number}. Get message for platform."):
            time_bot(previous_fe_release['releases'][0]['preQualification']['period']['endDate'])
            message = get_message_for_platform(ocid=ocid, initiator="bpe")
            allure.attach(str(message), "Message for platform.")

        step_number += 1
        with allure.step(f"# {step_number}. See result"):
            """
            Check the results of TestCase.
            """

            with allure.step(f'# {step_number}.1. Check the message for the platform,'
                             f'the Submission Period End process.'):
                """
                Check the message for platform.
                """
                actual_message = message[0]

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(SubmissionPeriodEndMessage(
                        environment=environment,
                        actual_message=actual_message,
                        cpid=cpid,
                        ocid=ocid,
                        test_mode=True
                    ))

                    expected_message = expected_message.build_expected_message()
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{actual_message['X-OPERATION-ID']}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.3. Check AP release.'):
                """
                Compare previous AP release and actual AP release.
                """
                actual_ap_release = requests.get(url=ap_url).json()
                try:
                    """
                    Build expected AP release.
                    """
                    expected_release = copy.deepcopy(SubmissionPeriodEndRelease(
                        environment, country, language, pmd, actual_message, service_host, ocid
                    ))
                    expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
                except ValueError:
                    ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                  f"cpid = '{cpid}' and operation_id = '{actual_message['X-OPERATION-ID']}' "
                                  f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FE release.'):
                """
                Compare previous FE release and actual FE release.
                """
                actual_fe_release = requests.get(url=fe_url).json()
                try:
                    """
                    Build expected FE release.
                    """
                    expected_fe_release = expected_release.build_expected_fe_release(
                        previous_fe_release, list_of_submission_payloads, list_of_submission_messages,
                        actual_fe_release
                    )
                except ValueError:
                    ValueError("Impossible to build expected FE release.")

                with allure.step("Compare actual and expected FE release."):
                    allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                    allure.attach(json.dumps(expected_fe_release), "Expected FE release.")

                    assert actual_fe_release == expected_fe_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{actual_message['X-OPERATION-ID']}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FA release.'):
                """
                Compare previous FA release and actual FA release.
                """
                actual_fa_release = requests.get(url=fa_url).json()
                try:
                    """
                    Build expected FA release.
                    """
                    expected_fa_release = expected_release.build_expected_fa_release(previous_fa_release)
                except ValueError:
                    ValueError("Impossible to build expected FA release.")

                with allure.step("Compare actual and expected FA release."):
                    allure.attach(json.dumps(actual_fa_release), "Actual Fa release.")
                    allure.attach(json.dumps(expected_fa_release), "Expected Fa release.")

                    assert actual_fa_release == expected_fa_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{actual_message['X-OPERATION-ID']}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        try:
            """
            CLean up the database.
            """
            # Clean after Create Submission process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)

            cleanup_table_of_services_for_submission_period_end(
                connect_to_ocds, connect_to_access, connect_to_dossier, connect_to_clarification,
                connect_to_qualification, cpid
            )
        except ValueError:
            ValueError("Impossible to cLean up the database.")
