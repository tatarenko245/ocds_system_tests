import copy
import json
import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid_and_operationid, \
    cleanup_table_of_services_for_issuing_framework
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import next_confirmation_step_process
from messages_collection.framework_agreement.next_confirmation_request_message import NextConfirmationStepMessage
from releases_collection.framework_agreement.next_confirmation_step_release import NextConfirmationStepRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Evaluation")
@allure.severity("Critical")
@allure.testcase(url="")
class TestNextConfirmationStep:
    @allure.testcase(url="")
    @allure.title("Check records: based on full data model.")
    def test_case_1(self, get_parameters, connect_to_keyspace, create_confirmation_response_by_buyer_tc_1):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        country = get_parameters[4]
        pmd = get_parameters[6]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]
        connect_to_submission = connect_to_keyspace[6]
        connect_to_contracting = connect_to_keyspace[7]

        cpid = create_confirmation_response_by_buyer_tc_1[0]
        ap_url = create_confirmation_response_by_buyer_tc_1[4]
        fa_url = create_confirmation_response_by_buyer_tc_1[5]
        ocid = create_confirmation_response_by_buyer_tc_1[23]
        fe_url = create_confirmation_response_by_buyer_tc_1[24]
        contract_id = create_confirmation_response_by_buyer_tc_1[32]
        contract_token = create_confirmation_response_by_buyer_tc_1[33]

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
            raise ValueError(f"FE release has invalid state: {previous_fe_release['releases'][0]['tender']['status']} "
                             f"and {previous_fe_release['releases'][0]['tender']['statusDetails']}.")

        """
        VR.COM-6.8.2: Check Contract state.
        """
        for i in range(len(previous_fe_release['releases'][0]['contracts'])):
            if previous_fe_release['releases'][0]['contracts'][i]['id'] == contract_id:
                if previous_fe_release['releases'][0]['contracts'][i]['status'] == "pending" and \
                        previous_fe_release['releases'][0]['contracts'][i]['statusDetails'] == "issued":
                    pass
                else:
                    raise ValueError(f"Contract {contract_id} has invalid state: "
                                     f"{previous_fe_release['releases'][0]['contracts'][i]['status']} and"
                                     f"{previous_fe_release['releases'][0]['contracts'][i]['statusDetails']}.")
            else:
                raise ValueError(f"Incorrect contract id into FE release: "
                                 f"{previous_fe_release['releases'][0]['contracts'][i]['id']} != {contract_id}.")

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Next Confirmation Step process."):
            """
            Tender platform authorization for Next Confirmation Step process.
            As result get Tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Next Confirmation Step process."):
            """
            Send request to BPE host to create a Next Confirmation Step process.
            """

            """According to FR.COM-6.19.1: use 'buyer' role."""
            synchronous_result = next_confirmation_step_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=operation_id,
                cpid=cpid,
                ocid=ocid,
                entity="contract",
                entity_id=contract_id,
                entity_token=contract_token,
                role="buyer",
                test_mode=True
            )

            platform_message_1 = get_message_for_platform(operation_id)
            allure.attach(str(platform_message_1), "Message 1 for platform, initiator = platform.")

            message = get_message_for_platform(ocid=ocid, initiator="platform")
            for q in range(len(message)):
                if "outcomes" in message[q]['data']:
                    if "requests" in message[q]['data']['outcomes']:
                        paltform_message_2 = message[q]
            allure.attach(str(paltform_message_2), "Message 2 for platform initiator = platform.")

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
                             f'the Next Confirmation Step process.'):
                """
                Check the message for platform.
                """
                actual_message_1 = platform_message_1
                actual_message_2 = paltform_message_2

                try:
                    """
                    Build expected message for platform.
                    """
                    expected_message = copy.deepcopy(NextConfirmationStepMessage(
                        environment=environment,
                        cpid=cpid,
                        ocid=ocid,
                        test_mode=True
                    ))

                    expected_platform_message = expected_message.build_expected_platform_message(actual_message_1)
                    expected_bpe_message = expected_message.build_expected_bpe_message(actual_message_2, 9)
                except ValueError:
                    raise ValueError("Impossible to build expected message for platform.")

                with allure.step('Compare actual and expected message for platform.'):
                    allure.attach(json.dumps(actual_message_1), "Actual platform message 1.")
                    allure.attach(json.dumps(expected_platform_message), "Expected platform message 1.")

                    assert actual_message_1 == expected_platform_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

                    allure.attach(json.dumps(actual_message_2), "Actual platform message 2.")
                    allure.attach(json.dumps(expected_bpe_message), "Expected platform message 2.")

                    assert actual_message_2 == expected_bpe_message, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.3. Check AP release.'):
                """
                Compare actual AP release and expected AP release.
                """
                actual_ap_release = requests.get(url=ap_url).json()

                try:
                    """
                    Build expected AP release.
                    """
                    expected_release = copy.deepcopy(NextConfirmationStepRelease(environment, ocid))
                    expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
                except ValueError:
                    raise ValueError("Impossible to build expected AP release.")

                with allure.step("Compare actual and expected AP release."):
                    allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
                    allure.attach(json.dumps(expected_ap_release), "Expected AP release.")

                    assert actual_ap_release == expected_ap_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FE release.'):
                """
                Compare actual FE release and expected FE release.
                """
                actual_fe_release = requests.get(url=fe_url).json()

                try:
                    """
                    Build expected FE release.
                    """
                    expected_fe_release = expected_release.build_expected_fe_release(
                        previous_fe_release, actual_fe_release, actual_message_1, connect_to_orchestrator,
                        connect_to_submission, country, pmd
                    )
                except ValueError:
                    raise ValueError("Impossible to build expected FE release.")

                with allure.step("Compare actual and expected FE release."):
                    allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
                    allure.attach(json.dumps(expected_fe_release), "Expected FE release.")

                    assert actual_fe_release == expected_fe_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

            with allure.step(f'# {step_number}.4. Check FA release.'):
                """
                Compare actual FA release and expected FA release.
                """
                actual_fa_release = requests.get(url=fa_url).json()

                try:
                    """
                    Build expected FA release.
                    """
                    expected_fa_release = expected_release.build_expected_fa_release(
                        previous_fa_release
                    )
                except ValueError:
                    raise ValueError("Impossible to build expected FA release.")

                with allure.step("Compare actual and expected FA release."):
                    allure.attach(json.dumps(actual_fa_release), "Actual Fa release.")
                    allure.attach(json.dumps(expected_fa_release), "Expected Fa release.")

                    assert actual_fa_release == expected_fa_release, \
                        allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
                                      f"cpid = '{cpid}' and operation_id = '{operation_id}' "
                                      f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")

        # try:
        #     """
        #     CLean up the database.
        #     """
        #     # Clean after Next Confirmation Step process:
        #     cleanup_orchestrator_steps_by_cpid_and_operationid(connect_to_orchestrator, cpid, operation_id)
        #
        #     cleanup_table_of_services_for_issuing_framework(
        #         connect_to_ocds, connect_to_access, connect_to_contracting, cpid
        #     )
        # except ValueError:
        #     raise ValueError("Impossible to cLean up the database.")

    # @allure.testcase(url="")
    # @allure.title("Check records: based on required data model.")
    # def test_case_2(self, get_parameters, connect_to_keyspace, create_confirmation_response_by_buyer_tc_2):
    #
    #     environment = get_parameters[0]
    #     bpe_host = get_parameters[2]
    #     country = get_parameters[4]
    #     pmd = get_parameters[6]
    #
    #     connect_to_ocds = connect_to_keyspace[0]
    #     connect_to_orchestrator = connect_to_keyspace[1]
    #     connect_to_access = connect_to_keyspace[2]
    #     connect_to_submission = connect_to_keyspace[6]
    #     connect_to_contracting = connect_to_keyspace[7]
    #
    #     cpid = create_confirmation_response_by_buyer_tc_2[0]
    #     ap_url = create_confirmation_response_by_buyer_tc_2[4]
    #     fa_url = create_confirmation_response_by_buyer_tc_2[5]
    #     ocid = create_confirmation_response_by_buyer_tc_2[23]
    #     fe_url = create_confirmation_response_by_buyer_tc_2[24]
    #     contract_id = create_confirmation_response_by_buyer_tc_2[28]
    #     contract_token = create_confirmation_response_by_buyer_tc_2[29]
    #
    #     previous_ap_release = requests.get(url=ap_url).json()
    #     previous_fa_release = requests.get(url=fa_url).json()
    #     previous_fe_release = requests.get(url=fe_url).json()
    #
    #     """
    #     VR.COM-1.17.2: Check FE state.
    #     """
    #     if previous_fe_release['releases'][0]['tender']['status'] == "active" and \
    #             previous_fe_release['releases'][0]['tender']['statusDetails'] == "evaluation":
    #         pass
    #     else:
    #         raise ValueError(f"FE release has invalid state: {previous_fe_release['releases'][0]['tender']['status']} "
    #                          f"and {previous_fe_release['releases'][0]['tender']['statusDetails']}.")
    #
    #     """
    #     VR.COM-6.8.2: Check Contract state.
    #     """
    #     for i in range(len(previous_fe_release['releases'][0]['contracts'])):
    #         if previous_fe_release['releases'][0]['contracts'][i]['id'] == contract_id:
    #             if previous_fe_release['releases'][0]['contracts'][i]['status'] == "pending" and \
    #                     previous_fe_release['releases'][0]['contracts'][i]['statusDetails'] == "issued":
    #                 pass
    #             else:
    #                 raise ValueError(f"Contract {contract_id} has invalid state: "
    #                                  f"{previous_fe_release['releases'][0]['contracts'][i]['status']} and"
    #                                  f"{previous_fe_release['releases'][0]['contracts'][i]['statusDetails']}.")
    #         else:
    #             raise ValueError(f"Incorrect contract id into FE release: "
    #                              f"{previous_fe_release['releases'][0]['contracts'][i]['id']} != {contract_id}.")
    #
    #     step_number = 1
    #     with allure.step(f"# {step_number}. Authorization platform one: Next Confirmation Step process."):
    #         """
    #         Tender platform authorization for Next Confirmation Step process.
    #         As result get Tender platform's access token and process operation-id.
    #         """
    #         platform_one = PlatformAuthorization(bpe_host)
    #         access_token = platform_one.get_access_token_for_platform_one()
    #         operation_id = platform_one.get_x_operation_id(access_token)
    #
    #     step_number += 1
    #     with allure.step(f"# {step_number}. Send a request to create a Next Confirmation Step process."):
    #         """
    #         Send request to BPE host to create a Next Confirmation Step process.
    #         """
    #
    #         """According to FR.COM-6.19.1: use 'buyer' role."""
    #         synchronous_result = next_confirmation_step_process(
    #             host=bpe_host,
    #             access_token=access_token,
    #             x_operation_id=operation_id,
    #             cpid=cpid,
    #             ocid=ocid,
    #             entity="contract",
    #             entity_id=contract_id,
    #             entity_token=contract_token,
    #             role="buyer",
    #             test_mode=True
    #         )
    #
    #         platform_message_1 = get_message_for_platform(operation_id)
    #         allure.attach(str(platform_message_1), "Message 1 for platform, initiator = platform.")
    #
    #         message = get_message_for_platform(ocid=ocid, initiator="platform")
    #         for q in range(len(message)):
    #             if "outcomes" in message[q]['data']:
    #                 if "requests" in message[q]['data']['outcomes']:
    #                     paltform_message_2 = message[q]
    #         allure.attach(str(paltform_message_2), "Message 2 for platform initiator = platform.")
    #
    #     step_number += 1
    #     with allure.step(f"# {step_number}. See result"):
    #         """
    #         Check the results of TestCase.
    #         """
    #
    #         with allure.step(f"# {step_number}.1. Check status code"):
    #             """
    #             Check the status code of sending the request.
    #             """
    #             with allure.step('Compare actual status code and expected status code '
    #                              'of sending request.'):
    #                 allure.attach(str(synchronous_result.status_code), "Actual status code.")
    #                 allure.attach(str(202), "Expected status code.")
    #                 assert synchronous_result.status_code == 202
    #
    #         with allure.step(f'# {step_number}.2. Check the message for the platform,'
    #                          f'the Next Confirmation Step process.'):
    #             """
    #             Check the message for platform.
    #             """
    #             actual_message_1 = platform_message_1
    #             actual_message_2 = paltform_message_2
    #
    #             try:
    #                 """
    #                 Build expected message for platform.
    #                 """
    #                 expected_message = copy.deepcopy(NextConfirmationStepMessage(
    #                     environment=environment,
    #                     cpid=cpid,
    #                     ocid=ocid,
    #                     test_mode=True
    #                 ))
    #
    #                 expected_platform_message = expected_message.build_expected_platform_message(actual_message_1)
    #                 expected_bpe_message = expected_message.build_expected_bpe_message(actual_message_2, 1)
    #             except ValueError:
    #                 raise ValueError("Impossible to build expected message for platform.")
    #
    #             with allure.step('Compare actual and expected message for platform.'):
    #                 allure.attach(json.dumps(actual_message_1), "Actual platform message 1.")
    #                 allure.attach(json.dumps(expected_platform_message), "Expected platform message 1.")
    #
    #                 assert actual_message_1 == expected_platform_message, \
    #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
    #                                   f"cpid = '{cpid}' ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
    #
    #                 allure.attach(json.dumps(actual_message_2), "Actual platform message 2.")
    #                 allure.attach(json.dumps(expected_bpe_message), "Expected platform message 2.")
    #
    #                 assert actual_message_2 == expected_bpe_message, \
    #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
    #                                   f"cpid = '{cpid}' ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
    #
    #         with allure.step(f'# {step_number}.3. Check AP release.'):
    #             """
    #             Compare actual AP release and expected AP release.
    #             """
    #             actual_ap_release = requests.get(url=ap_url).json()
    #
    #             try:
    #                 """
    #                 Build expected AP release.
    #                 """
    #                 expected_release = copy.deepcopy(NextConfirmationStepRelease(environment, ocid))
    #                 expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
    #             except ValueError:
    #                 raise ValueError("Impossible to build expected AP release.")
    #
    #             with allure.step("Compare actual and expected AP release."):
    #                 allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
    #                 allure.attach(json.dumps(expected_ap_release), "Expected AP release.")
    #
    #                 assert actual_ap_release == expected_ap_release, \
    #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
    #                                   f"cpid = '{cpid}' and operation_id = '{operation_id}' "
    #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
    #
    #         with allure.step(f'# {step_number}.4. Check FE release.'):
    #             """
    #             Compare actual FE release and expected FE release.
    #             """
    #             actual_fe_release = requests.get(url=fe_url).json()
    #
    #             try:
    #                 """
    #                 Build expected FE release.
    #                 """
    #                 expected_fe_release = expected_release.build_expected_fe_release(
    #                     previous_fe_release, actual_fe_release, actual_message_1, connect_to_orchestrator,
    #                     connect_to_submission, country, pmd
    #                 )
    #             except ValueError:
    #                 raise ValueError("Impossible to build expected FE release.")
    #
    #             with allure.step("Compare actual and expected FE release."):
    #                 allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
    #                 allure.attach(json.dumps(expected_fe_release), "Expected FE release.")
    #
    #                 assert actual_fe_release == expected_fe_release, \
    #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
    #                                   f"cpid = '{cpid}' and operation_id = '{operation_id}' "
    #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
    #
    #         with allure.step(f'# {step_number}.4. Check FA release.'):
    #             """
    #             Compare actual FA release and expected FA release.
    #             """
    #             actual_fa_release = requests.get(url=fa_url).json()
    #
    #             try:
    #                 """
    #                 Build expected FA release.
    #                 """
    #                 expected_fa_release = expected_release.build_expected_fa_release(
    #                     previous_fa_release
    #                 )
    #             except ValueError:
    #                 raise ValueError("Impossible to build expected FA release.")
    #
    #             with allure.step("Compare actual and expected FA release."):
    #                 allure.attach(json.dumps(actual_fa_release), "Actual Fa release.")
    #                 allure.attach(json.dumps(expected_fa_release), "Expected Fa release.")
    #
    #                 assert actual_fa_release == expected_fa_release, \
    #                     allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
    #                                   f"cpid = '{cpid}' and operation_id = '{operation_id}' "
    #                                   f"ALLOW FILTERING;", "Cassandra DataBase: steps of process.")
    #
    #     try:
    #         """
    #         CLean up the database.
    #         """
    #         # Clean after Next Confirmation Step process:
    #         cleanup_orchestrator_steps_by_cpid_and_operationid(connect_to_orchestrator, cpid, operation_id)
    #
    #         cleanup_table_of_services_for_issuing_framework(
    #             connect_to_ocds, connect_to_access, connect_to_contracting, cpid
    #         )
    #     except ValueError:
    #         raise ValueError("Impossible to cLean up the database.")
