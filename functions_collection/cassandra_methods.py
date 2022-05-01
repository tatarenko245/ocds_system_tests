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
