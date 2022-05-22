import copy
import json
import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid, \
    cleanup_table_of_services_for_qualification
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import qualification_process
from messages_collection.framework_agreement.qualification_message import QualificationMessage
from payloads_collection.framework_agreement.qualification_payload import QualificationPayload
from releases_collection.framework_agreement.qualification_release import QualificationRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Qualification")
@allure.severity("Critical")
@allure.testcase(url="")
class TestQualification:
    @allure.testcase(url="")
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace, qualification_consideration_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]
        connect_to_dossier = connect_to_keyspace[4]
        connect_to_qualification = connect_to_keyspace[5]

        cpid = qualification_consideration_tc_1[0]
        ap_url = qualification_consideration_tc_1[4]
        fa_url = qualification_consideration_tc_1[5]
        ocid = qualification_consideration_tc_1[23]
        fe_url = qualification_consideration_tc_1[24]
        list_of_submission_messages = [
            qualification_consideration_tc_1[26],
            qualification_consideration_tc_1[28],
            qualification_consideration_tc_1[30]
        ]
        submission_period_end_message = qualification_consideration_tc_1[31]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_fe_release = requests.get(url=fe_url).json()

        """Get qualification in state = pending.consideration: VR.COM-7.17.2"""
        qualification_list = list()
        for q in range(len(previous_fe_release['releases'][0]['qualifications'])):
            if previous_fe_release['releases'][0]['qualifications'][q]['status'] == "pending":
                if "statusDetails" in previous_fe_release['releases'][0]['qualifications'][q]:
                    if previous_fe_release['releases'][0]['qualifications'][q]['statusDetails'] == "consideration":
                        qualification_list.append(
                            {
                                "id": previous_fe_release['releases'][0]['qualifications'][q]['id'],
                                "token": None
                            }
                        )

        """Get qualification.token by qualification.id for Qualification process."""
        for ql in range(len(qualification_list)):
            for qm in range(len(submission_period_end_message['data']['outcomes']['qualifications'])):
                if submission_period_end_message['data']['outcomes']['qualifications'][qm]['id'] == \
                        qualification_list[ql]['id']:
                    qualification_list[ql]['token'] = \
                        submission_period_end_message['data']['outcomes']['qualifications'][qm]['X-TOKEN']

        """ Depends on quantity of qualifications in valid state, send requests"""
        step_number = 1
        for q in range(len(qualification_list)):
            step_number += q

            with allure.step(f"# {step_number}. Authorization platform one: Qualification process."):
                """
                Tender platform authorization for Qualification process.
                As result get Tender platform's access token and process operation-id.
                """
                platform_one = PlatformAuthorization(bpe_host)
                access_token = platform_one.get_access_token_for_platform_one()
                operation_id = platform_one.get_x_operation_id(access_token)

            step_number += 1
            with allure.step(f"# {step_number}. Send a request to create a Qualification process."):
                """
                Send request to BPE host to create a Qualification process.
                """
                try:
                    """
                    Build payload for Qualification process.
                    """
                    payload = copy.deepcopy(QualificationPayload(service_host))
                    payload.customize_qualification_documents(quantity_of_documents=3)
                    payload = payload.build_payload(status="active")
                except ValueError:
                    ValueError("Impossible to build payload for Qualification Declare process.")

                synchronous_result = qualification_process(
                    host=bpe_host,
                    access_token=access_token,
                    x_operation_id=operation_id,
                    payload=payload,
                    test_mode=True,
                    cpid=cpid,
                    ocid=ocid,
                    qualification_id=qualification_list[q]['id'],
                    qualification_token=qualification_list[q]['token']
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
                    with allure.step('Compare actual status code and expected status code '
                                     'of sending request.'):
                        allure.attach(str(synchronous_result.status_code), "Actual status code.")
                        allure.attach(str(202), "Expected status code.")
                        assert synchronous_result.status_code == 202

                with allure.step(f'# {step_number}.2. Check the message for the platform, the Qualification process.'):
                    """
                    Check the message for platform.
                    """
                    actual_message = message
                    try:
                        """
                        Build expected message for platform.
                        """
                        expected_message = copy.deepcopy(QualificationMessage(
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
                                          f"cpid = '{cpid}' and operation_id = '{operation_id}' "
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
                        expected_release = copy.deepcopy(QualificationRelease(
                            environment, payload, actual_message, ocid
                        ))
                        expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
                    except ValueError:
                        ValueError("Impossible to build expected AP release.")

                    with allure.step("Compare actual and expected AP release."):
                        allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                        allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
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
                            previous_fe_release,
                            actual_fe_release,
                            qualification_list[q]['id'],
                            list_of_submission_messages
                        )
                    except ValueError:
                        ValueError("Impossible to build expected FE release.")

                    with allure.step("Compare actual and expected FE release."):
                        allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                        allure.attach(json.dumps(expected_fe_release), "Expected FE release.")

                        assert actual_fe_release == expected_fe_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"cpid = '{cpid}' and operation_id = '{operation_id}' "
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
                        expected_fa_release = expected_release.build_expected_fa_release(
                            previous_fa_release
                        )
                    except ValueError:
                        ValueError("Impossible to build expected FA release.")

                    with allure.step("Compare actual and expected FA release."):
                        allure.attach(json.dumps(actual_fa_release), "Actual Fa release.")
                        allure.attach(json.dumps(expected_fa_release), "Expected Fa release.")

                        assert actual_fa_release == expected_fa_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            previous_ap_release = requests.get(url=ap_url).json()
            previous_fa_release = requests.get(url=fa_url).json()
            previous_fe_release = requests.get(url=fe_url).json()

        try:
            """
            CLean up the database.
            """
            # Clean after Qualification Declare Non Conflict Of Interest process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)

            cleanup_table_of_services_for_qualification(
                connect_to_ocds, connect_to_access, connect_to_qualification, connect_to_dossier, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")

    @allure.testcase(url="")
    @allure.title("Check records: based on required data model.")
    def test_case_2(self, get_parameters, connect_to_keyspace, qualification_consideration_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]
        connect_to_dossier = connect_to_keyspace[4]
        connect_to_qualification = connect_to_keyspace[5]

        cpid = qualification_consideration_tc_2[0]
        ap_url = qualification_consideration_tc_2[4]
        fa_url = qualification_consideration_tc_2[5]
        ocid = qualification_consideration_tc_2[23]
        fe_url = qualification_consideration_tc_2[24]
        list_of_submission_messages = [qualification_consideration_tc_2[26]]
        submission_period_end_message = qualification_consideration_tc_2[27]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_fe_release = requests.get(url=fe_url).json()

        """Get qualification in state = pending.consideration: VR.COM-7.17.2"""
        qualification_list = list()
        for q in range(len(previous_fe_release['releases'][0]['qualifications'])):
            if previous_fe_release['releases'][0]['qualifications'][q]['status'] == "pending":
                if "statusDetails" in previous_fe_release['releases'][0]['qualifications'][q]:
                    if previous_fe_release['releases'][0]['qualifications'][q]['statusDetails'] == "consideration":
                        qualification_list.append(
                            {
                                "id": previous_fe_release['releases'][0]['qualifications'][q]['id'],
                                "token": None
                            }
                        )

        """Get qualification.token by qualification.id for Qualification process."""
        for ql in range(len(qualification_list)):
            for qm in range(len(submission_period_end_message['data']['outcomes']['qualifications'])):
                if submission_period_end_message['data']['outcomes']['qualifications'][qm]['id'] == \
                        qualification_list[ql]['id']:
                    qualification_list[ql]['token'] = \
                        submission_period_end_message['data']['outcomes']['qualifications'][qm]['X-TOKEN']

        """ Depends on quantity of qualifications in valid state, send requests"""
        step_number = 1
        for q in range(len(qualification_list)):
            step_number += q

            with allure.step(f"# {step_number}. Authorization platform one: Qualification process."):
                """
                Tender platform authorization for Qualification process.
                As result get Tender platform's access token and process operation-id.
                """
                platform_one = PlatformAuthorization(bpe_host)
                access_token = platform_one.get_access_token_for_platform_one()
                operation_id = platform_one.get_x_operation_id(access_token)

            step_number += 1
            with allure.step(f"# {step_number}. Send a request to create a Qualification process."):
                """
                Send request to BPE host to create a Qualification process.
                """
                try:
                    """
                    Build payload for Qualification process.
                    """
                    payload = copy.deepcopy(QualificationPayload(service_host))
                    payload.delete_optional_fields(
                        "qualification.internalId",
                        "qualification.description",
                        "qualification.documents",
                        doc_position=0
                    )
                    payload = payload.build_payload(status="active")
                except ValueError:
                    ValueError("Impossible to build payload for Qualification Declare process.")

                synchronous_result = qualification_process(
                    host=bpe_host,
                    access_token=access_token,
                    x_operation_id=operation_id,
                    payload=payload,
                    test_mode=True,
                    cpid=cpid,
                    ocid=ocid,
                    qualification_id=qualification_list[q]['id'],
                    qualification_token=qualification_list[q]['token']
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
                    with allure.step('Compare actual status code and expected status code '
                                     'of sending request.'):
                        allure.attach(str(synchronous_result.status_code), "Actual status code.")
                        allure.attach(str(202), "Expected status code.")
                        assert synchronous_result.status_code == 202

                with allure.step(f'# {step_number}.2. Check the message for the platform, the Qualification process.'):
                    """
                    Check the message for platform.
                    """
                    actual_message = message
                    try:
                        """
                        Build expected message for platform.
                        """
                        expected_message = copy.deepcopy(QualificationMessage(
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
                                          f"cpid = '{cpid}' and operation_id = '{operation_id}' "
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
                        expected_release = copy.deepcopy(QualificationRelease(
                            environment, payload, actual_message, ocid
                        ))
                        expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
                    except ValueError:
                        ValueError("Impossible to build expected AP release.")

                    with allure.step("Compare actual and expected AP release."):
                        allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                        allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
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
                            previous_fe_release,
                            actual_fe_release,
                            qualification_list[q]['id'],
                            list_of_submission_messages
                        )
                    except ValueError:
                        ValueError("Impossible to build expected FE release.")

                    with allure.step("Compare actual and expected FE release."):
                        allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                        allure.attach(json.dumps(expected_fe_release), "Expected FE release.")

                        assert actual_fe_release == expected_fe_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"cpid = '{cpid}' and operation_id = '{operation_id}' "
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
                        expected_fa_release = expected_release.build_expected_fa_release(
                            previous_fa_release
                        )
                    except ValueError:
                        ValueError("Impossible to build expected FA release.")

                    with allure.step("Compare actual and expected FA release."):
                        allure.attach(json.dumps(actual_fa_release), "Actual Fa release.")
                        allure.attach(json.dumps(expected_fa_release), "Expected Fa release.")

                        assert actual_fa_release == expected_fa_release, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            previous_ap_release = requests.get(url=ap_url).json()
            previous_fa_release = requests.get(url=fa_url).json()
            previous_fe_release = requests.get(url=fe_url).json()

        try:
            """
            CLean up the database.
            """
            # Clean after Qualification Declare Non Conflict Of Interest process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)

            cleanup_table_of_services_for_qualification(
                connect_to_ocds, connect_to_access, connect_to_qualification, connect_to_dossier, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")
