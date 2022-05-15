import datetime


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
