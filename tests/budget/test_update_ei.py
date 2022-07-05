import copy
import json
import os
import uuid

import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_table_of_services_for_expenditure_item, \
    cleanup_orchestrator_steps_by_cpid, get_some_parameter_from_orchestrator_steps_by_cpid_and_operationid, \
    set_tender_status_for_ocds_budgetei
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import update_ei_process
from functions_collection.some_functions import get_affordable_currency
from messages_collection.budget.update_ei_message import ExpenditureItemMessage
from payloads_collection.budget.update_ei_payload import ExpenditureItemPayload
from releases_collection.budget.update_ei_release import ExpenditureItemRelease


@allure.parent_suite("Budget")
@allure.suite("Expenditure item")
@allure.severity("Critical")
@allure.testcase(url="https://docs.google.com/spreadsheets/d/1-I_7nLopu_q2wAyWzfTyscHMBL4GA1sIL6IpwBk-QCw/"
                     "edit#gid=109394188",
                 name="Test Suite")
class TestUpdateEI:
    @allure.title("Оновлення EI (додавання даних).")
    def test_case_1(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_2[1]
        ei_url = create_ei_tc_2[3]
        token = create_ei_tc_2[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                payload.add_new_tender_items(
                    quantity_of_items=1,
                    quantity_of_new_additional_classifications=1
                )

                payload.delete_optional_fields(
                    "tender.title"
                )
                payload = payload.build_payload()
            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Update EI process.'):
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
                        payload, actual_message, actual_release, previous_ei_release
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
                # Clean after Update EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;",    "Cassandra DataBase: steps of process.")

    @allure.title("Оновлення EI (редагування даних).")
    def test_case_2(self, get_parameters, connect_to_keyspace, create_ei_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_1[1]
        ei_url = create_ei_tc_1[3]
        token = create_ei_tc_1[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=0.99)
                )

                payload.update_old_tender_items(
                    previous_ei_release['releases'][0]['tender']['items'][0]['id'],
                    previous_items_list=previous_ei_release['releases'][0]['tender']['items'],
                    quantity_of_new_additional_classifications=1
                )
                payload = payload.build_payload()
            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Update EI process.'):
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
                        payload, actual_message, actual_release, previous_ei_release
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
                # Clean after Update EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Оновлення EI, (додавання об'єктів).")
    def test_case_3(self, get_parameters, connect_to_keyspace, create_ei_tc_3):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_3[1]
        ei_url = create_ei_tc_3[3]
        token = create_ei_tc_3[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                payload.update_old_tender_items(
                    previous_ei_release['releases'][0]['tender']['items'][0]['id'],
                    previous_items_list=previous_ei_release['releases'][0]['tender']['items'],
                    quantity_of_new_additional_classifications=1
                )

                payload.delete_optional_fields(
                    "planning",
                    "tender.description",
                    f"tender.items[{0}].title",
                    f"tender.items[{0}].deliveryAddress.streetAddress",
                    f"tender.items[{0}].deliveryAddress.postalCode",
                    f"tender.items[{0}].deliveryAddress.addressDetails.locality",
                )

                payload.add_new_tender_items(
                    quantity_of_items=1,
                    quantity_of_new_additional_classifications=1
                )
                payload = payload.build_payload()

                payload['tender']['title'] = previous_ei_release['releases'][0]['tender']['title']

                payload['tender']['items'][0]['description'] = previous_ei_release['releases'][0]['tender'][
                    'items'][0]['description']

                payload['tender']['items'][0]['quantity'] = previous_ei_release['releases'][0]['tender'][
                    'items'][0]['quantity']

                payload['tender']['items'][0]['unit']['id'] = previous_ei_release['releases'][0]['tender'][
                    'items'][0]['unit']['id']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['country']['id']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['country']['scheme']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['country']['description']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['region']['id']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['region']['scheme']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['description'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['region']['description']

            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Update EI process.'):
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
                        payload, actual_message, actual_release, previous_ei_release
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
                # Clean after Update EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Оновлення EI на опціональних даних (без айтемів).")
    def test_case_4(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_2[1]
        ei_url = create_ei_tc_2[3]
        token = create_ei_tc_2[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                # "tender.items" attribute was delete by default
                payload.delete_optional_fields(
                    "planning",
                    "tender.description"
                )
                payload = payload.build_payload()
            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Update EI process.'):
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
                        payload, actual_message, actual_release, previous_ei_release
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
                # Clean after Update EI process:
                cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
                cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
            except ValueError:
                ValueError("Impossible to cLean up the database.")
        else:
            with allure.step("The steps of process."):
                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

    @allure.title("Оновлення EI на опціональних даних (із айтемами).")
    def test_case_5(self, get_parameters, connect_to_keyspace, create_ei_tc_3):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        language = get_parameters[5]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_3[1]
        ei_url = create_ei_tc_3[3]
        token = create_ei_tc_3[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                payload.update_old_tender_items(
                    previous_ei_release['releases'][0]['tender']['items'][0]['id'],
                    previous_items_list=previous_ei_release['releases'][0]['tender']['items'],
                    quantity_of_new_additional_classifications=1
                )

                payload.delete_optional_fields(
                    "planning",
                    "tender.description",
                    f"tender.items[{0}].title",
                    f"tender.items[{0}].additionalClassifications",
                    f"tender.items[{0}].deliveryAddress.streetAddress",
                    f"tender.items[{0}].deliveryAddress.postalCode",
                    f"tender.items[{0}].deliveryAddress.addressDetails.locality",
                )

                payload = payload.build_payload()

                payload['tender']['items'][0]['description'] = previous_ei_release['releases'][0]['tender'][
                    'items'][0]['description']

                payload['tender']['items'][0]['quantity'] = previous_ei_release['releases'][0]['tender'][
                    'items'][0]['quantity']

                payload['tender']['items'][0]['unit']['id'] = previous_ei_release['releases'][0]['tender'][
                    'items'][0]['unit']['id']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['country']['id']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['country']['scheme']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['description'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['country']['description']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['region']['id']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['region']['scheme']

                payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['description'] = \
                    previous_ei_release['releases'][0]['tender']['items'][0]['deliveryAddress'][
                        'addressDetails']['region']['description']

            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Update EI process.'):
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
                        payload, actual_message, actual_release, previous_ei_release
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
                # Clean after Update EI process:
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
        @allure.title("Присутній planning.budget.amount.")
        def test_case_6(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

            environment = get_parameters[0]
            bpe_host = get_parameters[2]
            country = get_parameters[4]
            tender_classification_id = get_parameters[9]
            clean_up_database = get_parameters[10]

            connect_to_ocds = connect_to_keyspace[0]
            connect_to_orchestrator = connect_to_keyspace[1]

            cpid = create_ei_tc_2[1]
            ei_url = create_ei_tc_2[3]
            token = create_ei_tc_2[4]
            previous_ei_release = requests.get(ei_url).json()

            """
            VR.COM-14.9.2: Check EI state.
            """
            if previous_ei_release['releases'][0]['tender']['status'] == "planning":
                pass
            else:
                raise ValueError(f"The EI release has invalid state: "
                                 f"{previous_ei_release['releases'][0]['tender']['status']}.")

            step_number = 1
            with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
                """
                Tender platform authorization for Update EI process.
                As result, get tender platform's access token and process operation-id.
                """
                platform_one = PlatformAuthorization(bpe_host)
                access_token = platform_one.get_access_token_for_platform_one()
                operation_id = platform_one.get_x_operation_id(access_token)

            step_number += 1
            with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
                """
                Send api request to BPE host to create a Update EI process.
                And save in variable cpid.
                """
                try:
                    """
                    Build payload for Update EI process.
                    """
                    payload = copy.deepcopy(ExpenditureItemPayload(
                        connect_to_ocds=connect_to_ocds,
                        country=country,
                        tender_classification_id=tender_classification_id,
                        amount=100000.00)
                    )

                    # "tender.items" attribute was delete by default
                    payload = payload.build_payload()

                    payload['planning']['budget'] = dict()
                    payload['planning']['budget'].update(
                        {
                            "amount": {
                                "amount": 100000.00,
                                "currency": get_affordable_currency(country)
                            }
                        }
                    )

                except ValueError:
                    raise ValueError("Impossible to build payload for Update EI process.")

                synchronous_result = update_ei_process(
                    host=bpe_host,
                    access_token=access_token,
                    x_operation_id=operation_id,
                    cpid=cpid,
                    token=token,
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
                            error_code="VR.COM-14.10.2/10",
                            error_description="The planning.budget.amount in the request must be missing."
                        )
                    except ValueError:
                        ValueError("Impossible to build expected message for platform.")

                    with allure.step('Compare actual and expected message for platform.'):
                        allure.attach(json.dumps(actual_message), "Actual message.")
                        allure.attach(json.dumps(expected_message), "Expected message.")

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
        @allure.title("Значення planning.budget.amount.amount = 0, якщо країна = LT.")
        def test_case_7(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

            environment = get_parameters[0]
            bpe_host = get_parameters[2]
            country = get_parameters[4]
            tender_classification_id = get_parameters[9]
            clean_up_database = get_parameters[10]

            connect_to_ocds = connect_to_keyspace[0]
            connect_to_orchestrator = connect_to_keyspace[1]

            cpid = create_ei_tc_2[1]
            ei_url = create_ei_tc_2[3]
            token = create_ei_tc_2[4]
            previous_ei_release = requests.get(ei_url).json()

            """
            VR.COM-14.9.2: Check EI state.
            """
            if previous_ei_release['releases'][0]['tender']['status'] == "planning":
                pass
            else:
                raise ValueError(f"The EI release has invalid state: "
                                 f"{previous_ei_release['releases'][0]['tender']['status']}.")

            step_number = 1
            with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
                """
                Tender platform authorization for Update EI process.
                As result, get tender platform's access token and process operation-id.
                """
                platform_one = PlatformAuthorization(bpe_host)
                access_token = platform_one.get_access_token_for_platform_one()
                operation_id = platform_one.get_x_operation_id(access_token)

            step_number += 1
            with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
                """
                Send api request to BPE host to create a Update EI process.
                And save in variable cpid.
                """
                try:
                    """
                    Build payload for Update EI process.
                    """
                    payload = copy.deepcopy(ExpenditureItemPayload(
                        connect_to_ocds=connect_to_ocds,
                        country=country,
                        tender_classification_id=tender_classification_id,
                        amount=0)
                    )

                    # "tender.items" attribute was delete by default
                    payload = payload.build_payload()

                except ValueError:
                    raise ValueError("Impossible to build payload for Update EI process.")

                synchronous_result = update_ei_process(
                    host=bpe_host,
                    access_token=access_token,
                    x_operation_id=operation_id,
                    cpid=cpid,
                    token=token,
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
                            error_code="VR.COM-14.10.3/10",
                            error_description="The planning.budget.amount.amount from the request must be "
                                              "greater than 0."
                        )
                    except ValueError:
                        ValueError("Impossible to build expected message for platform.")

                    with allure.step('Compare actual and expected message for platform.'):
                        allure.attach(json.dumps(actual_message), "Actual message.")
                        allure.attach(json.dumps(expected_message), "Expected message.")

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

    @allure.title("Дубль ідентифікатора айтема.")
    def test_case_9(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_2[1]
        ei_url = create_ei_tc_2[3]
        token = create_ei_tc_2[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                payload.add_new_tender_items(
                    quantity_of_items=2,
                    quantity_of_new_additional_classifications=1
                )

                payload = payload.build_payload()

                payload['tender']['items'][1]['id'] = payload['tender']['items'][0]['id']
            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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
                        error_code="VR.COM-14.10.4/10",
                        error_description="The identifier of each item (tender.items[*].id) from the "
                                          "request must be unique."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

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

    @allure.title("Ідентифікатор класифікатор tender.classification.id не співпадає "
                  "за першими трьома знаками з tender.items[*].classification.id.")
    def test_case_10(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_2[1]
        ei_url = create_ei_tc_2[3]
        token = create_ei_tc_2[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                payload.add_new_tender_items(
                    quantity_of_items=1,
                    quantity_of_new_additional_classifications=1
                )

                payload = payload.build_payload()

                payload['tender']['items'][0]['classification']['id'] = "98344444-6"
            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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
                        error_code="VR.COM-14.10.6/10",
                        error_description="The qualifier identifier in tender.items[*].classification.id from "
                                          "the request must match the first 3 characters of the qualifier "
                                          "identifier in tender.classification.id in the service."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

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
                  "(tender.items[*].additionalClassifications[*].id) ")
    def test_case_11(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_2[1]
        ei_url = create_ei_tc_2[3]
        token = create_ei_tc_2[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                payload.add_new_tender_items(
                    quantity_of_items=1,
                    quantity_of_new_additional_classifications=2
                )

                payload = payload.build_payload()

                payload['tender']['items'][0]['additionalClassifications'][1]['id'] = \
                    payload['tender']['items'][0]['additionalClassifications'][0]['id']

            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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
                        error_code="VR.COM-14.10.5/10",
                        error_description="The identifier of each additional classifier must be unique within "
                                          "one item (tender.items[*].additionalClassifications[*].id) from the request."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

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
    def test_case_12(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_2[1]
        ei_url = create_ei_tc_2[3]
        token = create_ei_tc_2[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                payload.add_new_tender_items(
                    quantity_of_items=1,
                    quantity_of_new_additional_classifications=1
                )

                payload = payload.build_payload()

                payload['tender']['items'][0]['quantity'] = 0

            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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
                        error_code="VR.COM-14.10.7/10",
                        error_description="The value of tender.items[*].quantity in the request must be greater than 0."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

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

    @allure.title("Значення tender.items[*].quantity < 0.")
    def test_case_13(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_2[1]
        ei_url = create_ei_tc_2[3]
        token = create_ei_tc_2[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                payload.add_new_tender_items(
                    quantity_of_items=1,
                    quantity_of_new_additional_classifications=1
                )

                payload = payload.build_payload()

                payload['tender']['items'][0]['quantity'] = (-2)

            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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
                        error_code="RQ-4.2/1",
                        error_description="An error of parsing payload."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

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

    @allure.title("Некоректний токен в БД (не відповідає токену створеного EI).")
    def test_case_14(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_2[1]
        ei_url = create_ei_tc_2[3]
        token = str(uuid.uuid4())
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                # "tender.items" attribute was delete by default
                payload = payload.build_payload()

            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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
                        error_code="VR.COM-14.8.2/10",
                        error_description="The token value from the request must match the token value of "
                                          "the EI service."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

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

    @allure.title("Некоректний власник EI (не відповідає власнику створеного EI).")
    def test_case_15(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_2[1]
        ei_url = create_ei_tc_2[3]
        token = create_ei_tc_2[4]
        previous_ei_release = requests.get(ei_url).json()

        """
        VR.COM-14.9.2: Check EI state.
        """
        if previous_ei_release['releases'][0]['tender']['status'] == "planning":
            pass
        else:
            raise ValueError(f"The EI release has invalid state: "
                             f"{previous_ei_release['releases'][0]['tender']['status']}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_two()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                payload.add_new_tender_items(
                    quantity_of_items=1,
                    quantity_of_new_additional_classifications=1
                )

                # "tender.items" attribute was delete by default
                payload = payload.build_payload()

            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
                payload=payload,
                test_mode=True
            )
            data_from_orchestrator_steps = get_some_parameter_from_orchestrator_steps_by_cpid_and_operationid(
                connect_to_orchestrator, cpid, operation_id, "BudgetCheckAccessToEITask"
            )
            message = data_from_orchestrator_steps[1]
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
                actual_message = message['result']

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
                        error_code="VR.COM-14.8.3/10",
                        error_description="The owner value from the request must match the owner value of "
                                          "the EI service."
                    )

                    expected_message = expected_message['errors']

                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

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

    @allure.title("Невалідний статус для оновлення EI (статус не = х, х - validEIStates).")
    def test_case_16(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        tender_classification_id = get_parameters[9]
        clean_up_database = get_parameters[10]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]

        cpid = create_ei_tc_2[1]
        token = create_ei_tc_2[4]

        set_tender_status_for_ocds_budgetei(connect_to_ocds, cpid, "planned")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Update EI process."):
            """
            Tender platform authorization for Update EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Update EI process."):
            """
            Send api request to BPE host to create a Update EI process.
            And save in variable cpid.
            """
            try:
                """
                Build payload for Update EI process.
                """
                payload = copy.deepcopy(ExpenditureItemPayload(
                    connect_to_ocds=connect_to_ocds,
                    country=country,
                    tender_classification_id=tender_classification_id,
                    amount=100000.00)
                )

                # "tender.items" attribute was delete by default
                payload = payload.build_payload()

            except ValueError:
                raise ValueError("Impossible to build payload for Update EI process.")

            synchronous_result = update_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                token=token,
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
                        error_code="VR.COM-14.9.2/10",
                        error_description=f"The EI record with '{cpid}' has invalid state."
                    )
                except ValueError:
                    ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message), "Actual message.")
                    allure.attach(json.dumps(expected_message), "Expected message.")

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
#
