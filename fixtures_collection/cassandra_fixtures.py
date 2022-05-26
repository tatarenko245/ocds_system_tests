"""Prepare some fixtures."""
import os
import pytest
from cassandra import ProtocolVersion
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from fixtures_collection.get_hosts import get_hosts


@pytest.fixture(scope="class")
def log_in_database():
    """Log in the database."""

    environment = os.getenv("ENVIRONMENT")
    hosts = get_hosts(environment)
    database_host = hosts[0]
    cassandra_username = os.getenv("CASSANDRA_USERNAME")
    cassandra_password = os.getenv("CASSANDRA_PASSWORD")

    auth_provider = PlainTextAuthProvider(
        username=cassandra_username,
        password=cassandra_password
    )

    cluster = Cluster(
        contact_points=[database_host],
        auth_provider=auth_provider,
        protocol_version=ProtocolVersion.V4)
    return cluster


@pytest.fixture(scope="class")
def connect_to_keyspace(log_in_database):
    """Connect to  keyspace."""

    ocds_keyspace = log_in_database.connect('ocds')
    orchestrator_keyspace = log_in_database.connect('orchestrator')
    access_keyspace = log_in_database.connect('access')
    clarification_keyspace = log_in_database.connect('clarification')
    dossier_keyspace = log_in_database.connect('dossier')
    qualification_keyspace = log_in_database.connect('qualification')
    submission_keyspace = log_in_database.connect('submission')
    contracting_keyspace = log_in_database.connect('contracting')

    yield \
        ocds_keyspace,\
        orchestrator_keyspace,\
        access_keyspace,\
        clarification_keyspace, \
        dossier_keyspace,\
        qualification_keyspace, \
        submission_keyspace, \
        contracting_keyspace

    ocds_keyspace.shutdown()
    print(f"The connection to {ocds_keyspace} has been disconnected.")

    orchestrator_keyspace.shutdown()
    print(f"The connection to {orchestrator_keyspace} has been disconnected.")

    access_keyspace.shutdown()
    print(f"The connection to {access_keyspace} has been disconnected.")

    clarification_keyspace.shutdown()
    print(f"The connection to {clarification_keyspace} has been disconnected.")

    dossier_keyspace.shutdown()
    print(f"The connection to {dossier_keyspace} has been disconnected.")

    qualification_keyspace.shutdown()
    print(f"The connection to {qualification_keyspace} has been disconnected.")

    submission_keyspace.shutdown()
    print(f"The connection to {submission_keyspace} has been disconnected.")

    contracting_keyspace.shutdown()
    print(f"The connection to {contracting_keyspace} has been disconnected.")
