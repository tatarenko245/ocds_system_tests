"""Prepare the expected releases of the framework establishment process, framework agreement procedures."""
import copy

from functions_collection.cassandra_methods import fe_enquiry_period_end_date
from functions_collection.some_functions import is_it_uuid


class CreateFrameworkEstablishmentRelease:
    """This class creates instance of release."""

    def __init__(self, environment, host_to_service, country, language, pmd, ap_cpid, ap_ocid, fe_ocid, payload,
                 actual_message, previous_ap_release, actual_ap_release, actual_fe_release, previous_fa_release,
                 actual_fa_release):

        self.__environment = environment
        self.__host = host_to_service
        self.__country = country
        self.__language = language
        self.__pmd = pmd
        self.__ap_cpid = ap_cpid
        self.__ap_ocid = ap_ocid
        self.__fe_ocid = fe_ocid
        self.__payload = payload
        self.__actual_message = actual_message
        self.__previous_ap_release = previous_ap_release
        self.__actual_ap_release = actual_ap_release
        self.__previous_fa_release = previous_fa_release
        self.__actual_fa_release = actual_fa_release
        self.__actual_fe_release = actual_fe_release

        try:
            if environment == "dev":
                self.__metadata_tender_url = "http://dev.public.eprocurement.systems/tenders"

                self.__extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"
                ]

                self.__publisher_name = "M-Tender"
                self.__publisher_uri = "https://www.mtender.gov.md"
                self.__metadata_document_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get"
                self.__metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"

            elif environment == "sandbox":
                self.__metadata_tender_url = "http://public.eprocurement.systems/tenders"

                self.__extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.json"
                ]

                self.__publisher_name = "Viešųjų pirkimų tarnyba"
                self.__publisher_uri = "https://vpt.lrv.lt"
                self.__metadata_document_url = "http://storage.eprocurement.systems/get"
                self.__metadata_budget_url = "http://public.eprocurement.systems/budgets"
        except ValueError:
            ValueError("Check your environment: You must use 'dev' or 'sandbox' environment in pytest command")

        self.__expected_ap_release = {
            "uri": self.__previous_ap_release['uri'],
            "version": self.__previous_ap_release['version'],
            "extensions": self.__previous_ap_release['extensions'],
            "publisher": {
                "name": self.__previous_ap_release['publisher']['name'],
                "uri": self.__previous_ap_release['publisher']['uri']
            },
            "license": self.__previous_ap_release['license'],
            "publicationPolicy": self.__previous_ap_release['publicationPolicy'],
            "publishedDate": self.__previous_ap_release['publishedDate'],
            "releases": [
                {
                    "ocid": self.__previous_ap_release['releases'][0]['ocid'],
                    "id": f"{self.__ap_ocid}-{self.__actual_ap_release['releases'][0]['id'][46:59]}",
                    "date": self.__actual_message['data']['operationDate'],
                    "tag": self.__previous_ap_release['releases'][0]['tag'],
                    "language": self.__previous_ap_release['releases'][0]['language'],
                    "initiationType": self.__previous_ap_release['releases'][0]['initiationType'],
                    "parties": self.__previous_ap_release['releases'][0]['parties'],
                    "tender": {
                        "id": self.__previous_ap_release['releases'][0]['tender']['id'],
                        "status": "planned",
                        "statusDetails": "aggregated",
                        "items": [
                            {
                                "id": "",
                                "internalId": "",
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
                                "quantity": 0.0,
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
                                },
                                "relatedLot": ""
                            }
                        ],
                        "lots": [
                            {
                                "id": "",
                                "internalId": "",
                                "title": "",
                                "description": "",
                                "status": "",
                                "statusDetails": "",
                                "placeOfPerformance": {
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
                                    }
                                }
                            }
                        ],
                        "tenderPeriod": {
                            "startDate": self.__previous_ap_release['releases'][0]['tender']['tenderPeriod'][
                                'startDate']
                        },
                        "hasEnquiries": self.__previous_ap_release['releases'][0]['tender']['hasEnquiries'],
                        "documents": [
                            {
                                "id": "",
                                "documentType": "",
                                "title": "",
                                "description": "",
                                "url": "",
                                "datePublished": "",
                                "relatedLots": [""]
                            }
                        ],
                        "submissionMethod": self.__previous_ap_release['releases'][0]['tender']['submissionMethod'],
                        "submissionMethodDetails": self.__previous_ap_release['releases'][0]['tender'][
                            'submissionMethodDetails'],
                        "submissionMethodRationale": self.__previous_ap_release['releases'][0]['tender'][
                            'submissionMethodRationale'],
                        "requiresElectronicCatalogue": self.__previous_ap_release['releases'][0]['tender'][
                            'requiresElectronicCatalogue']
                    },
                    "hasPreviousNotice": self.__previous_ap_release['releases'][0]['hasPreviousNotice'],
                    "purposeOfNotice": {
                        "isACallForCompetition": self.__previous_ap_release['releases'][0][
                            'purposeOfNotice']['isACallForCompetition']
                    },
                    "relatedProcesses": self.__previous_ap_release['releases'][0]['relatedProcesses']
                }
            ]
        }

        self.__expected_fe_release = {
            "uri": f"{self.__metadata_tender_url}/{self.__actual_message['data']['ocid']}/"
                   f"{self.__actual_message['data']['outcomes']['fe'][0]['id']}",

            "version": "1.1",
            "extensions": self.__extensions,
            "publisher": {
                "name": self.__publisher_name,
                "uri": self.__publisher_uri
            },
            "license": "http://opendefinition.org/licenses/",
            "publicationPolicy": "http://opendefinition.org/licenses/",
            "publishedDate": self.__actual_message['data']['operationDate'],
            "releases": [
                {
                    "ocid": "",
                    "id": "",
                    "date": "",
                    "tag": [
                        ""
                    ],
                    "language": "",
                    "initiationType": "",
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
                            "persones": [
                                {
                                    "id": "",
                                    "title": "",
                                    "name": "",
                                    "identifier": {
                                        "scheme": "",
                                        "id": "",
                                        "uri": ""
                                    },
                                    "businessFunctions": [
                                        {
                                            "id": "",
                                            "type": "",
                                            "jobTitle": "",
                                            "period": {
                                                "startDate": ""
                                            },
                                            "documents": [
                                                {
                                                    "id": "",
                                                    "documentType": "",
                                                    "title": "",
                                                    "description": "",
                                                    "url": "",
                                                    "datePublished": ""
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "roles": [
                                ""
                            ]
                        }
                    ],
                    "tender": {
                        "id": "",
                        "status": "",
                        "statusDetails": "",
                        "criteria": [
                            {
                                "id": "",
                                "title": "",
                                "source": "",
                                "description": "",
                                "requirementGroups": [
                                    {
                                        "id": "",
                                        "description": "",
                                        "requirements": [
                                            {
                                                "id": "",
                                                "title": "",
                                                "dataType": "",
                                                "status": "",
                                                "datePublished": "",
                                                "description": "",
                                                "period": {
                                                    "startDate": "",
                                                    "endDate": ""
                                                },
                                                "eligibleEvidences": [
                                                    {
                                                        "id": "",
                                                        "title": "",
                                                        "type": "",
                                                        "description": "",
                                                        "relatedDocument": {
                                                            "id": ""
                                                        }
                                                    }
                                                ],
                                                "expectedValue": "",
                                                "minValue": "",
                                                "maxValue": ""
                                            }
                                        ]
                                    }
                                ],
                                "relatesTo": "",
                                "classification": {
                                    "scheme": "",
                                    "id": ""
                                }
                            }
                        ],
                        "otherCriteria": {
                            "reductionCriteria": "",
                            "qualificationSystemMethods": ""
                        },
                        "enquiryPeriod": {
                            "startDate": "",
                            "endDate": ""
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
                        "requiresElectronicCatalogue": False,
                        "procurementMethodModalities": [""],
                        "secondStage": {
                            "minimumCandidates": 1,
                            "maximumCandidates": 2
                        }
                    },
                    "preQualification": {
                        "period": {
                            "startDate": "",
                            "endDate": ""
                        }
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
            "uri": self.__previous_fa_release['uri'],
            "version": self.__previous_fa_release['version'],
            "extensions": self.__previous_fa_release['extensions'],
            "publisher": {
                "name": self.__previous_fa_release['publisher']['name'],
                "uri": self.__previous_fa_release['publisher']['uri']
            },
            "license": self.__previous_fa_release['license'],
            "publicationPolicy": self.__previous_fa_release['publicationPolicy'],
            "publishedDate": self.__previous_fa_release['publishedDate'],
            "releases": [
                {
                    "ocid": self.__previous_fa_release['releases'][0]['ocid'],
                    "id": f"{self.__ap_cpid}-{self.__actual_fa_release['releases'][0]['id'][46:59]}",
                    "date": self.__actual_message['data']['operationDate'],
                    "tag": self.__previous_fa_release['releases'][0]['tag'],
                    "language": self.__previous_fa_release['releases'][0]['language'],
                    "initiationType": self.__previous_fa_release['releases'][0]['initiationType'],
                    "tender": {
                        "id": self.__previous_fa_release['releases'][0]['tender']['id'],
                        "title": self.__previous_fa_release['releases'][0]['tender']['title'],
                        "description": self.__previous_fa_release['releases'][0]['tender']['description'],
                        "status": "active",
                        "statusDetails": "establishment",
                        "value": {
                            "amount": self.__previous_fa_release['releases'][0]['tender']['value']['amount'],
                            "currency": self.__previous_fa_release['releases'][0]['tender']['value']['currency']
                        },
                        "procurementMethod": self.__previous_fa_release['releases'][0]['tender']['procurementMethod'],
                        "procurementMethodDetails": self.__previous_fa_release['releases'][0]['tender'][
                            'procurementMethodDetails'],
                        "procurementMethodRationale": "",
                        "mainProcurementCategory": self.__previous_fa_release['releases'][0]['tender'][
                            'mainProcurementCategory'],
                        "hasEnquiries": self.__previous_fa_release['releases'][0]['tender']['hasEnquiries'],
                        "eligibilityCriteria": self.__previous_fa_release['releases'][0]['tender'][
                            'eligibilityCriteria'],
                        "contractPeriod": {
                            "startDate": self.__previous_fa_release['releases'][0]['tender']['contractPeriod'][
                                'startDate'],
                            "endDate": self.__previous_fa_release['releases'][0]['tender']['contractPeriod'][
                                'endDate']
                        },
                        "procuringEntity": {
                            "id": "",
                            "name": ""
                        },
                        "acceleratedProcedure": {
                            "isAcceleratedProcedure": self.__previous_fa_release['releases'][0]['tender'][
                                'acceleratedProcedure']['isAcceleratedProcedure']
                        },
                        "classification": {
                            "scheme": self.__previous_fa_release['releases'][0]['tender']['classification']['scheme'],
                            "id": self.__previous_fa_release['releases'][0]['tender']['classification']['id'],
                            "description": self.__previous_fa_release['releases'][0]['tender']['classification'][
                                'description']
                        },
                        "designContest": {
                            "serviceContractAward": self.__previous_fa_release['releases'][0]['tender'][
                                'designContest']['serviceContractAward']
                        },
                        "electronicWorkflows": {
                            "useOrdering": self.__previous_fa_release['releases'][0]['tender'][
                                'electronicWorkflows']['useOrdering'],
                            "usePayment": self.__previous_fa_release['releases'][0]['tender'][
                                'electronicWorkflows']['usePayment'],
                            "acceptInvoicing": self.__previous_fa_release['releases'][0]['tender'][
                                'electronicWorkflows']['acceptInvoicing']
                        },
                        "jointProcurement": {
                            "isJointProcurement": self.__previous_fa_release['releases'][0]['tender'][
                                'jointProcurement']['isJointProcurement']
                        },
                        "legalBasis": self.__previous_fa_release['releases'][0]['tender']['legalBasis'],
                        "procedureOutsourcing": {
                            "procedureOutsourced": self.__previous_fa_release['releases'][0]['tender'][
                                'procedureOutsourcing']['procedureOutsourced']
                        },
                        "dynamicPurchasingSystem": {
                            "hasDynamicPurchasingSystem": self.__previous_fa_release['releases'][0]['tender'][
                                'dynamicPurchasingSystem']['hasDynamicPurchasingSystem']
                        },
                        "framework": {
                            "isAFramework": self.__previous_fa_release['releases'][0]['tender'][
                                'framework']['isAFramework']
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

        self.__expected_ap_release['releases'][0]['tender']['lots'] = \
            self.__previous_ap_release['releases'][0]['tender']['lots']

        self.__expected_ap_release['releases'][0]['tender']['items'] = \
            self.__previous_ap_release['releases'][0]['tender']['items']

        if "documents" in self.__previous_ap_release['releases'][0]['tender']:
            self.__expected_ap_release['releases'][0]['tender']['documents'] = \
                self.__previous_ap_release['releases'][0]['tender']['documents']
        else:
            del self.__expected_ap_release['releases'][0]['tender']['documents']
        return self.__expected_ap_release

    def build_expected_fe_release(self, period_shift):
        """Build FE release."""

        # Enrich 'releases[0]' section:

        # FR.COM-3.2.5
        self.__expected_fe_release['releases'][0]['ocid'] = self.__actual_message['data']['outcomes']['fe'][0]['id']

        # FR.COM-3.2.21
        self.__expected_fe_release['releases'][0]['id'] = \
            f"{self.__actual_message['data']['outcomes']['fe'][0]['id']}-" \
            f"{self.__actual_fe_release['releases'][0]['id'][46:59]}"

        # FR.COM-3.2.23
        self.__expected_fe_release['releases'][0]['language'] = self.__language

        # FR.COM-3.2.4
        self.__expected_fe_release['releases'][0]['initiationType'] = "tender"

        self.__expected_fe_release['releases'][0]['date'] = self.__actual_message['data']['operationDate']

        # FR.COM-3.2.2
        self.__expected_fe_release['releases'][0]['tag'] = ["tender"]

        # Enrich 'releases[0].tender' section:
        # FR.COM-3.2.8

        # FR.COM-1.28.1
        try:
            """Set permanent id."""

            is_permanent_id_correct = is_it_uuid(
                self.__actual_fe_release['releases'][0]['tender']['id'])

            if is_permanent_id_correct is True:

                self.__expected_fe_release['releases'][0]['tender']['id'] = \
                    self.__actual_fe_release['releases'][0]['tender']['id']
            else:
                ValueError(f"The 'releases[0].tender.id' must be uuid.")
        except KeyError:
            KeyError("Mismatch key into path 'releases[0].tender.id'")

        # BR-1.0.1.4.2
        self.__expected_fe_release['releases'][0]['tender']['status'] = "active"
        self.__expected_fe_release['releases'][0]['tender']['statusDetails'] = "submission"

        # FR.COM-1.28.1
        if "criteria" in self.__payload['tender']:
            expected_criteria_array = list()

            try:
                """Prepare criteria array for expected FE release."""
                for q_0 in range(len(self.__payload['tender']['criteria'])):

                    expected_criteria_array.append(copy.deepcopy(
                        self.__expected_fe_release['releases'][0]['tender']['criteria'][0]
                    ))

                    # BR-1.0.1.16.1
                    try:
                        """Set permanent id."""

                        is_permanent_id_correct = is_it_uuid(
                            self.__actual_fe_release['releases'][0]['tender']['criteria'][q_0]['id'])

                        if is_permanent_id_correct is True:

                            expected_criteria_array[q_0]['id'] = \
                                self.__actual_fe_release['releases'][0]['tender']['criteria'][q_0]['id']
                        else:
                            ValueError(f"The 'releases[0].tender.criteria[{q_0}].id' must be uuid.")
                    except KeyError:
                        KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}].id'")

                    expected_criteria_array[q_0]['title'] = self.__payload['tender']['criteria'][q_0]['title']

                    # BR-1.0.1.16.2
                    expected_criteria_array[q_0]['source'] = "tenderer"

                    expected_criteria_array[q_0]['relatesTo'] = \
                        self.__payload['tender']['criteria'][q_0]['relatesTo']

                    # BR-1.0.1.16.3
                    expected_criteria_array[q_0]['classification']['id'] = \
                        self.__payload['tender']['criteria'][q_0]['classification']['id']

                    expected_criteria_array[q_0]['classification']['scheme'] = \
                        self.__payload['tender']['criteria'][q_0]['classification']['scheme']

                    if "description" in self.__payload['tender']['criteria'][q_0]:

                        expected_criteria_array[q_0]['description'] = \
                            self.__payload['tender']['criteria'][q_0]['description']
                    else:
                        del expected_criteria_array[q_0]['description']

                    expected_requirement_groups_array = list()
                    for q_1 in range(len(self.__payload['tender']['criteria'][q_0]['requirementGroups'])):

                        expected_requirement_groups_array.append(copy.deepcopy(
                            self.__expected_fe_release['releases'][0]['tender']['criteria'][0]['requirementGroups'][0]
                        ))

                        # BR-1.0.1.17.1
                        try:
                            """Set permanent id."""

                            is_permanent_id_correct = is_it_uuid(
                                self.__actual_fe_release['releases'][0]['tender']['criteria'][q_0][
                                    'requirementGroups'][q_1]['id']
                            )

                            if is_permanent_id_correct is True:

                                expected_requirement_groups_array[q_1]['id'] = \
                                    self.__actual_fe_release['releases'][0]['tender']['criteria'][q_0][
                                        'requirementGroups'][q_1]['id']
                            else:
                                ValueError(f"The 'releases[0].tender.criteria[{q_0}].requirementGroups[{q_1}]."
                                           f"id' must be uuid.")
                        except KeyError:
                            KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}]."
                                     f"requirementGroups[{q_1}].id'")

                        if "description" in self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1]:

                            expected_requirement_groups_array[q_1]['description'] = \
                                self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['description']
                        else:
                            del expected_requirement_groups_array[q_1]['description']

                        expected_requirements_array = list()
                        for q_2 in range(len(
                                self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements']
                        )):
                            expected_requirements_array.append(copy.deepcopy(
                                self.__expected_fe_release['releases'][0]['tender']['criteria'][0][
                                    'requirementGroups'][0]['requirements'][0]
                            ))

                            # BR-1.0.1.18.1
                            try:
                                """Set permanent id."""

                                is_permanent_id_correct = is_it_uuid(
                                    self.__actual_fe_release['releases'][0]['tender']['criteria'][q_0][
                                        'requirementGroups'][q_1]['requirements'][q_2]['id']
                                )

                                if is_permanent_id_correct is True:

                                    expected_requirements_array[q_2]['id'] = \
                                        self.__actual_fe_release['releases'][0]['tender']['criteria'][q_0][
                                            'requirementGroups'][q_1]['requirements'][q_2]['id']
                                else:
                                    ValueError(
                                        f"The 'releases[0].tender.criteria[{q_0}].requirementGroups[{q_1}]."
                                        f"requirements[{q_2}].id' must be uuid.")
                            except KeyError:
                                KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}]."
                                         f"requirementGroups[{q_1}].requirements[{q_2}].id'")

                            expected_requirements_array[q_2]['title'] = \
                                self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['title']

                            if "description" in self.__payload['tender']['criteria'][q_0][
                                    'requirementGroups'][q_1]['requirements'][q_2]:

                                expected_requirements_array[q_2]['description'] = \
                                    self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['description']
                            else:
                                del expected_requirements_array[q_2]['description']

                            if "period" in self.__payload['tender']['criteria'][q_0][
                                    'requirementGroups'][q_1]['requirements'][q_2]:

                                expected_requirements_array[q_2]['period']['startDate'] = \
                                    self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['period']['startDate']

                                expected_requirements_array[q_2]['period']['endDate'] = \
                                    self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['period']['endDate']
                            else:
                                del expected_requirements_array[q_2]['period']

                            if "expectedValue" not in self.__payload['tender']['criteria'][q_0][
                                    'requirementGroups'][q_1]['requirements'][q_2]:

                                del expected_requirements_array[q_2]['expectedValue']
                            else:
                                expected_requirements_array[q_2]['expectedValue'] = \
                                    self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['expectedValue']

                                expected_requirements_array[q_2]['dataType'] = \
                                    self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['dataType']

                            if "minValue" not in self.__payload['tender']['criteria'][q_0][
                                    'requirementGroups'][q_1]['requirements'][q_2]:

                                del expected_requirements_array[q_2]['minValue']
                            else:
                                expected_requirements_array[q_2]['minValue'] = \
                                    self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['minValue']

                                expected_requirements_array[q_2]['dataType'] = \
                                    self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['dataType']

                            if "maxValue" not in self.__payload['tender']['criteria'][q_0][
                                    'requirementGroups'][q_1]['requirements'][q_2]:

                                del expected_requirements_array[q_2]['maxValue']
                            else:
                                expected_requirements_array[q_2]['maxValue'] = \
                                    self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['maxValue']

                                expected_requirements_array[q_2]['dataType'] = \
                                    self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['dataType']

                            # BR-1.0.1.18.2
                            expected_requirements_array[q_2]['status'] = "active"

                            # BR-1.0.1.18.3
                            expected_requirements_array[q_2]['datePublished'] = \
                                self.__actual_message['data']['operationDate']

                            # BR-1.0.1.18.4
                            if "eligibleEvidences" in self.__payload['tender']['criteria'][q_0][
                                    'requirementGroups'][q_1]['requirements'][q_2]:

                                expected_eligible_evidences_array = list()
                                for q_3 in range(len(self.__payload['tender']['criteria'][q_0][
                                                         'requirementGroups'][q_1]['requirements'][q_2][
                                                         'eligibleEvidences'])):

                                    expected_eligible_evidences_array.append(copy.deepcopy(
                                        self.__expected_fe_release['releases'][0]['tender']['criteria'][0][
                                            'requirementGroups'][0]['requirements'][0]['eligibleEvidences'][0]
                                    ))

                                    try:
                                        """Set permanent id."""
                                        is_permanent_id_correct = is_it_uuid(
                                            self.__actual_fe_release['releases'][0]['tender']['criteria'][q_0][
                                                'requirementGroups'][q_1]['requirements'][q_2][
                                                'eligibleEvidences'][q_3]['id']
                                        )

                                        if is_permanent_id_correct is True:

                                            expected_eligible_evidences_array[q_3]['id'] = \
                                                self.__actual_fe_release['releases'][0]['tender']['criteria'][q_0][
                                                    'requirementGroups'][q_1]['requirements'][q_2][
                                                    'eligibleEvidences'][q_3]['id']
                                        else:
                                            ValueError(
                                                f"The 'releases[0].tender.criteria[{q_0}].requirementGroups[{q_1}]."
                                                f"requirements[{q_2}].eligibleEvidences[{q_3}].id' must be uuid.")
                                    except KeyError:
                                        KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}]."
                                                 f"requirementGroups[{q_1}].requirements[{q_2}]."
                                                 f"eligibleEvidences[{q_3}].id'")

                                    expected_eligible_evidences_array[q_3]['title'] = \
                                        self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                            'requirements'][q_2]['eligibleEvidences'][q_3]['title']

                                    if "description" in self.__payload['tender']['criteria'][q_0][
                                            'requirementGroups'][q_1]['requirements'][q_2]['eligibleEvidences'][q_3]:

                                        expected_eligible_evidences_array[q_3]['description'] = \
                                            self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                                'requirements'][q_2]['eligibleEvidences'][q_3]['description']
                                    else:
                                        del expected_eligible_evidences_array[q_3]['description']

                                    expected_eligible_evidences_array[q_3]['type'] = \
                                        self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                            'requirements'][q_2]['eligibleEvidences'][q_3]['type']

                                    if "relatedDocument" in self.__payload['tender']['criteria'][q_0][
                                            'requirementGroups'][q_1]['requirements'][q_2]['eligibleEvidences'][q_3]:

                                        expected_eligible_evidences_array[q_3]['relatedDocument']['id'] = \
                                            self.__payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                                'requirements'][q_2]['eligibleEvidences'][q_3]['relatedDocument']['id']
                                    else:
                                        del expected_eligible_evidences_array[q_3]['relatedDocument']

                                expected_requirements_array[q_2]['eligibleEvidences'] = \
                                    expected_eligible_evidences_array
                            else:
                                del expected_requirement_groups_array[q_1]['requirements'][q_2]['eligibleEvidences']

                        expected_requirement_groups_array[q_1]['requirements'] = expected_requirements_array
                    expected_criteria_array[q_0]['requirementGroups'] = expected_requirement_groups_array

            except AttributeError:
                AttributeError("Mismatch the attribute for expected criteria array.")

            self.__expected_fe_release['releases'][0]['tender']['criteria'] = expected_criteria_array
        else:
            del self.__expected_fe_release['releases'][0]['tender']['criteria']

        # FR.COM-1.28.1
        self.__expected_fe_release['releases'][0]['tender']['otherCriteria']['reductionCriteria'] = \
            self.__payload['tender']['otherCriteria']['reductionCriteria']

        self.__expected_fe_release['releases'][0]['tender']['otherCriteria']['qualificationSystemMethods'] = \
            self.__payload['tender']['otherCriteria']['qualificationSystemMethods']

        # FR.COM-3.2.8, FR.COM-8.1.1, FR.COM-8.1.2
        self.__expected_fe_release['releases'][0]['tender']['enquiryPeriod']['startDate'] = \
            self.__actual_message['data']['operationDate']

        expected_enquiry_period_end_date = fe_enquiry_period_end_date(
            pre_qualification_period_end_date=self.__payload['preQualification']['period']['endDate'],
            interval_seconds=int(period_shift)
        )

        self.__expected_fe_release['releases'][0]['tender']['enquiryPeriod']['endDate'] = \
            expected_enquiry_period_end_date

        # FR.COM-3.2.7
        self.__expected_fe_release['releases'][0]['tender']['hasEnquiries'] = False

        # FR.COM-1.28.1
        if "documents" in self.__payload['tender']:
            expected_documents_array = list()

            try:
                """Prepare documents array for expected FE release."""
                for q_0 in range(len(self.__payload['tender']['documents'])):

                    expected_documents_array.append(copy.deepcopy(
                        self.__expected_fe_release['releases'][0]['tender']['documents'][0]
                    ))

                    expected_documents_array[q_0]['id'] = self.__payload['tender']['documents'][q_0]['id']

                    expected_documents_array[q_0]['documentType'] = \
                        self.__payload['tender']['documents'][q_0]['documentType']

                    expected_documents_array[q_0]['title'] = \
                        self.__payload['tender']['documents'][q_0]['title']

                    if "description" in expected_documents_array[q_0]:

                        expected_documents_array[q_0]['description'] = \
                            self.__payload['tender']['documents'][q_0]['description']
                    else:
                        del expected_documents_array[q_0]['description']

                    expected_documents_array[q_0]['url'] = \
                        f"{self.__metadata_document_url}/{self.__payload['tender']['documents'][q_0]['id']}"

                    expected_documents_array[q_0]['datePublished'] = self.__actual_message['data']['operationDate']

            except AttributeError:
                AttributeError("Mismatch the attribute for expected documents array.")

            self.__expected_fe_release['releases'][0]['tender']['documents'] = expected_documents_array
        else:
            del self.__expected_fe_release['releases'][0]['tender']['documents']

        # FR.COM-1.28.1
        self.__expected_fe_release['releases'][0]['tender']['submissionMethod'] = \
            self.__actual_ap_release['releases'][0]['tender']['submissionMethod']

        # FR.COM-1.28.1
        self.__expected_fe_release['releases'][0]['tender']['submissionMethodDetails'] = \
            self.__actual_ap_release['releases'][0]['tender']['submissionMethodDetails']

        # FR.COM-1.28.1
        self.__expected_fe_release['releases'][0]['tender']['submissionMethodRationale'] = \
            self.__actual_ap_release['releases'][0]['tender']['submissionMethodRationale']

        # FR.COM-1.28.1
        self.__expected_fe_release['releases'][0]['tender']['requiresElectronicCatalogue'] = \
            self.__actual_ap_release['releases'][0]['tender']['requiresElectronicCatalogue']

        # FR.COM-1.28.1
        if "procurementMethodModalities" in self.__payload['tender']:
            self.__expected_fe_release['releases'][0]['tender']['procurementMethodModalities'] = \
                self.__payload['tender']['procurementMethodModalities']
        else:
            del self.__expected_fe_release['releases'][0]['tender']['procurementMethodModalities']

        # FR.COM-1.28.1
        if "secondStage" in self.__payload['tender']:
            self.__expected_fe_release['releases'][0]['tender']['secondStage'] = \
                self.__payload['tender']['secondStage']
        else:
            del self.__expected_fe_release['releases'][0]['tender']['secondStage']

        # FR.COM-3.2.9
        self.__expected_fe_release['releases'][0]['preQualification']['period']['startDate'] = \
            self.__actual_message['data']['operationDate']

        self.__expected_fe_release['releases'][0]['preQualification']['period']['endDate'] = \
            self.__payload['preQualification']['period']['endDate']

        # FR.COM-3.2.1
        self.__expected_fe_release['releases'][0]['hasPreviousNotice'] = True

        # FR.COM-3.2.3
        self.__expected_fe_release['releases'][0]['purposeOfNotice']['isACallForCompetition'] = True

        # Enrich 'releases[0].['parties']' section:
        # FR.COM-3.2.10, FR.COM-1.28.1
        expected_parties_array = list()

        for q_0 in range(len(self.__actual_ap_release['releases'][0]['parties'])):
            if self.__actual_ap_release['releases'][0]['parties'][q_0]['roles'] == ["centralPurchasingBody"]:
                expected_parties_array.append(self.__actual_ap_release['releases'][0]['parties'][q_0])
                expected_parties_array[q_0]['roles'] = ["procuringEntity"]

                # BR-1.0.1.15.2
                if "procuringEntity" in self.__payload['tender']:
                    expected_persones_array = list()
                    for q_1 in range(len(self.__payload['tender']['procuringEntity']['persones'])):

                        expected_persones_array.append(copy.deepcopy(
                            self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0]
                        ))

                        persones_scheme = \
                            self.__payload['tender']['procuringEntity']['persones'][q_1]['identifier']['scheme']

                        persones_id = \
                            self.__payload['tender']['procuringEntity']['persones'][q_1]['identifier']['id']

                        expected_persones_array[q_1]['id'] = f"{persones_scheme}-{persones_id}"

                        expected_persones_array[q_1]['title'] = \
                            self.__payload['tender']['procuringEntity']['persones'][q_1]['title']

                        expected_persones_array[q_1]['name'] = \
                            self.__payload['tender']['procuringEntity']['persones'][q_1]['name']

                        expected_persones_array[q_1]['identifier']['scheme'] = \
                            self.__payload['tender']['procuringEntity']['persones'][q_1]['identifier']['scheme']

                        expected_persones_array[q_1]['identifier']['id'] = \
                            self.__payload['tender']['procuringEntity']['persones'][q_1]['identifier']['id']

                        if "uri" in expected_persones_array[q_1]['identifier']:

                            expected_persones_array[q_1]['identifier']['uri'] = \
                                self.__payload['tender']['procuringEntity']['persones'][q_1]['identifier']['uri']
                        else:
                            del expected_persones_array[q_1]['identifier']['uri']

                        expected_business_functions_array = list()
                        for q_2 in range(len(
                                self.__payload['tender']['procuringEntity']['persones'][q_1]['businessFunctions'])):

                            expected_business_functions_array.append(copy.deepcopy(
                                self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0][
                                    'businessFunctions'][0]
                            ))

                            try:
                                """Set permanent id."""

                                is_permanent_id_correct = is_it_uuid(
                                    self.__actual_fe_release['releases'][0]['parties'][q_0]['persones'][q_1][
                                        'businessFunctions'][q_2]['id']
                                )

                                if is_permanent_id_correct is True:

                                    expected_business_functions_array[q_2]['id'] = \
                                        self.__actual_fe_release['releases'][0]['parties'][q_0]['persones'][q_1][
                                            'businessFunctions'][q_2]['id']
                                else:
                                    ValueError(
                                        f"The 'releases[0].parties[{q_0}].persones[{q_1}]."
                                        f"businessFunctions[{q_2}].id' must be uuid.")
                            except KeyError:
                                KeyError(f"Mismatch key into path 'releases[0].parties[{q_0}].persones[{q_1}]."
                                         f"businessFunctions[{q_2}].id'")

                            expected_business_functions_array[q_2]['type'] = \
                                self.__payload['tender']['procuringEntity']['persones'][q_1][
                                    'businessFunctions'][q_2]['type']

                            expected_business_functions_array[q_2]['jobTitle'] = \
                                self.__payload['tender']['procuringEntity']['persones'][q_1][
                                    'businessFunctions'][q_2]['jobTitle']

                            expected_business_functions_array[q_2]['period']['startDate'] = \
                                self.__payload['tender']['procuringEntity']['persones'][q_1][
                                    'businessFunctions'][q_2]['period']['startDate']

                            expected_bf_documents_array = list()
                            if "documents" in self.__payload['tender']['procuringEntity']['persones'][q_1][
                                    'businessFunctions'][q_2]:

                                for q_3 in range(len(self.__payload['tender']['procuringEntity']['persones'][q_1][
                                                         'businessFunctions'][q_2]['documents'])):

                                    expected_bf_documents_array.append(copy.deepcopy(
                                        self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0][
                                            'businessFunctions'][0]['documents'][0]
                                    ))

                                    expected_bf_documents_array[q_3]['id'] = \
                                        self.__payload['tender']['procuringEntity']['persones'][q_1][
                                            'businessFunctions'][q_2]['documents'][q_3]['id']

                                    expected_bf_documents_array[q_3]['documentType'] = \
                                        self.__payload['tender']['procuringEntity']['persones'][q_1][
                                            'businessFunctions'][q_2]['documents'][q_3]['documentType']

                                    expected_bf_documents_array[q_3]['title'] = \
                                        self.__payload['tender']['procuringEntity']['persones'][q_1][
                                            'businessFunctions'][q_2]['documents'][q_3]['title']

                                    if "description" in self.__payload['tender']['procuringEntity'][
                                            'persones'][q_1]['businessFunctions'][q_2]['documents'][q_3]:

                                        expected_bf_documents_array[q_3]['description'] = \
                                            self.__payload['tender']['procuringEntity']['persones'][q_1][
                                                'businessFunctions'][q_2]['documents'][q_3]['description']
                                    else:
                                        del expected_bf_documents_array[q_3]['description']

                                    expected_bf_documents_array[q_3]['url'] = \
                                        f"{self.__metadata_document_url}/" \
                                        f"{expected_bf_documents_array[q_3]['id']}"

                                    expected_bf_documents_array[q_3]['datePublished'] = \
                                        self.__actual_message['data']['operationDate']

                                expected_business_functions_array[q_2]['documents'] = \
                                    expected_bf_documents_array
                            else:
                                del expected_business_functions_array[q_2]['documents']

                        expected_persones_array[q_1]['businessFunctions'] = expected_business_functions_array
                    expected_parties_array[q_0]['persones'] = expected_persones_array

            if self.__actual_ap_release['releases'][0]['parties'][q_0]['roles'] == ["client"]:
                expected_parties_array.append(self.__actual_ap_release['releases'][0]['parties'][q_0])
                expected_parties_array[q_0]['roles'] = ["buyer"]

        final_expected_persones_array = list()

        if len(self.__actual_fe_release['releases'][0]['parties']) == len(expected_parties_array):
            for act in range(len(self.__actual_fe_release['releases'][0]['parties'])):
                for exp in range(len(expected_parties_array)):

                    if self.__actual_fe_release['releases'][0]['parties'][act]['id'] == \
                            expected_parties_array[exp]['id']:
                        final_expected_persones_array.append(expected_parties_array[exp])
        else:
            ValueError("The quantity of actual parties array != "
                       "quantity of expected parties array")
        self.__expected_fe_release['releases'][0]['parties'] = final_expected_persones_array

        # Enrich 'releases[0].['relatedProcesses']' section:
        # FR.COM-1.28.1
        expected_related_processes_array = list()

        # Prepare object, where 'relationship' = 'aggregatePlanning'.
        expected_related_processes_array.append(copy.deepcopy(
            self.__expected_fe_release['releases'][0]['relatedProcesses'][0]
        ))

        try:
            """Set permanent id."""

            is_permanent_id_correct = is_it_uuid(
                self.__actual_fe_release['releases'][0]['relatedProcesses'][0]['id']
            )

            if is_permanent_id_correct is True:

                expected_related_processes_array[0]['id'] = \
                    self.__expected_fe_release['releases'][0]['relatedProcesses'][0]
            else:
                ValueError(
                    f"The 'releases[0].relatedProcesses[{0}].id' must be uuid.")
        except KeyError:
            KeyError(f"Mismatch key into path 'releases[0].relatedProcesses[{0}].id'.")

        expected_related_processes_array[0]['relationship'] = ["aggregatePlanning"]
        expected_related_processes_array[0]['scheme'] = "ocid"
        expected_related_processes_array[0]['identifier'] = self.__ap_ocid
        expected_related_processes_array[0]['uri'] = \
            f"{self.__metadata_tender_url}/{self.__ap_cpid}/{self.__ap_ocid}"

        # Prepare object, where 'relationship' = 'parent'.
        expected_related_processes_array.append(copy.deepcopy(
            self.__expected_fe_release['releases'][0]['relatedProcesses'][0]
        ))

        expected_related_processes_array[1]['relationship'] = ["parent"]
        expected_related_processes_array[1]['scheme'] = "ocid"
        expected_related_processes_array[1]['identifier'] = self.__ap_cpid
        expected_related_processes_array[1]['uri'] = \
            f"{self.__metadata_tender_url}/{self.__ap_cpid}/{self.__ap_cpid}"

        final_expected_related_processes_array = list()
        if len(self.__actual_fe_release['releases'][0]['relatedProcesses']) == len(expected_related_processes_array):
            for act in range(len(self.__actual_fe_release['releases'][0]['relatedProcesses'])):
                for exp in range(len(expected_related_processes_array)):

                    if self.__actual_fe_release['releases'][0]['relatedProcesses'][act]['relationship'] == \
                            expected_related_processes_array[exp]['relationship']:

                        try:
                            """Set permanent id."""

                            is_permanent_id_correct = is_it_uuid(
                                self.__actual_fe_release['releases'][0]['relatedProcesses'][act]['id'])

                            if is_permanent_id_correct is True:

                                expected_related_processes_array[exp]['id'] = \
                                    self.__actual_fe_release['releases'][0]['relatedProcesses'][act]['id']
                            else:
                                ValueError(f"The 'releases[0].relatedProcesses[{act}].id' must be uuid.")
                        except KeyError:
                            KeyError("Mismatch key into path 'releases[0].relatedProcesses[*].id'")

                        final_expected_related_processes_array.append(expected_related_processes_array[exp])
        else:
            ValueError("The quantity of actual relatedProcesses array != "
                       "quantity of expected relatedProcesses array")
        self.__expected_fe_release['releases'][0]['relatedProcesses'] = final_expected_related_processes_array
        return self.__expected_fe_release

    def build_expected_fa_release(self):
        """Build FA release."""
        # Enrich 'procurementMethodRationale'.
        if "procurementMethodRationale" in self.__payload['tender']:
            self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale'] = \
                self.__payload['tender']['procurementMethodRationale']
        else:
            if "procurementMethodRationale" in self.__previous_fa_release['releases'][0]['tender']:
                self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale'] = \
                    self.__previous_fa_release['releases'][0]['tender']
            else:
                del self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale']

        # Enrich 'procuringEntity'.
        for q_0 in range(len(self.__expected_fe_release['releases'][0]['parties'])):
            if self.__expected_fe_release['releases'][0]['parties'][q_0]['roles'] == ["procuringEntity"]:
                expected_procuring_entity_object = {
                    "id": self.__expected_fe_release['releases'][0]['parties'][q_0]['id'],
                    "name": self.__expected_fe_release['releases'][0]['parties'][q_0]['name']
                }
                self.__expected_fa_release['releases'][0]['tender']['procuringEntity'] = \
                    expected_procuring_entity_object

        # Enrich 'relatedProcesses'.
        old_related_processes = self.__previous_fa_release['releases'][0]['relatedProcesses']
        new_related_processes = list()
        for i in range(1):
            new_related_processes.append(copy.deepcopy(
                self.__expected_fa_release['releases'][0]['relatedProcesses'][0]
            ))

            new_related_processes[i]['relationship'] = ["x_establishment"]
            new_related_processes[i]['scheme'] = "ocid"
            new_related_processes[i]['identifier'] = self.__fe_ocid
            new_related_processes[i]['uri'] = f"{self.__metadata_tender_url}/{self.__ap_cpid}/{self.__fe_ocid}"

            for act in range(len(self.__actual_fa_release['releases'][0]['relatedProcesses'])):
                if self.__actual_fa_release['releases'][0]['relatedProcesses'][act]['relationship'] == \
                        ["x_establishment"]:

                    try:
                        """Set permanent id."""
                        is_permanent_id_correct = is_it_uuid(
                            self.__actual_fa_release['releases'][0]['relatedProcesses'][act]['id'])
                        if is_permanent_id_correct is True:
                            new_related_processes[i]['id'] = \
                                self.__actual_fa_release['releases'][0]['relatedProcesses'][act]['id']
                        else:
                            ValueError(f"The 'releases[0].relatedProcesses[{act}].id' must be uuid.")
                    except KeyError:
                        KeyError("Mismatch key into path 'releases[0].relatedProcesses[*].id'")
        final_expected_related_processes_array = list()
        expected_related_processes_array = old_related_processes + new_related_processes

        # Sort 'relatedProcesses' array.
        if len(self.__actual_fa_release['releases'][0]['relatedProcesses']) == len(expected_related_processes_array):
            for act in range(len(self.__actual_fa_release['releases'][0]['relatedProcesses'])):
                for exp in range(len(expected_related_processes_array)):
                    if expected_related_processes_array[exp]['id'] == \
                            self.__actual_fa_release['releases'][0]['relatedProcesses'][act]['id']:
                        final_expected_related_processes_array.append(expected_related_processes_array[exp])
        self.__expected_fa_release['releases'][0]['relatedProcesses'] = final_expected_related_processes_array
        return self.__expected_fa_release
