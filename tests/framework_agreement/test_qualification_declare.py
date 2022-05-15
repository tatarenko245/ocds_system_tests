import copy
import json
import allure
import requests

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.cassandra_methods import cleanup_orchestrator_steps_by_cpid, \
    cleanup_table_of_services_for_create_submission
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_submission_process, qualification_declare_process
from functions_collection.some_functions import get_id_token_of_qualification_in_pending_awaiting_state
from messages_collection.framework_agreement.create_submission_message import CreateSubmissionMessage
from payloads_collection.framework_agreement.create_submission_payload import CreateSubmissionPayload
from payloads_collection.framework_agreement.qualification_declare_payload import \
    QualificationDeclareNonConflictOfInterestPayload
from releases_collection.framework_agreement.create_submission_release import CreateSubmissionRelease


@allure.parent_suite("Framework Agreement")
@allure.suite("Declaration")
@allure.severity("Critical")
@allure.testcase(url="")
class TestDeclarationNonConflictInterest:
    # @allure.title("Check records: based on full data model.")
    # @allure.testcase(
    #     url="https://docs.google.com/spreadsheets/d/1taw-E-4lryj80XYGdVwi1G-C2U6SQyilBuziGjXGyME/edit#gid=0",
    #     name="Why this test case was fall down?")
    # def test_case_1(self, get_parameters, connect_to_keyspace, submission_period_end_tc_1):
    #
    #     environment = get_parameters[0]
    #     bpe_host = get_parameters[2]
    #     service_host = get_parameters[3]
    #
    #     connect_to_ocds = connect_to_keyspace[0]
    #     connect_to_orchestrator = connect_to_keyspace[1]
    #     connect_to_access = connect_to_keyspace[2]
    #     connect_to_dossier = connect_to_keyspace[4]
    #
    #     cpid = submission_period_end_tc_1[0]
    #     ap_url = submission_period_end_tc_1[4]
    #     fa_url = submission_period_end_tc_1[5]
    #     ocid = submission_period_end_tc_1[23]
    #     fe_url = submission_period_end_tc_1[24]
    #     submission_period_end_message = submission_period_end_tc_1[27]
    #
    #     previous_ap_release = requests.get(url=ap_url).json()
    #     previous_fa_release = requests.get(url=fa_url).json()
    #     previous_fe_release = requests.get(url=fe_url).json()
    #
    #     """Get requirements for Qualification Declare"""
    #     if "criteria" in previous_fe_release['releases'][0]['tender']:
    #         requirements_list = list()
    #         for c in previous_fe_release['releases'][0]['tender']['criteria']:
    #             for c_1 in c:
    #                 if c_1 == "source":
    #                     if c['source'] == "procuringEntity":
    #                         requirement_groups_list = list()
    #                         for rg in c['requirementGroups']:
    #                             for rg_1 in rg:
    #                                 if rg_1 == "id":
    #                                     requirement_groups_list.append(rg['id'])
    #
    #                         for x in range(len(requirement_groups_list)):
    #                             for rr in c['requirementGroups'][x]['requirements']:
    #                                 for rr_1 in rr:
    #                                     if rr_1 == "id":
    #                                         requirements_list.append(rr['id'])
    #     else:
    #         raise KeyError("The 'criteria' array is missed into FE release.")
    #
    #     """Get candidates for Qualification Declare"""
    #     if "qualifications" in previous_fe_release['releases'][0]:
    #         candidates_list = list()
    #         for qu in previous_fe_release['releases'][0]['qualifications']:
    #             if qu['status'] == "pending":
    #                 if qu['statusDetails'] == "awaiting":
    #                     if 'submissions' in previous_fe_release['releases'][0]:
    #                         for s in previous_fe_release['releases'][0]['submissions']['details']:
    #                             if s['id'] == qu['relatedSubmission']:
    #                                 for cand in range(len(s['candidates'])):
    #                                     candidate_dictionary = {
    #                                         "qualification_id": qu['id'],
    #                                         "candidates": s['candidates'][cand]
    #                                     }
    #                                     candidates_list.append(candidate_dictionary)
    #                             else:
    #                                 raise KeyError("The 'submissions' object is missed into FE release.")
    #     else:
    #         raise KeyError("The 'qualifications' array is missed into FE release.")
    #
    #     """Get qualification.id and qualification.token for Qualification Declare"""
    #     qualifications_from_message = get_id_token_of_qualification_in_pending_awaiting_state(
    #         actual_qualifications_array=previous_fe_release['releases'][0]['qualifications'],
    #         feed_point_message=submission_period_end_message
    #     )
    #     qualification_list = list()
    #     for q in qualifications_from_message:
    #         qualification_list.append(q)
    #
    #     """ Depends on quantity of requirements into criteria and
    #     depends on quantity of candidates into Create Submission payload and
    #     depends on quantity of qualifications into FE release, send requests"""
    #     for x in range(len(requirements_list)):
    #         for y in range(len(candidates_list)):
    #             for q in range(len(qualification_list)):
    #                 if qualification_list[q][0] == candidates_list[y]['qualification_id']:
    #
    #                     step_number = x + y + q
    #                     with allure.step(f'# {step_number}. Authorization platform one: Qualification Declare '
    #                                      f'Non Conflict Interest process.'):
    #                         """
    #                         Tender platform authorization for Qualification Declare  Non Conflict Interest process.
    #                         As result get Tender platform's access token and process operation-id.
    #                         """
    #                         platform_one = PlatformAuthorization(bpe_host)
    #                         access_token = platform_one.get_access_token_for_platform_one()
    #                         operation_id = platform_one.get_x_operation_id(access_token)
    #
    #                     step_number += 1
    #                     with allure.step(f'# {step_number}. Send a request to create '
    #                                      f'a Qualification Declare  Non Conflict Interest process.'):
    #                         """
    #                         Send request to BPE host to create a Qualification Declare  Non Conflict Interest process.
    #                         """
    #                         try:
    #                             """
    #                             Build payload for Qualification Declare Non Conflict Interest process.
    #                             """
    #                             payload = copy.deepcopy(QualificationDeclareNonConflictOfInterestPayload(
    #                                 service_host=service_host,
    #                                 requirement_id=requirements_list[x],
    #                                 tenderer_id=candidates_list[y]['candidates']['id'],
    #                                 value=True
    #                             ))
    #
    #                             payload.customize_business_functions(
    #                                 quantity_of_bf=3,
    #                                 quantity_of_bf_documents=3
    #                             )
    #                             payload = payload.build_payload()
    #                         except ValueError:
    #                             ValueError("Impossible to build payload for"
    #                                        "Qualification Declare Non Conflict Interest process.")
    #
    #                         synchronous_result = qualification_declare_process(
    #                             host=bpe_host,
    #                             access_token=access_token,
    #                             x_operation_id=operation_id,
    #                             payload=payload,
    #                             test_mode=True,
    #                             cpid=cpid,
    #                             ocid=ocid,
    #                             qualification_id=qualification_list[q][0],
    #                             qualification_token=qualification_list[q][1]
    #                         )
    #
    #                         message = get_message_for_platform(operation_id)
    #                         allure.attach(str(message), "Message for platform.")
    #
    #                     step_number += 1
    #     # step_number += 1
    #     # with allure.step(f"# {step_number}. See result"):
    #     #     """
    #     #     Check the results of TestCase.
    #     #     """
    #     #
    #     #     with allure.step(f"# {step_number}.1. Check status code"):
    #     #         """
    #     #         Check the status code of sending the request.
    #     #         """
    #     #         with allure.step('Compare actual status code and expected status code of sending request.'):
    #     #             allure.attach(str(synchronous_result.status_code), "Actual status code.")
    #     #             allure.attach(str(202), "Expected status code.")
    #     #             assert synchronous_result.status_code == 202
    #     #
    #     #     with allure.step(f'# {step_number}.2. Check the message for the platform, the Create Submission process.'):
    #     #         """
    #     #         Check the message for platform.
    #     #         """
    #     #         actual_message = message
    #     #
    #     #         try:
    #     #             """
    #     #             Build expected message for platform.
    #     #             """
    #     #             expected_message = copy.deepcopy(CreateSubmissionMessage(
    #     #                 environment=environment,
    #     #                 actual_message=actual_message,
    #     #                 cpid=cpid,
    #     #                 ocid=ocid,
    #     #                 test_mode=True
    #     #             ))
    #     #
    #     #             expected_message = expected_message.build_expected_message()
    #     #         except ValueError:
    #     #             ValueError("Impossible to build expected message for platform.")
    #     #
    #     #         with allure.step('Compare actual and expected message for platform.'):
    #     #             allure.attach(json.dumps(actual_message), "Actual message.")
    #     #             allure.attach(json.dumps(expected_message), "Expected message.")
    #     #
    #     #             assert actual_message == expected_message, \
    #     #                 allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
    #     #                               f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
    #     #                               "Cassandra DataBase: steps of process.")
    #     #     with allure.step(f'# {step_number}.3. Check AP release.'):
    #     #         """
    #     #         Compare previous AP release and actual AP release.
    #     #         """
    #     #         actual_ap_release = requests.get(url=ap_url).json()
    #     #         try:
    #     #             """
    #     #             Build expected AP release.
    #     #             """
    #     #             expected_release = copy.deepcopy(CreateSubmissionRelease())
    #     #             expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
    #     #         except ValueError:
    #     #             ValueError("Impossible to build expected AP release.")
    #     #
    #     #         with allure.step("Compare actual and expected AP release."):
    #     #             allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
    #     #             allure.attach(json.dumps(expected_ap_release), "Expected AP release.")
    #     #
    #     #             allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
    #     #                           f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
    #     #                           "Cassandra DataBase: steps of process.")
    #     #
    #     #     with allure.step(f'# {step_number}.4. Check FE release.'):
    #     #         """
    #     #         Compare previous FE release and actual FE release.
    #     #         """
    #     #         actual_fe_release = requests.get(url=fe_url).json()
    #     #         try:
    #     #             """
    #     #             Build expected FE release.
    #     #             """
    #     #             expected_fe_release = expected_release.build_expected_fe_release(previous_fe_release)
    #     #         except ValueError:
    #     #             ValueError("Impossible to build expected FE release.")
    #     #
    #     #         with allure.step("Compare actual and expected FE release."):
    #     #             allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
    #     #             allure.attach(json.dumps(expected_fe_release), "Expected FE release.")
    #     #
    #     #             assert actual_fe_release == expected_fe_release, \
    #     #                 allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
    #     #                               f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
    #     #                               "Cassandra DataBase: steps of process.")
    #     #
    #     #     with allure.step(f'# {step_number}.4. Check FA release.'):
    #     #         """
    #     #         Compare previous FA release and actual FA release.
    #     #         """
    #     #         actual_fa_release = requests.get(url=fa_url).json()
    #     #         try:
    #     #             """
    #     #             Build expected FA release.
    #     #             """
    #     #             expected_fa_release = expected_release.build_expected_fa_release(previous_fa_release)
    #     #         except ValueError:
    #     #             ValueError("Impossible to build expected FA release.")
    #     #
    #     #         with allure.step("Compare actual and expected FA release."):
    #     #             allure.attach(json.dumps(actual_fa_release), "Actual Fa release.")
    #     #             allure.attach(json.dumps(expected_fa_release), "Expected Fa release.")
    #     #
    #     #             assert actual_fa_release == expected_fa_release, \
    #     #                 allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
    #     #                               f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
    #     #                               "Cassandra DataBase: steps of process.")
    #     # try:
    #     #     """
    #     #     CLean up the database.
    #     #     """
    #     #     # Clean after Create Submission process:
    #     #     cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
    #     #
    #     #     cleanup_table_of_services_for_create_submission(
    #     #         connect_to_ocds, connect_to_access, connect_to_dossier, cpid)
    #     # except ValueError:
    #     #     ValueError("Impossible to cLean up the database.")

    @allure.title("Check records: based on required data model.")
    def test_case_2(self, get_parameters, connect_to_keyspace, submission_period_end_tc_2):

        environment = get_parameters[0]
        bpe_host = get_parameters[2]
        service_host = get_parameters[3]

        connect_to_ocds = connect_to_keyspace[0]
        connect_to_orchestrator = connect_to_keyspace[1]
        connect_to_access = connect_to_keyspace[2]
        connect_to_dossier = connect_to_keyspace[4]

        cpid = submission_period_end_tc_2[0]
        ap_url = submission_period_end_tc_2[4]
        fa_url = submission_period_end_tc_2[5]
        ocid = submission_period_end_tc_2[23]
        fe_url = submission_period_end_tc_2[24]
        submission_period_end_message = submission_period_end_tc_2[27]

        previous_ap_release = requests.get(url=ap_url).json()
        previous_fa_release = requests.get(url=fa_url).json()
        previous_fe_release = requests.get(url=fe_url).json()

        """Get requirements for Qualification Declare"""
        if "criteria" in previous_fe_release['releases'][0]['tender']:
            requirements_list = list()
            for c in previous_fe_release['releases'][0]['tender']['criteria']:
                for c_1 in c:
                    if c_1 == "source":
                        if c['source'] == "procuringEntity":
                            requirement_groups_list = list()
                            for rg in c['requirementGroups']:
                                for rg_1 in rg:
                                    if rg_1 == "id":
                                        requirement_groups_list.append(rg['id'])

                            for x in range(len(requirement_groups_list)):
                                for rr in c['requirementGroups'][x]['requirements']:
                                    for rr_1 in rr:
                                        if rr_1 == "id":
                                            requirements_list.append(rr['id'])
        else:
            raise KeyError("The 'criteria' array is missed into FE release.")

        """Get candidates for Qualification Declare"""
        if "qualifications" in previous_fe_release['releases'][0]:
            candidates_list = list()
            for qu in previous_fe_release['releases'][0]['qualifications']:
                if qu['status'] == "pending":
                    if qu['statusDetails'] == "awaiting":
                        if 'submissions' in previous_fe_release['releases'][0]:
                            for s in previous_fe_release['releases'][0]['submissions']['details']:
                                if s['id'] == qu['relatedSubmission']:
                                    for cand in range(len(s['candidates'])):
                                        candidate_dictionary = {
                                            "qualification_id": qu['id'],
                                            "candidates": s['candidates'][cand]
                                        }
                                        candidates_list.append(candidate_dictionary)
                                else:
                                    raise KeyError("The 'submissions' object is missed into FE release.")
        else:
            raise KeyError("The 'qualifications' array is missed into FE release.")

        """Get qualification.id and qualification.token for Qualification Declare"""
        qualifications_from_message = get_id_token_of_qualification_in_pending_awaiting_state(
            actual_qualifications_array=previous_fe_release['releases'][0]['qualifications'],
            feed_point_message=submission_period_end_message
        )
        qualification_list = list()
        for q in qualifications_from_message:
            qualification_list.append(q)

        """ Depends on quantity of requirements into criteria and
        depends on quantity of candidates into Create Submission payload and
        depends on quantity of qualifications into FE release, send requests"""
        for x in range(len(requirements_list)):
            for y in range(len(candidates_list)):
                for q in range(len(qualification_list)):
                    if qualification_list[q][0] == candidates_list[y]['qualification_id']:

                        step_number = x + y + q
                        with allure.step(f'# {step_number}. Authorization platform one: Qualification Declare '
                                         f'Non Conflict Interest process.'):
                            """
                            Tender platform authorization for Qualification Declare  Non Conflict Interest process.
                            As result get Tender platform's access token and process operation-id.
                            """
                            platform_one = PlatformAuthorization(bpe_host)
                            access_token = platform_one.get_access_token_for_platform_one()
                            operation_id = platform_one.get_x_operation_id(access_token)

                        step_number += 1
                        with allure.step(f'# {step_number}. Send a request to create '
                                         f'a Qualification Declare  Non Conflict Interest process.'):
                            """
                            Send request to BPE host to create a Qualification Declare  Non Conflict Interest process.
                            """
                            try:
                                """
                                Build payload for Qualification Declare Non Conflict Interest process.
                                """
                                payload = copy.deepcopy(QualificationDeclareNonConflictOfInterestPayload(
                                    service_host=service_host,
                                    requirement_id=requirements_list[x],
                                    tenderer_id=candidates_list[y]['candidates']['id'],
                                    value=True
                                ))

                                payload.customize_business_functions(
                                    quantity_of_bf=1,
                                    quantity_of_bf_documents=0
                                )
                                payload.delete_optional_fields(
                                    "requirementResponse.responder.identifier.uri",
                                    "requirementResponse.responder.businessFunctions.documents",
                                    bf_position=0
                                )
                                payload = payload.build_payload()
                            except ValueError:
                                ValueError("Impossible to build payload for"
                                           "Qualification Declare Non Conflict Interest process.")

                            synchronous_result = qualification_declare_process(
                                host=bpe_host,
                                access_token=access_token,
                                x_operation_id=operation_id,
                                payload=payload,
                                test_mode=True,
                                cpid=cpid,
                                ocid=ocid,
                                qualification_id=qualification_list[q][0],
                                qualification_token=qualification_list[q][1]
                            )

                            message = get_message_for_platform(operation_id)
                            allure.attach(str(message), "Message for platform.")

                        step_number += 1
        # step_number += 1
        # with allure.step(f"# {step_number}. See result"):
        #     """
        #     Check the results of TestCase.
        #     """
        #
        #     with allure.step(f"# {step_number}.1. Check status code"):
        #         """
        #         Check the status code of sending the request.
        #         """
        #         with allure.step('Compare actual status code and expected status code of sending request.'):
        #             allure.attach(str(synchronous_result.status_code), "Actual status code.")
        #             allure.attach(str(202), "Expected status code.")
        #             assert synchronous_result.status_code == 202
        #
        #     with allure.step(f'# {step_number}.2. Check the message for the platform, the Create Submission process.'):
        #         """
        #         Check the message for platform.
        #         """
        #         actual_message = message
        #
        #         try:
        #             """
        #             Build expected message for platform.
        #             """
        #             expected_message = copy.deepcopy(CreateSubmissionMessage(
        #                 environment=environment,
        #                 actual_message=actual_message,
        #                 cpid=cpid,
        #                 ocid=ocid,
        #                 test_mode=True
        #             ))
        #
        #             expected_message = expected_message.build_expected_message()
        #         except ValueError:
        #             ValueError("Impossible to build expected message for platform.")
        #
        #         with allure.step('Compare actual and expected message for platform.'):
        #             allure.attach(json.dumps(actual_message), "Actual message.")
        #             allure.attach(json.dumps(expected_message), "Expected message.")
        #
        #             assert actual_message == expected_message, \
        #                 allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                               f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
        #                               "Cassandra DataBase: steps of process.")
        #     with allure.step(f'# {step_number}.3. Check AP release.'):
        #         """
        #         Compare previous AP release and actual AP release.
        #         """
        #         actual_ap_release = requests.get(url=ap_url).json()
        #         try:
        #             """
        #             Build expected AP release.
        #             """
        #             expected_release = copy.deepcopy(CreateSubmissionRelease())
        #             expected_ap_release = expected_release.build_expected_ap_release(previous_ap_release)
        #         except ValueError:
        #             ValueError("Impossible to build expected AP release.")
        #
        #         with allure.step("Compare actual and expected AP release."):
        #             allure.attach(json.dumps(actual_ap_release), "Actual AP release.")
        #             allure.attach(json.dumps(expected_ap_release), "Expected AP release.")
        #
        #             allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                           f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
        #                           "Cassandra DataBase: steps of process.")
        #
        #     with allure.step(f'# {step_number}.4. Check FE release.'):
        #         """
        #         Compare previous FE release and actual FE release.
        #         """
        #         actual_fe_release = requests.get(url=fe_url).json()
        #         try:
        #             """
        #             Build expected FE release.
        #             """
        #             expected_fe_release = expected_release.build_expected_fe_release(previous_fe_release)
        #         except ValueError:
        #             ValueError("Impossible to build expected FE release.")
        #
        #         with allure.step("Compare actual and expected FE release."):
        #             allure.attach(json.dumps(actual_fe_release), "Actual FE release.")
        #             allure.attach(json.dumps(expected_fe_release), "Expected FE release.")
        #
        #             assert actual_fe_release == expected_fe_release, \
        #                 allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                               f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
        #                               "Cassandra DataBase: steps of process.")
        #
        #     with allure.step(f'# {step_number}.4. Check FA release.'):
        #         """
        #         Compare previous FA release and actual FA release.
        #         """
        #         actual_fa_release = requests.get(url=fa_url).json()
        #         try:
        #             """
        #             Build expected FA release.
        #             """
        #             expected_fa_release = expected_release.build_expected_fa_release(previous_fa_release)
        #         except ValueError:
        #             ValueError("Impossible to build expected FA release.")
        #
        #         with allure.step("Compare actual and expected FA release."):
        #             allure.attach(json.dumps(actual_fa_release), "Actual Fa release.")
        #             allure.attach(json.dumps(expected_fa_release), "Expected Fa release.")
        #
        #             assert actual_fa_release == expected_fa_release, \
        #                 allure.attach(f"SELECT * FROM orchestrator.steps WHERE "
        #                               f"cpid = '{cpid}' and operation_id = '{operation_id}' ALLOW FILTERING;",
        #                               "Cassandra DataBase: steps of process.")
        # try:
        #     """
        #     CLean up the database.
        #     """
        #     # Clean after Create Submission process:
        #     cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid)
        #
        #     cleanup_table_of_services_for_create_submission(
        #         connect_to_ocds, connect_to_access, connect_to_dossier, cpid)
        # except ValueError:
        #     ValueError("Impossible to cLean up the database.")
