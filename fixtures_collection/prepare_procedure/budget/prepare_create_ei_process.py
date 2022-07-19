import copy
import random

import pytest as pytest
import allure

from class_collection.platform_authorization import PlatformAuthorization
from data_collection.data_constant import currency_tuple
from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid, \
    cleanup_table_of_services_for_expenditure_item
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_ei_process
from functions_collection.some_functions import get_affordable_schemes
from payloads_collection.budget.create_ei_payload import CreateExpenditureItemPayload


@pytest.fixture(scope="function")
# Create EI: Створення EI, повна модель
def create_ei_tc_1(get_parameters, connect_to_keyspace):
    bpe_host = get_parameters[2]
    country = get_parameters[4]
    language = get_parameters[5]
    tender_classification_id = get_parameters[9]
    clean_up_database = get_parameters[10]

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_orchestrator = connect_to_keyspace[1]

    currency = f"{random.choice(currency_tuple)}"

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
        Send request to BPE host to create a Create EI process.
        And save in variable cpid.
        """
        try:
            """
            Build payload for Create EI process.
            """
            affordable_schemes = get_affordable_schemes(country)
            buyer_id = 0
            buyer_scheme = affordable_schemes[0]

            payload = copy.deepcopy(CreateExpenditureItemPayload(
                connect_to_ocds=connect_to_ocds,
                country=country,
                buyer_id=buyer_id,
                tender_classification_id=tender_classification_id,
                amount=100000.00,
                currency=currency,
                buyer_scheme=buyer_scheme)
            )

            payload.customize_tender_items(
                quantity_of_items=1,
                quantity_of_items_additional_classifications=1
            )
            payload = payload.build_payload()
        except ValueError:
            raise ValueError("Impossible to build payload for Create EI process.")

        create_ei_process(
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
        token = message['data']['outcomes']['ei'][0]['X-TOKEN']
        ei_url = f"{message['data']['url']}/{cpid}"
        allure.attach(str(message), "Message for platform.")

        yield payload, cpid, message, ei_url, token, currency, buyer_id, buyer_scheme

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


@pytest.fixture(scope="function")
# Create EI: Створення EI, опціональна модель, без айтемів
def create_ei_tc_2(get_parameters, connect_to_keyspace):
    bpe_host = get_parameters[2]
    country = get_parameters[4]
    language = get_parameters[5]
    tender_classification_id = get_parameters[9]
    clean_up_database = get_parameters[10]

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_orchestrator = connect_to_keyspace[1]

    currency = f"{random.choice(currency_tuple)}"

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
        Send request to BPE host to create a Create EI process.
        And save in variable cpid.
        """

        try:
            """
            Build payload for Create EI process.
            """
            affordable_schemes = get_affordable_schemes(country)
            buyer_id = 0
            buyer_scheme = affordable_schemes[0]

            payload = copy.deepcopy(CreateExpenditureItemPayload(
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

        create_ei_process(
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
        token = message['data']['outcomes']['ei'][0]['X-TOKEN']
        ei_url = f"{message['data']['url']}/{cpid}"
        allure.attach(str(message), "Message for platform.")

        yield payload, cpid, message, ei_url, token, buyer_id, buyer_scheme

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


@pytest.fixture(scope="function")
# Створення EI, опціональна модель, з айтемами.
def create_ei_tc_3(get_parameters, connect_to_keyspace):

    bpe_host = get_parameters[2]
    country = get_parameters[4]
    language = get_parameters[5]
    tender_classification_id = get_parameters[9]
    clean_up_database = get_parameters[10]

    connect_to_ocds = connect_to_keyspace[0]
    connect_to_orchestrator = connect_to_keyspace[1]

    currency = f"{random.choice(currency_tuple)}"

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
            affordable_schemes = get_affordable_schemes(country)
            buyer_id = 0
            buyer_scheme = affordable_schemes[0]

            payload = copy.deepcopy(CreateExpenditureItemPayload(
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

        create_ei_process(
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
        token = message['data']['outcomes']['ei'][0]['X-TOKEN']
        ei_url = f"{message['data']['url']}/{cpid}"
        allure.attach(str(message), "Message for platform.")

        yield payload, cpid, message, ei_url, token, buyer_id, buyer_scheme

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
