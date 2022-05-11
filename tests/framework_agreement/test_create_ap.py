import copy
import json
import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import get_process_id_by_operation_id, \
    cleanup_ocds_orchestrator_operation_step_by_operation_id, \
    get_max_duration_of_fa_from_access_rules, cleanup_table_of_services_for_aggregated_plan
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_ap_process
from messages_collection.framework_agreement.create_ap_message import AggregatedPlanMessage
from payloads_collection.framework_agreement.create_ap_payload import AggregatedPlan
from releases_collection.framework_agreement.create_ap_release import CreateAggregatedPlanRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Aggregated Plan")
@allure.severity("Critical")
@allure.testcase(url="")
class TestCreateAP:
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]
        pmd = get_parameters[6]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_access = connect_to_keyspace[2]

        step_number = 1
        with allure.step(f'# {step_number}. Authorization platform one: Create AP process.'):
            """
            Tender platform authorization for Create AP process.
            As result get Tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f'# {step_number}. Send a request to create a Create AP process.'):
            """
            Send api request to BPE host to create a Create AP process.
            And save in variable cpid and token..
            """
            try:
                """
                Build payload for Create AP process.
                """
                max_duration_of_fa = get_max_duration_of_fa_from_access_rules(
                    connect_to_access,
                    country,
                    pmd
                )

                payload = copy.deepcopy(AggregatedPlan(
                    central_purchasing_body_id=55,
                    host_to_service=service_host,
                    max_duration_of_fa=max_duration_of_fa
                ))

                payload.customize_tender_procuring_entity_additional_identifiers(
                    quantity_of_tender_procuring_entity_additional_identifiers=3
                )

                payload.customize_tender_documents(
                    quantity_of_documents=3
                )

                payload = payload.build_payload()
            except ValueError:
                raise ValueError("Impossible to build payload for Create AP process.")

            synchronous_result = create_ap_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                payload=payload,
                test_mode=True,
                country=country,
                language=language,
                pmd=pmd
            )

            message = get_message_for_platform(operation_id)
            cpid = message['data']['outcomes']['ap'][0]['id']
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create AP process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(AggregatedPlanMessage(
                        environment=environment,
                        actual_message=actual_message,
                        test_mode=True
                    ))

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

            with allure.step(f'# {step_number}.3. Check AP release.'):
                """
                Compare actual AP release and expected AP release.
                """
                ap_url = f"{actual_message['data']['url']}/{actual_message['data']['outcomes']['ap'][0]['id']}"
                actual_ap_release = requests.get(url=ap_url).json()

                fa_url = f"{actual_message['data']['url']}/{actual_message['data']['ocid']}"
                actual_fa_release = requests.get(url=fa_url).json()

                try:
                    """
                    Build expected AP release.
                    """
                    expected_release = copy.deepcopy(CreateAggregatedPlanRelease(
                        environment=environment,
                        host_to_service=service_host,
                        language=language,
                        pmd=pmd,
                        ap_payload=payload,
                        ap_message=actual_message,
                        actual_ap_release=actual_ap_release,
                        actual_fa_release=actual_fa_release
                    ))

                    expected_ap_release = expected_release.build_expected_ap_release()
                except ValueError:
                    raise ValueError("Impossible to build expected AP release.")

                with allure.step('Compare actual and expected AP release.'):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    assert actual_ap_release == expected_ap_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FA release.'):
                """
                Compare actual MS release and expected FA release.
                """
                try:
                    """
                    Build expected FA release.
                    """
                    expected_fa_release = expected_release.build_expected_fa_release()
                except ValueError:
                    raise ValueError("Impossible to build expected FA release.")

                with allure.step('Compare actual and expected FA release.'):
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
            # Clean after Crate AP process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_aggregated_plan(connect_to_ocds, connect_to_access, cpid)
        except ValueError:
            raise ValueError("Impossible to cLean up the database.")

    @allure.title("Check records: based on required data model.")
    def test_case_2(self, get_parameters, connect_to_keyspace):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        language = get_parameters[5]
        pmd = get_parameters[6]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_access = connect_to_keyspace[2]

        step_number = 1
        with allure.step(f'# {step_number}. Authorization platform one: Create AP process.'):
            """
            Tender platform authorization for Create AP process.
            As result get Tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f'# {step_number}. Send a request to create a Create AP process.'):
            """
            Send api request to BPE host to create a Create AP process.
            And save in variable cpid and token..
            """
            try:
                """
                Build payload for Create AP process.
                """
                max_duration_of_fa = get_max_duration_of_fa_from_access_rules(
                    connect_to_access,
                    country,
                    pmd
                )

                payload = copy.deepcopy(AggregatedPlan(
                    central_purchasing_body_id=55,
                    host_to_service=service_host,
                    max_duration_of_fa=max_duration_of_fa
                ))

                payload.delete_optional_fields(
                    "tender.procurementMethodRationale",
                    "tender.procuringEntity.additionalIdentifiers",
                    "tender.procuringEntity.address.postalCode",
                    "tender.procuringEntity.contactPoint.faxNumber",
                    "tender.procuringEntity.contactPoint.url",
                    "tender.documents"
                )

                payload = payload.build_payload()
            except ValueError:
                raise ValueError("Impossible to build payload for Create AP process.")

            synchronous_result = create_ap_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                payload=payload,
                test_mode=True,
                country=country,
                language=language,
                pmd=pmd
            )

            message = get_message_for_platform(operation_id)
            cpid = message['data']['outcomes']['ap'][0]['id']
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Create AP process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(AggregatedPlanMessage(
                        environment=environment,
                        actual_message=actual_message,
                        test_mode=True
                    ))

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

            with allure.step(f'# {step_number}.3. Check AP release.'):
                """
                Compare actual AP release and expected AP release.
                """
                ap_url = f"{actual_message['data']['url']}/{actual_message['data']['outcomes']['ap'][0]['id']}"
                actual_ap_release = requests.get(url=ap_url).json()

                fa_url = f"{actual_message['data']['url']}/{actual_message['data']['ocid']}"
                actual_fa_release = requests.get(url=fa_url).json()

                try:
                    """
                    Build expected AP release.
                    """
                    expected_release = copy.deepcopy(CreateAggregatedPlanRelease(
                        environment=environment,
                        host_to_service=service_host,
                        language=language,
                        pmd=pmd,
                        ap_payload=payload,
                        ap_message=actual_message,
                        actual_ap_release=actual_ap_release,
                        actual_fa_release=actual_fa_release
                    ))

                    expected_ap_release = expected_release.build_expected_ap_release()
                except ValueError:
                    raise ValueError("Impossible to build expected AP release.")

                with allure.step('Compare actual and expected AP release.'):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    assert actual_ap_release == expected_ap_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FA release.'):
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

                with allure.step('Compare actual and expected FA release.'):
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
            # Clean after Crate AP process:
            cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
            cleanup_table_of_services_for_aggregated_plan(connect_to_ocds, connect_to_access, cpid)
        except ValueError:
            raise ValueError("Impossible to cLean up the database.")
