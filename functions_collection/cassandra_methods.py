import copy
import datetime
import json
import uuid


def cleanup_table_of_services_for_expenditure_item(connect_to_ocds, cp_id):
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cp_id}';").one()
    connect_to_ocds.execute(f"DELETE FROM budget_ei WHERE cp_id='{cp_id}';")
    connect_to_ocds.execute(f"DELETE FROM notice_budget_release WHERE cp_id='{cp_id}';")
    connect_to_ocds.execute(f"DELETE FROM notice_budget_offset WHERE cp_id='{cp_id}';")
    connect_to_ocds.execute(f"DELETE FROM notice_budget_compiled_release WHERE cp_id='{cp_id}';")


def cleanup_ocds_orchestrator_operation_step_by_operation_id(connect_to_ocds, operation_id):
    get_process_id = connect_to_ocds.execute(
        f"SELECT * FROM orchestrator_operation WHERE operation_id = '{operation_id}';").one()
    process_id = get_process_id.process_id
    connect_to_ocds.execute(f"DELETE FROM orchestrator_operation_step WHERE process_id = '{process_id}';")


def get_process_id_by_operation_id(connect_to_ocds, operation_id):
    get_process_id = connect_to_ocds.execute(
        f"SELECT * FROM orchestrator_operation WHERE operation_id = '{operation_id}';").one()
    process_id = get_process_id.process_id
    return process_id


def cleanup_table_of_services_for_financial_source(connect_to_ocds, cp_id):
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cp_id}';").one()
    connect_to_ocds.execute(f"DELETE FROM budget_ei WHERE cp_id='{cp_id}';")
    connect_to_ocds.execute(f"DELETE FROM budget_fs WHERE cp_id='{cp_id}';")
    connect_to_ocds.execute(f"DELETE FROM notice_budget_release WHERE cp_id='{cp_id}';")
    connect_to_ocds.execute(f"DELETE FROM notice_budget_offset WHERE cp_id='{cp_id}';")
    connect_to_ocds.execute(f"DELETE FROM notice_budget_compiled_release WHERE cp_id='{cp_id}';")


def cleanup_table_of_services_for_planning_notice(connect_to_ocds, connect_to_access, cp_id):
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cp_id}';").one()
    connect_to_ocds.execute(f"DELETE FROM budget_fs WHERE cp_id='{cp_id}';")
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cp_id}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cp_id}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cp_id}';")
    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cp_id}';")


def get_max_duration_of_fa_from_access_rules(connect_to_access, country, pmd):
    value = connect_to_access.execute(
        f"""SELECT value FROM access.rules WHERE 
        country ='{country}' and pmd='{pmd}' and operation_type='all' and parameter ='maxDurationOfFA' 
        ALLOW FILTERING;""").one()
    return value.value


def cleanup_table_of_services_for_aggregated_plan(connect_to_ocds, connect_to_access, cpid):
    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def cleanup_orchestrator_steps_by_cpid(connect_to_orchestrator, cpid):
    connect_to_orchestrator.execute(f"DELETE FROM steps WHERE cpid = '{cpid}';")


def cleanup_orchestrator_steps_by_cpid_and_operationid(connect_to_orchestrator, cpid, operation_id):
    connect_to_orchestrator.execute(f"DELETE FROM steps WHERE cpid = '{cpid}' AND operation_id = '{operation_id}';")


def cleanup_table_of_services_for_outsourcing_planning_notice(connect_to_ocds, connect_to_access, cpid):
    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def cleanup_table_of_services_for_relation_aggregated_plan(connect_to_ocds, connect_to_access, cpid):
    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def get_parameter_from_clarification_rules(connect_to_clarification, country, pmd, operation_type, parameter):
    value = connect_to_clarification.execute(
        f"""SELECT "value" FROM rules WHERE "country"='{country}' AND "pmd" = '{pmd}' AND
        "operation_type" = '{operation_type}' AND "parameter" = '{parameter}';""").one()
    return value.value


def fe_enquiry_period_end_date(pre_qualification_period_end_date, interval_seconds: int):
    duration_date_end = datetime.datetime.strptime(
        pre_qualification_period_end_date, '%Y-%m-%dT%H:%M:%SZ') - datetime.timedelta(seconds=interval_seconds)
    end_date = duration_date_end.strftime('%Y-%m-%dT%H:%M:%SZ')
    return end_date


def cleanup_table_of_services_for_framework_establishment(
        connect_to_ocds, connect_to_access, connect_to_clarification, connect_to_dossier, cpid):
    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_dossier.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_clarification.execute(f"DELETE FROM periods WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def cleanup_table_of_services_for_create_submission(
        connect_to_ocds, connect_to_access, connect_to_dossier, cpid):
    """ CLean up the tables of process."""

    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_dossier.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def cleanup_table_of_services_for_submission_period_end(
        connect_to_ocds, connect_to_access, connect_to_dossier, connect_to_clarification, connect_to_qualification,
        cpid):
    """ CLean up the tables of process."""

    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_dossier.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_dossier.execute(f"DELETE FROM submission WHERE cpid='{cpid}';")
    connect_to_clarification.execute(f"DELETE FROM periods WHERE cpid='{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM qualifications WHERE cpid='{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def cleanup_table_of_services_for_qualification_declare(
        connect_to_ocds, connect_to_access, connect_to_qualification, cpid):
    """ CLean up the tables of process."""

    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM qualifications WHERE cpid='{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def cleanup_table_of_services_for_qualification_consideration(
        connect_to_ocds, connect_to_access, connect_to_qualification, cpid):
    """ CLean up the tables of process."""

    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM qualifications WHERE cpid='{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def cleanup_table_of_services_for_qualification(
        connect_to_ocds, connect_to_access, connect_to_qualification, connect_to_dossier, cpid):
    """ CLean up the tables of process."""

    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM qualifications WHERE cpid='{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_dossier.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_dossier.execute(f"DELETE FROM submission WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def get_parameter_from_submission_rules(connect_to_submission, country, pmd, operation_type, parameter):
    value = connect_to_submission.execute(
        f"""SELECT "value" FROM rules WHERE "country"='{country}' AND "pmd" = '{pmd}' AND
        "operation_type" = '{operation_type}' AND "parameter" = '{parameter}';""").one()
    return value.value


def cleanup_table_of_services_for_qualification_protocol(
        connect_to_ocds, connect_to_access, connect_to_submission, connect_to_qualification, connect_to_dossier,
        connect_to_contracting, cpid):
    """ CLean up the tables of process."""

    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_submission.execute(f"DELETE FROM invitations WHERE cpid = '{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM qualifications WHERE cpid='{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_dossier.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_dossier.execute(f"DELETE FROM submission WHERE cpid='{cpid}';")
    connect_to_contracting.execute(f"DELETE FROM fc WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def get_value_from_qualification_rules(connect_to_qualification, country, pmd, operation_type, parameter):
    """ Get some 'value' from qualification.qualification_rules"""

    value = connect_to_qualification.execute(
        f"""SELECT "value" FROM qualification_rules WHERE "country"='{country}' AND "pmd" = '{pmd}' AND
        "operation_type" = '{operation_type}' AND "parameter" = '{parameter}';""").one()
    return value.value


def set_value_into_qualification_rules(connect_to_qualification, value, country, pmd, operation_type, parameter):
    """ Set some 'value' into qualification.qualification_rules"""

    connect_to_qualification.execute(
        f"""UPDATE qualification_rules SET value = '{value}' WHERE "country"='{country}' AND "pmd" ='{pmd}'
        AND "operation_type" = '{operation_type}' AND "parameter" = '{parameter}';""").one()


def cleanup_table_of_services_for_complete_qualification(
        connect_to_ocds, connect_to_access, connect_to_submission, connect_to_qualification, connect_to_dossier, cpid):
    """ CLean up the tables of process."""

    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_submission.execute(f"DELETE FROM invitations WHERE cpid = '{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM qualifications WHERE cpid='{cpid}';")
    connect_to_qualification.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_dossier.execute(f"DELETE FROM period WHERE cpid='{cpid}';")
    connect_to_dossier.execute(f"DELETE FROM submission WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def get_value_from_dossier_rules(connect_to_dossier, country, pmd, operation_type, parameter):
    """ Get some 'value' from qualification.qualification_rules"""

    value = connect_to_dossier.execute(
        f"""SELECT "value" FROM rules WHERE "country"='{country}' AND "pmd" = '{pmd}' AND
        "operation_type" = '{operation_type}' AND "parameter" = '{parameter}';""").one()
    return value.value


def set_value_into_dossier_rules(connect_to_dossier, value, country, pmd, operation_type, parameter):
    """ Set some 'value' into dossier.rules"""

    connect_to_dossier.execute(
        f"""UPDATE rules SET value = '{value}' WHERE "country"='{country}' AND "pmd" ='{pmd}'
        AND "operation_type" = '{operation_type}' AND "parameter" = '{parameter}';""").one()


def cleanup_table_of_services_for_issuing_framework(
        connect_to_ocds, connect_to_access, connect_to_contracting, cpid):
    """ CLean up the tables of process."""

    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_contracting.execute(f"DELETE FROM fc WHERE cpid='{cpid}';")
    connect_to_contracting.execute(f"DELETE FROM confirmation_requests WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def cleanup_table_of_services_for_create_confirmation_response(
        connect_to_ocds, connect_to_access, connect_to_contracting, cpid):
    """ CLean up the tables of process."""

    connect_to_access.execute(f"DELETE FROM tenders WHERE cpid='{cpid}';")
    connect_to_contracting.execute(f"DELETE FROM fc WHERE cpid='{cpid}';")
    connect_to_contracting.execute(f"DELETE FROM confirmation_requests WHERE cpid='{cpid}';")
    connect_to_contracting.execute(f"DELETE FROM confirmation_responses WHERE cpid='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM orchestrator_context WHERE cp_id='{cpid}';").one()
    connect_to_ocds.execute(f"DELETE FROM notice_release WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_offset WHERE cp_id='{cpid}';")
    connect_to_ocds.execute(f"DELETE FROM notice_compiled_release WHERE cp_id='{cpid}';")


def get_value_from_orchestrator_decisiontable(connect_to_orchestrator, key):
    """ Get some 'output' from orchestrator.decision_table"""

    value = connect_to_orchestrator.execute(
        f"""SELECT "output" FROM decision_table WHERE key = '{key}';""").one()
    if value is None:
        return value
    else:
        return value.output


def get_value_from_ocds_budgetrules(connect_to_ocds, key, parameter):
    """ Get some 'value' from ocds.budget_rules"""

    value = connect_to_ocds.execute(
        f"""SELECT "value" FROM budget_rules WHERE key = '{key}' AND parameter = '{parameter}';""").one()
    if value is None:
        return value
    else:
        return value.value


def get_cpid_from_orchestrator_steps(connect_to_orchestrator, operation_id):
    value = connect_to_orchestrator.execute(f"SELECT * FROM orchestrator.steps WHERE operation_id='{operation_id}' "
                                            f"ALLOW FILTERING;").one()

    cpid = value.cpid
    return cpid


def get_some_parameter_from_orchestrator_steps_by_cpid_and_operationid(
        connect_to_orchestrator, cpid, operation_id, task_id):
    process_data = connect_to_orchestrator.execute(
        f"SELECT * FROM steps WHERE cpid = '{cpid}' AND operation_id = '{operation_id}';"
    ).one()

    process_id = process_data.process_id

    value = connect_to_orchestrator.execute(
        f"SELECT * FROM steps WHERE cpid = '{cpid}' AND operation_id = '{operation_id}' "
        f"AND process_id = '{process_id}' AND task_id = '{task_id}';").one()

    request_data = json.loads(value.request)
    response_data = json.loads(value.response)

    return request_data, response_data


def set_tender_status_for_ocds_budgetei(connect_to_ocds, cpid, tender_status: str):

    previous_data = connect_to_ocds.execute(f"SELECT * FROM budget_ei WHERE cp_id = '{cpid}';").one()

    previous_token_entity = previous_data.token_entity
    previous_json_data = json.loads(previous_data.json_data)

    new_json_data = copy.deepcopy(previous_json_data)

    new_json_data['tender']['status'] = tender_status

    connect_to_ocds.execute(f"""UPDATE budget_ei SET json_data = '{json.dumps(new_json_data)}' WHERE  
    cp_id = '{cpid}' AND token_entity = {previous_token_entity};""").one()
