"""Prepare the expected release of the create financial source process, budget."""
import copy

from functions_collection.some_functions import is_it_uuid, get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv, get_unique_party_from_list_by_id


class FinancialSourceRelease:
    """This class creates instance of release."""

    def __init__(self, environment, host_to_service, language, cpid, ei_payload, fs_payload, fs_message,
                 actual_fs_release):

        self.environment = environment
        self.host = host_to_service
        self.language = language
        self.cpid = cpid
        self.ei_payload = ei_payload
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
            ValueError("Check your environment: You must use 'dev' or 'sandbox' environment.")

        # BR-4.16, BR-4.242, BR-4.243, BR-4.244, BR-4.246:
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
                    "initiationType": "tender",
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

    def build_expected_fs_release(self):
        """Build FS release."""

        # Build the releases.tender object. Enrich or delete optional fields and enrich required fields:
        # BR-4.12:
        try:
            """Set permanent id."""

            is_permanent_id_correct = is_it_uuid(self.actual_fs_release['releases'][0]['tender']['id'])
            if is_permanent_id_correct is True:

                self.expected_fs_release['releases'][0]['tender']['id'] = \
                    self.actual_fs_release['releases'][0]['tender']['id']
            else:
                ValueError(f"The 'releases[0].tender.id' must be uuid.")
        except KeyError:
            KeyError("Mismatch key into path 'releases[0].tender.id'")

        self.expected_fs_release['releases'][0]['tender']['status'] = "active"
        self.expected_fs_release['releases'][0]['tender']['statusDetails'] = "empty"

        # Build the releases.parties array. Enrich or delete optional fields and enrich required fields:
        # BR-4.17:
        payer_role_array = list()
        funder_role_array = list()

        if "buyer" in self.fs_payload:

            funder_role_object = copy.deepcopy(self.expected_fs_release['releases'][0]['parties'][0])

            funder_role_object['id'] = f"{self.fs_payload['buyer']['identifier']['scheme']}-" \
                                       f"{self.fs_payload['buyer']['identifier']['id']}"

            funder_role_object['name'] = self.fs_payload['buyer']['name']
            funder_role_object['identifier']['scheme'] = self.fs_payload['buyer']['identifier']['scheme']
            funder_role_object['identifier']['id'] = self.fs_payload['buyer']['identifier']['id']

            funder_role_object['identifier']['legalName'] = \
                self.fs_payload['buyer']['identifier']['legalName']

            funder_role_object['address']['streetAddress'] = self.fs_payload['buyer']['address']['streetAddress']

            if "postalCode" in self.fs_payload['buyer']['address']:
                funder_role_object['address']['postalCode'] = self.fs_payload['buyer']['address']['postalCode']
            else:
                del funder_role_object['address']['postalCode']

            try:
                """
                Prepare addressDetails object for party with funder role.
                """
                funder_country_data = get_value_from_country_csv(
                    country=self.fs_payload['buyer']['address']['addressDetails']['country']['id'],
                    language=self.language
                )
                expected_funder_country_object = [{
                    "scheme": funder_country_data[2],
                    "id": self.fs_payload['buyer']['address']['addressDetails']['country']['id'],
                    "description": funder_country_data[1],
                    "uri": funder_country_data[3]
                }]

                funder_region_data = get_value_from_region_csv(
                    region=self.fs_payload['buyer']['address']['addressDetails']['region']['id'],
                    country=self.fs_payload['buyer']['address']['addressDetails']['country']['id'],
                    language=self.language
                )
                expected_funder_region_object = [{
                    "scheme": funder_region_data[2],
                    "id": self.fs_payload['buyer']['address']['addressDetails']['region']['id'],
                    "description": funder_region_data[1],
                    "uri": funder_region_data[3]
                }]

                if self.fs_payload['buyer']['address']['addressDetails']['locality']['scheme'] == "CUATM":

                    funder_locality_data = get_value_from_locality_csv(
                        locality=self.fs_payload['buyer']['address']['addressDetails']['locality']['id'],
                        region=self.fs_payload['buyer']['address']['addressDetails']['region']['id'],
                        country=self.fs_payload['buyer']['address']['addressDetails']['country']['id'],
                        language=self.language
                    )
                    expected_funder_locality_object = [{
                        "scheme": funder_locality_data[2],
                        "id": self.fs_payload['buyer']['address']['addressDetails']['locality']['id'],
                        "description": funder_locality_data[1],
                        "uri": funder_locality_data[3]
                    }]
                else:
                    expected_funder_locality_object = [{
                        "scheme": self.fs_payload['buyer']['address']['addressDetails']['locality']['scheme'],
                        "id": self.fs_payload['buyer']['address']['addressDetails']['locality']['id'],
                        "description": self.fs_payload['buyer']['address']['addressDetails']['locality']['description']
                    }]

                funder_role_object['address']['addressDetails']['country'] = expected_funder_country_object[0]
                funder_role_object['address']['addressDetails']['region'] = expected_funder_region_object[0]
                funder_role_object['address']['addressDetails']['locality'] = expected_funder_locality_object[0]
            except ValueError:
                ValueError(
                    "Impossible to prepare addressDetails object for party with funder role.")

            if "uri" in self.fs_payload['buyer']['identifier']:
                funder_role_object['identifier']['uri'] = self.fs_payload['buyer']['identifier']['uri']
            else:
                del funder_role_object['identifier']['uri']

            if "additionalIdentifiers" in self.fs_payload['buyer']:
                del funder_role_object['additionalIdentifiers'][0]
                additional_identifiers = list()
                for p_0 in range(len(self.fs_payload['buyer']['additionalIdentifiers'])):
                    additional_identifiers.append(copy.deepcopy(
                        self.expected_fs_release['releases'][0]['parties'][0]['additionalIdentifiers'][0]
                    ))

                    additional_identifiers[p_0]['scheme'] =\
                        self.fs_payload['buyer']['additionalIdentifiers'][p_0]['scheme']

                    additional_identifiers[p_0]['id'] = \
                        self.fs_payload['buyer']['additionalIdentifiers'][p_0]['id']

                    additional_identifiers[p_0]['legalName'] = \
                        self.fs_payload['buyer']['additionalIdentifiers'][p_0]['legalName']

                    additional_identifiers[p_0]['uri'] = \
                        self.fs_payload['buyer']['additionalIdentifiers'][p_0]['uri']

                    funder_role_object['additionalIdentifiers'] = additional_identifiers
            else:
                del funder_role_object['additionalIdentifiers']

            if "faxNumber" in self.fs_payload['buyer']['contactPoint']:
                funder_role_object['contactPoint']['faxNumber'] = self.fs_payload['buyer']['contactPoint']['faxNumber']
            else:
                del funder_role_object['contactPoint']['faxNumber']

            if "url" in self.fs_payload['buyer']['contactPoint']:
                funder_role_object['contactPoint']['url'] = self.fs_payload['buyer']['contactPoint']['url']
            else:
                del funder_role_object['contactPoint']['url']

            funder_role_object['contactPoint']['name'] = self.fs_payload['buyer']['contactPoint']['name']
            funder_role_object['contactPoint']['email'] = self.fs_payload['buyer']['contactPoint']['email']
            funder_role_object['contactPoint']['telephone'] = self.fs_payload['buyer']['contactPoint']['telephone']
            funder_role_object['roles'] = ["funder"]

            funder_role_array.append(funder_role_object)

        payer_role_object = copy.deepcopy(self.expected_fs_release['releases'][0]['parties'][0])

        payer_role_object['id'] = \
            f"{self.fs_payload['tender']['procuringEntity']['identifier']['scheme']}-" \
            f"{self.fs_payload['tender']['procuringEntity']['identifier']['id']}"

        payer_role_object['name'] = self.fs_payload['tender']['procuringEntity']['name']
        payer_role_object['identifier']['scheme'] = self.fs_payload['tender']['procuringEntity']['identifier']['scheme']
        payer_role_object['identifier']['id'] = self.fs_payload['tender']['procuringEntity']['identifier']['id']

        payer_role_object['identifier']['legalName'] = \
            self.fs_payload['tender']['procuringEntity']['identifier']['legalName']

        payer_role_object['address']['streetAddress'] = \
            self.fs_payload['tender']['procuringEntity']['address']['streetAddress']

        if "postalCode" in self.fs_payload['tender']['procuringEntity']['address']:

            payer_role_object['address']['postalCode'] = \
                self.fs_payload['tender']['procuringEntity']['address']['postalCode']
        else:
            del payer_role_object['address']['postalCode']

        try:
            """
            Prepare addressDetails object for party with payer role.
            """
            payer_country_data = get_value_from_country_csv(
                country=self.fs_payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
                language=self.language
            )
            expected_payer_country_object = [{
                "scheme": payer_country_data[2],
                "id": self.fs_payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
                "description": payer_country_data[1],
                "uri": payer_country_data[3]
            }]

            payer_region_data = get_value_from_region_csv(
                region=self.fs_payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
                country=self.fs_payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
                language=self.language
            )
            expected_payer_region_object = [{
                "scheme": payer_region_data[2],
                "id": self.fs_payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
                "description": payer_region_data[1],
                "uri": payer_region_data[3]
            }]

            if self.fs_payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] == \
                    "CUATM":

                payer_locality_data = get_value_from_locality_csv(
                    locality=self.fs_payload['tender']['procuringEntity']['address']['addressDetails'][
                        'locality']['id'],

                    region=self.fs_payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],

                    country=self.fs_payload['tender']['procuringEntity']['address']['addressDetails'][
                        'country']['id'],

                    language=self.language
                )
                expected_payer_locality_object = [{
                    "scheme": payer_locality_data[2],
                    "id": self.fs_payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],
                    "description": payer_locality_data[1],
                    "uri": payer_locality_data[3]
                }]
            else:
                expected_payer_locality_object = [{
                    "scheme": self.fs_payload['tender']['procuringEntity']['address']['addressDetails'][
                        'locality']['scheme'],

                    "id": self.fs_payload['tender']['procuringEntity']['address']['addressDetails'][
                        'locality']['id'],

                    "description": self.fs_payload['tender']['procuringEntity']['address']['addressDetails'][
                        'locality']['description']
                }]

            payer_role_object['address']['addressDetails']['country'] = expected_payer_country_object[0]
            payer_role_object['address']['addressDetails']['region'] = expected_payer_region_object[0]
            payer_role_object['address']['addressDetails']['locality'] = expected_payer_locality_object[0]
        except ValueError:
            ValueError(
                "Impossible to prepare addressDetails object for party with funder role.")

        if "uri" in self.fs_payload['tender']['procuringEntity']['identifier']:

            payer_role_object['identifier']['uri'] = \
                self.fs_payload['tender']['procuringEntity']['identifier']['uri']
        else:
            del payer_role_object['identifier']['uri']

        if "additionalIdentifiers" in self.fs_payload['tender']['procuringEntity']:
            del payer_role_object['additionalIdentifiers'][0]
            additional_identifiers = list()
            for p_1 in range(len(self.fs_payload['tender']['procuringEntity']['additionalIdentifiers'])):

                additional_identifiers.append(copy.deepcopy(
                    self.expected_fs_release['releases'][0]['parties'][0]['additionalIdentifiers'][0]
                ))

                additional_identifiers[p_1]['scheme'] = \
                    self.fs_payload['tender']['procuringEntity']['additionalIdentifiers'][p_1]['scheme']

                additional_identifiers[p_1]['id'] = \
                    self.fs_payload['tender']['procuringEntity']['additionalIdentifiers'][p_1]['id']

                additional_identifiers[p_1]['legalName'] = \
                    self.fs_payload['tender']['procuringEntity']['additionalIdentifiers'][p_1]['legalName']

                additional_identifiers[p_1]['uri'] = \
                    self.fs_payload['tender']['procuringEntity']['additionalIdentifiers'][p_1]['uri']

                payer_role_object['additionalIdentifiers'] = additional_identifiers
        else:
            del payer_role_object['additionalIdentifiers']

        if "faxNumber" in self.fs_payload['tender']['procuringEntity']['contactPoint']:

            payer_role_object['contactPoint']['faxNumber'] = \
                self.fs_payload['tender']['procuringEntity']['contactPoint']['faxNumber']
        else:
            del payer_role_object['contactPoint']['faxNumber']

        if "url" in self.fs_payload['tender']['procuringEntity']['contactPoint']:

            payer_role_object['contactPoint']['url'] = \
                self.fs_payload['tender']['procuringEntity']['contactPoint']['url']
        else:
            del payer_role_object['contactPoint']['url']

        payer_role_object['contactPoint']['name'] = \
            self.fs_payload['tender']['procuringEntity']['contactPoint']['name']

        payer_role_object['contactPoint']['email'] = \
            self.fs_payload['tender']['procuringEntity']['contactPoint']['email']

        payer_role_object['contactPoint']['telephone'] = \
            self.fs_payload['tender']['procuringEntity']['contactPoint']['telephone']

        payer_role_object['roles'] = ["payer"]
        payer_role_array.append(payer_role_object)

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
            ValueError("Quantity of objects into actual ms release doesn't equal "
                             "quantity of objects into prepared parties array")

        self.expected_fs_release['releases'][0]['parties'] = expected_parties_array

        # Build the releases.planning object. Enrich or delete optional fields and enrich required fields:
        # BR-4.253:
        if "id" in self.fs_payload['planning']['budget']:

            self.expected_fs_release['releases'][0]['planning']['budget']['id'] = \
                self.fs_payload['planning']['budget']['id']
        else:
            del self.expected_fs_release['releases'][0]['planning']['budget']['id']

        if "description" in self.fs_payload['planning']['budget']:

            self.expected_fs_release['releases'][0]['planning']['budget']['description'] = \
                self.fs_payload['planning']['budget']['description']
        else:
            del self.expected_fs_release['releases'][0]['planning']['budget']['description']

        self.expected_fs_release['releases'][0]['planning']['budget']['period']['startDate'] = \
            self.fs_payload['planning']['budget']['period']['startDate']

        self.expected_fs_release['releases'][0]['planning']['budget']['period']['endDate'] = \
            self.fs_payload['planning']['budget']['period']['endDate']

        self.expected_fs_release['releases'][0]['planning']['budget']['amount']['amount'] = \
            self.fs_payload['planning']['budget']['amount']['amount']

        self.expected_fs_release['releases'][0]['planning']['budget']['amount']['currency'] = \
            self.fs_payload['planning']['budget']['amount']['currency']

        self.expected_fs_release['releases'][0]['planning']['budget']['isEuropeanUnionFunded'] = \
            self.fs_payload['planning']['budget']['isEuropeanUnionFunded']

        if self.expected_fs_release['releases'][0]['planning']['budget']['isEuropeanUnionFunded'] is True:

            self.expected_fs_release['releases'][0]['planning']['budget']['europeanUnionFunding'][
                'projectIdentifier'] = \
                self.fs_payload['planning']['budget']['europeanUnionFunding']['projectIdentifier']

            self.expected_fs_release['releases'][0]['planning']['budget']['europeanUnionFunding']['projectName'] = \
                self.fs_payload['planning']['budget']['europeanUnionFunding']['projectName']

            if "uri" in self.fs_payload['planning']['budget']['europeanUnionFunding']:

                self.expected_fs_release['releases'][0]['planning']['budget']['europeanUnionFunding']['uri'] = \
                    self.fs_payload['planning']['budget']['europeanUnionFunding']['uri']
            else:
                del self.expected_fs_release['releases'][0]['planning']['budget']['europeanUnionFunding']['uri']
        else:
            del self.expected_fs_release['releases'][0]['planning']['budget']['europeanUnionFunding']

        if "buyer" in self.fs_payload:
            self.expected_fs_release['releases'][0]['tender']['status'] = "active"
            self.expected_fs_release['releases'][0]['planning']['budget']['verified'] = True

            self.expected_fs_release['releases'][0]['planning']['budget']['sourceEntity']['id'] = \
                f"{self.fs_payload['buyer']['identifier']['scheme']}-{self.fs_payload['buyer']['identifier']['id']}"

            self.expected_fs_release['releases'][0]['planning']['budget']['sourceEntity']['name'] = \
                self.fs_payload['buyer']['name']
        else:
            self.expected_fs_release['releases'][0]['tender']['status'] = "planning"
            self.expected_fs_release['releases'][0]['planning']['budget']['verified'] = False

            self.expected_fs_release['releases'][0]['planning']['budget']['sourceEntity']['id'] = \
                f"{self.ei_payload['buyer']['identifier']['scheme']}-{self.ei_payload['buyer']['identifier']['id']}"

            self.expected_fs_release['releases'][0]['planning']['budget']['sourceEntity']['name'] = \
                self.ei_payload['buyer']['name']

        if "project" in self.fs_payload['planning']['budget']:

            self.expected_fs_release['releases'][0]['planning']['budget']['project'] = \
                self.fs_payload['planning']['budget']['project']
        else:
            del self.expected_fs_release['releases'][0]['planning']['budget']['project']

        if "projectID" in self.fs_payload['planning']['budget']:

            self.expected_fs_release['releases'][0]['planning']['budget']['projectID'] = \
                self.fs_payload['planning']['budget']['projectID']
        else:
            del self.expected_fs_release['releases'][0]['planning']['budget']['projectID']

        if "uri" in self.fs_payload['planning']['budget']:

            self.expected_fs_release['releases'][0]['planning']['budget']['uri'] = \
                self.fs_payload['planning']['budget']['uri']
        else:
            del self.expected_fs_release['releases'][0]['planning']['budget']['uri']

        if "rationale" in self.fs_payload['planning']:
            self.expected_fs_release['releases'][0]['planning']['rationale'] = self.fs_payload['planning']['rationale']
        else:
            del self.expected_fs_release['releases'][0]['planning']['rationale']

        # Build the releases.relatedProcesses array. Enrich or delete optional fields and enrich required fields:
        # BR-4.13, BR-4.247, BR-4.248, BR-4.14, BR-4.249, BR-4.15:
        try:
            """Set permanent id."""

            is_permanent_id_correct = is_it_uuid(self.actual_fs_release['releases'][0]['relatedProcesses'][0]['id'])
            if is_permanent_id_correct is True:

                self.expected_fs_release['releases'][0]['relatedProcesses'][0]['id'] = \
                    self.actual_fs_release['releases'][0]['relatedProcesses'][0]['id']
            else:
                ValueError(f"The 'releases[0].relatedProcesses[0].id' must be uuid.")
        except KeyError:
            KeyError("Mismatch key into path 'releases[0].relatedProcesses[0].id'")

        self.expected_fs_release['releases'][0]['relatedProcesses'][0]['relationship'][0] = "parent"
        self.expected_fs_release['releases'][0]['relatedProcesses'][0]['scheme'] = "ocid"
        self.expected_fs_release['releases'][0]['relatedProcesses'][0]['identifier'] = self.cpid

        self.expected_fs_release['releases'][0]['relatedProcesses'][0]['uri'] = \
            f"{self.metadata_budget_url}/{self.cpid}/{self.cpid}"

        return self.expected_fs_release
