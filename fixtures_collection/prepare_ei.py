import pytest

from functions_collection.cassandra_methods import cleanup_ocds_orchestrator_operation_step_by_operation_id, \
    cleanup_table_of_services_for_expenditure_item
from tests.budgets.test_create_ei import TestCreateEi


@pytest.fixture(scope="class")
def create_ei_tc_1(get_credits):
    connect_to_ocds = get_credits[6]
    instance = TestCreateEi().test_case_1
    print("instance ")
    print(instance)
    yield instance
    # Clean after crateEi process:
    cleanup_ocds_orchestrator_operation_step_by_operation_id(
        connect_to_ocds,
        instance[0]
    )

    cleanup_table_of_services_for_expenditure_item(
        connect_to_ocds,
        instance[1]
    )
