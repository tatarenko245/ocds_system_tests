import os

import allure
import pytest

from fixtures_collection.get_hosts import get_hosts
from functions_collection.some_functions import prepare_tender_classification_id


@pytest.fixture(scope="class")
def get_credits():
    environment = os.getenv("ENVIRONMENT")
    country = os.getenv("COUNTRY")
    language = os.getenv("LANGUAGE")
    pmd = os.getenv("PMD")
    cassandra_username = os.getenv("CASSANDRA_USERNAME")
    cassandra_password = os.getenv("CASSANDRA_PASSWORD")

    hosts = get_hosts(environment)
    tender_classification_id = prepare_tender_classification_id()

    allure.attach(environment, "environment")
    allure.attach(hosts[0], "database_host")
    allure.attach(hosts[1], "bpe_host")
    allure.attach(hosts[2], "service_host")
    allure.attach(country, "country")
    allure.attach(language, "Language")
    allure.attach(pmd, "pmd")
    allure.attach(tender_classification_id, "tenderClassificationId")

    yield \
        hosts[0],\
        hosts[1],\
        hosts[2],\
        country,\
        language,\
        pmd,\
        cassandra_username,\
        cassandra_password,\
        tender_classification_id
