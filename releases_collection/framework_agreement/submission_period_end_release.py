"""Prepare the expected releases of the submission period end process, framework agreement procedures."""
import copy
import math

from functions_collection.mdm_methods import get_criteria, get_requirement_groups, get_requirements
from functions_collection.prepare_date import get_min_date
from functions_collection.some_functions import get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv, is_it_uuid


class SubmissionPeriodEndRelease:
    """This class creates instance of release."""

    def __init__(self, environment, country, language, pmd, actual_message, host_for_service, ocid):
        self.__country = country
        self.__pmd = pmd
        self.__language = language
        self.__actual_message = actual_message
        self.__host = host_for_service
        self.__ocid = ocid
        try:
            if environment == "dev":
                self.__metadata_document_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get"
            elif environment == "sandbox":
                self.__metadata_document_url = "http://storage.eprocurement.systems/get"

        except ValueError:
            ValueError("Check your environment: You must use 'dev' or 'sandbox' environment in pytest command")

        self.__expected_ap_release = {
            "uri": "",
            "version": "",
            "extensions": [
                "",
                ""
            ],
            "publisher": {
                "name": "",
                "uri": ""
            },
            "license": "",
            "publicationPolicy": "",
            "publishedDate": "",
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
                                        "scheme": "i",
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
                                "faxNumber": "r",
                                "url": ""
                            },
                            "details": {
                                "typeOfBuyer": "",
                                "mainGeneralActivity": "",
                                "mainSectoralActivity": ""
                            },
                            "roles": [
                                ""
                            ]
                        }
                    ],
                    "tender": {
                        "id": "",
                        "status": "",
                        "statusDetails": "",
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
                            "startDate": ""
                        },
                        "hasEnquiries": False or True,
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
                        "requiresElectronicCatalogue": False or True
                    },
                    "hasPreviousNotice": False or True,
                    "purposeOfNotice": {
                        "isACallForCompetition": False or True
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

        self.__expected_fe_release = {
            "uri": "",
            "version": "",
            "extensions": [
                "",
                ""
            ],
            "publisher": {
                "name": "",
                "uri": ""
            },
            "license": "",
            "publicationPolicy": "",
            "publishedDate": "",
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
                            "details": {
                                "typeOfSupplier": "",
                                "mainEconomicActivities": [
                                    {
                                        "scheme": "",
                                        "id": "",
                                        "description": "",
                                        "uri": ""
                                    }
                                ],
                                "bankAccounts": [
                                    {
                                        "description": "",
                                        "bankName": "",
                                        "address": {
                                            "streetAddress": "",
                                            "postalCode": "",
                                            "addressDetails": {
                                                "country": {
                                                    "scheme": "",
                                                    "id": "MD",
                                                    "description": ""
                                                },
                                                "region": {
                                                    "scheme": "",
                                                    "id": "",
                                                    "description": ""
                                                },
                                                "locality": {
                                                    "scheme": "",
                                                    "id": "",
                                                    "description": ""
                                                }
                                            }
                                        },
                                        "identifier": {
                                            "id": "",
                                            "scheme": ""
                                        },
                                        "accountIdentification": {
                                            "id": "",
                                            "scheme": ""
                                        },
                                        "additionalAccountIdentifiers": [
                                            {
                                                "scheme": "",
                                                "id": ""
                                            }]
                                    }
                                ],
                                "legalForm": {
                                    "id": "",
                                    "scheme": "",
                                    "description": "",
                                    "uri": ""
                                },
                                "scale": ""
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
                                                "description": ""
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
                            "qualificationSystemMethods": [
                                ""
                            ]
                        },
                        "enquiryPeriod": {
                            "startDate": "",
                            "endDate": ""
                        },
                        "hasEnquiries": True or False,
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
                        "requiresElectronicCatalogue": True or False,
                        "procurementMethodModalities": [
                            ""
                        ],
                        "secondStage": {
                            "minimumCandidates": int,
                            "maximumCandidates": int
                        }
                    },
                    "submissions": {
                        "details": [
                            {
                                "id": "",
                                "date": "",
                                "status": "",
                                "requirementResponses": [
                                    {
                                        "id": "",
                                        "value": "",
                                        "requirement": {
                                            "id": ""
                                        },
                                        "evidences": [
                                            {
                                                "id": "",
                                                "title": "",
                                                "description": "",
                                                "relatedDocument": {
                                                    "id": ""
                                                }
                                            }
                                        ]
                                    }
                                ],
                                "candidates": [
                                    {
                                        "id": "",
                                        "name": ""
                                    }
                                ],
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
                    },
                    "qualifications": [
                        {
                            "id": "",
                            "date": "",
                            "status": "",
                            "statusDetails": "",
                            "relatedSubmission": ""
                        }
                    ],
                    "preQualification": {
                        "period": {
                            "startDate": "",
                            "endDate": ""
                        },
                        "qualificationPeriod": {
                            "startDate": ""
                        }
                    },
                    "hasPreviousNotice": True or False,
                    "purposeOfNotice": {
                        "isACallForCompetition": True or False
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
            "uri": "",
            "version": "",
            "extensions": [
                "",
                ""
            ],
            "publisher": {
                "name": "",
                "uri": ""
            },
            "license": "",
            "publicationPolicy": "",
            "publishedDate": "",
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
                    "tender": {
                        "id": "",
                        "title": "",
                        "description": "",
                        "status": "",
                        "statusDetails": "",
                        "value": {
                            "amount": 0.0,
                            "currency": ""
                        },
                        "procurementMethod": "",
                        "procurementMethodDetails": "",
                        "procurementMethodRationale": "",
                        "mainProcurementCategory": "",
                        "hasEnquiries": True or False,
                        "eligibilityCriteria": "",
                        "contractPeriod": {
                            "startDate": "",
                            "endDate": ""
                        },
                        "procuringEntity": {
                            "id": "",
                            "name": ""
                        },
                        "acceleratedProcedure": {
                            "isAcceleratedProcedure": True or False
                        },
                        "classification": {
                            "scheme": "",
                            "id": "",
                            "description": ""
                        },
                        "designContest": {
                            "serviceContractAward": True or False
                        },
                        "electronicWorkflows": {
                            "useOrdering": True or False,
                            "usePayment": True or False,
                            "acceptInvoicing": True or False
                        },
                        "jointProcurement": {
                            "isJointProcurement": True or False
                        },
                        "legalBasis": "",
                        "procedureOutsourcing": {
                            "procedureOutsourced": True or False
                        },
                        "dynamicPurchasingSystem": {
                            "hasDynamicPurchasingSystem": True or False
                        },
                        "framework": {
                            "isAFramework": True or False
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

    def build_expected_ap_release(self, previous_ap_release):
        """Build AP release."""

        """Enrich general attribute for expected AP release"""
        self.__expected_ap_release['uri'] = previous_ap_release['uri']
        self.__expected_ap_release['version'] = previous_ap_release['version']
        self.__expected_ap_release['extensions'] = previous_ap_release['extensions']
        self.__expected_ap_release['publisher']['name'] = previous_ap_release['publisher']['name']
        self.__expected_ap_release['publisher']['uri'] = previous_ap_release['publisher']['uri']
        self.__expected_ap_release['license'] = previous_ap_release['license']
        self.__expected_ap_release['publicationPolicy'] = previous_ap_release['publicationPolicy']
        self.__expected_ap_release['publishedDate'] = previous_ap_release['publishedDate']

        """Enrich general attribute for expected AP release: releases[0]"""
        self.__expected_ap_release['releases'][0]['ocid'] = previous_ap_release['releases'][0]['ocid']
        self.__expected_ap_release['releases'][0]['id'] = previous_ap_release['releases'][0]['id']
        self.__expected_ap_release['releases'][0]['date'] = previous_ap_release['releases'][0]['date']
        self.__expected_ap_release['releases'][0]['tag'] = previous_ap_release['releases'][0]['tag']
        self.__expected_ap_release['releases'][0]['language'] = previous_ap_release['releases'][0]['language']
        self.__expected_ap_release['releases'][0]['initiationType'] = \
            previous_ap_release['releases'][0]['initiationType']
        self.__expected_ap_release['releases'][0]['hasPreviousNotice'] = \
            previous_ap_release['releases'][0]['hasPreviousNotice']
        self.__expected_ap_release['releases'][0]['purposeOfNotice']['isACallForCompetition'] = \
            previous_ap_release['releases'][0]['purposeOfNotice']['isACallForCompetition']

        """Enrich 'parties' array for expected AP release: releases[0].parties[*]"""
        self.__expected_ap_release['releases'][0]['parties'] = previous_ap_release['releases'][0]['parties']

        """Enrich 'tender' object for expected AP release: releases[0].tender"""
        self.__expected_ap_release['releases'][0]['tender']['id'] = previous_ap_release['releases'][0]['tender']['id']
        self.__expected_ap_release['releases'][0]['tender']['status'] = \
            previous_ap_release['releases'][0]['tender']['status']
        self.__expected_ap_release['releases'][0]['tender']['statusDetails'] = \
            previous_ap_release['releases'][0]['tender']['statusDetails']
        self.__expected_ap_release['releases'][0]['tender']['items'] = \
            previous_ap_release['releases'][0]['tender']['items']
        self.__expected_ap_release['releases'][0]['tender']['lots'] = \
            previous_ap_release['releases'][0]['tender']['lots']
        self.__expected_ap_release['releases'][0]['tender']['tenderPeriod'] = \
            previous_ap_release['releases'][0]['tender']['tenderPeriod']
        self.__expected_ap_release['releases'][0]['tender']['hasEnquiries'] = \
            previous_ap_release['releases'][0]['tender']['hasEnquiries']
        if "documents" in previous_ap_release['releases'][0]['tender']:
            self.__expected_ap_release['releases'][0]['tender']['documents'] = \
                previous_ap_release['releases'][0]['tender']['documents']
        else:
            del self.__expected_ap_release['releases'][0]['tender']['documents']
        self.__expected_ap_release['releases'][0]['tender']['submissionMethod'] = \
            previous_ap_release['releases'][0]['tender']['submissionMethod']
        self.__expected_ap_release['releases'][0]['tender']['submissionMethodDetails'] = \
            previous_ap_release['releases'][0]['tender']['submissionMethodDetails']
        self.__expected_ap_release['releases'][0]['tender']['submissionMethodRationale'] = \
            previous_ap_release['releases'][0]['tender']['submissionMethodRationale']
        self.__expected_ap_release['releases'][0]['tender']['requiresElectronicCatalogue'] = \
            previous_ap_release['releases'][0]['tender']['requiresElectronicCatalogue']

        """Enrich 'relatedProcesses' array for expected AP release: releases[0].relatedProcesses[*]"""
        self.__expected_ap_release['releases'][0]['relatedProcesses'] = \
            previous_ap_release['releases'][0]['relatedProcesses']
        return self.__expected_ap_release

    def build_expected_fe_release(self, previous_fe_release, list_of_submission_payloads, list_of_submission_messages,
                                  actual_fe_release):
        """Build FE release."""

        """Enrich general attribute for expected FE release"""
        self.__expected_fe_release['uri'] = previous_fe_release['uri']
        self.__expected_fe_release['version'] = previous_fe_release['version']
        self.__expected_fe_release['extensions'] = previous_fe_release['extensions']
        self.__expected_fe_release['publisher']['name'] = previous_fe_release['publisher']['name']
        self.__expected_fe_release['publisher']['uri'] = previous_fe_release['publisher']['uri']
        self.__expected_fe_release['license'] = previous_fe_release['license']
        self.__expected_fe_release['publicationPolicy'] = previous_fe_release['publicationPolicy']
        self.__expected_fe_release['publishedDate'] = previous_fe_release['publishedDate']

        """Enrich general attribute for expected FE release: releases[0]"""
        self.__expected_fe_release['releases'][0]['ocid'] = previous_fe_release['releases'][0]['ocid']
        self.__expected_fe_release['releases'][0]['id'] = \
            f"{self.__ocid}-{actual_fe_release['releases'][0]['id'][46:59]}"
        self.__expected_fe_release['releases'][0]['date'] = self.__actual_message['data']['operationDate']
        self.__expected_fe_release['releases'][0]['tag'] = previous_fe_release['releases'][0]['tag']
        self.__expected_fe_release['releases'][0]['language'] = previous_fe_release['releases'][0]['language']
        self.__expected_fe_release['releases'][0]['initiationType'] = \
            previous_fe_release['releases'][0]['initiationType']
        self.__expected_fe_release['releases'][0]['hasPreviousNotice'] = \
            previous_fe_release['releases'][0]['hasPreviousNotice']
        self.__expected_fe_release['releases'][0]['purposeOfNotice']['isACallForCompetition'] = \
            previous_fe_release['releases'][0]['purposeOfNotice']['isACallForCompetition']

        """Prepare 'preQualification' object for expected FE release: releases[0].preQualification"""
        self.__expected_fe_release['releases'][0]['preQualification']['period'] = \
            previous_fe_release['releases'][0]['preQualification']['period']
        self.__expected_fe_release['releases'][0]['preQualification']['qualificationPeriod']['startDate'] = \
            self.__actual_message['data']['operationDate']

        """Prepare 'parties' array for expected FE release: releases[0].parties"""
        old_parties_array = list()
        for p_0 in range(len(actual_fe_release['releases'][0]['parties'])):
            if actual_fe_release['releases'][0]['parties'][p_0]['roles'] == ["buyer"]:
                old_parties_array.append(actual_fe_release['releases'][0]['parties'][p_0])
            elif actual_fe_release['releases'][0]['parties'][p_0]['roles'] == ["procuringEntity"]:
                old_parties_array.append(actual_fe_release['releases'][0]['parties'][p_0])

        new_parties_array = list()
        for p_0 in range(len(list_of_submission_payloads)):
            temp_new_parties_array = list()
            for p_1 in range(len(list_of_submission_payloads[p_0]['submission']['candidates'])):
                temp_new_parties_array.append(
                    copy.deepcopy(self.__expected_fe_release['releases'][0]['parties'][0]))
                candidate_from_payload = list_of_submission_payloads[p_0]['submission']['candidates'][p_1]

                temp_new_parties_array[p_1]['id'] = \
                    f"{candidate_from_payload['identifier']['scheme']}-{candidate_from_payload['identifier']['id']}"

                temp_new_parties_array[p_1]['name'] = candidate_from_payload['name']

                # Prepare 'identifier' object:
                temp_new_parties_array[p_1]['identifier']['scheme'] = candidate_from_payload['identifier']['scheme']
                temp_new_parties_array[p_1]['identifier']['id'] = candidate_from_payload['identifier']['id']
                temp_new_parties_array[p_1]['identifier']['legalName'] = candidate_from_payload['identifier'][
                    'legalName']
                if "uri" in candidate_from_payload['identifier']:
                    temp_new_parties_array[p_1]['identifier']['uri'] = candidate_from_payload['identifier']['uri']
                else:
                    del temp_new_parties_array[p_1]['identifier']['uri']

                # Prepare 'address' object:
                temp_new_parties_array[p_1]['address']['streetAddress'] = candidate_from_payload['address'][
                    'streetAddress']
                if "postalCode" in candidate_from_payload['address']:
                    temp_new_parties_array[p_1]['address']['postalCode'] = candidate_from_payload['address'][
                        'postalCode']
                else:
                    del temp_new_parties_array[p_1]['address']['postalCode']

                try:
                    f"""
                        Prepare 'addressDetails' object for temp_new_parties_array[{p_1}]['address'].
                        """
                    country_data = get_value_from_country_csv(
                        country=candidate_from_payload['address']['addressDetails']['country']['id'],
                        language=self.__language
                    )
                    expected_country_object = [{
                        "scheme": country_data[2].upper(),
                        "id": candidate_from_payload['address']['addressDetails']['country']['id'],
                        "description": country_data[1],
                        "uri": country_data[3]
                    }]

                    region_data = get_value_from_region_csv(
                        region=candidate_from_payload['address']['addressDetails']['region']['id'],
                        country=candidate_from_payload['address']['addressDetails']['country']['id'],
                        language=self.__language
                    )
                    expected_region_object = [{
                        "scheme": region_data[2],
                        "id": candidate_from_payload['address']['addressDetails']['region']['id'],
                        "description": region_data[1],
                        "uri": region_data[3]
                    }]

                    if candidate_from_payload['address']['addressDetails']['locality']['scheme'] == "CUATM":

                        locality_data = get_value_from_locality_csv(
                            locality=candidate_from_payload['address']['addressDetails']['locality']['id'],
                            region=candidate_from_payload['address']['addressDetails']['region']['id'],
                            country=candidate_from_payload['address']['addressDetails']['country']['id'],
                            language=self.__language
                        )
                        expected_locality_object = [{
                            "scheme": locality_data[2],
                            "id": candidate_from_payload['address']['addressDetails']['locality']['id'],
                            "description": locality_data[1],
                            "uri": locality_data[3]
                        }]
                    else:
                        expected_locality_object = [{
                            "scheme": candidate_from_payload['address']['addressDetails']['locality']['scheme'],
                            "id": candidate_from_payload['address']['addressDetails']['locality']['id'],
                            "description": candidate_from_payload['address']['addressDetails']['locality'][
                                'description']
                        }]

                    temp_new_parties_array[p_1]['address']['addressDetails']['country'] = expected_country_object[0]
                    temp_new_parties_array[p_1]['address']['addressDetails']['region'] = expected_region_object[0]
                    temp_new_parties_array[p_1]['address']['addressDetails']['locality'] = expected_locality_object[
                        0]
                except ValueError:
                    raise ValueError(f"Impossible to prepare Prepare 'addressDetails' object for "
                                     f"temp_new_parties_array[{p_0 + p_1}]['address']")

                # Prepare 'additionalIdentifiers' array:
                if "additionalIdentifiers" in candidate_from_payload:
                    additional_identifiers_array = list()
                    for p_2 in range(len(candidate_from_payload['additionalIdentifiers'])):
                        additional_identifiers_array.append(copy.deepcopy(
                            self.__expected_fe_release['releases'][0]['parties'][0]['additionalIdentifiers'][0]
                        ))

                        additional_identifiers_array[p_2]['scheme'] = \
                            candidate_from_payload['additionalIdentifiers'][p_2]['scheme']

                        additional_identifiers_array[p_2]['id'] = \
                            candidate_from_payload['additionalIdentifiers'][p_2]['id']

                        additional_identifiers_array[p_2]['legalName'] = \
                            candidate_from_payload['additionalIdentifiers'][p_2]['legalName']

                        if "uri" in candidate_from_payload['additionalIdentifiers'][p_2]:
                            additional_identifiers_array[p_2]['uri'] = \
                                candidate_from_payload['additionalIdentifiers'][p_2]['uri']
                        else:
                            del additional_identifiers_array[p_2]['uri']
                    temp_new_parties_array[p_1]['additionalIdentifiers'] = additional_identifiers_array
                else:
                    del temp_new_parties_array[p_1]['additionalIdentifiers']

                # Prepare 'contactPoint' object:
                temp_new_parties_array[p_1]['contactPoint']['name'] = candidate_from_payload['contactPoint']['name']
                temp_new_parties_array[p_1]['contactPoint']['email'] = candidate_from_payload['contactPoint'][
                    'email']

                temp_new_parties_array[p_1]['contactPoint']['telephone'] = \
                    candidate_from_payload['contactPoint']['telephone']

                if "faxNumber" in candidate_from_payload['contactPoint']:
                    temp_new_parties_array[p_1]['contactPoint']['faxNumber'] = \
                        candidate_from_payload['contactPoint']['faxNumber']
                else:
                    del temp_new_parties_array[p_1]['contactPoint']['faxNumber']

                if "url" in candidate_from_payload['contactPoint']:
                    temp_new_parties_array[p_1]['contactPoint']['url'] = \
                        candidate_from_payload['contactPoint']['url']
                else:
                    del temp_new_parties_array[p_1]['contactPoint']['url']

                # Prepare 'details' object:
                if "typeOfSupplier" in candidate_from_payload['details']:
                    temp_new_parties_array[p_1]['details']['typeOfSupplier'] = \
                        candidate_from_payload['details']['typeOfSupplier']
                else:
                    del temp_new_parties_array[p_1]['details']['typeOfSupplier']

                if "mainEconomicActivities" in candidate_from_payload['details']:
                    main_economic_activities_array = list()
                    for m_0 in range(len(candidate_from_payload['details']['mainEconomicActivities'])):
                        main_economic_activities_array.append(copy.deepcopy(
                            self.__expected_fe_release['releases'][0]['parties'][0]['details'][
                                'mainEconomicActivities'][0]
                        ))

                        main_economic_activities_array[m_0]['scheme'] = \
                            candidate_from_payload['details']['mainEconomicActivities'][m_0]['scheme']

                        main_economic_activities_array[m_0]['id'] = \
                            candidate_from_payload['details']['mainEconomicActivities'][m_0]['id']

                        main_economic_activities_array[m_0]['description'] = \
                            candidate_from_payload['details']['mainEconomicActivities'][m_0]['description']

                        if "uri" in candidate_from_payload['details']['mainEconomicActivities'][m_0]:
                            main_economic_activities_array[m_0]['uri'] = \
                                candidate_from_payload['details']['mainEconomicActivities'][m_0]['uri']
                        else:
                            del main_economic_activities_array[m_0]['uri']
                    temp_new_parties_array[p_1]['details'][
                        'mainEconomicActivities'] = main_economic_activities_array
                else:
                    del temp_new_parties_array[p_1]['details']['mainEconomicActivities']

                if "bankAccounts" in candidate_from_payload['details']:
                    bank_accounts_array = list()
                    for b_0 in range(len(candidate_from_payload['details']['bankAccounts'])):
                        bank_accounts_array.append(copy.deepcopy(
                            self.__expected_fe_release['releases'][0]['parties'][0]['details']['bankAccounts'][0]
                        ))

                        bank_accounts_array[b_0]['description'] = \
                            candidate_from_payload['details']['bankAccounts'][b_0]['description']

                        bank_accounts_array[b_0]['bankName'] = \
                            candidate_from_payload['details']['bankAccounts'][b_0]['bankName']

                        bank_accounts_array[b_0]['address']['streetAddress'] = \
                            candidate_from_payload['details']['bankAccounts'][b_0]['address']['streetAddress']

                        if "postalCode" in candidate_from_payload['details']['bankAccounts'][b_0]['address']:
                            bank_accounts_array[b_0]['address']['postalCode'] = \
                                candidate_from_payload['details']['bankAccounts'][b_0]['address']['postalCode']
                        else:
                            del bank_accounts_array[b_0]['address']['postalCode']

                        try:
                            """
                            Prepare 'addressDetails' object for ank_accounts_array[b_0]['address'].
                            """
                            country_data = get_value_from_country_csv(
                                country=candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                    'addressDetails']['country']['id'],
                                language=self.__language
                            )
                            expected_country_object = [{
                                "scheme": country_data[2].upper(),
                                "id": candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                    'addressDetails']['country']['id'],
                                "description": country_data[1],
                                "uri": country_data[3]
                            }]

                            region_data = get_value_from_region_csv(
                                region=candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                    'addressDetails']['region']['id'],
                                country=candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                    'addressDetails']['country']['id'],
                                language=self.__language
                            )
                            expected_region_object = [{
                                "scheme": region_data[2],
                                "id": candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                    'addressDetails']['region']['id'],
                                "description": region_data[1],
                                "uri": region_data[3]
                            }]

                            if candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                    'addressDetails']['locality']['scheme'] == "CUATM":

                                locality_data = get_value_from_locality_csv(
                                    locality=candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                        'addressDetails']['locality']['id'],
                                    region=candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                        'addressDetails']['region']['id'],
                                    country=candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                        'addressDetails']['country']['id'],
                                    language=self.__language
                                )

                                expected_locality_object = [{
                                    "scheme": locality_data[2],
                                    "id": candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                        'addressDetails']['locality']['id'],
                                    "description": locality_data[1],
                                    "uri": locality_data[3]
                                }]
                            else:
                                expected_locality_object = [{
                                    "scheme": candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                        'addressDetails']['locality']['scheme'],
                                    "id": candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                        'addressDetails']['locality']['id'],
                                    "description":
                                        candidate_from_payload['details']['bankAccounts'][b_0]['address'][
                                            'addressDetails']['locality']['description']
                                }]

                            bank_accounts_array[b_0]['address']['addressDetails']['country'] = \
                                expected_country_object[0]

                            bank_accounts_array[b_0]['address']['addressDetails']['region'] = \
                                expected_region_object[0]

                            bank_accounts_array[b_0]['address']['addressDetails']['locality'] = \
                                expected_locality_object[0]
                        except ValueError:
                            raise ValueError("Impossible to prepare Prepare 'addressDetails' object for "
                                             "ank_accounts_array[b_0]['address']")

                        bank_accounts_array[b_0]['identifier']['id'] = \
                            candidate_from_payload['details']['bankAccounts'][b_0]['identifier']['id']

                        bank_accounts_array[b_0]['identifier']['scheme'] = \
                            candidate_from_payload['details']['bankAccounts'][b_0]['identifier']['scheme']

                        bank_accounts_array[b_0]['accountIdentification']['id'] = \
                            candidate_from_payload['details']['bankAccounts'][b_0]['accountIdentification']['id']

                        bank_accounts_array[b_0]['accountIdentification']['scheme'] = \
                            candidate_from_payload['details']['bankAccounts'][b_0]['accountIdentification'][
                                'scheme']

                        if "additionalAccountIdentifiers" in candidate_from_payload['details']['bankAccounts'][b_0]:
                            additional_account_identifiers = list()
                            for b_1 in range(len(
                                    candidate_from_payload['details']['bankAccounts'][b_0][
                                        'additionalAccountIdentifiers']
                            )):
                                additional_account_identifiers.append(copy.deepcopy(
                                    self.__expected_fe_release['releases'][0]['parties'][0]['details'][
                                        'bankAccounts'][0]['additionalAccountIdentifiers'][0]
                                ))

                                additional_account_identifiers[b_1]['scheme'] = \
                                    candidate_from_payload['details']['bankAccounts'][b_0][
                                        'additionalAccountIdentifiers'][b_1]['scheme']

                                additional_account_identifiers[b_1]['id'] = \
                                    candidate_from_payload['details']['bankAccounts'][b_0][
                                        'additionalAccountIdentifiers'][b_1]['id']

                            bank_accounts_array[b_0][
                                'additionalAccountIdentifiers'] = additional_account_identifiers
                        else:
                            del bank_accounts_array[b_0]['additionalAccountIdentifiers']

                    temp_new_parties_array[p_1]['details']['bankAccounts'] = bank_accounts_array
                else:
                    del temp_new_parties_array[p_1]['details']['bankAccounts']

                temp_new_parties_array[p_1]['details']['legalForm']['id'] = \
                    candidate_from_payload['details']['legalForm']['id']

                temp_new_parties_array[p_1]['details']['legalForm']['scheme'] = \
                    candidate_from_payload['details']['legalForm']['scheme']

                temp_new_parties_array[p_1]['details']['legalForm']['description'] = \
                    candidate_from_payload['details']['legalForm']['description']

                if "uri" in candidate_from_payload['details']['legalForm']:
                    temp_new_parties_array[p_1]['details']['legalForm']['uri'] = \
                        candidate_from_payload['details']['legalForm']['uri']
                else:
                    del temp_new_parties_array[p_1]['details']['legalForm']['uri']

                temp_new_parties_array[p_1]['details']['scale'] = candidate_from_payload['details']['scale']

                # Prepare 'persones' array:
                if "persones" in candidate_from_payload:
                    persones = list()
                    for cp_0 in range(len(candidate_from_payload['persones'])):
                        persones.append(copy.deepcopy(
                            self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0]
                        ))

                        persones[cp_0]['id'] = \
                            f"{candidate_from_payload['persones'][cp_0]['identifier']['scheme']}-" \
                            f"{candidate_from_payload['persones'][cp_0]['identifier']['id']}"

                        persones[cp_0]['title'] = candidate_from_payload['persones'][cp_0]['title']
                        persones[cp_0]['name'] = candidate_from_payload['persones'][cp_0]['name']

                        persones[cp_0]['identifier']['scheme'] = \
                            candidate_from_payload['persones'][cp_0]['identifier']['scheme']

                        persones[cp_0]['identifier']['id'] = \
                            candidate_from_payload['persones'][cp_0]['identifier']['id']

                        if "uri" in candidate_from_payload['persones'][cp_0]['identifier']:
                            persones[cp_0]['identifier']['uri'] = \
                                candidate_from_payload['persones'][cp_0]['identifier']['uri']
                        else:
                            del persones[cp_0]['identifier']['uri']

                        business_functions = list()
                        for cp_1 in range(len(candidate_from_payload['persones'][cp_0]['businessFunctions'])):
                            business_functions.append(copy.deepcopy(
                                self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0][
                                    'businessFunctions'][0]
                            ))

                            try:
                                """Set permanent id."""
                                for apwcr_0 in range(len(actual_fe_release['releases'][0]['parties'])):
                                    if actual_fe_release['releases'][0]['parties'][apwcr_0]['roles'] == \
                                            ["candidate"]:
                                        if actual_fe_release['releases'][0]['parties'][apwcr_0]['id'] == \
                                                temp_new_parties_array[p_1]['id']:

                                            is_permanent_id_correct = is_it_uuid(
                                                actual_fe_release['releases'][0]['parties'][apwcr_0][
                                                    'persones'][cp_0]['businessFunctions'][cp_1]['id']
                                            )
                                            if is_permanent_id_correct is True:

                                                business_functions[cp_1]['id'] = \
                                                    actual_fe_release['releases'][0]['parties'][apwcr_0][
                                                        'persones'][cp_0]['businessFunctions'][cp_1]['id']
                                            else:
                                                raise ValueError(f"The 'self.__actual_fe_release['releases'][0]"
                                                                 f"['parties'][{apwcr_0}]['persones'][{cp_1}]['id']' "
                                                                 f"must be uuid.")
                            except KeyError:
                                raise KeyError("Mismatch key into path 'self.__actual_fe_release['releases'][0]["
                                               f"'parties'][*]['persones'][{cp_1}]['id']'")

                            business_functions[cp_1]['type'] = \
                                candidate_from_payload['persones'][cp_0]['businessFunctions'][cp_1]['type']

                            business_functions[cp_1]['jobTitle'] = \
                                candidate_from_payload['persones'][cp_0]['businessFunctions'][cp_1]['jobTitle']

                            business_functions[cp_1]['period']['startDate'] = \
                                candidate_from_payload['persones'][cp_0]['businessFunctions'][cp_1]['period'][
                                    'startDate']

                            if "documents" in candidate_from_payload['persones'][cp_0]['businessFunctions'][cp_1]:
                                bf_documents = list()
                                for cp_2 in range(len(
                                        candidate_from_payload['persones'][cp_0]['businessFunctions'][cp_1][
                                            'documents']
                                )):
                                    bf_documents.append(copy.deepcopy(
                                        self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0][
                                            'businessFunctions'][0]['documents'][0]
                                    ))

                                    bf_documents[cp_2]['id'] = candidate_from_payload['persones'][cp_0][
                                        'businessFunctions'][cp_1]['documents'][cp_2]['id']

                                    bf_documents[cp_2]['documentType'] = candidate_from_payload['persones'][cp_0][
                                        'businessFunctions'][cp_1]['documents'][cp_2]['documentType']

                                    bf_documents[cp_2]['title'] = candidate_from_payload['persones'][cp_0][
                                        'businessFunctions'][cp_1]['documents'][cp_2]['title']

                                    if "description" in candidate_from_payload['persones'][cp_0][
                                            'businessFunctions'][cp_1]['documents'][cp_2]:
                                        bf_documents[cp_2]['description'] = \
                                            candidate_from_payload['persones'][cp_0][
                                                'businessFunctions'][cp_1]['documents'][cp_2]['description']
                                    else:
                                        del bf_documents[cp_2]['description']

                                    bf_documents[cp_2]['url'] = \
                                        f"{self.__metadata_document_url}/{bf_documents[cp_2]['id']}"

                                    bf_documents[cp_2]['datePublished'] = self.__actual_message['data'][
                                        'operationDate']

                                business_functions[cp_1]['documents'] = bf_documents
                            else:
                                del business_functions[cp_1]['documents']

                        persones[cp_0]['businessFunctions'] = business_functions
                    temp_new_parties_array[p_1]['persones'] = persones
                else:
                    del temp_new_parties_array[p_1]['persones']
                temp_new_parties_array[p_1]['roles'] = ["candidate"]

            new_parties_array += temp_new_parties_array

        # Sort 'releases[0].parties' array:
        temp_array = old_parties_array + new_parties_array
        expected_parties_array = list()
        if len(actual_fe_release['releases'][0]['parties']) == len(temp_array):
            for act in range(len(actual_fe_release['releases'][0]['parties'])):
                for exp in range(len(temp_array)):
                    if temp_array[exp]['id'] == actual_fe_release['releases'][0]['parties'][act]['id']:
                        expected_parties_array.append(temp_array[exp])
        else:
            raise ValueError(
                "The quantity of actual 'releases[0].parties' array != expected 'releases[0].parties'.")
        self.__expected_fe_release['releases'][0]['parties'] = expected_parties_array

        """Prepare 'tender' object for expected FE release: releases[0].tender"""
        self.__expected_fe_release['releases'][0]['tender']['id'] = previous_fe_release['releases'][0]['tender']['id']

        # (https://ustudio.atlassian.net/wiki/spaces/ES/pages/2736128006/10.0.0.2+Modify+Tender):
        if "qualifications" in self.__expected_fe_release['releases'][0]:
            self.__expected_fe_release['releases'][0]['tender']['status'] = "active"
            self.__expected_fe_release['releases'][0]['tender']['statusDetails'] = "qualification"
        else:
            self.__expected_fe_release['releases'][0]['tender']['status'] = "unsuccessful"
            self.__expected_fe_release['releases'][0]['tender']['statusDetails'] = "lackOfSubmissions"

        # Prepare 'releases[0].tender.criteria' array:
        old_criteria_array = list()
        if "criteria" in previous_fe_release['releases'][0]['tender']:
            old_criteria_array = previous_fe_release['releases'][0]['tender']['criteria']

        # FR.COM-3.2.3 (https://ustudio.atlassian.net/wiki/spaces/ES/pages/1266286655/R10.3.2+eNotice+Amend+FE+v1):
        criteria_from_mdm = get_criteria(
            host=self.__host,
            language=self.__language,
            country=self.__country,
            pmd=self.__pmd,
            phase="qualification"
        )
        # (https://ustudio.atlassian.net/wiki/spaces/ES/pages/2739142677/10.0.0.13+Create+Criteria+For+
        # Procuring+Entity)
        new_criteria_array = list()
        if len(criteria_from_mdm['data']) > 0:
            for ec_0 in range(len(criteria_from_mdm['data'])):
                new_criteria_array.append(copy.deepcopy(
                    self.__expected_fe_release['releases'][0]['tender']['criteria'][0]
                ))

                new_criteria_array[ec_0]['id'] = criteria_from_mdm['data'][ec_0]['id']
                new_criteria_array[ec_0]['title'] = criteria_from_mdm['data'][ec_0]['title']

                # (https://ustudio.atlassian.net/wiki/spaces/ES/pages/915275865/R10.1.12+eAccess+
                # Create+Criteria+For+Procuring+Entity):
                # # FR.COM-1.12.1
                new_criteria_array[ec_0]['source'] = "procuringEntity"

                # FR.COM-1.12.5:
                new_criteria_array[ec_0]['relatesTo'] = "qualification"

                if "description" in criteria_from_mdm['data'][ec_0]:
                    new_criteria_array[ec_0]['description'] = \
                        criteria_from_mdm['data'][ec_0]['description']
                else:
                    del new_criteria_array[ec_0]['description']

                # FR.COM-1.12.6:
                new_criteria_array[ec_0]['classification'] = \
                    criteria_from_mdm['data'][ec_0]['classification']

                criteria_groups_from_mdm = get_requirement_groups(
                    host=self.__host,
                    language=self.__language,
                    country=self.__country,
                    pmd=self.__pmd,
                    phase="qualification",
                    criterion_id=new_criteria_array[ec_0]['id']
                )
                del new_criteria_array[ec_0]['requirementGroups'][0]
                if len(criteria_groups_from_mdm['data']) > 0:
                    for ec_1 in range(len(criteria_groups_from_mdm['data'])):
                        new_criteria_array[ec_0]['requirementGroups'].append(copy.deepcopy(
                            self.__expected_fe_release['releases'][0]['tender']['criteria'][0]['requirementGroups'][
                                0]
                        ))

                        new_criteria_array[ec_0]['requirementGroups'][ec_1]['id'] = \
                            criteria_groups_from_mdm['data'][ec_1]['id']

                        if "description" in criteria_groups_from_mdm['data'][ec_1]:
                            new_criteria_array[ec_0]['requirementGroups'][ec_1]['description'] = \
                                criteria_groups_from_mdm['data'][ec_1]['description']
                        else:
                            del new_criteria_array[ec_0]['requirementGroups'][ec_1]['description']

                        requirements_from_mdm = get_requirements(
                            host=self.__host,
                            language=self.__language,
                            country=self.__country,
                            pmd=self.__pmd,
                            phase="qualification",
                            requirement_group_id=new_criteria_array[ec_0]['requirementGroups'][ec_1]['id']
                        )
                        del new_criteria_array[ec_0]['requirementGroups'][ec_1]['requirements'][0]
                        if len(requirements_from_mdm['data']) > 0:
                            for ec_2 in range(len(requirements_from_mdm['data'])):
                                new_criteria_array[ec_0]['requirementGroups'][ec_1]['requirements'].append(
                                    copy.deepcopy(
                                        self.__expected_fe_release['releases'][0]['tender']['criteria'][0][
                                            'requirementGroups'][0]['requirements'][0]
                                    )
                                )

                                new_criteria_array[ec_0]['requirementGroups'][ec_1]['requirements'][ec_2]['id'] = \
                                    requirements_from_mdm['data'][ec_2]['id']

                                if "description" in requirements_from_mdm['data'][ec_2]:

                                    new_criteria_array[ec_0]['requirementGroups'][ec_1]['requirements'][ec_2][
                                        'description'] = requirements_from_mdm['data'][ec_2]['description']
                                else:
                                    del new_criteria_array[ec_0]['requirementGroups'][ec_1]['requirements'][ec_2][
                                        'description']

                                new_criteria_array[ec_0]['requirementGroups'][ec_1]['requirements'][ec_2]['title'] = \
                                    requirements_from_mdm['data'][ec_2]['title']

                                # FR.COM-1.12.2:
                                new_criteria_array[ec_0]['requirementGroups'][ec_1]['requirements'][ec_2][
                                    'dataType'] = "boolean"

                                # FR.COM-1.12.7:
                                new_criteria_array[ec_0]['requirementGroups'][ec_1]['requirements'][ec_2][
                                    'status'] = "active"

                                # FR.COM-1.12.8:
                                new_criteria_array[ec_0]['requirementGroups'][ec_1]['requirements'][ec_2][
                                    'datePublished'] = self.__actual_message['data']['operationDate']

                        else:
                            raise ValueError(f"Empty array from MDM database: 'criteria[{ec_0}]."
                                             f"requirementGroups[{ec_1}].requirements[*]'.")
                else:
                    raise ValueError(f"Empty array from MDM database: 'criteria[{ec_0}].requirementGroups[*]'.")

        if len(old_criteria_array + new_criteria_array) > 0:
            self.__expected_fe_release['releases'][0]['tender'][
                'criteria'] = old_criteria_array + new_criteria_array
        else:
            del self.__expected_fe_release['releases'][0]['tender']['criteria']

        # Prepare 'submissionMethod' array:
        self.__expected_fe_release['releases'][0]['tender']['submissionMethod'] = \
            previous_fe_release['releases'][0]['tender']['submissionMethod']
        # Prepare 'submissionMethodDetails' attribute:
        self.__expected_fe_release['releases'][0]['tender']['submissionMethodDetails'] = \
            previous_fe_release['releases'][0]['tender']['submissionMethodDetails']
        # Prepare 'submissionMethodRationale' attribute:
        self.__expected_fe_release['releases'][0]['tender']['submissionMethodRationale'] = \
            previous_fe_release['releases'][0]['tender']['submissionMethodRationale']
        # Prepare 'requiresElectronicCatalogue' attribute:
        self.__expected_fe_release['releases'][0]['tender']['requiresElectronicCatalogue'] = \
            previous_fe_release['releases'][0]['tender']['requiresElectronicCatalogue']
        # Prepare 'procurementMethodModalities' attribute:
        if "procurementMethodModalities" in previous_fe_release['releases'][0]['tender']:
            self.__expected_fe_release['releases'][0]['tender']['procurementMethodModalities'] = \
                previous_fe_release['releases'][0]['tender']['procurementMethodModalities']
        else:
            del self.__expected_fe_release['releases'][0]['tender']['procurementMethodModalities']
        # Prepare 'secondStage' object:
        if "secondStage" in previous_fe_release['releases'][0]['tender']:
            self.__expected_fe_release['releases'][0]['tender']['secondStage'] = \
                previous_fe_release['releases'][0]['tender']['secondStage']
        else:
            del self.__expected_fe_release['releases'][0]['tender']['secondStage']
        # Prepare 'otherCriteria' object:
        self.__expected_fe_release['releases'][0]['tender']['otherCriteria']['reductionCriteria'] = \
            previous_fe_release['releases'][0]['tender']['otherCriteria']['reductionCriteria']
        self.__expected_fe_release['releases'][0]['tender']['otherCriteria']['qualificationSystemMethods'] = \
            previous_fe_release['releases'][0]['tender']['otherCriteria']['qualificationSystemMethods']
        # Prepare 'enquiryPeriod' object:
        self.__expected_fe_release['releases'][0]['tender']['enquiryPeriod'] = \
            previous_fe_release['releases'][0]['tender']['enquiryPeriod']
        # Prepare 'hasEnquiries' attribute:
        self.__expected_fe_release['releases'][0]['tender']['hasEnquiries'] = \
            previous_fe_release['releases'][0]['tender']['hasEnquiries']
        # Prepare 'documents' array:

        if "documents" in previous_fe_release['releases'][0]['tender']:
            self.__expected_fe_release['releases'][0]['tender']['documents'] = \
                previous_fe_release['releases'][0]['tender']['documents']
        else:
            del self.__expected_fe_release['releases'][0]['tender']['documents']

        """Prepare 'submission' object for expected FE release: releases[0].submission"""
        # Build 'releases[0].submissions' object:
        # (https://ustudio.atlassian.net/wiki/spaces/ES/pages/875036832)
        # FR.COM-5.8.8, FR.COM-5.8.9:
        submission_details = list()
        if len(actual_fe_release['releases'][0]['submissions']['details']) == len(list_of_submission_messages):
            for act_s in range(len(actual_fe_release['releases'][0]['submissions']['details'])):
                for exp_s in range(len(list_of_submission_messages)):
                    if list_of_submission_messages[exp_s]['data']['outcomes']['submissions'][0]['id'] == \
                            actual_fe_release['releases'][0]['submissions']['details'][act_s]['id']:
                        for q_0 in range(len(list_of_submission_payloads)):
                            candidates_array = list()
                            for q_1 in range(len(list_of_submission_payloads[q_0]['submission']['candidates'])):
                                candidates_array.append(copy.deepcopy(
                                    self.__expected_fe_release['releases'][0]['submissions']['details'][0][
                                        'candidates'][0]
                                ))

                                candidate_scheme = \
                                    list_of_submission_payloads[q_0]['submission']['candidates'][q_1][
                                        'identifier']['scheme']

                                candidate_id = \
                                    list_of_submission_payloads[q_0]['submission']['candidates'][q_1][
                                        'identifier']['id']

                                candidates_array[q_1]['id'] = f"{candidate_scheme}-{candidate_id}"

                                candidates_array[q_1]['name'] = \
                                    list_of_submission_payloads[q_0]['submission']['candidates'][q_1]['name']

                            if actual_fe_release['releases'][0]['submissions']['details'][act_s][
                                    'candidates'] == candidates_array:

                                submission_details.append(copy.deepcopy(
                                    self.__expected_fe_release['releases'][0]['submissions']['details'][0]
                                ))
                                submission_details[act_s]['id'] = \
                                    list_of_submission_messages[exp_s]['data']['outcomes'][
                                        'submissions'][0]['id']

                                # FR.COM-5.8.2:
                                submission_details[act_s]['date'] = \
                                    list_of_submission_messages[exp_s]['data']['operationDate']

                                # FR.COM-5.8.1:
                                submission_details[act_s]['status'] = "pending"

                                # FR.COM-5.8.5:
                                submission_details[act_s]['candidates'] = candidates_array

                                del submission_details[act_s]['requirementResponses'][0]
                                if "requirementResponses" in list_of_submission_payloads[q_0]['submission']:
                                    requirement_responses = list()
                                    for r_0 in range(len(list_of_submission_payloads[q_0]['submission'][
                                                             'requirementResponses'])):
                                        requirement_responses.append(copy.deepcopy(
                                            self.__expected_fe_release['releases'][0]['submissions']['details'][0][
                                                'requirementResponses'][0]
                                        ))

                                        try:
                                            """Set permanent id."""
                                            is_permanent_id_correct = is_it_uuid(
                                                actual_fe_release['releases'][0]['submissions'][
                                                    'details'][act_s]['requirementResponses'][r_0]['id']
                                            )
                                            if is_permanent_id_correct is True:

                                                requirement_responses[r_0]['id'] = \
                                                    actual_fe_release['releases'][0]['submissions'][
                                                        'details'][act_s]['requirementResponses'][r_0]['id']
                                            else:
                                                raise ValueError(
                                                    f"The 'self.__actual_fe_release['releases'][0]['submissions']"
                                                    f"['details'][{act_s}]['requirementResponses']"
                                                    f"[{r_0}]['id']' must be uuid.")
                                        except KeyError:
                                            raise KeyError(
                                                f"Mismatch key into path 'self.__actual_fe_release['releases'][0]"
                                                f"['submissions']['details'][{act_s}]['requirementResponses']"
                                                f"[{r_0}]['id']'")

                                        requirement_responses[r_0]['value'] = \
                                            list_of_submission_payloads[q_0]['submission'][
                                                'requirementResponses'][r_0]['value']

                                        requirement_responses[r_0]['requirement']['id'] = \
                                            list_of_submission_payloads[q_0]['submission'][
                                                'requirementResponses'][r_0]['requirement']['id']

                                        del requirement_responses[r_0]['evidences'][0]
                                        if "evidences" in list_of_submission_payloads[q_0]['submission'][
                                                'requirementResponses'][r_0]:

                                            evidences = list()
                                            for r_1 in range(
                                                    len(list_of_submission_payloads[q_0]['submission'][
                                                            'requirementResponses'][r_0]['evidences'])):

                                                evidences.append(copy.deepcopy(
                                                    self.__expected_fe_release['releases'][0]['submissions'][
                                                        'details'][0]['requirementResponses'][0]['evidences'][0]
                                                ))

                                                try:
                                                    """Set permanent id."""
                                                    is_permanent_id_correct = is_it_uuid(
                                                        actual_fe_release['releases'][0]['submissions'][
                                                            'details'][act_s]['requirementResponses'][r_0][
                                                            'evidences'][r_1]['id']
                                                    )
                                                    if is_permanent_id_correct is True:

                                                        evidences[r_1]['id'] = \
                                                            actual_fe_release['releases'][0]['submissions'][
                                                                'details'][act_s]['requirementResponses'][r_0][
                                                                'evidences'][r_1]['id']
                                                    else:
                                                        raise ValueError(
                                                            f"The 'self.__actual_fe_release['releases'][0]"
                                                            f"['submissions']['details'][{act_s}]"
                                                            f"['requirementResponses'][{r_0}]['evidences']"
                                                            f"[{r_1}]['id']' must be uuid.")
                                                except KeyError:
                                                    raise KeyError(f"Mismatch key into path "
                                                                   f"'self.__actual_fe_release['releases'][0]"
                                                                   f"['submissions']['details'][{act_s}]"
                                                                   f"['requirementResponses'][{r_0}]['evidences']"
                                                                   f"[{r_1}]['id']'")

                                                evidences[r_1]['title'] = list_of_submission_payloads[q_0][
                                                    'submission']['requirementResponses'][r_0]['evidences'][r_1][
                                                    'title']

                                                if "description" in list_of_submission_payloads[q_0][
                                                        'submission']['requirementResponses'][r_0]['evidences'][r_1]:

                                                    evidences[r_1]['description'] = \
                                                        list_of_submission_payloads[q_0]['submission'][
                                                            'requirementResponses'][r_0]['evidences'][r_1][
                                                            'description']
                                                else:
                                                    del evidences[r_1]['description']

                                                if "relatedDocument" in list_of_submission_payloads[q_0][
                                                        'submission']['requirementResponses'][r_0]['evidences'][r_1]:

                                                    evidences[r_1]['relatedDocument']['id'] = \
                                                        list_of_submission_payloads[q_0]['submission'][
                                                            'requirementResponses'][r_0]['evidences'][r_1][
                                                            'relatedDocument']['id']
                                                else:
                                                    del evidences[r_1]['relatedDocument']

                                            requirement_responses[r_0]['evidences'] = evidences

                                        else:
                                            del requirement_responses[r_0]['evidences']

                                    submission_details[act_s]['requirementResponses'] = requirement_responses
                                else:
                                    del submission_details[act_s]['requirementResponses']

                                del submission_details[act_s]['documents'][0]
                                if "documents" in list_of_submission_payloads[q_0]['submission']:
                                    documents = list()
                                    for d_0 in range(len(
                                            list_of_submission_payloads[q_0]['submission']['documents'])):

                                        documents.append(copy.deepcopy(
                                            self.__expected_fe_release['releases'][0]['submissions']['details'][0][
                                                'documents'][0]
                                        ))

                                        documents[d_0]['id'] = \
                                            list_of_submission_payloads[q_0]['submission'][
                                                'documents'][d_0]['id']

                                        documents[d_0]['documentType'] = list_of_submission_payloads[q_0][
                                            'submission']['documents'][d_0]['documentType']

                                        documents[d_0]['title'] = list_of_submission_payloads[q_0][
                                            'submission']['documents'][d_0]['title']

                                        if "description" in list_of_submission_payloads[q_0][
                                                'submission']['documents'][d_0]:

                                            documents[d_0]['description'] = list_of_submission_payloads[q_0][
                                                'submission']['documents'][d_0]['description']
                                        else:
                                            del documents[d_0]['description']

                                        documents[d_0][
                                            'url'] = f"{self.__metadata_document_url}/{documents[d_0]['id']}"
                                        documents[d_0]['datePublished'] = self.__actual_message['data'][
                                            'operationDate']

                                    submission_details[act_s]['documents'] = documents
                                else:
                                    del submission_details[act_s]['documents']
        self.__expected_fe_release['releases'][0]['submissions']['details'] = submission_details

        """Prepare 'qualifications' array for expected FE release: releases[0].qualification"""
        # Build 'releases[0].qualifications' array:
        # (https://ustudio.atlassian.net/wiki/spaces/ES/pages/890601483/R10.7.11+eQualification+Create+Qualifications)
        qualifications_array = list()
        for qu_0 in range(len(list_of_submission_messages)):
            qualifications_array.append(
                copy.deepcopy(self.__expected_fe_release['releases'][0]['qualifications'][0]))

            # FR.COM-7.11.1:
            qualifications_array[qu_0]['id'] = self.__actual_message['data']['outcomes']['qualifications'][qu_0][
                'id']

            # FR.COM-7.11.2:
            qualifications_array[qu_0]['status'] = "pending"
            # FR.COM-7.11.3:
            qualifications_array[qu_0]['date'] = self.__actual_message['data']['operationDate']

            # FR.COM-7.11.4:
            for qu_1 in range(len(actual_fe_release['releases'][0]['qualifications'])):
                if actual_fe_release['releases'][0]['qualifications'][qu_1]['id'] == \
                        qualifications_array[qu_0]['id']:

                    for e in range(len(self.__expected_fe_release['releases'][0]['submissions']['details'])):
                        if actual_fe_release['releases'][0]['qualifications'][qu_1]['relatedSubmission'] == \
                                self.__expected_fe_release['releases'][0]['submissions']['details'][e]['id']:
                            qualifications_array[qu_0]['relatedSubmission'] = \
                                actual_fe_release['releases'][0]['qualifications'][qu_1]['relatedSubmission']

            # FR.COM-7.11.10:
            scoring = 1

            # FR.COM-7.11.6:
            if self.__expected_fe_release['releases'][0]['tender']['otherCriteria'][
                'reductionCriteria'] == "scoring" \
                    and self.__expected_fe_release['releases'][0]['tender']['otherCriteria'][
                    'qualificationSystemMethods'] == ["automated"]:
                # FR.COM-7.11.7:
                coefficients_list = list()
                if "criteria" in self.__expected_fe_release['releases'][0]['tender'] and \
                        "conversions" in self.__expected_fe_release['releases'][0]['tender']:

                    for qu_2 in range(len(list_of_submission_payloads)):
                        if "requirementResponses" in list_of_submission_payloads[qu_2]['submission']:
                            for qu_3 in range(len(list_of_submission_payloads[qu_2][
                                                      'submission']['requirementResponses'])):

                                for c in range(
                                        len(self.__expected_fe_release['releases'][0]['tender']['criteria'])):
                                    if self.__expected_fe_release['releases'][0]['tender'][
                                           'criteria'][c]['classification']['id'][:19] == "CRITERION.SELECTION" and \
                                            self.__expected_fe_release['releases'][0]['tender'][
                                                'criteria'][c]['relatesTo'] == "tenderer":

                                        for g in range(len(self.__expected_fe_release['releases'][0]['tender'][
                                                               'criteria'][c]['requirementGroups'])):

                                            for r in range(len(
                                                    self.__expected_fe_release['releases'][0]['tender'][
                                                        'criteria'][c]['requirementGroups'][g]['requirements'])):

                                                if self.__expected_fe_release['releases'][0]['tender'][
                                                    'criteria'][c]['requirementGroups'][g]['requirements'][r][
                                                    'id'] == \
                                                        list_of_submission_payloads[qu_2][
                                                            'submission']['requirementResponses'][qu_3][
                                                            'requirement']['id']:

                                                    for conv_0 in range(
                                                            len(self.__expected_fe_release['releases'][0][
                                                                    'tender']['conversions'])):

                                                        if self.__expected_fe_release['releases'][0]['tender'][
                                                            'conversions'][conv_0]['relatedItem'] == \
                                                                list_of_submission_payloads[qu_2][
                                                                    'submission']['requirementResponses'][
                                                                    qu_3]['requirement']['id']:

                                                            for conv_1 in range(
                                                                    len(self.__expected_fe_release['releases'][0][
                                                                            'tender']['conversions'][conv_0][
                                                                            'coefficients'])):

                                                                if list_of_submission_payloads[qu_2][
                                                                    'submission']['requirementResponses'][qu_3][
                                                                    'value'] == self.__expected_fe_release[
                                                                    'releases'][0]['tender']['conversions'][conv_0][
                                                                        'coefficients'][conv_1]['value']:

                                                                    data_type = self.__expected_fe_release[
                                                                        'releases'][0]['tender']['criteria'][c][
                                                                        'requirementGroups'][g]['requirements'][r][
                                                                        'dataType']

                                                                    if data_type == "number" and \
                                                                            type(list_of_submission_payloads[
                                                                                     qu_2]['submission'][
                                                                                     'requirementResponses'][qu_3][
                                                                                     'value']) is float \
                                                                            or \
                                                                            data_type == "number" and \
                                                                            type(list_of_submission_payloads[
                                                                                     qu_2]['submission'][
                                                                                     'requirementResponses'][qu_3][
                                                                                     'value']) is int:

                                                                        coefficients_list.append(
                                                                            self.__expected_fe_release[
                                                                                'releases'][0]['tender'][
                                                                                'conversions'][conv_0][
                                                                                'coefficients'][conv_1][
                                                                                'coefficient'])

                                                                    elif data_type == "boolean" and \
                                                                            type(list_of_submission_payloads[
                                                                                     qu_2]['submission'][
                                                                                     'requirementResponses'][qu_3][
                                                                                     'value']) is bool:
                                                                        coefficients_list.append(
                                                                            self.__expected_fe_release[
                                                                                'releases'][0]['tender'][
                                                                                'conversions'][conv_0][
                                                                                'coefficients'][conv_1][
                                                                                'coefficient'])
                if len(coefficients_list) > 0:
                    scoring = round(math.prod(coefficients_list), 3)

            qualifications_array[qu_0]['scoring'] = scoring

        # FR.COM-7.13.1 (Rank Qualifications):
        if self.__expected_fe_release['releases'][0]['tender']['otherCriteria']['reductionCriteria'] == "scoring" \
                and self.__expected_fe_release['releases'][0]['tender']['otherCriteria'][
                'qualificationSystemMethods'] == ["automated"]:

            if "criteria" in self.__expected_fe_release['releases'][0]['tender']:
                is_source_procuring_entity = False
                for c_0 in range(len(self.__expected_fe_release['releases'][0]['tender']['criteria'])):

                    if self.__expected_fe_release['releases'][0]['tender']['criteria'][c_0]['source'] == \
                            "procuringEntity":
                        is_source_procuring_entity = True

                if is_source_procuring_entity is True:
                    temp_scoring = list()
                    for q_0 in range(len(qualifications_array)):
                        temp_scoring.append(qualifications_array[q_0]['scoring'])

                    temp_scoring = min(temp_scoring)

                    temp_qualifications = list()
                    for q_0 in range(len(qualifications_array)):
                        if qualifications_array[q_0]['scoring'] == temp_scoring:
                            temp_qualifications.append(qualifications_array[q_0])

                    if len(temp_qualifications) > 1:
                        date_list = list()
                        for q_0 in range(len(temp_qualifications)):
                            for me_0 in range(len(list_of_submission_messages)):
                                if temp_qualifications[q_0]['relatedSubmission'] == \
                                        list_of_submission_messages[me_0][
                                            'data']['outcomes']['submissions'][0]['id']:
                                    date_list.append(list_of_submission_messages[me_0][
                                                         'data']['operationDate'])
                        min_date = get_min_date(date_list)

                        for q_1 in range(len(temp_qualifications)):
                            for me_0 in range(len(list_of_submission_messages)):
                                if list_of_submission_messages[me_0]['data']['operationDate'] == min_date:
                                    if temp_qualifications[q_1]['relatedSubmission'] == \
                                            list_of_submission_messages[me_0][
                                                'data']['outcomes']['submissions'][0]['id']:
                                        temp_qualifications[q_1]['statusDetails'] = "awaiting"

                    for q_0 in range(len(qualifications_array)):
                        for q_1 in range(len(temp_qualifications)):
                            if qualifications_array[q_0]['id'] == temp_qualifications[q_1]['id']:
                                if temp_qualifications[q_1]['statusDetails'] == "awaiting":
                                    qualifications_array[q_0]['statusDetails'] = \
                                        temp_qualifications[q_1]['statusDetails']

                    for q_0 in range(len(qualifications_array)):
                        if qualifications_array[q_0]['statusDetails'] == "":
                            del qualifications_array[q_0]['statusDetails']

                elif is_source_procuring_entity is False:
                    temp_scoring = list()
                    for q_0 in range(len(qualifications_array)):
                        temp_scoring.append(qualifications_array[q_0]['scoring'])

                    temp_scoring = min(temp_scoring)

                    temp_qualifications = list()
                    for q_0 in range(len(qualifications_array)):
                        if qualifications_array[q_0]['scoring'] == temp_scoring:
                            temp_qualifications.append(qualifications_array[q_0])

                    if len(temp_qualifications) > 1:
                        date_list = list()
                        for q_0 in range(len(temp_qualifications)):
                            for me_0 in range(len(list_of_submission_messages)):
                                if temp_qualifications[q_0]['relatedSubmission'] == \
                                        list_of_submission_messages[me_0][
                                            'data']['outcomes']['submissions'][0]['id']:
                                    date_list.append(list_of_submission_messages[me_0][
                                                         'data']['operationDate'])
                        min_date = get_min_date(date_list)

                        for q_1 in range(len(temp_qualifications)):
                            for me_0 in range(len(list_of_submission_messages)):
                                if list_of_submission_messages[me_0]['data']['operationDate'] == min_date:
                                    if temp_qualifications[q_1]['relatedSubmission'] == \
                                            list_of_submission_messages[me_0][
                                                'data']['outcomes']['submissions'][0]['id']:
                                        temp_qualifications[q_1]['statusDetails'] = "consideration"

                        for q_0 in range(len(qualifications_array)):
                            for q_1 in range(len(temp_qualifications)):
                                if qualifications_array[q_0]['id'] == temp_qualifications[q_1]['id']:
                                    if temp_qualifications[q_1]['statusDetails'] == "consideration":
                                        qualifications_array[q_0]['statusDetails'] = \
                                            temp_qualifications[q_1]['statusDetails']

                        for q_0 in range(len(qualifications_array)):
                            if qualifications_array[q_0]['statusDetails'] == "":
                                del qualifications_array[q_0]['statusDetails']

                    for q_0 in range(len(qualifications_array)):
                        for q_1 in range(len(temp_qualifications)):
                            if qualifications_array[q_0]['id'] == temp_qualifications[q_1]['id']:
                                if "statusDetails" in temp_qualifications[q_1]:
                                    qualifications_array[q_0]['statusDetails'] = \
                                        temp_qualifications[q_1]['statusDetails']
            else:
                for q_0 in range(len(qualifications_array)):
                    del qualifications_array[q_0]['statusDetails']

        elif self.__expected_fe_release['releases'][0]['tender']['otherCriteria']['reductionCriteria'] == \
                "scoring" and self.__expected_fe_release['releases'][0]['tender']['otherCriteria'][
                'qualificationSystemMethods'] == ["manual"]:
            if "criteria" in self.__expected_fe_release['releases'][0]['tender']:
                is_source_procuring_entity = False
                for c_0 in range(len(self.__expected_fe_release['releases'][0]['tender']['criteria'])):

                    if self.__expected_fe_release['releases'][0]['tender']['criteria'][c_0]['source'] == \
                            "procuringEntity":
                        is_source_procuring_entity = True

                if is_source_procuring_entity is True:
                    for q_0 in range(len(qualifications_array)):
                        qualifications_array[q_0]['statusDetails'] = "awaiting"
                        del qualifications_array[q_0]['scoring']
                else:
                    if is_source_procuring_entity is False:
                        for q_0 in range(len(qualifications_array)):
                            qualifications_array[q_0]['statusDetails'] = "consideration"
                            del qualifications_array[q_0]['scoring']
            else:
                for q_0 in range(len(qualifications_array)):
                    del qualifications_array[q_0]['statusDetails']

        elif self.__expected_fe_release['releases'][0]['tender']['otherCriteria']['reductionCriteria'] == \
                "none" and self.__expected_fe_release['releases'][0]['tender']['otherCriteria'][
                'qualificationSystemMethods'] == ["automated"]:
            if "criteria" in self.__expected_fe_release['releases'][0]['tender']:
                is_source_procuring_entity = False
                for c_0 in range(len(self.__expected_fe_release['releases'][0]['tender']['criteria'])):

                    if self.__expected_fe_release['releases'][0]['tender']['criteria'][c_0]['source'] == \
                            "procuringEntity":
                        is_source_procuring_entity = True

                if is_source_procuring_entity is True:
                    for q_0 in range(len(qualifications_array)):
                        qualifications_array[q_0]['statusDetails'] = "awaiting"
                        del qualifications_array[q_0]['scoring']
                else:
                    if is_source_procuring_entity is False:
                        for q_0 in range(len(qualifications_array)):
                            qualifications_array[q_0]['statusDetails'] = "consideration"
                            del qualifications_array[q_0]['scoring']
            else:
                for q_0 in range(len(qualifications_array)):
                    del qualifications_array[q_0]['statusDetails']

        elif self.__expected_fe_release['releases'][0]['tender']['otherCriteria']['reductionCriteria'] == \
                "none" and self.__expected_fe_release['releases'][0]['tender']['otherCriteria'][
                'qualificationSystemMethods'] == ["manual"]:
            if "criteria" in self.__expected_fe_release['releases'][0]['tender']:
                is_source_procuring_entity = False
                for c_0 in range(len(self.__expected_fe_release['releases'][0]['tender']['criteria'])):

                    if self.__expected_fe_release['releases'][0]['tender']['criteria'][c_0]['source'] == \
                            "procuringEntity":
                        is_source_procuring_entity = True

                if is_source_procuring_entity is True:
                    for q_0 in range(len(qualifications_array)):
                        qualifications_array[q_0]['statusDetails'] = "awaiting"
                        del qualifications_array[q_0]['scoring']
                else:
                    if is_source_procuring_entity is False:
                        for q_0 in range(len(qualifications_array)):
                            qualifications_array[q_0]['statusDetails'] = "consideration"
                            del qualifications_array[q_0]['scoring']
            else:
                for q_0 in range(len(qualifications_array)):
                    del qualifications_array[q_0]['statusDetails']
        self.__expected_fe_release['releases'][0]['qualifications'] = qualifications_array

        """Prepare 'relatedProcesses' array for expected FE release: releases[0].relatedProcesses"""
        self.__expected_fe_release['releases'][0]['relatedProcesses'] = \
            previous_fe_release['releases'][0]['relatedProcesses']
        return self.__expected_fe_release

    def build_expected_fa_release(self, previous_fa_release):
        """Build FA release."""

        """Enrich general attribute for expected FA release"""
        self.__expected_fa_release['uri'] = previous_fa_release['uri']
        self.__expected_fa_release['version'] = previous_fa_release['version']
        self.__expected_fa_release['extensions'] = previous_fa_release['extensions']
        self.__expected_fa_release['publisher']['name'] = previous_fa_release['publisher']['name']
        self.__expected_fa_release['publisher']['uri'] = previous_fa_release['publisher']['uri']
        self.__expected_fa_release['license'] = previous_fa_release['license']
        self.__expected_fa_release['publicationPolicy'] = previous_fa_release['publicationPolicy']
        self.__expected_fa_release['publishedDate'] = previous_fa_release['publishedDate']

        """Enrich general attribute for expected FA release: releases[0]"""
        self.__expected_fa_release['releases'][0]['ocid'] = previous_fa_release['releases'][0]['ocid']
        self.__expected_fa_release['releases'][0]['id'] = previous_fa_release['releases'][0]['id']
        self.__expected_fa_release['releases'][0]['date'] = previous_fa_release['releases'][0]['date']
        self.__expected_fa_release['releases'][0]['tag'] = previous_fa_release['releases'][0]['tag']
        self.__expected_fa_release['releases'][0]['language'] = previous_fa_release['releases'][0]['language']
        self.__expected_fa_release['releases'][0]['initiationType'] = \
            previous_fa_release['releases'][0]['initiationType']

        """Enrich 'tender' object for expected FA release: releases[0].tender"""
        self.__expected_fa_release['releases'][0]['tender']['id'] = previous_fa_release['releases'][0]['tender']['id']
        self.__expected_fa_release['releases'][0]['tender']['title'] = \
            previous_fa_release['releases'][0]['tender']['title']
        self.__expected_fa_release['releases'][0]['tender']['description'] = \
            previous_fa_release['releases'][0]['tender']['description']
        self.__expected_fa_release['releases'][0]['tender']['status'] = \
            previous_fa_release['releases'][0]['tender']['status']
        self.__expected_fa_release['releases'][0]['tender']['statusDetails'] = \
            previous_fa_release['releases'][0]['tender']['statusDetails']
        self.__expected_fa_release['releases'][0]['tender']['value']['amount'] = \
            previous_fa_release['releases'][0]['tender']['value']['amount']
        self.__expected_fa_release['releases'][0]['tender']['value']['currency'] = \
            previous_fa_release['releases'][0]['tender']['value']['currency']
        self.__expected_fa_release['releases'][0]['tender']['procurementMethod'] = \
            previous_fa_release['releases'][0]['tender']['procurementMethod']
        self.__expected_fa_release['releases'][0]['tender']['procurementMethodDetails'] = \
            previous_fa_release['releases'][0]['tender']['procurementMethodDetails']

        if "procurementMethodRationale" in previous_fa_release['releases'][0]['tender']:
            self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale'] = \
                previous_fa_release['releases'][0]['tender']['procurementMethodRationale']
        else:
            del self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale']
        self.__expected_fa_release['releases'][0]['tender']['mainProcurementCategory'] = \
            previous_fa_release['releases'][0]['tender']['mainProcurementCategory']
        self.__expected_fa_release['releases'][0]['tender']['hasEnquiries'] = \
            previous_fa_release['releases'][0]['tender']['hasEnquiries']
        self.__expected_fa_release['releases'][0]['tender']['eligibilityCriteria'] = \
            previous_fa_release['releases'][0]['tender']['eligibilityCriteria']
        self.__expected_fa_release['releases'][0]['tender']['contractPeriod']['startDate'] = \
            previous_fa_release['releases'][0]['tender']['contractPeriod']['startDate']
        self.__expected_fa_release['releases'][0]['tender']['contractPeriod']['endDate'] = \
            previous_fa_release['releases'][0]['tender']['contractPeriod']['endDate']
        self.__expected_fa_release['releases'][0]['tender']['procuringEntity']['id'] = \
            previous_fa_release['releases'][0]['tender']['procuringEntity']['id']
        self.__expected_fa_release['releases'][0]['tender']['procuringEntity']['name'] = \
            previous_fa_release['releases'][0]['tender']['procuringEntity']['name']
        self.__expected_fa_release['releases'][0]['tender']['acceleratedProcedure']['isAcceleratedProcedure'] = \
            previous_fa_release['releases'][0]['tender']['acceleratedProcedure']['isAcceleratedProcedure']
        self.__expected_fa_release['releases'][0]['tender']['classification']['scheme'] = \
            previous_fa_release['releases'][0]['tender']['classification']['scheme']
        self.__expected_fa_release['releases'][0]['tender']['classification']['id'] = \
            previous_fa_release['releases'][0]['tender']['classification']['id']
        self.__expected_fa_release['releases'][0]['tender']['classification']['description'] = \
            previous_fa_release['releases'][0]['tender']['classification']['description']
        self.__expected_fa_release['releases'][0]['tender']['designContest']['serviceContractAward'] = \
            previous_fa_release['releases'][0]['tender']['designContest']['serviceContractAward']
        self.__expected_fa_release['releases'][0]['tender']['electronicWorkflows']['useOrdering'] = \
            previous_fa_release['releases'][0]['tender']['electronicWorkflows']['useOrdering']
        self.__expected_fa_release['releases'][0]['tender']['electronicWorkflows']['usePayment'] = \
            previous_fa_release['releases'][0]['tender']['electronicWorkflows']['usePayment']
        self.__expected_fa_release['releases'][0]['tender']['electronicWorkflows']['acceptInvoicing'] = \
            previous_fa_release['releases'][0]['tender']['electronicWorkflows']['acceptInvoicing']
        self.__expected_fa_release['releases'][0]['tender']['jointProcurement']['isJointProcurement'] = \
            previous_fa_release['releases'][0]['tender']['jointProcurement']['isJointProcurement']
        self.__expected_fa_release['releases'][0]['tender']['legalBasis'] = \
            previous_fa_release['releases'][0]['tender']['legalBasis']
        self.__expected_fa_release['releases'][0]['tender']['procedureOutsourcing']['procedureOutsourced'] = \
            previous_fa_release['releases'][0]['tender']['procedureOutsourcing']['procedureOutsourced']
        self.__expected_fa_release['releases'][0]['tender']['dynamicPurchasingSystem']['hasDynamicPurchasingSystem'] = \
            previous_fa_release['releases'][0]['tender']['dynamicPurchasingSystem']['hasDynamicPurchasingSystem']
        self.__expected_fa_release['releases'][0]['tender']['framework']['isAFramework'] = \
            previous_fa_release['releases'][0]['tender']['framework']['isAFramework']

        """Enrich 'relatedProcesses' array for expected FA release: releases[0].relatedProcesses"""
        self.__expected_fa_release['releases'][0]['relatedProcesses'] = \
            previous_fa_release['releases'][0]['relatedProcesses']
        return self.__expected_fa_release
