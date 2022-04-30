import pytest


def pytest_addoption(parser):
    parser.addoption("--country", action="store", type=str)
    parser.addoption("--language", action="store", type=str)
    parser.addoption("--environment", action="store", type=str)
    parser.addoption("--pmd", action="store", type=str)
    parser.addoption("--cassandra_username", action="store", type=str)
    parser.addoption("--cassandra_password", action="store", type=str)


@pytest.fixture(scope="session")
def parse_country(request):
    """Handler for --additional_value parameter"""
    country = request.config.getoption("--country")
    return country


@pytest.fixture(scope="session")
def parse_language(request):
    """Handler for --additional_value parameter"""
    language = request.config.getoption("--language")
    # allure.attach(language, "Language")
    return language


@pytest.fixture(scope="session")
def parse_environment(request):
    """Handler for --additional_value parameter"""
    environment = request.config.getoption("--environment")
    return environment


@pytest.fixture(scope="session")
def parse_pmd(request):
    """Handler for --additional_value parameter"""
    return request.config.getoption("--pmd")


@pytest.fixture(scope="session")
def parse_cassandra_username(request):
    """Handler for --additional_value parameter"""
    cassandra_username = request.config.getoption("--cassandra_username")
    return cassandra_username


@pytest.fixture(scope="session")
def parse_cassandra_password(request):
    """Handler for --additional_value parameter"""
    cassandra_password = request.config.getoption("--cassandra_password")
    return cassandra_password
