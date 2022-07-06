pytest_plugins = [
    "fixtures_collection.parameters_for_procedure",
    "fixtures_collection.cassandra_fixtures",
    "fixtures_collection.mongo_fixtures",
    "fixtures_collection.prepare_some_procedure",
    "fixtures_collection.prepare_currency",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_outsource_pn_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_relation_ap_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_update_ap_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_create_fe_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_amend_fe_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_create_submission_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_submission_period_end_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_qualification_declare_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_qualification_consideration_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_qualification_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_qualification_protocol_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_complete_qualification_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_issuing_framework_process",
    "fixtures_collection.prepare_procedure.framework_agreement.prepare_confirmation_response_by_buyer_process",
    "fixtures_collection.prepare_procedure.budget.prepare_create_ei_process",
    "fixtures_collection.prepare_procedure.budget.prepare_confirm_ei_process",
]
