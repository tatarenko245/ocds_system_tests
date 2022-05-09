import copy
import json
import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import get_process_id_by_operation_id, \
    cleanup_table_of_services_for_expenditure_item, cleanup_ocds_orchestrator_operation_step_by_operation_id
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_ei_process
from messages_collection.budget.create_ei_message import ExpenditureItemMessage
from payloads_collection.budget.create_ei_payload import ExpenditureItemPayload
from releases_collection.budget.create_ei_release import ExpenditureItemRelease


@allure.parent_suite("Budget")
@allure.suite("Expenditure item")
@allure.severity("Critical")
@allure.testcase(url="")
class TestCreateEI:
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]

        connect_to_ocds = connect_to_keyspace[0]

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Create EI process."):
            """
            Tender platform authorization for Create EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Create EI process."):
            """
            Send api request to BPE host to create a CreateEi process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Create EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    buyer_id=0,
                    tender_classification_id=tender_classification_id)
                )

                payload.customize_tender_items(
                    quantity_of_items=3,
                    quantity_of_items_additional_classifications=3
                )
                payload = payload.build_payload()
            except ValueError:
                raise ValueError("Impossible to build payload for Create EI process.")

            synchronous_result = create_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                country=country,
                language=language,
                payload=payload,
                test_mode=True
            )
            message = get_message_for_platform(operation_id)
            cpid = message['data']['ocid']
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create EI process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(ExpenditureItemMessage(
                        environment=environment,
                        actual_message=actual_message,
                        test_mode=True)
                    )

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

            with allure.step(f'# {step_number}.3. Check EI release.'):
                """
                Compare actual EI release and expected EI release.
                """
                url = f"{actual_message['data']['url']}/{cpid}"
                actual_release = requests.get(url=url).json()

                try:
                    """
                    Build expected EI release.
                    """
                    expected_release = copy.deepcopy(ExpenditureItemRelease(
                        environment=environment,
                        host_to_service=service_host,
                        language=language,
                        ei_payload=payload,
                        ei_message=actual_message,
                        actual_ei_release=actual_release,
                        tender_classification_id=tender_classification_id
                    ))
                    expected_release = expected_release.build_expected_ei_release()
                except ValueError:
                    raise ValueError("Impossible to build expected EI release.")

                with allure.step("Compare actual and expected releases."):
                    allure.attach(json.dumps(actual_release), "Actual release.")
                    allure.attach(json.dumps(expected_release), "Expected release.")

                    assert actual_release == expected_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")
        try:
            """
            CLean up the database.
            """
            # Clean after Crate EI process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
        except ValueError:
            raise ValueError("Impossible to cLean up the database.")

    @allure.title("Check records: based on required data model.")
    def test_case_2(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]

        connect_to_ocds = connect_to_keyspace[0]

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Create EI process."):
            """
            Tender platform authorization for Create EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Create EI process."):
            """
            Send api request to BPE host to create a CreateEi process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Create EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    buyer_id=0,
                    tender_classification_id=tender_classification_id)
                )

                payload.delete_optional_fields(
                    "tender.description",
                    "tender.items",
                    "planning.rationale",
                    "buyer.identifier.uri",
                    "buyer.address.postalCode",
                    "buyer.additionalIdentifiers",
                    "buyer.contactPoint.faxNumber",
                    "buyer.contactPoint.url",
                    "buyer.details"
                )

                payload = payload.build_payload()
            except ValueError:
                raise ValueError("Impossible to build payload for Create EI process.")

            synchronous_result = create_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                country=country,
                language=language,
                payload=payload,
                test_mode=True
            )
            message = get_message_for_platform(operation_id)
            cpid = message['data']['ocid']
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create EI process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(ExpenditureItemMessage(
                        environment=environment,
                        actual_message=actual_message,
                        test_mode=True)
                    )

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

            with allure.step(f'# {step_number}.3. Check EI release.'):
                """
                Compare actual EI release and expected EI release.
                """
                url = f"{actual_message['data']['url']}/{cpid}"
                actual_release = requests.get(url=url).json()

                try:
                    """
                    Build expected EI release.
                    """
                    expected_release = copy.deepcopy(ExpenditureItemRelease(
                        environment=environment,
                        host_to_service=service_host,
                        language=language,
                        ei_payload=payload,
                        ei_message=actual_message,
                        actual_ei_release=actual_release,
                        tender_classification_id=tender_classification_id
                    ))
                    expected_release = expected_release.build_expected_ei_release()
                except ValueError:
                    raise ValueError("Impossible to build expected EI release.")

                with allure.step("Compare actual and expected releases."):
                    allure.attach(json.dumps(actual_release), "Actual release.")
                    allure.attach(json.dumps(expected_release), "Expected release.")

                    assert actual_release == expected_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")
        try:
            """
            CLean up the database.
            """
            # Clean after Crate EI process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
        except ValueError:
            raise ValueError("Impossible to cLean up the database.")