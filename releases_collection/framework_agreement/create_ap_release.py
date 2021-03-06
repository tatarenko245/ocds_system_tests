"""Prepare the expected releases of the aggregated plan process, framework agreement procedures."""
import copy

from functions_collection.some_functions import is_it_uuid, get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv, get_value_from_cpv_dictionary_xls


class CreateAggregatedPlanRelease:
    """This class creates instance of release."""

    def __init__(self, environment, host_to_service, language, pmd, ap_payload, ap_message, actual_ap_release,
                 actual_fa_release):

        self.__environment = environment
        self.__host = host_to_service
        self.__language = language
        self.__pmd = pmd
        self.__ap_payload = ap_payload
        self.__ap_message = ap_message
        self.__actual_ap_release = actual_ap_release
        self.__actual_fa_release = actual_fa_release

        extensions = None
        publisher_name = None
        publisher_uri = None
        self.__metadata_document_url = None
        try:
            if environment == "dev":
                self.__metadata_tender_url = "http://dev.public.eprocurement.systems/tenders"

                extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"
                ]

                publisher_name = "M-Tender"
                publisher_uri = "https://www.mtender.gov.md"
                self.__metadata_document_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get"
                self.__metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"

            elif environment == "sandbox":
                self.__metadata_tender_url = "http://public.eprocurement.systems/tenders"

                extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.json"
                ]

                publisher_name = "Vie????j?? pirkim?? tarnyba"
                publisher_uri = "https://vpt.lrv.lt"
                self.__metadata_document_url = "http://storage.eprocurement.systems/get"
                self.__metadata_budget_url = "http://public.eprocurement.systems/budgets"
        except ValueError:
            ValueError("Check your environment: You must use 'dev' or 'sandbox' environment in pytest command")

        self.__expected_ap_release = {
            "uri": f"{self.__metadata_tender_url}/{ap_message['data']['ocid']}/"
                   f"{ap_message['data']['outcomes']['ap'][0]['id']}",

            "version": "1.1",
            "extensions": extensions,
            "publisher": {
                "name": publisher_name,
                "uri": publisher_uri
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": ap_message['data']['operationDate'],
            "releases": [
                {
                    "ocid": ap_message['data']['outcomes']['ap'][0]['id'],

                    "id": f"{ap_message['data']['outcomes']['ap'][0]['id']}-"
                          f"{actual_ap_release['releases'][0]['id'][46:59]}",

                    "date": ap_message['data']['operationDate'],
                    "tag": [
                        "planning"
                    ],
                    "language": language,
                    "initiationType": "tender",
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
                            "roles": [
                                ""
                            ]
                        }
                    ],
                    "tender": {
                        "id": "",
                        "status": "planning",
                        "statusDetails": "aggregation",
                        "tenderPeriod": {
                            "startDate": ""
                        },
                        "hasEnquiries": False,
                        "documents": [
                            {
                                "id": "",
                                "documentType": "",
                                "title": "",
                                "description": "",
                                "url": "",
                                "datePublished": ""
                            }
                        ],
                        "submissionMethod": [
                            ""
                        ],
                        "submissionMethodDetails": "",
                        "submissionMethodRationale": [
                            ""
                        ],
                        "requiresElectronicCatalogue": False
                    },
                    "hasPreviousNotice": False,
                    "purposeOfNotice": {
                        "isACallForCompetition": False
                    },
                    "relatedProcesses": [
                        {
                            "id": "",
                            "relationship": [
                                ""
                            ],
                            "scheme": "",
                            "identifier": "",
                            "uri": ""
                        }
                    ]
                }
            ]
        }

        self.__expected_fa_release = {
            "uri": f"{self.__metadata_tender_url}/{ap_message['data']['ocid']}/{ap_message['data']['ocid']}",
            "version": "1.1",
            "extensions": extensions,
            "publisher": {
                "name": publisher_name,
                "uri": publisher_uri
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": ap_message['data']['operationDate'],
            "releases": [
                {
                    "ocid": ap_message['data']['ocid'],
                    "id": f"{ap_message['data']['ocid']}-{actual_fa_release['releases'][0]['id'][29:42]}",
                    "date": ap_message['data']['operationDate'],
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
                        "statusDetails": "aggregatePlanning",
                        "value": {
                            "currency": ""
                        },
                        "procurementMethod": "",
                        "procurementMethodDetails": "",
                        "procurementMethodRationale": "",
                        "hasEnquiries": False,
                        "eligibilityCriteria": "",
                        "contractPeriod": {
                            "startDate": "",
                            "endDate": ""
                        },
                        "acceleratedProcedure": {
                            "isAcceleratedProcedure": False
                        },
                        "classification": {
                            "scheme": "",
                            "id": "",
                            "description": ""
                        },
                        "designContest": {
                            "serviceContractAward": False
                        },
                        "electronicWorkflows": {
                            "useOrdering": False,
                            "usePayment": False,
                            "acceptInvoicing": False
                        },
                        "jointProcurement": {
                            "isJointProcurement": False
                        },
                        "legalBasis": "",
                        "procedureOutsourcing": {
                            "procedureOutsourced": False
                        },
                        "dynamicPurchasingSystem": {
                            "hasDynamicPurchasingSystem": False
                        },
                        "framework": {
                            "isAFramework": True
                        }
                    },
                    "relatedProcesses": [
                        {
                            "id": "",
                            "relationship": [
                                ""
                            ],
                            "scheme": "",
                            "identifier": "",
                            "uri": ""
                        }
                    ]
                }
            ]
        }

    def build_expected_ap_release(self):
        """Build AP release."""

        if "documents" in self.__ap_payload['tender']:
            try:
                """
                Build the releases.tender.documents array.
                """
                new_documents_array = list()
                for q_0 in range(len(self.__ap_payload['tender']['documents'])):

                    new_documents_array.append(copy.deepcopy(
                        self.__expected_ap_release['releases'][0]['tender']['documents'][0]))

                    # Enrich or delete optional fields:
                    if "description" in self.__ap_payload['tender']['documents'][q_0]:
                        new_documents_array[q_0]['description'] = self.__ap_payload['tender']['documents'][q_0][
                            'description']
                    else:
                        del new_documents_array[q_0]['description']

                    # Enrich required fields:
                    new_documents_array[q_0]['id'] = self.__ap_payload['tender']['documents'][q_0]['id']
                    new_documents_array[q_0]['documentType'] = self.__ap_payload['tender']['documents'][q_0][
                        'documentType']
                    new_documents_array[q_0]['title'] = self.__ap_payload['tender']['documents'][q_0]['title']

                    new_documents_array[q_0]['url'] = \
                        f"{self.__metadata_document_url}/{self.__ap_payload['tender']['documents'][q_0]['id']}"

                    new_documents_array[q_0]['datePublished'] = self.__ap_message['data']['operationDate']
                self.__expected_ap_release['releases'][0]['tender']['documents'] = new_documents_array
            except ValueError:
                ValueError("Impossible to build the expected releases.tender.documents array.")
        else:
            del self.__expected_ap_release['releases'][0]['tender']['documents']

        # Enrich required fields:
        is_permanent_tender_id_correct = is_it_uuid(
            self.__actual_ap_release['releases'][0]['tender']['id'])

        if is_permanent_tender_id_correct is True:

            self.__expected_ap_release['releases'][0]['tender']['id'] = \
                self.__actual_ap_release['releases'][0]['tender']['id']
        else:
            ValueError(f"The relases0.relatedProcess0.id must be uuid.")

        self.__expected_ap_release['releases'][0]['tender']['tenderPeriod']['startDate'] = \
            self.__ap_payload['tender']['tenderPeriod']['startDate']

        self.__expected_ap_release['releases'][0]['tender']['submissionMethod'][0] = "electronicSubmission"

        self.__expected_ap_release['releases'][0]['tender']['submissionMethodDetails'] = \
            "Lista platformelor: achizitii, ebs, licitatie, yptender"

        self.__expected_ap_release['releases'][0]['tender']['submissionMethodRationale'][0] = \
            "Ofertele vor fi primite prin intermediul unei platforme electronice de achizi??ii publice"

        central_purchasing_body_array = list()
        central_purchasing_body_array.append(copy.deepcopy(self.__expected_ap_release['releases'][0]['parties'][0]))

        central_purchasing_body_array[0]['id'] = \
            f"{self.__ap_payload['tender']['procuringEntity']['identifier']['scheme']}-" \
            f"{self.__ap_payload['tender']['procuringEntity']['identifier']['id']}"

        central_purchasing_body_array[0]['name'] = self.__ap_payload['tender']['procuringEntity']['name']

        central_purchasing_body_array[0]['identifier']['scheme'] = \
            self.__ap_payload['tender']['procuringEntity']['identifier']['scheme']

        central_purchasing_body_array[0]['identifier']['id'] = \
            self.__ap_payload['tender']['procuringEntity']['identifier']['id']

        central_purchasing_body_array[0]['identifier']['legalName'] = \
            self.__ap_payload['tender']['procuringEntity']['identifier']['legalName']

        central_purchasing_body_array[0]['address']['streetAddress'] = \
            self.__ap_payload['tender']['procuringEntity']['address']['streetAddress']

        if "postalCode" in self.__ap_payload['tender']['procuringEntity']['address']:

            central_purchasing_body_array[0]['address']['postalCode'] = \
                self.__ap_payload['tender']['procuringEntity']['address']['postalCode']
        else:
            del central_purchasing_body_array[0]['address']['postalCode']

        try:
            """
            Prepare addressDetails object for party with buyer role.
            """
            central_purchasing_body_country_data = get_value_from_country_csv(
                country=self.__ap_payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
                language=self.__language
            )
            expected_central_purchasing_body_country_object = {
                "scheme": central_purchasing_body_country_data[2],
                "id": self.__ap_payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
                "description": central_purchasing_body_country_data[1],
                "uri": central_purchasing_body_country_data[3]
            }

            central_purchasing_body_region_data = get_value_from_region_csv(
                region=self.__ap_payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
                country=self.__ap_payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
                language=self.__language
            )
            expected_central_purchasing_body_region_object = {
                "scheme": central_purchasing_body_region_data[2],
                "id": self.__ap_payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
                "description": central_purchasing_body_region_data[1],
                "uri": central_purchasing_body_region_data[3]
            }

            if self.__ap_payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] == \
                    "CUATM":

                central_purchasing_body_locality_data = get_value_from_locality_csv(
                    locality=self.__ap_payload['tender']['procuringEntity']['address'][
                        'addressDetails']['locality']['id'],

                    region=self.__ap_payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],

                    country=self.__ap_payload['tender']['procuringEntity']['address'][
                        'addressDetails']['country']['id'],

                    language=self.__language
                )
                expected_central_purchasing_body_locality_object = {
                    "scheme": central_purchasing_body_locality_data[2],
                    "id": self.__ap_payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],
                    "description": central_purchasing_body_locality_data[1],
                    "uri": central_purchasing_body_locality_data[3]
                }
            else:
                expected_central_purchasing_body_locality_object = {
                    "scheme": self.__ap_payload['tender']['procuringEntity']['address'][
                        'addressDetails']['locality']['scheme'],

                    "id": self.__ap_payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],

                    "description": self.__ap_payload['tender']['procuringEntity']['address'][
                        'addressDetails']['locality']['description']
                }

            central_purchasing_body_array[0]['address']['addressDetails']['country'] = \
                expected_central_purchasing_body_country_object

            central_purchasing_body_array[0]['address']['addressDetails']['region'] = \
                expected_central_purchasing_body_region_object

            central_purchasing_body_array[0]['address']['addressDetails']['locality'] = \
                expected_central_purchasing_body_locality_object
        except ValueError:
            ValueError(
                "Impossible to prepare addressDetails object for party with buyer role.")

        if "uri" in self.__ap_payload['tender']['procuringEntity']['identifier']:
            central_purchasing_body_array[0]['identifier']['uri'] = \
                self.__ap_payload['tender']['procuringEntity']['identifier']['uri']
        else:
            del central_purchasing_body_array[0]['identifier']['uri']

        if "additionalIdentifiers" in self.__ap_payload['tender']['procuringEntity']:
            del central_purchasing_body_array[0]['additionalIdentifiers'][0]
            additional_identifiers = list()
            for q_1 in range(len(self.__ap_payload['tender']['procuringEntity']['additionalIdentifiers'])):

                additional_identifiers.append(copy.deepcopy(
                    self.__expected_ap_release['releases'][0]['parties'][0]['additionalIdentifiers'][0]
                ))

                additional_identifiers[q_1]['scheme'] = \
                    self.__ap_payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['scheme']

                additional_identifiers[q_1]['id'] = \
                    self.__ap_payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['id']

                additional_identifiers[q_1]['legalName'] = \
                    self.__ap_payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['legalName']

                additional_identifiers[q_1]['uri'] = \
                    self.__ap_payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['uri']

                central_purchasing_body_array[0]['additionalIdentifiers'] = additional_identifiers
        else:
            del central_purchasing_body_array[0]['additionalIdentifiers']

        if "faxNumber" in self.__ap_payload['tender']['procuringEntity']['contactPoint']:

            central_purchasing_body_array[0]['contactPoint']['faxNumber'] = \
                self.__ap_payload['tender']['procuringEntity']['contactPoint']['faxNumber']
        else:
            del central_purchasing_body_array[0]['contactPoint']['faxNumber']

        if "url" in self.__ap_payload['tender']['procuringEntity']['contactPoint']:

            central_purchasing_body_array[0]['contactPoint']['url'] = \
                self.__ap_payload['tender']['procuringEntity']['contactPoint']['url']
        else:
            del central_purchasing_body_array[0]['contactPoint']['url']

        central_purchasing_body_array[0]['contactPoint']['name'] = \
            self.__ap_payload['tender']['procuringEntity']['contactPoint']['name']

        central_purchasing_body_array[0]['contactPoint']['email'] = \
            self.__ap_payload['tender']['procuringEntity']['contactPoint']['email']

        central_purchasing_body_array[0]['contactPoint']['telephone'] = \
            self.__ap_payload['tender']['procuringEntity']['contactPoint']['telephone']

        central_purchasing_body_array[0]['roles'] = ["centralPurchasingBody"]

        self.__expected_ap_release['releases'][0]['parties'] = central_purchasing_body_array

        # Build the releases.relatedProcesses array. Enrich required fields
        is_permanent_related_process_id_correct = is_it_uuid(
            self.__actual_ap_release['releases'][0]['relatedProcesses'][0]['id'])

        if is_permanent_related_process_id_correct is True:

            self.__expected_ap_release['releases'][0]['relatedProcesses'][0]['id'] = \
                self.__actual_ap_release['releases'][0]['relatedProcesses'][0]['id']
        else:
            ValueError(f"The relases0.relatedProcess0.id must be uuid.")

        self.__expected_ap_release['releases'][0]['relatedProcesses'][0]['relationship'][0] = "parent"
        self.__expected_ap_release['releases'][0]['relatedProcesses'][0]['scheme'] = "ocid"

        self.__expected_ap_release['releases'][0]['relatedProcesses'][0]['identifier'] = \
            self.__ap_message['data']['ocid']

        self.__expected_ap_release['releases'][0]['relatedProcesses'][0]['uri'] = \
            f"{self.__metadata_tender_url}/{self.__ap_message['data']['ocid']}/{self.__ap_message['data']['ocid']}"

        return self.__expected_ap_release

    def build_expected_fa_release(self):
        """Build MS release."""

        # Build the releases.tender object. Enrich or delete optional fields and enrich required fields:
        is_permanent_tender_id_correct = is_it_uuid(
            self.__actual_fa_release['releases'][0]['tender']['id'])

        if is_permanent_tender_id_correct is True:

            self.__expected_fa_release['releases'][0]['tender']['id'] = \
                self.__actual_fa_release['releases'][0]['tender']['id']
        else:
            ValueError(f"The relases0.tender.id must be uuid.")

        self.__expected_fa_release['releases'][0]['tender']['title'] = self.__ap_payload['tender']['title']
        self.__expected_fa_release['releases'][0]['tender']['description'] = self.__ap_payload['tender']['description']

        expected_cpv_data = get_value_from_cpv_dictionary_xls(
            cpv=self.__ap_payload['tender']['classification']['id'],
            language=self.__language
        )

        self.__expected_fa_release['releases'][0]['tender']['classification']['id'] = expected_cpv_data[0]
        self.__expected_fa_release['releases'][0]['tender']['classification']['description'] = expected_cpv_data[1]
        self.__expected_fa_release['releases'][0]['tender']['classification']['scheme'] = "CPV"

        self.__expected_fa_release['releases'][0]['tender']['legalBasis'] = self.__ap_payload['tender']['legalBasis']

        try:
            """
            Enrich procurementMethod and procurementMethodDetails, depends on pmd.
            """
            expected_procurement_method = None
            expected_procurement_method_details = None
            has_dynamic_purchasing_system = None
            if self.__pmd == "TEST_CF":
                expected_procurement_method = 'selective'
                expected_procurement_method_details = "testClosedFA"
                has_dynamic_purchasing_system = False
            elif self.__pmd == "CF":
                expected_procurement_method = 'selective'
                expected_procurement_method_details = "closedFA"
                has_dynamic_purchasing_system = False
            elif self.__pmd == "TEST_OF":
                expected_procurement_method = 'selective'
                expected_procurement_method_details = "testOpenFA"
                has_dynamic_purchasing_system = True
            elif self.__pmd == "OF":
                expected_procurement_method = 'selective'
                expected_procurement_method_details = "openFA"
                has_dynamic_purchasing_system = True
            else:
                ValueError("Check your pmd: You must use 'TEST_CF', 'TEST_CF', 'TEST_OF', 'OF' in pytest command")

            self.__expected_fa_release['releases'][0]['tender']['procurementMethod'] = expected_procurement_method

            self.__expected_fa_release['releases'][0]['tender'][
                'procurementMethodDetails'] = expected_procurement_method_details

            if "procurementMethodRationale" in self.__ap_payload['tender']:

                self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale'] = \
                    self.__ap_payload['tender']['procurementMethodRationale']
            else:
                del self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale']

            self.__expected_fa_release['releases'][0]['tender']['dynamicPurchasingSystem'][
                'hasDynamicPurchasingSystem'] = has_dynamic_purchasing_system

        except KeyError:
            KeyError("Could not parse a pmd into pytest command.")

        try:
            """
            Enrich eligibilityCriteria, depends on language.
            """
            expected_eligibility_criteria = None
            if self.__language == "ro":
                expected_eligibility_criteria = "Regulile generale privind na??ionalitatea ??i originea, precum ??i " \
                                               "alte criterii de eligibilitate sunt enumerate ??n " \
                                               "Ghidul practic privind procedurile de contractare " \
                                               "a ac??iunilor externe ale UE (PRAG)"
            elif self.__language == "en":
                expected_eligibility_criteria = "The general rules on nationality and origin, " \
                                               "as well as other eligibility criteria are listed " \
                                               "in the Practical Guide to Contract Procedures for EU " \
                                               "External Actions (PRAG)"
            else:
                ValueError("Check your language: You must use 'ro', 'en' in pytest command.")

            self.__expected_fa_release['releases'][0]['tender']['eligibilityCriteria'] = expected_eligibility_criteria
        except KeyError:
            KeyError("Could not parse a language into pytest command.")

        self.__expected_fa_release['releases'][0]['tender']['contractPeriod']['startDate'] = \
            self.__ap_payload['tender']['contractPeriod']['startDate']

        self.__expected_fa_release['releases'][0]['tender']['contractPeriod']['endDate'] = \
            self.__ap_payload['tender']['contractPeriod']['endDate']

        self.__expected_fa_release['releases'][0]['tender']['value']['currency'] = \
            self.__ap_payload['tender']['value']['currency']

        # Build the releases.relatedProcesses array. Enrich required fields:
        is_permanent_related_process_id_correct = is_it_uuid(
            self.__actual_fa_release['releases'][0]['relatedProcesses'][0]['id'])

        if is_permanent_related_process_id_correct is True:

            self.__expected_fa_release['releases'][0]['relatedProcesses'][0]['id'] = \
                self.__actual_fa_release['releases'][0]['relatedProcesses'][0]['id']
        else:
            ValueError(f"The relases0.relatedProcess0.id must be uuid.")
        self.__expected_fa_release['releases'][0]['relatedProcesses'][0]['relationship'][0] = "aggregatePlanning"
        self.__expected_fa_release['releases'][0]['relatedProcesses'][0]['scheme'] = "ocid"

        self.__expected_fa_release['releases'][0]['relatedProcesses'][0]['identifier'] = \
            self.__ap_message['data']['outcomes']['ap'][0]['id']

        self.__expected_fa_release['releases'][0]['relatedProcesses'][0]['uri'] = \
            f"{self.__metadata_tender_url}/{self.__ap_message['data']['ocid']}/" \
            f"{self.__ap_message['data']['outcomes']['ap'][0]['id']}"

        return self.__expected_fa_release
