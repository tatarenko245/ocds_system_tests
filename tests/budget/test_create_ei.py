import copy
import json
import os

import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_table_of_services_for_expenditure_item, \
    cleanup_orchestrator_steps_by_cpid, get_cpid_from_orchestrator_steps
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.prepare_date import ei_period, old_period
from functions_collection.requests_collection import create_ei_process
from functions_collection.some_functions import get_affordable_currency
from messages_collection.budget.create_ei_message import ExpenditureItemMessage
from payloads_collection.budget.create_ei_payload import ExpenditureItemPayload
from releases_collection.budget.create_ei_release import ExpenditureItemRelease


@allure.parent_suite("Budget")
@allure.suite("Expenditure item")
@allure.severity("Critical")
@allure.testcase(url="https://docs.google.com/spreadsheets/d/1-I_7nLopu_q2wAyWzfTyscHMBL4GA1sIL6IpwBk-QCw/edit#gid=0",
                 name="Test Suite")
class TestCreateEI:
    @allure.title("Створення EI, повна модель.")
    def test_case_1(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00,
                    currency=currency)
                )

                payload.customize_tender_items(
                    quantity_of_items=1,
                    quantity_of_items_additional_classifications=1
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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_success_message()
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

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
                        environment, language, tender_classification_id
                    ))
                    expected_release = expected_release.build_expected_ei_release(
                        payload, actual_message, actual_release
                    )
                except ValueError:
                    ValueError("Impossible to build expected EI release.")

                with allure.step("Compare actual and expected releases."):
                    allure.attach(json.dumps(actual_release), "Actual release.")
                    allure.attach(json.dumps(expected_release), "Expected release.")

                    assert actual_release == expected_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Створення EI, опціональна модель, без айтемів.")
    def test_case_2(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00,
                    currency=currency)
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
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_success_message()
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

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
                        environment, language, tender_classification_id
                    ))
                    expected_release = expected_release.build_expected_ei_release(
                        payload, actual_message, actual_release
                    )
                except ValueError:
                    ValueError("Impossible to build expected EI release.")

                with allure.step("Compare actual and expected releases."):
                    allure.attach(json.dumps(actual_release), "Actual release.")
                    allure.attach(json.dumps(expected_release), "Expected release.")

                    assert actual_release == expected_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Створення EI, опціональна модель, з айтемами.")
    def test_case_3(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00,
                    currency=currency)
                )

                payload.customize_tender_items(
                    quantity_of_items=1, quantity_of_items_additional_classifications=1
                )

                payload.delete_optional_fields(
                    "tender.description",
                    "planning.rationale",
                    "buyer.identifier.uri",
                    "buyer.address.postalCode",
                    "buyer.additionalIdentifiers",
                    "buyer.contactPoint.faxNumber",
                    "buyer.contactPoint.url",
                    "buyer.details",
                    "tender.items.additionalClassifications",
                    "tender.items.deliveryAddress.streetAddress",
                    "tender.items.deliveryAddress.postalCode",
                    "tender.items.deliveryAddress.addressDetails.locality",
                    item_position=0, additional_classification_position=0
                )

                payload = payload.build_payload()
            except ValueError:
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_success_message()
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

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
                        environment, language, tender_classification_id
                    ))
                    expected_release = expected_release.build_expected_ei_release(
                        payload, actual_message, actual_release
                    )
                except ValueError:
                    ValueError("Impossible to build expected EI release.")

                with allure.step("Compare actual and expected releases."):
                    allure.attach(json.dumps(actual_release), "Actual release.")
                    allure.attach(json.dumps(expected_release), "Expected release.")

                    assert actual_release == expected_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Значення language не входить в перелік mdm.languages[*] для країни.")
    def test_case_4(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00,
                    currency=currency)
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
                ValueError("Impossible to build payload for Create EI process.")

            language = "QWERTY"

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.1/10",
                        error_description="The value of language in the request must be in the list of "
                                          "mdm.languages[*] values provided for the country from the request."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Значення planning.budget.period.endDate раніше planning.budget.period.startDate.")
    def test_case_5(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00,
                    currency=currency)
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

                period = ei_period()
                payload['planning']['budget']['period']['startDate'] = period[1]
                payload['planning']['budget']['period']['endDate'] = period[0]
            except ValueError:
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.2/10",
                        error_description="The planning.budget.period.endDate value from the request must be later "
                                          "than the planning.budget.period.startDate value in the request."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Значення planning.budget.period.endDate дорівнює planning.budget.period.startDate.")
    def test_case_6(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00,
                    currency=currency)
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

                period = ei_period()
                payload['planning']['budget']['period']['startDate'] = period[0]
                payload['planning']['budget']['period']['endDate'] = period[0]
            except ValueError:
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.2/10",
                        error_description="The planning.budget.period.endDate value from the request must be later "
                                          "than the planning.budget.period.startDate value in the request."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Значення planning.budget.period.endDate раніше date в запиті.")
    def test_case_7(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00,
                    currency=currency)
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

                correct_period = ei_period()
                incorrect_period = old_period()
                payload['planning']['budget']['period']['startDate'] = correct_period[0]
                payload['planning']['budget']['period']['endDate'] = incorrect_period[1]
            except ValueError:
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.2/10",
                        error_description="The planning.budget.period.endDate value from the request must be later "
                                          "than the planning.budget.period.startDate value in the request."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    country = os.getenv("COUNTRY")
    if country == "MD":
        @allure.title("Присутній planning.budget.amount, якщо країна = MD.")
        def test_case_8(self, get_parameters, connect_to_keyspace):

            environment = get_parameters[0]
            bpe_host = get_parameters[2]
            country = get_parameters[4]
            language = get_parameters[5]
            tender_classification_id = get_parameters[9]
            clean_up_database = get_parameters[10]

            connect_to_ocds = connect_to_keyspace[0]
            connect_to_orchestrator = connect_to_keyspace[1]

            currency = get_affordable_currency(country)

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
                        connect_to_ocds=connect_to_ocds,
                        country=country,
                        buyer_id=0,
                        tender_classification_id=tender_classification_id,
                        amount=100000.00,
                        currency=currency)
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
                    payload['planning']['budget']['amount'] = {
                        "amount": 100000.00,
                        "currency": currency
                    }
                except ValueError:
                    ValueError("Impossible to build payload for Create EI process.")

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
                            country=country,
                            actual_message=actual_message,
                            test_mode=True)
                        )

                        expected_message = expected_message.build_expected_failure_message(
                            error_code="VR.COM-14.1.4/10",
                            error_description="The planning.budget.amount in the request must be missing."
                        )
                    except ValueError:
                        ValueError("Impossible to build expected message for platform.")

                    with allure.step('Compare actual and expected message for platform.'):
                        allure.attach(json.dumps(actual_message), "Actual message.")
                        allure.attach(json.dumps(expected_message), "Expected message.")

                        cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                        assert actual_message == expected_message, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            if clean_up_database is True:
                try:
                    """
                    CLean up the database.
                    """
                    # Clean after Crate EI process:
                    cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                    cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
                except ValueError:
                    ValueError("Impossible to cLean up the database.")
            else:
                with allure.step("The steps of process."):
                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                  f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                  f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    elif country == "LT":
        @allure.title("Відсутній planning.budget.amount , якщо країна = LT.")
        def test_case_9(self, get_parameters, connect_to_keyspace):

            environment = get_parameters[0]
            bpe_host = get_parameters[2]
            country = get_parameters[4]
            language = get_parameters[5]
            tender_classification_id = get_parameters[9]
            clean_up_database = get_parameters[10]

            connect_to_ocds = connect_to_keyspace[0]
            connect_to_orchestrator = connect_to_keyspace[1]

            currency = get_affordable_currency(country)

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
                        connect_to_ocds=connect_to_ocds,
                        country=country,
                        buyer_id=0,
                        tender_classification_id=tender_classification_id,
                        amount=100000.00,
                        currency=currency)
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

                    del payload['planning']['budget']['amount']
                except ValueError:
                    ValueError("Impossible to build payload for Create EI process.")

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
                            country=country,
                            actual_message=actual_message,
                            test_mode=True)
                        )

                        expected_message = expected_message.build_expected_failure_message(
                            error_code="VR.COM-14.1.5/10",
                            error_description="There must be a planning.budget.amount in the request."
                        )
                    except ValueError:
                        ValueError("Impossible to build expected message for platform.")

                    with allure.step('Compare actual and expected message for platform.'):
                        allure.attach(json.dumps(actual_message), "Actual message.")
                        allure.attach(json.dumps(expected_message), "Expected message.")

                        cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                        assert actual_message == expected_message, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            if clean_up_database is True:
                try:
                    """
                    CLean up the database.
                    """
                    # Clean after Crate EI process:
                    cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                    cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
                except ValueError:
                    ValueError("Impossible to cLean up the database.")
            else:
                with allure.step("The steps of process."):
                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                  f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                  f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        @allure.title("Значення planning.budget.amount.amount = 0, якщо країна = LT.")
        def test_case_10(self, get_parameters, connect_to_keyspace):

            environment = get_parameters[0]
            bpe_host = get_parameters[2]
            country = get_parameters[4]
            language = get_parameters[5]
            tender_classification_id = get_parameters[9]
            clean_up_database = get_parameters[10]

            connect_to_ocds = connect_to_keyspace[0]
            connect_to_orchestrator = connect_to_keyspace[1]

            currency = get_affordable_currency(country)

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
                        connect_to_ocds=connect_to_ocds,
                        country=country,
                        buyer_id=0,
                        tender_classification_id=tender_classification_id,
                        amount=0,
                        currency=currency)
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
                    ValueError("Impossible to build payload for Create EI process.")

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
                            country=country,
                            actual_message=actual_message,
                            test_mode=True)
                        )

                        expected_message = expected_message.build_expected_failure_message(
                            error_code="VR.COM-14.1.6/10",
                            error_description="The planning.budget.amount.amount from the request must be "
                                              "greater than 0."
                        )
                    except ValueError:
                        ValueError("Impossible to build expected message for platform.")

                    with allure.step('Compare actual and expected message for platform.'):
                        allure.attach(json.dumps(actual_message), "Actual message.")
                        allure.attach(json.dumps(expected_message), "Expected message.")

                        cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                        assert actual_message == expected_message, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            if clean_up_database is True:
                try:
                    """
                    CLean up the database.
                    """
                    # Clean after Crate EI process:
                    cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                    cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
                except ValueError:
                    ValueError("Impossible to cLean up the database.")
            else:
                with allure.step("The steps of process."):
                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                  f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                  f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        @allure.title("Значення planning.budget.amount.currency не входить в перелік mdm.currencies[*] для країни, "
                      "якщо країна = LT.")
        def test_case_12(self, get_parameters, connect_to_keyspace):

            environment = get_parameters[0]
            bpe_host = get_parameters[2]
            country = get_parameters[4]
            language = get_parameters[5]
            tender_classification_id = get_parameters[9]
            clean_up_database = get_parameters[10]

            connect_to_ocds = connect_to_keyspace[0]
            connect_to_orchestrator = connect_to_keyspace[1]

            currency = "QWERTY"

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
                        connect_to_ocds=connect_to_ocds,
                        country=country,
                        buyer_id=0,
                        tender_classification_id=tender_classification_id,
                        amount=10000.00,
                        currency=currency)
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
                    ValueError("Impossible to build payload for Create EI process.")

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
                            country=country,
                            actual_message=actual_message,
                            test_mode=True)
                        )

                        expected_message = expected_message.build_expected_failure_message(
                            error_code="VR.COM-14.1.13/10",
                            error_description="The planning.budget.amount.currency value in the request must be "
                                              "in the list of mdm.currencies[*] values provided for the country "
                                              "from the request."
                        )
                    except ValueError:
                        ValueError("Impossible to build expected message for platform.")

                    with allure.step('Compare actual and expected message for platform.'):
                        allure.attach(json.dumps(actual_message), "Actual message.")
                        allure.attach(json.dumps(expected_message), "Expected message.")

                        cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                        assert actual_message == expected_message, \
                            allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                          f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                          f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            if clean_up_database is True:
                try:
                    """
                    CLean up the database.
                    """
                    # Clean after Crate EI process:
                    cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                    cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
                except ValueError:
                    ValueError("Impossible to cLean up the database.")
            else:
                with allure.step("The steps of process."):
                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                  f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                  f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Значення tender.classification.id повинно містити три знаки коду, "
                  "а інші знаки (з 4 по 8) не повинні дорівнювати 0.")
    def test_case_13(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = "98344444-6"
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=10000.00,
                    currency=currency)
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
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.7/10",
                        error_description="The tender.classification.id value from the request should only "
                                          "contain the first 3 characters in the code, and the remaining "
                                          "characters (4 through 8) in the code should be zero."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Ідентифікатор класифікатор tender.classification.id не співпадає за першими трьома знаками з "
                  "tender.items[*].classification.id.")
    def test_case_14(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=10000.00,
                    currency=currency)
                )

                payload.delete_optional_fields(
                    "tender.description",
                    "planning.rationale",
                    "buyer.identifier.uri",
                    "buyer.address.postalCode",
                    "buyer.additionalIdentifiers",
                    "buyer.contactPoint.faxNumber",
                    "buyer.contactPoint.url",
                    "buyer.details"
                )

                payload = payload.build_payload()

                tender_classification_id = tender_classification_id[:0] + "999" + tender_classification_id[3:]
                payload['tender']['classification']['id'] = tender_classification_id
            except ValueError:
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.8/10",
                        error_description="The qualifier identifier in tender.classification.id from the request "
                                          "must match the first 3 characters of each qualifier identifier in "
                                          "tender.items[*].classification.id."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Дубль ідентифікатора додаткового класифікатора айтема "
                  "(tender.items[*].additionalClassifications[*].id).")
    def test_case_15(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=10000.00,
                    currency=currency)
                )

                payload.delete_optional_fields(
                    "tender.description",
                    "planning.rationale",
                    "buyer.identifier.uri",
                    "buyer.address.postalCode",
                    "buyer.additionalIdentifiers",
                    "buyer.contactPoint.faxNumber",
                    "buyer.contactPoint.url",
                    "buyer.details"
                )

                payload.customize_tender_items(quantity_of_items=1, quantity_of_items_additional_classifications=2)
                payload = payload.build_payload()

                payload['tender']['items'][0]['additionalClassifications'][1]['id'] = \
                    payload['tender']['items'][0]['additionalClassifications'][0]['id']
            except ValueError:
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.9/10",
                        error_description="The identifier of each additional classifier must be unique within one "
                                          "item (tender.items[*].additionalClassifications[*].id) from the request."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Значення tender.items[*].quantity = 0.")
    def test_case_16(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=10000.00,
                    currency=currency)
                )
                payload.customize_tender_items(quantity_of_items=1, quantity_of_items_additional_classifications=0)

                payload.delete_optional_fields(
                    "tender.description",
                    "planning.rationale",
                    "buyer.identifier.uri",
                    "buyer.address.postalCode",
                    "buyer.additionalIdentifiers",
                    "buyer.contactPoint.faxNumber",
                    "buyer.contactPoint.url",
                    "buyer.details",
                    "tender.items.additionalClassifications",
                    item_position=0
                )

                payload = payload.build_payload()

                payload['tender']['items'][0]['quantity'] = 0
            except ValueError:
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.10/10",
                        error_description="The value of each tender.items[*].quantity in the request "
                                          "must be greater than 0."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Дубль ідентифікатора додаткового класифікатора організації (buyer.additionalIdentifiers.id).")
    def test_case_18(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=10000.00,
                    currency=currency)
                )

                payload.delete_optional_fields(
                    "tender.description",
                    "planning.rationale",
                    "buyer.identifier.uri",
                    "buyer.address.postalCode",
                    "buyer.contactPoint.faxNumber",
                    "buyer.contactPoint.url",
                    "buyer.details",
                    "tender.items"

                )

                payload.customize_buyer_additional_identifiers(quantity_of_buyer_additional_identifiers=2)
                payload = payload.build_payload()

                payload['buyer']['additionalIdentifiers'][1]['id'] = payload['buyer']['additionalIdentifiers'][0]['id']
            except ValueError:
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.11/10",
                        error_description="The identifier of each additional organization classifier "
                                          "(buyer.additionalIdentifiers.id) from the request must be unique."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Значення buyer.identifier.scheme для країни організації (buyer.address.addressDetails.country.id) "
                  "не входить в перелік mdm.registrationSchemes[*].schemes[*] для країни.")
    def test_case_19(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=10000.00,
                    currency=currency)
                )

                payload.delete_optional_fields(
                    "tender.description",
                    "planning.rationale",
                    "buyer.identifier.uri",
                    "buyer.additionalIdentifiers",
                    "buyer.address.postalCode",
                    "buyer.contactPoint.faxNumber",
                    "buyer.contactPoint.url",
                    "buyer.details",
                    "tender.items"
                )

                payload = payload.build_payload()

                payload['buyer']['identifier']['scheme'] = "other"
            except ValueError:
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.12/10",
                        error_description="The value of buyer.identifier.scheme for the organization's country "
                                          "(buyer.address.addressDetails.country.id) from the request must be "
                                          "included in the list of mdm.registrationSchemes[*].schemes[*] values "
                                          "provided for the same country in the request."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Дубль айтема (tender.items[*].id).")
    def test_case_20(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        currency = get_affordable_currency(country)

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
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    buyer_id=0,
                    tender_classification_id=tender_classification_id,
                    amount=10000.00,
                    currency=currency)
                )

                payload.delete_optional_fields(
                    "tender.description",
                    "planning.rationale",
                    "buyer.identifier.uri",
                    "buyer.additionalIdentifiers",
                    "buyer.address.postalCode",
                    "buyer.contactPoint.faxNumber",
                    "buyer.contactPoint.url",
                    "buyer.details"
                )

                payload.customize_tender_items(
                    quantity_of_items=2,
                    quantity_of_items_additional_classifications=1
                )

                payload = payload.build_payload()
                payload['tender']['items'][1]['id'] = payload['tender']['items'][0]['id']

            except ValueError:
                ValueError("Impossible to build payload for Create EI process.")

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
                        country=country,
                        actual_message=actual_message,
                        test_mode=True)
                    )

                    expected_message = expected_message.build_expected_failure_message(
                        error_code="VR.COM-14.1.14/10",
                        error_description="The identifier of each item (tender.items[*].id) from the "
                                          "request must be unique. Duplicated id '0'."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

                    cpid = get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id)

                    assert actual_message == expected_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        if clean_up_database is True:
            try:
                """
                CLean up the database.
                """
                # Clean after Crate EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
