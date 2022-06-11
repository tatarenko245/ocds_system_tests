import copy
import json
import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid, \
     cleanup_table_of_services_for_issuing_framework
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import issuing_framework_process, create_confirmation_response_process
from messages_collection.framework_agreement.create_confirmation_response_message import \
    CreateConfirmationResponseMessage
from messages_collection.framework_agreement.issuing_framework_message import IssuingFrameworkMessage
from payloads_collection.framework_agreement.create_confirmation_response_payload import \
    CreateConfirmationResponsePayload
from payloads_collection.framework_agreement.issuing_framework_payload import IssuingFrameworkPayload
from releases_collection.framework_agreement.create_confirmation_response_release import \
    CreateConfirmationResponseRelease
from releases_collection.framework_agreement.issuing_framework_release import IssuingFrameworkRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Contracting")
@allure.severity("Critical")
@allure.testcase(url="")
class TestCreateConfirmationResponse:
    @allure.testcase(url="")
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace, issuing_framework_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]
        country = get_parameters[4]
        pmd = get_parameters[6]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]
        connect_to_submission = connect_to_keyspace[6]
        connect_to_contracting = connect_to_keyspace[7]

        cpid = issuing_framework_tc_1[0]
        token = issuing_framework_tc_1[2]
        ap_url = issuing_framework_tc_1[4]
        fa_url = issuing_framework_tc_1[5]
        ocid = issuing_framework_tc_1[23]
        fe_url = issuing_framework_tc_1[24]
        contract_id = issuing_framework_tc_1[32]
        issuing_framework_message = issuing_framework_tc_1[34]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_fe_release = requests.get(url=fe_url).json()

        """
        VR.COM-1.17.2: Check FE state.
        """
        if previous_fe_release['releases'][0]['tender']['status'] == "active" and \
                previous_fe_release['releases'][0]['tender']['statusDetails'] == "evaluation":
            pass
        else:
            ValueError(f"FE release has invalid state: {previous_fe_release['releases'][0]['tender']['status']} and"
                       f"{previous_fe_release['releases'][0]['tender']['statusDetails']}.")

        """
        VR.COM-6.8.2: Check Contract state.
        """
        for i in range(len(previous_fe_release['releases'][0]['contracts'])):
            if previous_fe_release['releases'][0]['contracts'][i]['id'] == contract_id:
                if previous_fe_release['releases'][0]['contracts'][i]['status'] == "pending" and \
                        previous_fe_release['releases'][0]['contracts'][i]['statusDetails'] == "issued":
                    pass
                else:
                    ValueError(f"Contract {contract_id} has invalid state: "
                               f"{previous_fe_release['releases'][0]['contracts'][i]['status']} and"
                               f"{previous_fe_release['releases'][0]['contracts'][i]['statusDetails']}.")
            else:
                ValueError(f"Incorrect contract id into FE release: "
                           f"{previous_fe_release['releases'][0]['contracts'][i]['id']} != {contract_id}.")

        """
        Send request, depends on quantity of objects into 
        'releases[0].contracts[0].confirmationRequests[0].request'
        """
        for q_0 in range(len(previous_fe_release['releases'][0]['contracts'][0]['confirmationRequests'])):
            if previous_fe_release['releases'][0]['contracts'][0]['confirmationRequests'][q_0]['source'] == "buyer":
                for q_1 in range(len(
                        previous_fe_release['releases'][0]['contracts'][0]['confirmationRequests'][q_0]['requests']
                )):
                    request_id = previous_fe_release['releases'][0]['contracts'][0][
                        'confirmationRequests'][q_0]['requests'][q_1]['id']
                    request_token = None
                    for q in range(len(issuing_framework_message['data']['outcomes']['requests'])):
                        if issuing_framework_message['data']['outcomes']['requests'][q]['id'] == request_id:
                            request_token = issuing_framework_message['data']['outcomes']['requests'][q]['X-TOKEN']
                    step_number = 1
                    with allure.step(f"# {step_number}. Authorization platform one: Create Confirmation "
                                     f"Response process."):
                        """
                        Tender platform authorization for Create Confirmation Response process.
                        As result get Tender platform's access token and process operation-id.
                        """
                        platform_one = PlatformAuthorization(bpe_host)
                        access_token = platform_one.get_access_token_for_platform_one()
                        operation_id = platform_one.get_x_operation_id(access_token)

                    step_number += 1
                    with allure.step(f"# {step_number}. Send a request to create a Create Confirmation "
                                     f"Response process."):
                        """
                        Send request to BPE host to create a Create Confirmation Response process.
                        """

                        try:
                            """
                            Build payload for Create Confirmation Response process.
                            """
                            payload = CreateConfirmationResponsePayload(environment, service_host, request_id)

                            payload.customize_business_functions(quantity_of_bf=3, quantity_of_bf_documents=3)
                            payload = payload.build_payload()
                            print("\n Payload")
                            print(json.dumps(payload))
                        except ValueError:
                            ValueError("Impossible to build payload for Create Confirmation Response process.")

                        synchronous_result = create_confirmation_response_process(
                            host=bpe_host,
                            access_token=access_token,
                            x_operation_id=operation_id,
                            payload=payload,
                            entity="contract",
                            cpid=cpid,
                            ocid=ocid,
                            entity_id=contract_id,
                            token=request_token,
                            role="buyer",
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
                            with allure.step('Compare actual status code and expected status code '
                                             'of sending request.'):
                                allure.attach(str(synchronous_result.status_code), "Actual status code.")
                                allure.attach(str(202), "Expected status code.")
                                assert synchronous_result.status_code == 202

                        with allure.step(f'# {step_number}.2. Check the message for the platform,'
                                         f'the Create Confirmation Response process.'):
                            """
                            Check the message for platform.
                            """
                            actual_message = message

                            try:
                                """
                                Build expected message for platform.
                                """
                                expected_message = copy.deepcopy(CreateConfirmationResponseMessage(
                                    environment=environment,
                                    cpid=cpid,
                                    ocid=ocid,
                                    test_mode=True
                                ))

                                expected_message = expected_message.build_expected_platform_message(actual_message, 1)
                            except ValueError:
                                ValueError("Impossible to build expected message for platform.")

                            with allure.step('Compare actual and expected message for platform.'):
                                allure.attach(json.dumps(actual_message), "Actual message.")
                                allure.attach(json.dumps(expected_message), "Expected message.")

                                assert actual_message == expected_message, \
                                    allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                                  f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                                  f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

                        with allure.step(f'# {step_number}.3. Check AP release.'):
                            """
                            Compare actual AP release and expected AP release.
                            """
                            actual_ap_release = requests.get(url=ap_url).json()

                            try:
                                """
                                Build expected AP release.
                                """
                                expected_release = copy.deepcopy(CreateConfirmationResponseRelease(
                                    environment, actual_message, ocid, payload
                                ))
                                expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
                            except ValueError:
                                ValueError("Impossible to build expected AP release.")

                            with allure.step("Compare actual and expected AP release."):
                                allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                                allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                                allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                              f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                              f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

                        with allure.step(f'# {step_number}.4. Check FE release.'):
                            """
                            Compare actual FE release and expected FE release.
                            """
                            actual_fe_release = requests.get(url=fe_url).json()

                            print("\nActual FE release")
                            print(json.dumps(actual_fe_release))
                            try:
                                """
                                Build expected FE release.
                                """
                                expected_fe_release = expected_release.build_expected_fe_release(
                                    previous_fe_release, actual_fe_release, connect_to_submission, country, pmd
                                )
                            except ValueError:
                                ValueError("Impossible to build expected FE release.")

                            print("\n Expected_fe_release")
                            print(json.dumps(expected_fe_release))

                            #
                            # with allure.step("Compare actual and expected FE release."):
                            #     allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                            #     allure.attach(json.dumps(expected_fe_release), "Expected FE release.")
                            #
                            #     assert actual_fe_release == expected_fe_release, \
                            #         allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                            #                       f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                            #                       f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
                    #
                    #     with allure.step(f'# {step_number}.4. Check FA release.'):
                    #         """
                    #         Compare actual FA release and expected FA release.
                    #         """
                    #         actual_fa_release = requests.get(url=fa_url).json()
                    #
                    #         try:
                    #             """
                    #             Build expected FA release.
                    #             """
                    #             expected_fa_release = expected_release.build_expected_fa_release(
                    #                 previous_fa_release
                    #             )
                    #         except ValueError:
                    #             ValueError("Impossible to build expected FA release.")
                    #
                    #         with allure.step("Compare actual and expected FA release."):
                    #             allure.attach(json.dumps(actual_fa_release), "Actual Fa release.")
                    #             allure.attach(json.dumps(expected_fa_release), "Expected Fa release.")
                    #
                    #             assert actual_fa_release == expected_fa_release, \
                    #                 allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                    #                               f"cpid = '{cpid}' ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
        # try:
        #     """
        #     CLean up the database.
        #     """
        #     # Clean after Complete Qualification process:
        #     cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
        #
        #     cleanup_table_of_services_for_issuing_framework(
        #         connect_to_ocds, connect_to_access, connect_to_contracting, cpid
        #     )
        #
        # except ValueError:
        #     ValueError("Impossible to cLean up the database.")

