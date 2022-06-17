"""Prepare the expected release of the create expenditure item process, budget."""
import copy

from functions_collection.some_functions import get_value_from_cpvs_dictionary_csv, is_it_uuid, \
    get_value_from_cpv_dictionary_xls, get_value_from_classification_unit_dictionary_csv, \
    get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv


class ExpenditureItemRelease:
    """This class creates instance of release."""

    def __init__(self, environment, host_to_service, language, ei_payload, ei_message, actual_ei_release,
                 tender_classification_id):

        self.environment = environment
        self.host = host_to_service
        self.language = language
        self.ei_payload = ei_payload
        self.ei_message = ei_message
        self.actual_ei_release = actual_ei_release
        self.tender_classification_id = tender_classification_id

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

        # BR-4.228, BR-4.229, BR-4.230, BR-4.232, BR-4.234, BR-4.235,
        self.expected_ei_release = {
            "uri": f"{self.metadata_budget_url}/{ei_message['data']['ocid']}/"
                   f"{ei_message['data']['outcomes']['ei'][0]['id']}",

            "version": "1.1",
            "extensions": extensions,
            "publisher": {
                "name": publisher_name,
                "uri": publisher_uri
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": ei_message['data']['operationDate'],
            "releases": [
                {
                    "ocid": ei_message['data']['outcomes']['ei'][0]['id'],

                    "id": f"{ei_message['data']['outcomes']['ei'][0]['id']}-"
                          f"{actual_ei_release['releases'][0]['id'][29:42]}",

                    "date": ei_message['data']['operationDate'],
                    "tag": [
                        "compiled"
                    ],
                    "language": language,
                    "initiationType": "tender",
                    "tender": {
                        "id": "",
                        "title": "",
                        "description": "",
                        "status": "planning",
                        "statusDetails": "empty",
                        "items": [
                            {
                                "id": "",
                                "description": "",
                                "classification": {
                                    "scheme": "",
                                    "id": "",
                                    "description": ""
                                },
                                "additionalClassifications": [
                                    {
                                        "scheme": "",
                                        "id": "",
                                        "description": ""
                                    }
                                ],
                                "quantity": 0,
                                "unit": {
                                    "name": "",
                                    "id": ""
                                },
                                "deliveryAddress": {
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
                                }
                            }
                        ],
                        "mainProcurementCategory": "",
                        "classification": {
                            "scheme": "",
                            "id": "",
                            "description": ""
                        }
                    },
                    "buyer": {
                        "id": "",
                        "name": ""
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
                            "details": {
                                "typeOfBuyer": "",
                                "mainGeneralActivity": "",
                                "mainSectoralActivity": ""
                            },
                            "roles": [""]
                        }
                    ],
                    "planning": {
                        "budget": {
                            "id": "",
                            "period": {
                                "startDate": "",
                                "endDate": ""
                            }
                        },
                        "rationale": ""
                    }

                }
            ]
        }

    def build_expected_ei_release(self):
        """Build EI release."""

        # Build the releases.tender object. Enrich or delete optional fields and enrich required fields:
        # BR-4.233
        if "items" in self.ei_payload['tender']:
            try:
                """
                Build the releases.tender.items array.
                """
                new_items_array = list()
                for q_0 in range(len(self.ei_payload['tender']['items'])):

                    new_items_array.append(copy.deepcopy(
                        self.expected_ei_release['releases'][0]['tender']['items'][0]))

                    # Enrich or delete optional fields:
                    if "additionalClassifications" in self.ei_payload['tender']['items'][q_0]:
                        new_item_additional_classifications_array = list()
                        for q_1 in range(len(self.ei_payload['tender']['items'][q_0]['additionalClassifications'])):
                            new_item_additional_classifications_array.append(copy.deepcopy(
                                self.expected_ei_release['releases'][0]['tender']['items'][0][
                                    'additionalClassifications'][0]))

                            expected_cpvs_data = get_value_from_cpvs_dictionary_csv(
                                cpvs=self.ei_payload['tender']['items'][q_0]['additionalClassifications'][q_1]['id'],
                                language=self.language
                            )

                            new_item_additional_classifications_array[q_1]['scheme'] = "CPVS"
                            new_item_additional_classifications_array[q_1]['id'] = expected_cpvs_data[0]
                            new_item_additional_classifications_array[q_1]['description'] = expected_cpvs_data[2]

                        new_items_array[q_0]['additionalClassifications'] = \
                            new_item_additional_classifications_array
                    else:
                        del new_items_array[q_0]['additionalClassifications']

                    # Enrich required fields:
                    try:
                        """Set permanent id."""

                        is_permanent_id_correct = is_it_uuid(
                            self.actual_ei_release['releases'][0]['tender']['items'][q_0]['id']
                        )
                        if is_permanent_id_correct is True:

                            new_items_array[q_0]['id'] = \
                                self.actual_ei_release['releases'][0]['tender']['items'][q_0]['id']
                        else:
                            new_items_array[q_0]['id'] = \
                                f"The 'releases[0].tender.items[{q_0}].id' must be uuid."
                    except KeyError:
                        KeyError(f"Mismatch key into path 'releases[0].tender.items[{q_0}].id'")

                    new_items_array[q_0]['description'] = self.ei_payload['tender']['items'][q_0]['description']

                    expected_cpv_data = get_value_from_cpv_dictionary_xls(
                        cpv=self.ei_payload['tender']['items'][q_0]['classification']['id'],
                        language=self.language
                    )

                    new_items_array[q_0]['classification']['scheme'] = "CPV"
                    new_items_array[q_0]['classification']['id'] = expected_cpv_data[0]
                    new_items_array[q_0]['classification']['description'] = expected_cpv_data[1]
                    new_items_array[q_0]['quantity'] = int(float(self.ei_payload['tender']['items'][q_0]['quantity']))

                    expected_unit_data = get_value_from_classification_unit_dictionary_csv(
                        unit_id=self.ei_payload['tender']['items'][q_0]['unit']['id'],
                        language=self.language
                    )

                    new_items_array[q_0]['unit']['id'] = expected_unit_data[0]
                    new_items_array[q_0]['unit']['name'] = expected_unit_data[1]

                    new_items_array[q_0]['deliveryAddress']['streetAddress'] = \
                        self.ei_payload['tender']['items'][q_0]['deliveryAddress']['streetAddress']

                    if "postalCode" in self.ei_payload['tender']['items'][q_0]['deliveryAddress']:

                        new_items_array[q_0]['deliveryAddress']['postalCode'] = \
                            self.ei_payload['tender']['items'][q_0]['deliveryAddress']['postalCode']
                    else:
                        del new_items_array[q_0]['deliveryAddress']['postalCode']

                    try:
                        """
                        Prepare addressDetails object for items array.
                        """
                        item_country_data = get_value_from_country_csv(

                            country=self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                'country']['id'],

                            language=self.language
                        )
                        expected_item_country_object = [{
                            "scheme": item_country_data[2],
                            "id": self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                'country']['id'],

                            "description": item_country_data[1],
                            "uri": item_country_data[3]
                        }]

                        item_region_data = get_value_from_region_csv(

                            region=self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                'region']['id'],

                            country=self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                'country']['id'],

                            language=self.language
                        )
                        expected_item_region_object = [{
                            "scheme": item_region_data[2],

                            "id": self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                'region']['id'],

                            "description": item_region_data[1],
                            "uri": item_region_data[3]
                        }]

                        if self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                'locality']['scheme'] == "CUATM":

                            item_locality_data = get_value_from_locality_csv(

                                locality=self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'locality']['id'],

                                region=self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'region']['id'],

                                country=self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'country']['id'],

                                language=self.language
                            )
                            expected_item_locality_object = [{
                                "scheme": item_locality_data[2],

                                "id": self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'locality']['id'],

                                "description": item_locality_data[1],
                                "uri": item_locality_data[3]
                            }]
                        else:
                            expected_item_locality_object = [{

                                "scheme": self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'locality']['scheme'],

                                "id": self.ei_payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'locality']['id'],

                                "description": self.ei_payload['tender']['items'][q_0]['deliveryAddress'][
                                    'addressDetails']['locality']['description']
                            }]

                        new_items_array[q_0]['deliveryAddress']['addressDetails']['country'] = \
                            expected_item_country_object[0]

                        new_items_array[q_0]['deliveryAddress']['addressDetails']['region'] = \
                            expected_item_region_object[0]

                        new_items_array[q_0]['deliveryAddress']['addressDetails']['locality'] = \
                            expected_item_locality_object[0]
                    except ValueError:
                        ValueError("Impossible to prepare addressDetails object for items array")

                self.expected_ei_release['releases'][0]['tender']['items'] = new_items_array
            except ValueError:
                ValueError("Impossible to build the expected releases.tender.items array.")
        else:
            del self.expected_ei_release['releases'][0]['tender']['items']

        if "description" in self.ei_payload['tender']:
            self.expected_ei_release['releases'][0]['tender']['description'] = self.ei_payload['tender']['description']
        else:
            del self.expected_ei_release['releases'][0]['tender']['description']

        try:
            """Set permanent id."""

            is_permanent_id_correct = is_it_uuid(self.actual_ei_release['releases'][0]['tender']['id'])
            if is_permanent_id_correct is True:

                self.expected_ei_release['releases'][0]['tender']['id'] = \
                    self.actual_ei_release['releases'][0]['tender']['id']
            else:
                ValueError(f"The 'releases[0].tender.id' must be uuid.")
        except KeyError:
            KeyError("Mismatch key into path 'releases[0].tender.id'")

        self.expected_ei_release['releases'][0]['tender']['title'] = self.ei_payload['tender']['title']
        self.expected_ei_release['releases'][0]['tender']['status'] = "planning"
        self.expected_ei_release['releases'][0]['tender']['statusDetails'] = "empty"

        try:
            """
           Enrich mainProcurementCategory, depends on tender.classification.id.
           """
            expected_main_procurement_category = None
            if \
                    self.tender_classification_id[0:2] == "03" or \
                    self.tender_classification_id[0] == "1" or \
                    self.tender_classification_id[0] == "2" or \
                    self.tender_classification_id[0] == "3" or \
                    self.tender_classification_id[0:2] == "44" or \
                    self.tender_classification_id[0:2] == "48":
                expected_main_procurement_category = "goods"

            elif \
                    self.tender_classification_id[0:2] == "45":
                expected_main_procurement_category = "works"

            elif \
                    self.tender_classification_id[0] == "5" or \
                    self.tender_classification_id[0] == "6" or \
                    self.tender_classification_id[0] == "7" or \
                    self.tender_classification_id[0] == "8" or \
                    self.tender_classification_id[0:2] == "92" or \
                    self.tender_classification_id[0:2] == "98":
                expected_main_procurement_category = "services"

            else:
                ValueError("Check your tender.classification.id")

            self.expected_ei_release['releases'][0]['tender']['mainProcurementCategory'] = \
                expected_main_procurement_category

        except KeyError:
            KeyError("Could not parse tender.classification.id.")

        # BR-12.2.1:
        try:
            """
            Enrich releases.tender.classification object, depends on items into payload.
            """

            expected_cpv_data = get_value_from_cpv_dictionary_xls(
                cpv=self.tender_classification_id,
                language=self.language
            )

            self.expected_ei_release['releases'][0]['tender']['classification']['id'] = expected_cpv_data[0]
            self.expected_ei_release['releases'][0]['tender']['classification']['description'] = expected_cpv_data[1]
            self.expected_ei_release['releases'][0]['tender']['classification']['scheme'] = "CPV"
        except ValueError:
            ValueError("Impossible to enrich releases.tender.classification object.")

        # Build the releases.buyer object. Enrich or delete optional fields and enrich required fields:
        # BR-4.5:
        self.expected_ei_release['releases'][0]['buyer']['id'] = \
            f"{self.ei_payload['buyer']['identifier']['scheme']}-{self.ei_payload['buyer']['identifier']['id']}"

        self.expected_ei_release['releases'][0]['buyer']['name'] = self.ei_payload['buyer']['name']

        # Build the releases.parties array. Enrich or delete optional fields and enrich required fields:
        # BR-4.2:
        buyer_role_array = list()
        buyer_role_array.append(copy.deepcopy(self.expected_ei_release['releases'][0]['parties'][0]))

        buyer_role_array[0]['id'] = f"{self.ei_payload['buyer']['identifier']['scheme']}-" \
                                    f"{self.ei_payload['buyer']['identifier']['id']}"

        buyer_role_array[0]['name'] = self.ei_payload['buyer']['name']
        buyer_role_array[0]['identifier']['scheme'] = self.ei_payload['buyer']['identifier']['scheme']
        buyer_role_array[0]['identifier']['id'] = self.ei_payload['buyer']['identifier']['id']
        buyer_role_array[0]['identifier']['legalName'] = self.ei_payload['buyer']['identifier']['legalName']

        if "uri" in self.ei_payload['buyer']['identifier']:
            buyer_role_array[0]['identifier']['uri'] = self.ei_payload['buyer']['identifier']['uri']
        else:
            del buyer_role_array[0]['identifier']['uri']

        buyer_role_array[0]['address']['streetAddress'] = self.ei_payload['buyer']['address']['streetAddress']

        if "postalCode" in self.ei_payload['buyer']['address']:
            buyer_role_array[0]['address']['postalCode'] = self.ei_payload['buyer']['address']['postalCode']
        else:
            del buyer_role_array[0]['address']['postalCode']

        try:
            """
            Prepare addressDetails object for party with buyer role.
            """
            buyer_country_data = get_value_from_country_csv(
                country=self.ei_payload['buyer']['address']['addressDetails']['country']['id'],
                language=self.language
            )
            expected_buyer_country_object = [{
                "scheme": buyer_country_data[2],
                "id": self.ei_payload['buyer']['address']['addressDetails']['country']['id'],
                "description": buyer_country_data[1],
                "uri": buyer_country_data[3]
            }]

            buyer_region_data = get_value_from_region_csv(
                region=self.ei_payload['buyer']['address']['addressDetails']['region']['id'],
                country=self.ei_payload['buyer']['address']['addressDetails']['country']['id'],
                language=self.language
            )
            expected_buyer_region_object = [{
                "scheme": buyer_region_data[2],
                "id": self.ei_payload['buyer']['address']['addressDetails']['region']['id'],
                "description": buyer_region_data[1],
                "uri": buyer_region_data[3]
            }]

            if self.ei_payload['buyer']['address']['addressDetails']['locality']['scheme'] == "CUATM":

                buyer_locality_data = get_value_from_locality_csv(
                    locality=self.ei_payload['buyer']['address']['addressDetails']['locality']['id'],
                    region=self.ei_payload['buyer']['address']['addressDetails']['region']['id'],
                    country=self.ei_payload['buyer']['address']['addressDetails']['country']['id'],
                    language=self.language
                )
                expected_buyer_locality_object = [{
                    "scheme": buyer_locality_data[2],
                    "id": self.ei_payload['buyer']['address']['addressDetails']['locality']['id'],
                    "description": buyer_locality_data[1],
                    "uri": buyer_locality_data[3]
                }]
            else:
                expected_buyer_locality_object = [{
                    "scheme": self.ei_payload['buyer']['address']['addressDetails']['locality']['scheme'],
                    "id": self.ei_payload['buyer']['address']['addressDetails']['locality']['id'],
                    "description": self.ei_payload['buyer']['address']['addressDetails']['locality']['description']
                }]

            buyer_role_array[0]['address']['addressDetails']['country'] = expected_buyer_country_object[0]
            buyer_role_array[0]['address']['addressDetails']['region'] = expected_buyer_region_object[0]
            buyer_role_array[0]['address']['addressDetails']['locality'] = expected_buyer_locality_object[0]
        except ValueError:
            ValueError(
                "Impossible to prepare addressDetails object for party with buyer role.")

        if "additionalIdentifiers" in self.ei_payload['buyer']:
            for q_1 in range(len(self.ei_payload['buyer']['additionalIdentifiers'])):
                buyer_role_array[0]['additionalIdentifiers'][q_1]['scheme'] = \
                    self.ei_payload['buyer']['additionalIdentifiers'][q_1]['scheme']

                buyer_role_array[0]['additionalIdentifiers'][q_1]['id'] = \
                    self.ei_payload['buyer']['additionalIdentifiers'][q_1]['id']

                buyer_role_array[0]['additionalIdentifiers'][q_1]['legalName'] = \
                    self.ei_payload['buyer']['additionalIdentifiers'][q_1]['legalName']

                buyer_role_array[0]['additionalIdentifiers'][q_1]['uri'] = \
                    self.ei_payload['buyer']['additionalIdentifiers'][q_1]['uri']
        else:
            del buyer_role_array[0]['additionalIdentifiers']

        if "faxNumber" in self.ei_payload['buyer']['contactPoint']:
            buyer_role_array[0]['contactPoint']['faxNumber'] = self.ei_payload['buyer']['contactPoint']['faxNumber']
        else:
            del buyer_role_array[0]['contactPoint']['faxNumber']

        if "url" in self.ei_payload['buyer']['contactPoint']:
            buyer_role_array[0]['contactPoint']['url'] = self.ei_payload['buyer']['contactPoint']['url']
        else:
            del buyer_role_array[0]['contactPoint']['url']

        buyer_role_array[0]['contactPoint']['name'] = self.ei_payload['buyer']['contactPoint']['name']
        buyer_role_array[0]['contactPoint']['email'] = self.ei_payload['buyer']['contactPoint']['email']
        buyer_role_array[0]['contactPoint']['telephone'] = self.ei_payload['buyer']['contactPoint']['telephone']

        if "details" in self.ei_payload['buyer']:
            if "typeOfBuyer" in self.ei_payload['buyer']['details']:
                buyer_role_array[0]['details']['typeOfBuyer'] = self.ei_payload['buyer']['details']['typeOfBuyer']
            else:
                del buyer_role_array['buyer']['details']['typeOfBuyer']

            if "mainGeneralActivity" in self.ei_payload['buyer']['details']:

                buyer_role_array[0]['details']['mainGeneralActivity'] = \
                    self.ei_payload['buyer']['details']['mainGeneralActivity']
            else:
                del buyer_role_array[0]['details']['mainGeneralActivity']

            if "mainSectoralActivity" in self.ei_payload['buyer']['details']:

                buyer_role_array[0]['details']['mainSectoralActivity'] = \
                    self.ei_payload['buyer']['details']['mainSectoralActivity']
            else:
                del buyer_role_array[0]['details']['mainSectoralActivity']
        else:
            del buyer_role_array[0]['details']

        buyer_role_array[0]['roles'] = ["buyer"]
        self.expected_ei_release['releases'][0]['parties'] = buyer_role_array

        # Build the releases.planning object. Enrich or delete optional fields and enrich required fields:
        # BR-4.233:
        self.expected_ei_release['releases'][0]['planning']['budget']['id'] = self.tender_classification_id

        self.expected_ei_release['releases'][0]['planning']['budget']['period']['startDate'] = \
            self.ei_payload['planning']['budget']['period']['startDate']

        self.expected_ei_release['releases'][0]['planning']['budget']['period']['endDate'] = \
            self.ei_payload['planning']['budget']['period']['endDate']

        if "rationale" in self.ei_payload['planning']:
            self.expected_ei_release['releases'][0]['planning']['rationale'] = self.ei_payload['planning']['rationale']
        else:
            del self.expected_ei_release['releases'][0]['planning']['rationale']

        return self.expected_ei_release
