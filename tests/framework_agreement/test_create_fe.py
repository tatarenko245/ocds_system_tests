import copy
import json
import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from class_collection.prepare_criteria_array import CriteriaArray
from functions_collection.cassandra_methods import get_process_id_by_operation_id, \
    cleanup_ocds_orchestrator_operation_step_by_operation_id, get_parameter_from_clarification_rules, \
    cleanup_table_of_services_for_framework_establishment
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.mdm_methods import get_standard_criteria
from functions_collection.requests_collection import create_fe_process
from messages_collection.framework_agreement.create_fe_message import FrameworkEstablishmentMessage
from payloads_collection.framework_agreement.create_fe_payload import FrameworkEstablishmentPayload
from releases_collection.framework_agreement.create_fe_release import CreateFrameworkEstablishmentRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Framework Establishment")
@allure.severity("Critical")
@allure.testcase(url="https://docs.google.com/spreadsheets/d/1taw-E-4lryj80XYGdVwi1G-C2U6SQyilBuziGjXGyME/edit#gid=0",
                 name="Why this test case was fall down?")
class TestCreateFE:
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace, update_ap_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]
        pmd = get_parameters[6]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_access = connect_to_keyspace[2]
        connect_to_clarification = connect_to_keyspace[3]
        connect_to_dossier = connect_to_keyspace[4]

        cpid = update_ap_tc_1[0]
        ocid = update_ap_tc_1[1]
        token = update_ap_tc_1[2]
        create_ap_payload = update_ap_tc_1[3]
        ap_url = update_ap_tc_1[4]
        fa_url = update_ap_tc_1[5]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()

        step_number = 1
        with allure.step(f'# {step_number}. Authorization platform one: Create FE process.'):
            """
            Tender platform authorization for Create FE process.
            As result get Tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

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
                    ap_payload=create_ap_payload,
                    host_to_service=service_host,
                    country=country,
                    language=language,
                    environment=environment)
                )
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

                payload = payload.build_payload()
            except ValueError:
                ValueError("Impossible to build payload for Create FE process.")

            synchronous_result = create_fe_process(
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
            fe_ocid = message['data']['outcomes']['fe'][0]['id']
            fe_url = f"{message['data']['url']}/{fe_ocid}"
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create FE process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(FrameworkEstablishmentMessage(
                        environment=environment,
                        actual_message=actual_message,
                        test_mode=True
                    ))

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

            with allure.step(f'# {step_number}.3. Check AP release.'):
                """
                Compare previous AP release and actual AP release.
                """
                actual_ap_release = requests.get(url=ap_url).json()
                actual_fa_release = requests.get(url=fa_url).json()
                actual_fe_release = requests.get(url=fe_url).json()

                try:
                    """
                    Build expected AP release.
                    """
                    expected_release = copy.deepcopy(CreateFrameworkEstablishmentRelease(
                        environment,
                        service_host,
                        country,
                        language,
                        pmd,
                        cpid,
                        ocid,
                        fe_ocid,
                        payload,
                        actual_message,
                        previous_ap_release,
                        actual_ap_release,
                        actual_fe_release,
                        previous_fa_release,
                        actual_fa_release
                    ))

                    expected_ap_release = expected_release.build_expected_ap_release()
                except ValueError:
                    ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    process_id = get_process_id_by_operation_id(connect_to_ocds, operation_id)

                    assert actual_ap_release == expected_ap_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FE release.'):
                """
                Compare previous FE release and actual FE release.
                """
                try:
                    """
                    Build expected FE release.
                    """
                    period_shift = get_parameter_from_clarification_rules(
                        connect_to_clarification, country, pmd, "all", "period_shift")

                    expected_fe_release = expected_release.build_expected_fe_release(period_shift)
                except ValueError:
                    ValueError("Impossible to build expected FE release.")

                with allure.step("Compare actual and expected FE release."):
                    allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                    allure.attach(json.dumps(expected_fe_release), "Expected FE release.")

                    assert actual_fe_release == expected_fe_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FA release.'):
                """
                Compare previous FA release and actual FA release.
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
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

        try:
            """
            CLean up the database.
            """
            # Clean after Framework Establishment process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)

            cleanup_table_of_services_for_framework_establishment(
                connect_to_ocds, connect_to_access, connect_to_clarification, connect_to_dossier, cpid
            )
        except ValueError:
            ValueError("Impossible to cLean up the database.")

    @allure.title("Check records: based on required data model.")
    def test_case_2(self, get_parameters, connect_to_keyspace, update_ap_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]
        pmd = get_parameters[6]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_access = connect_to_keyspace[2]
        connect_to_clarification = connect_to_keyspace[3]
        connect_to_dossier = connect_to_keyspace[4]

        cpid = update_ap_tc_2[0]
        ocid = update_ap_tc_2[1]
        token = update_ap_tc_2[2]
        create_ap_payload = update_ap_tc_2[3]
        ap_url = update_ap_tc_2[4]
        fa_url = update_ap_tc_2[5]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()

        step_number = 1
        with allure.step(f'# {step_number}. Authorization platform one: Create FE process.'):
            """
            Tender platform authorization for Create FE process.
            As result get Tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

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
                    ap_payload=create_ap_payload,
                    host_to_service=service_host,
                    country=country,
                    language=language,
                    environment=environment)
                )
                payload.delete_optional_fields(
                    "tender.secondStage",
                    "tender.procurementMethodModalities",
                    "tender.procurementMethodRationale",
                    "tender.procuringEntity",
                    "tender.criteria",
                    "tender.documents"
                )
                payload = payload.build_payload()
            except ValueError:
                ValueError("Impossible to build payload for Create FE process.")

            synchronous_result = create_fe_process(
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
            fe_ocid = message['data']['outcomes']['fe'][0]['id']
            fe_url = f"{message['data']['url']}/{fe_ocid}"
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create FE process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(FrameworkEstablishmentMessage(
                        environment=environment,
                        actual_message=actual_message,
                        test_mode=True
                    ))

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

            with allure.step(f'# {step_number}.3. Check AP release.'):
                """
                Compare previous AP release and actual AP release.
                """
                actual_ap_release = requests.get(url=ap_url).json()
                actual_fa_release = requests.get(url=fa_url).json()
                actual_fe_release = requests.get(url=fe_url).json()

                try:
                    """
                    Build expected AP release.
                    """
                    expected_release = copy.deepcopy(CreateFrameworkEstablishmentRelease(
                        environment,
                        service_host,
                        country,
                        language,
                        pmd,
                        cpid,
                        ocid,
                        fe_ocid,
                        payload,
                        actual_message,
                        previous_ap_release,
                        actual_ap_release,
                        actual_fe_release,
                        previous_fa_release,
                        actual_fa_release
                    ))

                    expected_ap_release = expected_release.build_expected_ap_release()
                except ValueError:
                    ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    process_id = get_process_id_by_operation_id(connect_to_ocds, operation_id)

                    assert actual_ap_release == expected_ap_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FE release.'):
                """
                Compare previous FE release and actual FE release.
                """
                try:
                    """
                    Build expected FE release.
                    """
                    period_shift = get_parameter_from_clarification_rules(
                        connect_to_clarification, country, pmd, "all", "period_shift")

                    expected_fe_release = expected_release.build_expected_fe_release(period_shift)
                except ValueError:
                    ValueError("Impossible to build expected FE release.")

                with allure.step("Compare actual and expected FE release."):
                    allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                    allure.attach(json.dumps(expected_fe_release), "Expected FE release.")

                    assert actual_fe_release == expected_fe_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FA release.'):
                """
                Compare previous FA release and actual FA release.
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
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

        try:
            """
            CLean up the database.
            """
            # Clean after Framework Establishment process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)

            cleanup_table_of_services_for_framework_establishment(
                connect_to_ocds, connect_to_access, connect_to_clarification, connect_to_dossier, cpid
            )
        except ValueError:
            ValueError("Impossible to cLean up the database.")
