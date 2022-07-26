import copy
import json
import allure
import requests

from deepdiff import DeepDiff
from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import get_process_id_by_operation_id, \
    cleanup_ocds_orchestrator_operation_step_by_operation_id, cleanup_table_of_services_for_financial_source
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_fs_process
from functions_collection.some_functions import is_it_uuid, get_affordable_currency
from messages_collection.budget.create_fs_message import FinancialSourceMessage
from payloads_collection.budget.create_fs_payload import FinancialSourcePayload
from releases_collection.budget.create_fs_release import FinancialSourceRelease


@allure.parent_suite("Budget")
@allure.suite("Financial source")
@allure.severity("Critical")
class TestCreateFS:
    @allure.title("Check records: based on full data model.")
    @allure.testcase(
        url="https://docs.google.com/spreadsheets/d/1taw-E-4lryj80XYGdVwi1G-C2U6SQyilBuziGjXGyME/edit#gid=0",
        name="Why this test case was fall down?")
    def test_case_1(self, get_parameters, connect_to_keyspace, create_ei_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]

        connect_to_ocds = connect_to_keyspace[0]

        ei_payload = create_ei_tc_1[0]
        cpid = create_ei_tc_1[1]
        ei_message = create_ei_tc_1[2]

        url = f"{ei_message['data']['url']}/{cpid}"
        actual_ei_release_before_fs_creating = requests.get(url=url).json()

        currency = get_affordable_currency(country)

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Create FS process."):
            """
            Tender platform authorization for Create FS process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Create FS process."):
            """
            Send api request to BPE host to create a Create FS process.
            """
            try:
                """
                Build payload for Create FS process.
                """
                payload = copy.deepcopy(FinancialSourcePayload(
                    country=country,
                    ei_payload=ei_payload,
                    amount=89999.89,
                    currency=currency,
                    payer_id=1,
                    funder_id=2
                ))

                payload.customize_buyer_additional_identifiers(
                    quantity_of_buyer_additional_identifiers=3
                )
                payload.customize_tender_procuring_entity_additional_identifiers(
                    quantity_of_tender_procuring_entity_additional_identifiers=3
                )
                payload = payload.build_payload()
            except ValueError:
                ValueError("Impossible to build payload for Create Fs process.")

            synchronous_result = create_fs_process(
                host=bpe_host,
                cpid=cpid,
                access_token=access_token,
                x_operation_id=operation_id,
                payload=payload,
                test_mode=True
            )

            message = get_message_for_platform(operation_id)
            ocid = message['data']['outcomes']['fs'][0]['id']
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create FS process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(FinancialSourceMessage(
                        environment=environment,
                        actual_message=actual_message,
                        test_mode=True)
                    )

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

            with allure.step(f'# {step_number}.3. Check FS release.'):
                """
                Compare actual FS release and expected FS release.
                """
                url = f"{actual_message['data']['url']}/{ocid}"
                actual_release = requests.get(url=url).json()

                try:
                    """
                    Build expected FS release.
                    """
                    expected_release = copy.deepcopy(FinancialSourceRelease(
                        environment=environment,
                        host_to_service=service_host,
                        language=language,
                        cpid=cpid,
                        ei_payload=ei_payload,
                        fs_payload=payload,
                        fs_message=actual_message,
                        actual_fs_release=actual_release
                    ))
                    expected_release = expected_release.build_expected_fs_release()
                except ValueError:
                    ValueError("Impossible to build expected FS release.")

                with allure.step('Compare actual and expected releases.'):
                    allure.attach(json.dumps(actual_release), "Actual release.")
                    allure.attach(json.dumps(expected_release), "Expected release.")

                    assert actual_release == expected_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check EI release.'):
                """
                Compare actual EI release before and after FS creating.
                """
                url = f"{ei_message['data']['url']}/{cpid}"
                actual_ei_release_after_fs_creating = requests.get(url=url).json()

                actual_result_of_comparing_releases = dict(DeepDiff(
                    actual_ei_release_before_fs_creating,
                    actual_ei_release_after_fs_creating
                ))

                dictionary_item_added_was_cleaned = \
                    str(actual_result_of_comparing_releases['dictionary_item_added']).replace('root', '')[1:-1]

                actual_result_of_comparing_releases['dictionary_item_added'] = dictionary_item_added_was_cleaned
                actual_result_of_comparing_releases = dict(actual_result_of_comparing_releases)

                # BR-2.1.3.6, BR-2.1.3.5, BR-2.1.3.4, BR-2.1.3.3, BR-2.1.3.2, BR-2.1.3.1
                expected_result_of_comparing_releases = {
                    "dictionary_item_added": "['releases'][0]['relatedProcesses'], "
                                             "['releases'][0]['planning']['budget']['amount']",
                    "values_changed": {
                        "root['releases'][0]['id']": {
                            "new_value": f"{cpid}-{actual_ei_release_after_fs_creating['releases'][0]['id'][29:42]}",
                            "old_value": actual_ei_release_before_fs_creating['releases'][0]['id']
                        },
                        "root['releases'][0]['date']": {
                            "new_value": actual_message['data']['operationDate'],
                            "old_value": actual_ei_release_before_fs_creating['releases'][0]['date']
                        }
                    }
                }

                # BR-2.1.3.9, BR-2.1.3.10, BR-2.1.3.11, BR-2.1.3.12, BR-2.1.3.13, BR-2.1.3.14
                actual_related_processes_array = \
                    actual_ei_release_after_fs_creating['releases'][0]['relatedProcesses']
                try:
                    """Prepare expected 'releases[0].relatedProcesses' array."""

                    try:
                        """Set permanent id."""

                        is_permanent_id_correct = is_it_uuid(
                            actual_ei_release_after_fs_creating['releases'][0]['relatedProcesses'][0]['id'])
                        if is_permanent_id_correct is True:
                            related_processes_id = \
                                actual_ei_release_after_fs_creating['releases'][0]['relatedProcesses'][0]['id']
                        else:
                            ValueError(f"The 'releases[0].relatedProcesses[0].id' must be uuid.")
                    except KeyError:
                        KeyError("Mismatch key into path 'releases[0].relatedProcesses[0].id'")

                    if environment == "dev":
                        metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"
                    elif environment == "sandbox":
                        metadata_budget_url = "http://public.eprocurement.systems/budgets"

                    expected_related_processes_array = [{
                        "id": related_processes_id,
                        "relationship": ["x_fundingSource"],
                        "scheme": "ocid",
                        "identifier": ocid,
                        "uri": f"{metadata_budget_url}/{cpid}/{ocid}"
                    }]
                except ValueError:
                    ValueError("Impossible to prepare expected 'releases[0].relatedProcesses' array.")

                # BR-2.1.3.7, BR-2.1.3.8:
                actual_amount_object = \
                    actual_ei_release_after_fs_creating['releases'][0]['planning']['budget']['amount']
                try:
                    """Prepare expected 'releases[0].planning.budget.amount' object."""
                    expected_amount_object = {
                        "amount": payload['planning']['budget']['amount']['amount'],
                        "currency": payload['planning']['budget']['amount']['currency']
                    }
                except ValueError:
                    ValueError("Impossible to prepare expected 'releases[0].planning.budget.amount' object.")

                with allure.step("Compare actual and expected results of comparing EI releases."):
                    allure.attach(json.dumps(actual_result_of_comparing_releases), "Actual result.")
                    allure.attach(json.dumps(expected_result_of_comparing_releases), "Expected result.")

                    assert actual_result_of_comparing_releases == expected_result_of_comparing_releases, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

                with allure.step("'Compare actual and expected 'releases[0].relatedProcesses' array."):
                    allure.attach(json.dumps(actual_related_processes_array), "Actual result.")
                    allure.attach(json.dumps(expected_related_processes_array), "Expected result.")

                    assert actual_related_processes_array == expected_related_processes_array, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

                with allure.step("'Compare actual and expected 'releases[0].planning.budget.amount' object."):
                    allure.attach(json.dumps(actual_amount_object), "Actual result.")
                    allure.attach(json.dumps(expected_amount_object), "Expected result.")

                    assert actual_amount_object == expected_amount_object, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")
        try:
            """
            CLean up the database.
            """
            # Clean after Crate FS process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_financial_source(connect_to_ocds, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")

    @allure.title("Check records: based on required data model.")
    @allure.testcase(
        url="https://docs.google.com/spreadsheets/d/1taw-E-4lryj80XYGdVwi1G-C2U6SQyilBuziGjXGyME/edit#gid=0",
        name="Why this test case was fall down?")
    def test_case_2(self, get_parameters, connect_to_keyspace, create_ei_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]

        connect_to_ocds = connect_to_keyspace[0]

        ei_payload = create_ei_tc_2[0]
        cpid = create_ei_tc_2[1]
        ei_message = create_ei_tc_2[2]

        url = f"{ei_message['data']['url']}/{cpid}"
        actual_ei_release_before_fs_creating = requests.get(url=url).json()

        currency = get_affordable_currency(country)

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Create FS process."):
            """
            Tender platform authorization for Create FS process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Create FS process."):
            """
            Send api request to BPE host to create a Create FS process.
            """
            try:
                """
                Build payload for Create FS process.
                """
                payload = copy.deepcopy(FinancialSourcePayload(
                    country=country,
                    ei_payload=ei_payload,
                    amount=89999.89,
                    currency=currency,
                    payer_id=1
                ))
                payload.delete_optional_fields(
                    "tender.procuringEntity.identifier.uri",
                    "tender.procuringEntity.address.postalCode",
                    "tender.procuringEntity.additionalIdentifiers",
                    "tender.procuringEntity.contactPoint.faxNumber",
                    "tender.procuringEntity.contactPoint.url",
                    "planning.budget.id",
                    "planning.budget.description",
                    "planning.budget.europeanUnionFunding",
                    "planning.budget.project",
                    "planning.budget.projectID",
                    "planning.budget.uri",
                    "planning.rationale",
                    "buyer"
                )
                payload = payload.build_payload()
            except ValueError:
                ValueError("Impossible to build payload for Create Fs process.")

            synchronous_result = create_fs_process(
                host=bpe_host,
                cpid=cpid,
                access_token=access_token,
                x_operation_id=operation_id,
                payload=payload,
                test_mode=True
            )

            message = get_message_for_platform(operation_id)
            ocid = message['data']['outcomes']['fs'][0]['id']
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create FS process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(FinancialSourceMessage(
                        environment=environment,
                        actual_message=actual_message,
                        test_mode=True)
                    )

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

            with allure.step(f'# {step_number}.3. Check FS release.'):
                """
                Compare actual FS release and expected FS release.
                """
                url = f"{actual_message['data']['url']}/{ocid}"
                actual_release = requests.get(url=url).json()

                try:
                    """
                    Build expected FS release.
                    """
                    expected_release = copy.deepcopy(FinancialSourceRelease(
                        environment=environment,
                        host_to_service=service_host,
                        language=language,
                        cpid=cpid,
                        ei_payload=ei_payload,
                        fs_payload=payload,
                        fs_message=actual_message,
                        actual_fs_release=actual_release
                    ))
                    expected_release = expected_release.build_expected_fs_release()
                except ValueError:
                    ValueError("Impossible to build expected FS release.")

                with allure.step('Compare actual and expected releases.'):
                    allure.attach(json.dumps(actual_release), "Actual release.")
                    allure.attach(json.dumps(expected_release), "Expected release.")

                    assert actual_release == expected_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check EI release.'):
                """
                Compare actual EI release before and after FS creating.
                """
                url = f"{ei_message['data']['url']}/{cpid}"
                actual_ei_release_after_fs_creating = requests.get(url=url).json()

                actual_result_of_comparing_releases = dict(DeepDiff(
                    actual_ei_release_before_fs_creating,
                    actual_ei_release_after_fs_creating
                ))

                dictionary_item_added_was_cleaned = \
                    str(actual_result_of_comparing_releases['dictionary_item_added']).replace('root', '')[1:-1]

                actual_result_of_comparing_releases['dictionary_item_added'] = dictionary_item_added_was_cleaned
                actual_result_of_comparing_releases = dict(actual_result_of_comparing_releases)

                # BR-2.1.3.6, BR-2.1.3.5, BR-2.1.3.4, BR-2.1.3.3, BR-2.1.3.2, BR-2.1.3.1
                expected_result_of_comparing_releases = {
                    "dictionary_item_added": "['releases'][0]['relatedProcesses'], "
                                             "['releases'][0]['planning']['budget']['amount']",
                    "values_changed": {
                        "root['releases'][0]['id']": {
                            "new_value": f"{cpid}-{actual_ei_release_after_fs_creating['releases'][0]['id'][29:42]}",
                            "old_value": actual_ei_release_before_fs_creating['releases'][0]['id']
                        },
                        "root['releases'][0]['date']": {
                            "new_value": actual_message['data']['operationDate'],
                            "old_value": actual_ei_release_before_fs_creating['releases'][0]['date']
                        }
                    }
                }

                # BR-2.1.3.9, BR-2.1.3.10, BR-2.1.3.11, BR-2.1.3.12, BR-2.1.3.13, BR-2.1.3.14
                actual_related_processes_array = \
                    actual_ei_release_after_fs_creating['releases'][0]['relatedProcesses']
                try:
                    """Prepare expected 'releases[0].relatedProcesses' array."""

                    try:
                        """Set permanent id."""

                        is_permanent_id_correct = is_it_uuid(
                            actual_ei_release_after_fs_creating['releases'][0]['relatedProcesses'][0]['id'])
                        if is_permanent_id_correct is True:
                            related_processes_id = \
                                actual_ei_release_after_fs_creating['releases'][0]['relatedProcesses'][0]['id']
                        else:
                            ValueError(f"The 'releases[0].relatedProcesses[0].id' must be uuid.")
                    except KeyError:
                        KeyError("Mismatch key into path 'releases[0].relatedProcesses[0].id'")

                    if environment == "dev":
                        metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"
                    elif environment == "sandbox":
                        metadata_budget_url = "http://public.eprocurement.systems/budgets"

                    expected_related_processes_array = [{
                        "id": related_processes_id,
                        "relationship": ["x_fundingSource"],
                        "scheme": "ocid",
                        "identifier": ocid,
                        "uri": f"{metadata_budget_url}/{cpid}/{ocid}"
                    }]
                except ValueError:
                    ValueError("Impossible to prepare expected 'releases[0].relatedProcesses' array.")

                # BR-2.1.3.7, BR-2.1.3.8:
                actual_amount_object = \
                    actual_ei_release_after_fs_creating['releases'][0]['planning']['budget']['amount']
                try:
                    """Prepare expected 'releases[0].planning.budget.amount' object."""
                    expected_amount_object = {
                        "amount": payload['planning']['budget']['amount']['amount'],
                        "currency": payload['planning']['budget']['amount']['currency']
                    }
                except ValueError:
                    ValueError("Impossible to prepare expected 'releases[0].planning.budget.amount' object.")

                with allure.step("Compare actual and expected results of comparing EI releases."):
                    allure.attach(json.dumps(actual_result_of_comparing_releases), "Actual result.")
                    allure.attach(json.dumps(expected_result_of_comparing_releases), "Expected result.")

                    assert actual_result_of_comparing_releases == expected_result_of_comparing_releases, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

                with allure.step("'Compare actual and expected 'releases[0].relatedProcesses' array."):
                    allure.attach(json.dumps(actual_related_processes_array), "Actual result.")
                    allure.attach(json.dumps(expected_related_processes_array), "Expected result.")

                    assert actual_related_processes_array == expected_related_processes_array, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

                with allure.step("'Compare actual and expected 'releases[0].planning.budget.amount' object."):
                    allure.attach(json.dumps(actual_amount_object), "Actual result.")
                    allure.attach(json.dumps(expected_amount_object), "Expected result.")

                    assert actual_amount_object == expected_amount_object, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")
        try:
            """
            CLean up the database.
            """
            # Clean after Crate FS process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_financial_source(connect_to_ocds, cpid)
        except ValueError:
            ValueError("Impossible to cLean up the database.")
