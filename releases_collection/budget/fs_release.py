"""Prepare the expected release of the create financial source process, budget."""
import copy
import json

from functions_collection.some_functions import get_value_from_cpvs_dictionary_csv, is_it_uuid, \
    get_value_from_cpv_dictionary_xls, get_value_from_classification_unit_dictionary_csv, \
    generate_tender_classification_id, get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv, get_unique_party_from_list_by_id


class FinancialSourceRelease:
    """This class creates instance of release."""

    def __init__(self, environment, host_to_service, language, cpid, fs_payload, fs_message, actual_fs_release):

        self.environment = environment
        self.host = host_to_service
        self.language = language
        self.cpid = cpid
        self.fs_payload = fs_payload
        self.fs_message = fs_message
        self.actual_fs_release = actual_fs_release

        extensions = None
        publisher_name = None
        publisher_uri = None
        self.__metadata_document_url = None
        try:
            if environment == "dev":
                self.metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"

                extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"
                ]

                publisher_name = "M-Tender"
                publisher_uri = "https://www.mtender.gov.md"

            elif environment == "sandbox":
                self.metadata_budget_url = "http://public.eprocurement.systems/budgets"

                extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.json"
                ]

                publisher_name = "Viešųjų pirkimų tarnyba"
                publisher_uri = "https://vpt.lrv.lt"

        except ValueError:
            raise ValueError("Check your environment: You must use 'dev' or 'sandbox' environment.")

        self.expected_fs_release = {
            "uri": f"{self.metadata_budget_url}/{cpid}/{fs_message['data']['outcomes']['fs'][0]['id']}",

            "version": "1.1",
            "extensions": extensions,
            "publisher": {
                "name": publisher_name,
                "uri": publisher_uri
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": fs_message['data']['operationDate'],
            "releases": [
                {
                    "ocid": fs_message['data']['outcomes']['fs'][0]['id'],

                    "id": f"{fs_message['data']['outcomes']['fs'][0]['id']}-"
                          f"{actual_fs_release['releases'][0]['id'][46:59]}",

                    "date": fs_message['data']['operationDate'],
                    "tag": [
                        "planning"
                    ],
                    "language": language,
                    "initiationType":    "tender",
                    "tender": {
                        "id": "",
                        "status": "active",
                        "statusDetails": "empty"
                    },
                    "parties": [
                        {
                            "id": "",
                            "name": "",
                            "identifier": {
                                "scheme": "",
                                "id": "",
                                "legalName": "",
                                "uri": ""
                            },
                            "address": {
                                "streetAddress": "",
                                "postalCode": "",
                                "addressDetails": {
                                    "country": {
                                        "scheme": "",
                                        "id": "",
                                        "description": "",
                                        "uri": ""
                                    },
                                    "region": {
                                        "scheme": "",
                                        "id": "",
                                        "description": "",
                                        "uri": ""
                                    },
                                    "locality": {
                                        "scheme": "",
                                        "id": "",
                                        "description": "",
                                        "uri": ""
                                    }
                                }
                            },
                            "additionalIdentifiers": [
                                {
                                    "scheme": "",
                                    "id": "",
                                    "legalName": "",
                                    "uri": ""
                                }
                            ],
                            "contactPoint": {
                                "name": "",
                                "email": "",
                                "telephone": "",
                                "faxNumber": "",
                                "url": ""
                            },
                            "roles": [""]
                        }
                    ],
                    "planning": {
                        "budget": {
                            "id": "",
                            "description": "",
                            "period": {
                                "startDate": "",
                                "endDate": ""
                            },
                            "amount": {
                                "amount": 0,
                                "currency": ""
                            },
                            "europeanUnionFunding": {
                                "projectIdentifier": "",
                                "projectName": "",
                                "uri": ""
                            },
                            "isEuropeanUnionFunded": True,
                            "verified": True,
                            "sourceEntity": {
                                "id": "",
                                "name": ""
                            },
                            "project": "",
                            "projectID": "",
                            "uri": ""
                        },
                        "rationale": ""
                    },
                    "relatedProcesses": [
                        {
                            "id": "",
                            "relationship": [
                                "parent"
                            ],
                            "scheme": "ocid",
                            "identifier": cpid,
                            "uri": f"{self.metadata_budget_url}/{cpid}/{cpid}"
                        }
                    ]

                }
            ]
        }

    def build_expected_fs_release(self, fs_payloads_list):
        """Build FS release."""

        # Build the releases.tender object. Enrich or delete optional fields and enrich required fields:
        try:
            """Set permanent id."""

            is_permanent_id_correct = is_it_uuid(self.actual_fs_release['releases'][0]['tender']['id'])
            if is_permanent_id_correct is True:

                self.expected_fs_release['releases'][0]['tender']['id'] = \
                    self.actual_fs_release['releases'][0]['tender']['id']
            else:
                raise ValueError(f"The 'releases[0].tender.id' must be uuid.")
        except KeyError:
            raise KeyError("Mismatch key into path 'releases[0].tender.id'")

        self.expected_fs_release['releases'][0]['tender']['status'] = "active"
        self.expected_fs_release['releases'][0]['tender']['statusDetails'] = "empty"

        # Build the releases.parties array. Enrich or delete optional fields and enrich required fields:
        payer_role_array = list()
        funder_role_array = list()
        for q_0 in range(len(fs_payloads_list)):
            if "buyer" in fs_payloads_list[q_0]:
                funder_role_array.append(copy.deepcopy(self.expected_fs_release['releases'][0]['parties'][0]))

                funder_role_array[q_0]['id'] = f"{fs_payloads_list[q_0]['buyer']['identifier']['scheme']}-" \
                                               f"{fs_payloads_list[q_0]['buyer']['identifier']['id']}"

                funder_role_array[q_0]['name'] = fs_payloads_list[q_0]['buyer']['name']
                funder_role_array[q_0]['identifier']['scheme'] = fs_payloads_list[q_0]['buyer']['identifier']['scheme']
                funder_role_array[q_0]['identifier']['id'] = fs_payloads_list[q_0]['buyer']['identifier']['id']

                funder_role_array[q_0]['identifier']['legalName'] = \
                    fs_payloads_list[q_0]['buyer']['identifier']['legalName']

                funder_role_array[q_0]['address']['streetAddress'] = fs_payloads_list[q_0]['buyer']['address'][
                    'streetAddress']

                if "postalCode" in fs_payloads_list[q_0]['buyer']['address']:

                    funder_role_array[q_0]['address']['postalCode'] = \
                        fs_payloads_list[q_0]['buyer']['address']['postalCode']
                else:
                    del funder_role_array[q_0]['address']['postalCode']

                try:
                    """
                    Prepare addressDetails object for party with funder role.
                    """
                    funder_country_data = get_value_from_country_csv(
                        country=fs_payloads_list[q_0]['buyer']['address']['addressDetails']['country']['id'],
                        language=self.language
                    )
                    expected_funder_country_object = [{
                        "scheme": funder_country_data[2],
                        "id": fs_payloads_list[q_0]['buyer']['address']['addressDetails']['country']['id'],
                        "description": funder_country_data[1],
                        "uri": funder_country_data[3]
                    }]

                    funder_region_data = get_value_from_region_csv(
                        region=fs_payloads_list[q_0]['buyer']['address']['addressDetails']['region']['id'],
                        country=fs_payloads_list[q_0]['buyer']['address']['addressDetails']['country']['id'],
                        language=self.language
                    )
                    expected_funder_region_object = [{
                        "scheme": funder_region_data[2],
                        "id": fs_payloads_list[q_0]['buyer']['address']['addressDetails']['region']['id'],
                        "description": funder_region_data[1],
                        "uri": funder_region_data[3]
                    }]

                    if fs_payloads_list[q_0]['buyer']['address']['addressDetails']['locality']['scheme'] == "CUATM":

                        funder_locality_data = get_value_from_locality_csv(
                            locality=fs_payloads_list[q_0]['buyer']['address']['addressDetails']['locality']['id'],
                            region=fs_payloads_list[q_0]['buyer']['address']['addressDetails']['region']['id'],
                            country=fs_payloads_list[q_0]['buyer']['address']['addressDetails']['country']['id'],
                            language=self.language
                        )
                        expected_funder_locality_object = [{
                            "scheme": funder_locality_data[2],
                            "id": fs_payloads_list[q_0]['buyer']['address']['addressDetails']['locality']['id'],
                            "description": funder_locality_data[1],
                            "uri": funder_locality_data[3]
                        }]
                    else:
                        expected_funder_locality_object = [{
                            "scheme": fs_payloads_list[q_0]['buyer']['address']['addressDetails']['locality']['scheme'],
                            "id": fs_payloads_list[q_0]['buyer']['address']['addressDetails']['locality']['id'],

                            "description":
                                fs_payloads_list[q_0]['buyer']['address']['addressDetails']['locality']['description']
                        }]

                    funder_role_array[q_0]['address']['addressDetails']['country'] = expected_funder_country_object[0]
                    funder_role_array[q_0]['address']['addressDetails']['region'] = expected_funder_region_object[0]
                    funder_role_array[q_0]['address']['addressDetails']['locality'] = expected_funder_locality_object[0]
                except ValueError:
                    raise ValueError(
                        "Impossible to prepare addressDetails object for party with funder role.")

                if "uri" in fs_payloads_list[q_0]['buyer']['identifier']:
                    funder_role_array[q_0]['identifier']['uri'] = fs_payloads_list[q_0]['buyer']['identifier']['uri']
                else:
                    del funder_role_array[q_0]['identifier']['uri']

                if "additionalIdentifiers" in fs_payloads_list[q_0]['buyer']:
                    for p_0 in range(len(fs_payloads_list[q_0]['buyer']['additionalIdentifiers'])):
                        funder_role_array[q_0]['additionalIdentifiers'][p_0]['scheme'] = \
                            fs_payloads_list[q_0]['buyer']['additionalIdentifiers'][p_0]['scheme']

                        funder_role_array[q_0]['additionalIdentifiers'][p_0]['id'] = \
                            fs_payloads_list[q_0]['buyer']['additionalIdentifiers'][p_0]['id']

                        funder_role_array[q_0]['additionalIdentifiers'][p_0]['legalName'] = \
                            fs_payloads_list[q_0]['buyer']['additionalIdentifiers'][p_0]['legalName']

                        funder_role_array[q_0]['additionalIdentifiers'][p_0]['uri'] = \
                            fs_payloads_list[q_0]['buyer']['additionalIdentifiers'][p_0]['uri']
                else:
                    del funder_role_array[q_0]['additionalIdentifiers']

                if "faxNumber" in fs_payloads_list[q_0]['buyer']['contactPoint']:

                    funder_role_array[q_0]['contactPoint']['faxNumber'] = \
                        fs_payloads_list[q_0]['buyer']['contactPoint']['faxNumber']
                else:
                    del funder_role_array[q_0]['contactPoint']['faxNumber']

                if "url" in fs_payloads_list[q_0]['buyer']['contactPoint']:
                    funder_role_array[q_0]['contactPoint']['url'] = fs_payloads_list[q_0]['buyer']['contactPoint'][
                        'url']
                else:
                    del funder_role_array[q_0]['contactPoint']['url']

                funder_role_array[q_0]['contactPoint']['name'] = \
                    fs_payloads_list[q_0]['buyer']['contactPoint']['name']

                funder_role_array[q_0]['contactPoint']['email'] = \
                    fs_payloads_list[q_0]['buyer']['contactPoint']['email']

                funder_role_array[q_0]['contactPoint']['telephone'] = \
                    fs_payloads_list[q_0]['buyer']['contactPoint']['telephone']

                funder_role_array[q_0]['roles'] = ["funder"]

        for p_0 in range(len(fs_payloads_list)):
            payer_role_array.append(copy.deepcopy(self.expected_fs_release['releases'][0]['parties'][0]))

            payer_role_array[p_0]['id'] = \
                f"{fs_payloads_list[p_0]['tender']['procuringEntity']['identifier']['scheme']}-" \
                f"{fs_payloads_list[p_0]['tender']['procuringEntity']['identifier']['id']}"

            payer_role_array[p_0]['name'] = fs_payloads_list[p_0]['tender']['procuringEntity']['name']

            payer_role_array[p_0]['identifier']['scheme'] = \
                fs_payloads_list[p_0]['tender']['procuringEntity']['identifier']['scheme']

            payer_role_array[p_0]['identifier']['id'] = \
                fs_payloads_list[p_0]['tender']['procuringEntity']['identifier']['id']

            payer_role_array[p_0]['identifier']['legalName'] = \
                fs_payloads_list[p_0]['tender']['procuringEntity']['identifier']['legalName']

            payer_role_array[p_0]['address']['streetAddress'] = \
                fs_payloads_list[p_0]['tender']['procuringEntity']['address']['streetAddress']

            if "postalCode" in fs_payloads_list[p_0]['tender']['procuringEntity']['address']:

                payer_role_array[p_0]['address']['postalCode'] = \
                    fs_payloads_list[p_0]['tender']['procuringEntity']['address']['postalCode']
            else:
                del payer_role_array[p_0]['address']['postalCode']

            try:
                """
                Prepare addressDetails object for party with payer role.
                """
                payer_country_data = get_value_from_country_csv(
                    country=fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                        'country']['id'],

                    language=self.language
                )
                expected_payer_country_object = [{
                    "scheme": payer_country_data[2],

                    "id": fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                        'country']['id'],

                    "description": payer_country_data[1],
                    "uri": payer_country_data[3]
                }]

                payer_region_data = get_value_from_region_csv(
                    region=fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                        'region']['id'],

                    country=fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                        'country']['id'],

                    language=self.language
                )
                expected_payer_region_object = [{
                    "scheme": payer_region_data[2],

                    "id": fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                        'region']['id'],

                    "description": payer_region_data[1],
                    "uri": payer_region_data[3]
                }]

                if fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                        'locality']['scheme'] == "CUATM":

                    payer_locality_data = get_value_from_locality_csv(
                        locality=fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                            'locality']['id'],

                        region=fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                            'region']['id'],

                        country=fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                            'country']['id'],

                        language=self.language
                    )
                    expected_payer_locality_object = [{
                        "scheme": payer_locality_data[2],
                        "id": fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                            'locality']['id'],

                        "description": payer_locality_data[1],
                        "uri": payer_locality_data[3]
                    }]
                else:
                    expected_payer_locality_object = [{
                        "scheme": fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                            'locality']['scheme'],

                        "id": fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                            'locality']['id'],

                        "description": fs_payloads_list[p_0]['tender']['procuringEntity']['address']['addressDetails'][
                            'locality']['description']
                    }]

                payer_role_array[p_0]['address']['addressDetails']['country'] = expected_payer_country_object[0]
                payer_role_array[p_0]['address']['addressDetails']['region'] = expected_payer_region_object[0]
                payer_role_array[p_0]['address']['addressDetails']['locality'] = expected_payer_locality_object[0]
            except ValueError:
                raise ValueError(
                    "Impossible to prepare addressDetails object for party with funder role.")

            if "uri" in fs_payloads_list[p_0]['tender']['procuringEntity']['identifier']:

                payer_role_array[p_0]['identifier']['uri'] = \
                    fs_payloads_list[p_0]['tender']['procuringEntity']['identifier']['uri']
            else:
                del payer_role_array[p_0]['identifier']['uri']

            if "additionalIdentifiers" in fs_payloads_list[p_0]['tender']['procuringEntity']:
                for p_1 in range(len(fs_payloads_list[p_0]['tender']['procuringEntity']['additionalIdentifiers'])):
                    payer_role_array[p_0]['additionalIdentifiers'][p_1]['scheme'] = \
                        fs_payloads_list[p_0]['tender']['procuringEntity']['additionalIdentifiers'][p_1]['scheme']

                    payer_role_array[p_0]['additionalIdentifiers'][p_1]['id'] = \
                        fs_payloads_list[p_0]['tender']['procuringEntity']['additionalIdentifiers'][p_1]['id']

                    payer_role_array[p_0]['additionalIdentifiers'][p_1]['legalName'] = \
                        fs_payloads_list[p_0]['tender']['procuringEntity']['additionalIdentifiers'][p_1]['legalName']

                    payer_role_array[p_0]['additionalIdentifiers'][p_1]['uri'] = \
                        fs_payloads_list[p_0]['tender']['procuringEntity']['additionalIdentifiers'][p_1]['uri']
            else:
                del payer_role_array[p_0]['additionalIdentifiers']

            if "faxNumber" in fs_payloads_list[p_0]['tender']['procuringEntity']['contactPoint']:

                payer_role_array[p_0]['contactPoint']['faxNumber'] = \
                    fs_payloads_list[p_0]['tender']['procuringEntity']['contactPoint']['faxNumber']
            else:
                del payer_role_array[p_0]['contactPoint']['faxNumber']

            if "url" in fs_payloads_list[p_0]['tender']['procuringEntity']['contactPoint']:

                payer_role_array[p_0]['contactPoint']['url'] = \
                    fs_payloads_list[p_0]['tender']['procuringEntity']['contactPoint']['url']
            else:
                del payer_role_array[p_0]['contactPoint']['url']

            payer_role_array[p_0]['contactPoint']['name'] = \
                fs_payloads_list[p_0]['tender']['procuringEntity']['contactPoint']['name']

            payer_role_array[p_0]['contactPoint']['email'] = \
                fs_payloads_list[p_0]['tender']['procuringEntity']['contactPoint']['email']

            payer_role_array[p_0]['contactPoint']['telephone'] = \
                fs_payloads_list[p_0]['tender']['procuringEntity']['contactPoint']['telephone']

            payer_role_array[p_0]['roles'] = ["payer"]

        unique_payer_role_array = get_unique_party_from_list_by_id(payer_role_array)
        unique_funder_role_array = get_unique_party_from_list_by_id(funder_role_array)

        unique_payer_id_array = list()
        for payer in range(len(unique_payer_role_array)):
            unique_payer_id_array.append(unique_payer_role_array[payer]['id'])

        unique_funder_id_array = list()
        for funder in range(len(unique_funder_role_array)):
            unique_funder_id_array.append(unique_funder_role_array[funder]['id'])

        temp_parties_with_payer_role_array = list()
        temp_parties_with_funder_role_array = list()

        same_id_into_payer_and_funder = list(set(unique_payer_id_array) & set(unique_funder_id_array))

        if len(same_id_into_payer_and_funder) > 0:
            for funder in range(len(unique_funder_role_array)):
                for i_1 in range(len(same_id_into_payer_and_funder)):
                    for payer in range(len(unique_payer_role_array)):
                        if unique_funder_role_array[funder]['id'] == same_id_into_payer_and_funder[i_1] == \
                                unique_payer_role_array[payer]['id']:
                            unique_funder_role_array[funder]['roles'] = \
                                unique_funder_role_array[funder]['roles'] + unique_payer_role_array[payer]['roles']

                            temp_parties_with_funder_role_array.append(unique_funder_role_array[payer])

                    for payer in range(len(unique_payer_role_array)):
                        if unique_funder_role_array[funder]['id'] != same_id_into_payer_and_funder[i_1]:
                            temp_parties_with_funder_role_array.append(unique_funder_role_array[funder])

                        if unique_funder_role_array[payer]['id'] != same_id_into_payer_and_funder[i_1]:
                            temp_parties_with_payer_role_array.append(unique_funder_role_array[payer])
        else:
            temp_parties_with_payer_role_array = unique_payer_role_array
            temp_parties_with_funder_role_array = unique_funder_role_array

        parties_array = \
            temp_parties_with_payer_role_array + temp_parties_with_funder_role_array

        expected_parties_array = list()
        if len(self.actual_fs_release['releases'][0]['parties']) == len(parties_array):
            for act in range(len(self.actual_fs_release['releases'][0]['parties'])):
                for exp in range(len(parties_array)):
                    if parties_array[exp]['id'] == self.actual_fs_release['releases'][0]['parties'][act]['id']:
                        expected_parties_array.append(parties_array[exp])
        else:
            raise ValueError("Quantity of objects into actual ms release doesn't equal "
                             "quantity of objects into prepared parties array")

        print("\nActual parties array")
        print(json.dumps(self.actual_fs_release['releases'][0]['parties']))
        print("\nExpected parties array")
        print(json.dumps(expected_parties_array))

        self.expected_fs_release['releases'][0]['parties'] = expected_parties_array

        # # Build the releases.planning object. Enrich or delete optional fields and enrich required fields:
        # self.expected_fs_release['releases'][0]['planning']['budget']['id'] = self.tender_classification_id
        #
        # self.expected_fs_release['releases'][0]['planning']['budget']['period']['startDate'] = \
        #     self.fs_payload['planning']['budget']['period']['startDate']
        #
        # self.expected_fs_release['releases'][0]['planning']['budget']['period']['endDate'] = \
        #     self.fs_payload['planning']['budget']['period']['endDate']
        #
        # if "rationale" in self.fs_payload['planning']:
        #     self.expected_fs_release['releases'][0]['planning']['rationale'] = self.fs_payload['planning']['rationale']
        # else:
        #     del self.expected_fs_release['releases'][0]['planning']['rationale']
        #
        # return self.expected_fs_release
