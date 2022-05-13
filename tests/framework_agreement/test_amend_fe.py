import copy
import json
import allure
import requests
from deepdiff import DeepDiff

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import get_process_id_by_operation_id, \
    get_parameter_from_clarification_rules
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.prepare_date import framework_agreement_enquiry_period_end_date
from functions_collection.requests_collection import amend_fe_process
from messages_collection.framework_agreement.amend_fe_message import AmendFrameworkEstablishmentMessage
from payloads_collection.framework_agreement.amend_fe_payload import AmendFrameworkEstablishmentPayload
from releases_collection.framework_agreement.amend_fe_release import AmendFrameworkEstablishmentRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Framework Establishment")
@allure.severity("Critical")
@allure.testcase(url="https://docs.google.com/spreadsheets/d/1taw-E-4lryj80XYGdVwi1G-C2U6SQyilBuziGjXGyME/edit#gid=0",
                 name="Why this test case was fall down?")
class TestAmendFE:
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace, create_fe_tc_1):

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

        cpid = create_fe_tc_1[0]
        token = create_fe_tc_1[2]
        create_ap_payload = create_fe_tc_1[3]
        ap_url = create_fe_tc_1[4]
        fa_url = create_fe_tc_1[5]
        create_fe_payload = create_fe_tc_1[22]
        ocid = create_fe_tc_1[23]
        fe_url = create_fe_tc_1[24]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_fe_release = requests.get(url=fe_url).json()

        metadata_tender_url = None
        metadata_document_url = None
        metadata_budget_url = None
        try:
            if environment == "dev":
                metadata_tender_url = "http://dev.public.eprocurement.systems/tenders"
                metadata_document_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get"
                metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"

            elif environment == "sandbox":
                metadata_tender_url = "http://public.eprocurement.systems/tenders"
                metadata_document_url = "http://storage.eprocurement.systems/get"
                metadata_budget_url = "http://public.eprocurement.systems/budgets"
        except ValueError:
            ValueError("Check your environment: You must use 'dev' or 'sandbox' environment in pytest command")

        step_number = 1
        with allure.step(f'# {step_number}. Authorization platform one: Amend FE process.'):
            """
            Tender platform authorization for Amend FE process.
            As result get Tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f'# {step_number}. Send a request to create a Amend FE process.'):
            """
            Send request to BPE host to create a Amend FE process.
            """
            try:
                """
                Build payload for Amend FE process.
                """
                payload = copy.deepcopy(AmendFrameworkEstablishmentPayload(
                    ap_payload=create_ap_payload,
                    create_fe_payload=create_fe_payload,
                    previous_fe_release=previous_fe_release,
                    host_to_service=service_host,
                    country=country,
                    language=language,
                    environment=environment,
                    person_title="Ms.",
                    business_functions_type="contactPoint",
                    tender_documents_type="complaints"
                ))

                payload.customize_old_persones(
                    "MD-IDNO-create fe: tender.procuringEntity.persones[0].id",
                    "MD-IDNO-create fe: tender.procuringEntity.persones[1].id",
                    "MD-IDNO-create fe: tender.procuringEntity.persones[2].id",
                    need_to_add_new_bf=True,
                    quantity_of_new_bf_objects=3,
                    need_to_add_new_document=True,
                    quantity_of_new_documents_objects=3
                )
                payload.add_new_persones(
                    quantity_of_persones_objects=3,
                    quantity_of_bf_objects=3,
                    quantity_of_documents_objects=3
                )
                payload.customize_old_tender_documents(
                    previous_fe_release['releases'][0]['tender']['documents'][0]['id'],
                    previous_fe_release['releases'][0]['tender']['documents'][1]['id']
                )
                payload.add_new_tender_documents(quantity_of_new_documents=3)
                payload = payload.build_payload()
            except ValueError:
                ValueError("Impossible to build payload for Amend FE process.")

            synchronous_result = amend_fe_process(
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

            with allure.step(f'# {step_number}.2. Check the message for the platform, the Amend FE process.'):
                """
                Check the message for platform.
                """
                actual_message = message

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(AmendFrameworkEstablishmentMessage(
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
                    expected_release = copy.deepcopy(AmendFrameworkEstablishmentRelease(
                        environment,
                        country,
                        language,
                        pmd,
                        cpid,
                        ocid,
                        payload,
                        actual_message,
                        previous_ap_release,
                        previous_fe_release,
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
                    expected_fe_release = expected_release.build_expected_fe_release()
                except ValueError:
                    ValueError("Impossible to build expected FE release.")

                with allure.step("Compare actual and expected FE release."):
                    allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                    allure.attach(json.dumps(expected_fe_release), "Expected FE release.")

                    process_id = get_process_id_by_operation_id(connect_to_ocds, operation_id)
                    print("actual_fe_release")
                    print(json.dumps(actual_fe_release))
                    print("expected_fe_release")
                    print(json.dumps(expected_fe_release))
                    assert actual_fe_release == expected_fe_release, \
                        allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
                                      f"process_id = '{process_id}' ALLOW FILTERING;",
                                      "Cassandra DataBase: steps of process.")
        #
        #     with allure.step(f'# {step_number}.4. Check FA release.'):
        #         """
        #         Compare previous FA release and actual FA release.
        #         """
        #         try:
        #             """
        #             Build expected FA release.
        #             """
        #             expected_fa_release = expected_release.build_expected_fa_release()
        #         except ValueError:
        #             ValueError("Impossible to build expected FA release.")
        #
        #         with allure.step("Compare actual and expected FA release."):
        #             allure.attach(json.dumps(actual_fa_release), "Actual FA release.")
        #             allure.attach(json.dumps(expected_fa_release), "Expected FA release.")
        #
        #             assert actual_fa_release == expected_fa_release, \
        #                 allure.attach(f"SELECT * FROM ocds.orchestrator_operation_step WHERE "
        #                               f"process_id = '{process_id}' ALLOW FILTERING;",
        #                               "Cassandra DataBase: steps of process.")
        #
        # try:
        #     """
        #     CLean up the database.
        #     """
        #     # Clean after Framework Establishment process:
        #     cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id)
        #
        #     cleanup_table_of_services_for_framework_establishment(
        #         connect_to_ocds, connect_to_access, connect_to_clarification, connect_to_dossier, cpid
        #     )
        # except ValueError:
        #     ValueError("Impossible to cLean up the database.")
