import copy
import json
import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid, \
    cleanup_table_of_services_for_create_submission
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_submission_process
from messages_collection.framework_agreement.create_submission_message import CreateSubmissionMessage
from payloads_collection.framework_agreement.create_submission_payload import CreateSubmissionPayload
from releases_collection.framework_agreement.create_submission_release import CreateSubmissionRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Submission")
@allure.severity("Critical")
@allure.testcase(url="")
class TestCreateSubmission:
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace, amend_fe_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]
        connect_to_dossier = connect_to_keyspace[4]

        cpid = amend_fe_tc_1[0]
        ap_url = amend_fe_tc_1[4]
        fa_url = amend_fe_tc_1[5]
        ocid = amend_fe_tc_1[23]
        fe_url = amend_fe_tc_1[24]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_fe_release = requests.get(url=fe_url).json()

        step_number = 1
        with allure.step(f'# {step_number}. Authorization platform one: Create Submission process.'):
            """
            Tender platform authorization for Create Submission process.
            As result get Tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

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
                payload = payload.build_payload()
            except ValueError:
                ValueError("Impossible to build payload for Create Submisison process.")

            synchronous_result = create_submission_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                payload=payload,
                test_mode=True,
                cpid=cpid,
                ocid=ocid
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create Submission process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(CreateSubmissionMessage(
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
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.3. Check AP release.'):
                """
                Compare previous AP release and actual AP release.
                """
                actual_ap_release = requests.get(url=ap_url).json()
                try:
                    """
                    Build expected AP release.
                    """
                    expected_release = copy.deepcopy(CreateSubmissionRelease())
                    expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
                except ValueError:
                    ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                  f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
                                  "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FE release.'):
                """
                Compare previous FE release and actual FE release.
                """
                actual_fe_release = requests.get(url=fe_url).json()
                try:
                    """
                    Build expected FE release.
                    """
                    expected_fe_release = expected_release.build_expected_fe_release(previous_fe_release)
                except ValueError:
                    ValueError("Impossible to build expected FE release.")

                with allure.step("Compare actual and expected FE release."):
                    allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                    allure.attach(json.dumps(expected_fe_release), "Expected FE release.")

                    assert actual_fe_release == expected_fe_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

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
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")
        try:
            """
            CLean up the database.
            """
            # Clean after Create Submission process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)

            cleanup_table_of_services_for_create_submission(
                connect_to_ocds, connect_to_access, connect_to_dossier, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")

    @allure.title("Check records: based on required data model.")
    def test_case_2(self, get_parameters, connect_to_keyspace, amend_fe_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]
        connect_to_dossier = connect_to_keyspace[4]

        cpid = amend_fe_tc_2[0]
        ap_url = amend_fe_tc_2[4]
        fa_url = amend_fe_tc_2[5]
        ocid = amend_fe_tc_2[23]
        fe_url = amend_fe_tc_2[24]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_fe_release = requests.get(url=fe_url).json()

        step_number = 1
        with allure.step(f'# {step_number}. Authorization platform one: Create Submission process.'):
            """
            Tender platform authorization for Create Submission process.
            As result get Tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

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
                payload = payload.build_payload()
            except ValueError:
                ValueError("Impossible to build payload for Create Submission process.")

            synchronous_result = create_submission_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                payload=payload,
                test_mode=True,
                cpid=cpid,
                ocid=ocid
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create Submission process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(CreateSubmissionMessage(
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
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")
            with allure.step(f'# {step_number}.3. Check AP release.'):
                """
                Compare previous AP release and actual AP release.
                """
                actual_ap_release = requests.get(url=ap_url).json()
                try:
                    """
                    Build expected AP release.
                    """
                    expected_release = copy.deepcopy(CreateSubmissionRelease())
                    expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
                except ValueError:
                    ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                  f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
                                  "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FE release.'):
                """
                Compare previous FE release and actual FE release.
                """
                actual_fe_release = requests.get(url=fe_url).json()
                try:
                    """
                    Build expected FE release.
                    """
                    expected_fe_release = expected_release.build_expected_fe_release(previous_fe_release)
                except ValueError:
                    ValueError("Impossible to build expected FE release.")

                with allure.step("Compare actual and expected FE release."):
                    allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                    allure.attach(json.dumps(expected_fe_release), "Expected FE release.")

                    assert actual_fe_release == expected_fe_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

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
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")
        try:
            """
            CLean up the database.
            """
            # Clean after Create Submission process:
            cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)

            cleanup_table_of_services_for_create_submission(
                connect_to_ocds, connect_to_access, connect_to_dossier, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")
