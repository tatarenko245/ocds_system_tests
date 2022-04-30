import copy
import json
import random

import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from data_collection.data_constant import currency_tuple
from functions_collection.cassandra_methods import get_process_id_by_operation_id, \
    cleanup_table_of_services_for_expenditure_item, cleanup_ocds_orchestrator_operation_step_by_operation_id
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_ei_process, create_fs_process
from messages_collection.budget.create_ei_message import ExpenditureItemMessage
from messages_collection.budget.create_fs_message import FinancialSourceMessage
from payloads_collection.budget.ei_payload import ExpenditureItemPayload
from payloads_collection.budget.fs_payload import FinancialSourcePayload
from releases_collection.budget.ei_release import ExpenditureItemRelease
from releases_collection.budget.fs_release import FinancialSourceRelease


@allure.parent_suite("Budget")
@allure.suite("Financial source")
@allure.severity("Critical")
@allure.testcase(url="")
class TestCreateFS:
    @allure.title("Check records: based on required data model.")
    def test_case_1(self, create_ei_tc_1, get_credits, connect_to_keyspace):

        environment = get_credits[0]
        bpe_host = get_credits[2]
        service_host = get_credits[3]
        country = get_credits[4]
        language = get_credits[5]
        tender_classification_id = get_credits[9]
        connect_to_ocds = connect_to_keyspace[0]

        ei_payload = create_ei_tc_1[0]
        cpid = create_ei_tc_1[1]
        currency = f"{random.choice(currency_tuple)}"
        fs_payloads_list = list()
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
                    ei_payload=ei_payload,
                    amount=89999.89,
                    currency=currency,
                    payer_id=1,
                    funder_id=2)
                )
                # payload.delete_optional_fields(
                #     "tender.procuringEntity.identifier.uri",
                #     "tender.procuringEntity.address.postalCode",
                #     "tender.procuringEntity.additionalIdentifiers",
                #     "tender.procuringEntity.additionalIdentifiers.uri",
                #     "tender.procuringEntity.contactPoint.faxNumber",
                #     "tender.procuringEntity.contactPoint.url",
                #     "planning.budget.id",
                #     "planning.budget.description",
                #     "planning.budget.europeanUnionFunding",
                #     "planning.budget.europeanUnionFunding.uri",
                #     "planning.budget.project",
                #     "planning.budget.projectID",
                #     "planning.budget.uri",
                #     "planning.rationale",
                #     "buyer",
                #     "buyer.identifier.uri",
                #     "buyer.address.postalCode",
                #     "buyer.additionalIdentifiers",
                #     "buyer.additionalIdentifiers.uri",
                #     "buyer.contactPoint.faxNumber",
                #     "buyer.contactPoint.url",
                #
                # )
                payload = payload.build_financial_source_payload()
                fs_payloads_list.append(payload)
            except ValueError:
                raise ValueError("Impossible to build payload for Create Fs process.")

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
                    raise ValueError("Impossible to build expected message for platform.")

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
                print("actual_release")
                print(json.dumps(actual_release))
                try:
                    """
                    Build expected FS release.
                    """
                    expected_release = copy.deepcopy(FinancialSourceRelease(
                        environment=environment,
                        host_to_service=service_host,
                        language=language,
                        cpid=cpid,
                        fs_payload=payload,
                        fs_message=actual_message,
                        actual_fs_release=actual_release
                    ))
                    expected_release = expected_release.build_expected_fs_release(fs_payloads_list)
                except ValueError:
                    raise ValueError("Impossible to build expected FS release.")
        #
        #         with allure.step('Compare actual and expected releases.'):
        #             allure.attach(json.dumps(actual_release), "Actual release.")
        #             allure.attach(json.dumps(expected_release), "Expected release.")
        #
        #             assert actual_release == expected_release, \
        #                 allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
        #                               f"process_id = '{process_id}' ALLOW FILTERING;",
        #                               "Cassandra DataBase: steps of process.")
        # try:
        #     """
        #     CLean up the database.
        #     """
        #     # Clean after Crate Ei process:
        #     cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, ei_operation_id)
        #     cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cpid)
        # except ValueError:
        #     raise ValueError("Impossible to cLean up the database.")
