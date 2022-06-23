import json

import bson


def get_payload_model(connect_to_mongo_test_cluster, country, process, pmd):
    """Connect to  keyspace."""

    db = connect_to_mongo_test_cluster['domain_models']

    # Choose table.
    collection = db['domain_models']

    value = collection.find_one(
        {
            "country": country,
            "process": process,
            "pmd": pmd
        }
    )

    return value['payload']
