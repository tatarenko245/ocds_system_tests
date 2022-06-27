"""Prepare some fixtures."""
import os
import pytest

from pymongo import MongoClient


@pytest.fixture(scope="class")
def connect_to_mongo_test_cluster():
    """Connect to the cluster."""

    database_host = os.getenv("TEST_SERVER_HOST")
    cluster = MongoClient(host=database_host, port=27017)

    yield cluster

    cluster.close()
    print(f"The connection to {cluster} has been disconnected.")
