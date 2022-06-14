"""Prepare the expected releases of the create confirmation response process, framework agreement procedures."""
import copy
import json

from functions_collection.cassandra_methods import get_parameter_from_submission_rules
from functions_collection.prepare_date import is_the_date_within_range
from functions_collection.some_functions import is_it_uuid


class CreateConfirmationResponseRelease:
    """This class creates instance of release."""

    def __init__(self, environment, actual_message, ocid, payload):
        self.__actual_message = actual_message
        self.__ocid = ocid
        self.__payload = payload

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
                    "contracts": [
                        {
                            "id": "",
                            "internalId": "",
                            "date": "",
                            "status": "",
                            "statusDetails": "",
                            "documents": [
                                {
                                    "id": "",
                                    "documentType": "",
                                    "url": "",
                                    "datePublished": ""
                                }],
                            "dateSigned": "",
                            "isFrameworkOrDynamic": False,
                            "confirmationRequests": [
                                {
                                    "id": "",
                                    "type": "",
                                    "relatesTo": "",
                                    "relatedItem": "",
                                    "source": "",
                                    "requests": [
                                        {
                                            "id": "",
                                            "relatedOrganization": {
                                                "id": "",
                                                "name": ""
                                            }
                                        }]
                                }]
                        }
                    ],
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
                    "invitations": [
                        {
                            "id": "",
                            "date": "",
                            "status": "",
                            "tenderers": [
                                {
                                    "id": "",
                                    "name": ""
                                },
                                {
                                    "id": "",
                                    "name": ""
                                }
                            ],
                            "relatedQualification": ""
                        }
                    ],
                    "qualifications": [
                        {
                            "id": "",
                            "date": "",
                            "status": "",
                            "statusDetails": "",
                            "relatedSubmission": "",
                            "requirementResponses": [
                                {
                                    "id": "",
                                    "value": True or False or int or float or str,
                                    "requirement": {
                                        "id": ""
                                    },
                                    "responder": {
                                        "id": "",
                                        "name": ""
                                    },
                                    "relatedTenderer": {
                                        "id": ""
                                    }
                                }],
                            "internalId": "",
                            "description": "",
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
                    ],
                    "preQualification": {
                        "period": {
                            "startDate": "",
                            "endDate": ""
                        },
                        "qualificationPeriod": {
                            "startDate": "",
                            "endDate": ""
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

    def build_expected_fe_release(self, previous_fe_release, actual_fe_release, connect_to_submission, country, pmd):
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
        try:
            """Check that the date is within range"""
            is_date_ok = is_the_date_within_range(
                actual_fe_release['releases'][0]['date'],
                self.__actual_message['data']['operationDate']
            )
            if is_date_ok is True:
                self.__expected_fe_release['releases'][0]['date'] = actual_fe_release['releases'][0]['date']
            else:
                self.__expected_fe_release['releases'][0]['date'] = self.__actual_message['data']['operationDate']
        except ValueError:
            ValueError("Impossible to check that the date is within range.")

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
            previous_fe_release['releases'][0]['preQualification']['qualificationPeriod']['startDate']
        self.__expected_fe_release['releases'][0]['preQualification']['qualificationPeriod']['endDate'] = \
            previous_fe_release['releases'][0]['preQualification']['qualificationPeriod']['endDate']

        """Prepare 'parties' array for expected FE release”"""
        expected_persones_list = list()
        person_list = list()
        # Get 'releases[0].parties' array from previous FE release:
        parties = previous_fe_release['releases'][0]['parties']
        for od in range(len(parties)):
            if parties[od]['roles'][0] == "buyer":
                if "persones" in parties[od]:
                    person_list = (copy.deepcopy(parties[od]['persones']))
        # If some person preset into payload, then update person.
        if "relatedPerson" in self.__payload['confirmationResponse']:
            for rp in range(len(person_list)):
                for pp in range(len(self.__payload['confirmationResponse']['relatedPerson'])):
                    p_person_id = \
                        f"{self.__payload['confirmationResponse']['relatedPerson'][pp]['identifier']['scheme']}-" \
                        f"{self.__payload['confirmationResponse']['relatedPerson'][pp]['identifier']['id']}"
                    if p_person_id == person_list[rp]['id']:
                        person_list[rp]['title'] = self.__payload['confirmationResponse']['relatedPerson'][pp]['title']
                        person_list[rp]['name'] = self.__payload['confirmationResponse']['relatedPerson'][pp]['name']
                        person_list[rp]['identifier']['scheme'] = \
                            self.__payload['confirmationResponse']['relatedPerson'][pp]['identifier']['scheme']
                        person_list[rp]['identifier']['id'] = \
                            self.__payload['confirmationResponse']['relatedPerson'][pp]['identifier']['id']
                        for rbf in range(len(person_list[rp]['businessFunctions'])):
                            for pbf in range(len(self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                     'businessFunctions'])):

                                if person_list[rp]['businessFunctions'][rbf]['id'] == \
                                        self.__payload['confirmationResponse']['relatedPerson'][pp][
                                            'businessFunctions'][pbf]['id']:

                                    person_list[rp]['businessFunctions'][rbf]['type'] = \
                                        self.__payload['confirmationResponse']['relatedPerson'][pp][
                                            'businessFunctions'][pbf]['type']

                                    person_list[rp]['businessFunctions'][rbf]['jobTitle'] = \
                                        self.__payload['confirmationResponse']['relatedPerson'][pp][
                                            'businessFunctions'][pbf]['jobTitle']

                                    person_list[rp]['businessFunctions'][rbf]['period']['startDate'] = \
                                        self.__payload['confirmationResponse']['relatedPerson'][pp][
                                            'businessFunctions'][pbf]['period']['startDate']

                                    if "documents" in person_list[rp]['businessFunctions'][rbf] and \
                                            "documents" in self.__payload['confirmationResponse']['relatedPerson'][pp][
                                        'businessFunctions'][pbf]:

                                        release_bf_doc_id = list()
                                        payload_bf_doc_id = list()
                                        for rbfd in range(len(person_list[rp]['businessFunctions'][rbf]['documents'])):
                                            for pbfd in range(
                                                    len(self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                            'businessFunctions'][pbf]['documents'])):

                                                release_bf_doc_id.append(
                                                    person_list[rp]['businessFunctions'][rbf]['documents'][rbfd]['id'])

                                                payload_bf_doc_id.append(
                                                    self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                        'businessFunctions'][pbf]['documents'][pbfd]['id']
                                                )

                                                if person_list[rp]['businessFunctions'][rbf][
                                                    'documents'][rbfd]['id'] == \
                                                        self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                            'businessFunctions'][pbf]['documents'][pbfd]['id']:

                                                    person_list[rp]['businessFunctions'][rbf][
                                                        'documents'][rbfd]['documentType'] = \
                                                        self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                            'businessFunctions'][pbf]['documents'][pbfd]['documentType']

                                                    person_list[rp]['businessFunctions'][rbf][
                                                        'documents'][rbfd]['title'] = \
                                                        self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                            'businessFunctions'][pbf]['documents'][pbfd]['title']

                                                    if "description" in self.__payload['confirmationResponse'][
                                                        'relatedPerson'][pp]['businessFunctions'][pbf][
                                                        'documents'][pbfd]:
                                                        person_list[rp]['businessFunctions'][rbf][
                                                            'documents'][rbfd]['description'] = \
                                                            self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                                'businessFunctions'][pbf]['documents'][pbfd][
                                                                'description']

                                        release_bf_doc_id = list()
                                        for rbfd in range(len(person_list[rp]['businessFunctions'][rbf]['documents'])):
                                            release_bf_doc_id.append(
                                                person_list[rp]['businessFunctions'][rbf]['documents'][rbfd]['id'])
                                        payload_bf_doc_id = list()
                                        for pbfd in range(
                                                len(self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                        'businessFunctions'][pbf]['documents'])):
                                            payload_bf_doc_id.append(
                                                self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                    'businessFunctions'][pbf]['documents'][pbfd]['id']
                                            )
                                        diff_doc_id = list(set(payload_bf_doc_id) - set(release_bf_doc_id))
                                        for i in range(len(diff_doc_id)):
                                            for pbfd in range(
                                                    len(self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                            'businessFunctions'][pbf]['documents'])):

                                                if diff_doc_id[i] == self.__payload['confirmationResponse'][
                                                    'relatedPerson'][pp]['businessFunctions'][pbf][
                                                    'documents'][pbfd]['id']:

                                                    new_bf_doc_obj = copy.deepcopy(
                                                        self.__expected_fe_release['releases'][0]['parties'][0][
                                                            'persones'][0]['businessFunctions'][0]['documents'][0]
                                                    )
                                                    new_bf_doc_obj['id'] = self.__payload[
                                                        'confirmationResponse']['relatedPerson'][pp][
                                                        'businessFunctions'][pbf]['documents'][pbfd]['id']

                                                    new_bf_doc_obj['documentType'] = self.__payload[
                                                        'confirmationResponse']['relatedPerson'][pp][
                                                        'businessFunctions'][pbf]['documents'][pbfd]['documentType']

                                                    new_bf_doc_obj['title'] = self.__payload[
                                                        'confirmationResponse']['relatedPerson'][pp][
                                                        'businessFunctions'][pbf]['documents'][pbfd]['title']

                                                    if "description" in self.__payload[
                                                        'confirmationResponse']['relatedPerson'][pp][
                                                        'businessFunctions'][pbf]['documents'][pbfd]:

                                                        new_bf_doc_obj['description'] = self.__payload[
                                                            'confirmationResponse']['relatedPerson'][pp][
                                                            'businessFunctions'][pbf]['documents'][pbfd]['description']
                                                    else:
                                                        del new_bf_doc_obj['description']
                                                    new_bf_doc_obj['url'] = f"{self.__metadata_document_url}/" \
                                                                            f"{new_bf_doc_obj['id']}"
                                                    new_bf_doc_obj['datePublished'] = self.__actual_message[
                                                        'data']['operationDate']
                                                    person_list[rp]['businessFunctions'][rbf]['documents'].append(
                                                        new_bf_doc_obj)
                        release_bf_id = list()
                        for rbf in range(len(person_list[rp]['businessFunctions'])):
                            release_bf_id.append(
                                person_list[rp]['businessFunctions'][rbf]['id'])
                        payload_bf_id = list()
                        for pbf in range(
                                len(self.__payload['confirmationResponse']['relatedPerson'][pp]['businessFunctions'])):
                            payload_bf_id.append(
                                self.__payload['confirmationResponse']['relatedPerson'][pp][
                                    'businessFunctions'][pbf]['id']
                            )
                        diff_bf_id = list(set(payload_bf_id) - set(release_bf_id))
                        for i in range(len(diff_bf_id)):
                            for pbf in range(
                                    len(self.__payload['confirmationResponse']['relatedPerson'][pp][
                                            'businessFunctions'])):

                                if diff_bf_id[i] == self.__payload['confirmationResponse']['relatedPerson'][pp][
                                    'businessFunctions'][pbf]['id']:

                                    new_bf_obj = copy.deepcopy(
                                        self.__expected_fe_release['releases'][0]['parties'][0][
                                            'persones'][0]['businessFunctions'][0]
                                    )
                                    new_bf_obj['id'] = self.__payload['confirmationResponse']['relatedPerson'][pp][
                                        'businessFunctions'][pbf]['id']

                                    new_bf_obj['type'] = self.__payload['confirmationResponse']['relatedPerson'][pp][
                                        'businessFunctions'][pbf]['type']

                                    new_bf_obj['jobTitle'] = self.__payload['confirmationResponse'][
                                        'relatedPerson'][pp]['businessFunctions'][pbf]['jobTitle']

                                    new_bf_obj['period']['startDate'] = self.__payload['confirmationResponse'][
                                        'relatedPerson'][pp]['businessFunctions'][pbf]['period']['startDate']

                                    del new_bf_obj['documents'][0]
                                    if "documents" in self.__payload['confirmationResponse']['relatedPerson'][pp][
                                        'businessFunctions'][pbf]:

                                        for pbfd in range(
                                                len(self.__payload['confirmationResponse']['relatedPerson'][pp][
                                                        'businessFunctions'][pbf]['documents'])):

                                            new_bf_doc_obj = copy.deepcopy(
                                                self.__expected_fe_release['releases'][0]['parties'][0][
                                                    'persones'][0]['businessFunctions'][0]['documents'][0]
                                            )

                                            new_bf_doc_obj['id'] = self.__payload['confirmationResponse'][
                                                'relatedPerson'][pp]['businessFunctions'][pbf]['documents'][pbfd]['id']

                                            new_bf_doc_obj['documentType'] = self.__payload['confirmationResponse'][
                                                'relatedPerson'][pp]['businessFunctions'][pbf]['documents'][pbfd][
                                                'documentType']

                                            new_bf_doc_obj['title'] = self.__payload['confirmationResponse'][
                                                'relatedPerson'][pp]['businessFunctions'][pbf]['documents'][pbfd][
                                                'title']

                                            if "description" in self.__payload['confirmationResponse'][
                                                'relatedPerson'][pp]['businessFunctions'][pbf]['documents'][pbfd]:

                                                new_bf_doc_obj['description'] = self.__payload[
                                                    'confirmationResponse']['relatedPerson'][pp][
                                                    'businessFunctions'][pbf]['documents'][pbfd]['description']
                                            else:
                                                del new_bf_doc_obj['description']
                                            new_bf_doc_obj['url'] = f"{self.__metadata_document_url}/" \
                                                                    f"{new_bf_doc_obj['id']}"

                                            new_bf_doc_obj['datePublished'] = self.__actual_message[
                                                'data']['operationDate']

                                            new_bf_obj['documents'].append(new_bf_doc_obj)
                                    person_list[rp]['businessFunctions'].append(new_bf_obj)
            expected_persones_list += person_list
            print("\nexpected_persones_list 1")
            print(json.dumps(expected_persones_list))
            release_person_id = list()
            for rp in range(len(person_list)):
                release_person_id.append(person_list[rp]['id'])
            payload_person_id = list()
            for pp in range(len(self.__payload['confirmationResponse']['relatedPerson'])):
                p_person_id = \
                    f"{self.__payload['confirmationResponse']['relatedPerson']['identifier']['scheme']}-" \
                    f"{self.__payload['confirmationResponse']['relatedPerson']['identifier']['id']}"
                payload_person_id.append(p_person_id)
            dif_person_id = list(set(payload_person_id) - set(release_person_id))
            print("\ndif_person_id")
            print(dif_person_id)
            for i in range(len(dif_person_id)):
                p_person_id = \
                    f"{self.__payload['confirmationResponse']['relatedPerson']['identifier']['scheme']}-" \
                    f"{self.__payload['confirmationResponse']['relatedPerson']['identifier']['id']}"
                if dif_person_id[i] == p_person_id:
                    new_person_obj = copy.deepcopy(
                        self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0]
                    )
                    new_person_obj['id'] = p_person_id
                    new_person_obj['title'] = self.__payload['confirmationResponse']['relatedPerson']['title']
                    new_person_obj['name'] = self.__payload['confirmationResponse']['relatedPerson']['name']
                    new_person_obj['identifier']['scheme'] = \
                        self.__payload['confirmationResponse']['relatedPerson']['identifier']['scheme']
                    new_person_obj['identifier']['id'] = \
                        self.__payload['confirmationResponse']['relatedPerson']['identifier']['id']
                    if "uri" in self.__payload['confirmationResponse']['relatedPerson']['identifier']:
                        new_person_obj['identifier']['uri'] = \
                            self.__payload['confirmationResponse']['relatedPerson']['identifier']['uri']
                    else:
                        del new_person_obj['identifier']['uri']
                    del new_person_obj['businessFunctions'][0]
                    for pbf in range(len(
                            self.__payload['confirmationResponse']['relatedPerson']['businessFunctions']
                    )):
                        new_bf_obj = copy.deepcopy(
                            self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0][
                                'businessFunctions'][0]
                        )
                        new_bf_obj['id'] = self.__payload['confirmationResponse']['relatedPerson'][
                            'businessFunctions'][pbf]['id']
                        new_bf_obj['type'] = self.__payload['confirmationResponse']['relatedPerson'][
                            'businessFunctions'][pbf]['type']
                        new_bf_obj['jobTitle'] = self.__payload['confirmationResponse']['relatedPerson'][
                            'businessFunctions'][pbf]['jobTitle']
                        new_bf_obj['period']['startDate'] = self.__payload['confirmationResponse'][
                            'relatedPerson']['businessFunctions'][pbf]['period']['startDate']
                        del new_bf_obj['documents'][0]
                        if "documents" in self.__payload['confirmationResponse']['relatedPerson'][
                            'businessFunctions'][pbf]:

                            for pbfd in range(len(
                                    self.__payload['confirmationResponse']['relatedPerson'][
                                        'businessFunctions'][pbf]['documents']
                            )):
                                new_bf_doc_obj = copy.deepcopy(
                                    self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0][
                                        'businessFunctions'][0]['documents'][0]
                                )
                                new_bf_doc_obj['id'] = self.__payload['confirmationResponse']['relatedPerson'][
                                    'businessFunctions'][pbf]['documents'][pbfd]['id']
                                new_bf_doc_obj['documentType'] = self.__payload['confirmationResponse'][
                                    'relatedPerson']['businessFunctions'][pbf]['documents'][pbfd][
                                    'documentType']
                                new_bf_doc_obj['title'] = self.__payload['confirmationResponse'][
                                    'relatedPerson']['businessFunctions'][pbf]['documents'][pbfd]['title']
                                if "description" in self.__payload['confirmationResponse']['relatedPerson'][
                                    'businessFunctions'][pbf]['documents'][pbfd]:
                                    new_bf_doc_obj['description'] = self.__payload['confirmationResponse'][
                                        'relatedPerson']['businessFunctions'][pbf]['documents'][pbfd][
                                        'description']
                                else:
                                    del new_bf_doc_obj['description']
                                new_bf_doc_obj['url'] = f"{self.__metadata_document_url}/{new_bf_doc_obj['id']}"
                                new_bf_doc_obj['datePublished'] = self.__actual_message['data']['operationDate']
                                new_bf_obj['documents'].append(new_bf_doc_obj)
                        else:
                            del new_bf_obj['documents']
                        new_person_obj['businessFunctions'].append(new_bf_obj)
                    expected_persones_list.append(new_person_obj)
            print("\nexpected_persones_list 2")
            print(json.dumps(expected_persones_list))
            self.__expected_fe_release['releases'][0]['parties'] = previous_fe_release['releases'][0]['parties']

            # Sort objects into persones, businessFunctions, documents:
            expected_persones_was_sorted = list()
            for od in range(len(actual_fe_release['releases'][0]['parties'])):
                if actual_fe_release['releases'][0]['parties'][od]['roles'][0] == "buyer":
                    if "persones" in actual_fe_release['releases'][0]['parties'][od]:
                        for act in range(len(actual_fe_release['releases'][0]['parties'][od]['persones'])):
                            for exp in range(len(expected_persones_list)):
                                if expected_persones_list[exp]['id'] == \
                                        actual_fe_release['releases'][0]['parties'][od]['persones'][act]['id']:
                                    expected_bf_was_sorted = list()
                                    for act_1 in range(
                                            len(actual_fe_release['releases'][0]['parties'][od]['persones'][act][
                                                    'businessFunctions'])):
                                        for exp_1 in range(len(expected_persones_list[exp]['businessFunctions'])):
                                            if expected_persones_list[exp]['businessFunctions'][exp_1]['type'] == \
                                                    actual_fe_release['releases'][0]['parties'][od]['persones'][act][
                                                        'businessFunctions'][act_1]['type'] and \
                                                    expected_persones_list[exp]['businessFunctions'][exp_1]['jobTitle'] == \
                                                    actual_fe_release['releases'][0]['parties'][od]['persones'][act][
                                                        'businessFunctions'][act_1]['jobTitle'] and \
                                                    expected_persones_list[exp]['businessFunctions'][exp_1]['period'] == \
                                                    actual_fe_release['releases'][0]['parties'][od]['persones'][act][
                                                        'businessFunctions'][act_1]['period']:
                                                # Set terminal id for 'persones[*].businessFucntions[*].id':
                                                # try:
                                                #     """Set permanent id."""
                                                #     is_permanent_id_correct = is_it_uuid(
                                                #         actual_fe_release['releases'][0]['parties'][od]['persones'][
                                                #             act]['businessFunctions'][act_1]['id']
                                                #     )
                                                #     if is_permanent_id_correct is True:
                                                #         expected_persones_list[exp]['businessFunctions'][exp_1]['id'] = \
                                                #             actual_fe_release['releases'][0]['parties'][od][
                                                #                 'persones'][act]['businessFunctions'][act_1]['id']
                                                #     else:
                                                #         ValueError(f"The 'releases[0].parties[{od}].persones[{act}."
                                                #                    f"businessFunctions[{act_1}].id' must be uuid.")
                                                # except KeyError:
                                                #     KeyError(f"Mismatch key into path 'releases[0].parties[{od}]."
                                                #              f"persones[{act}.businessFunctions[{act_1}].id'.")

                                                if "documents" in actual_fe_release['releases'][0]['parties'][od][
                                                    'persones'][act]['businessFunctions'][act_1] and \
                                                        "documents" in expected_persones_list[exp][
                                                    'businessFunctions'][exp_1]:
                                                    expected_bf_doc_was_sorted = list()
                                                    for act_2 in range(len(actual_fe_release['releases'][0][
                                                                               'parties'][od]['persones'][act][
                                                                               'businessFunctions'][act_1]['documents'])):
                                                        for exp_2 in range(len(expected_persones_list[exp][
                                                                                   'businessFunctions'][exp_1][
                                                                                   'documents'])):
                                                            if expected_persones_list[exp]['businessFunctions'][exp_1][
                                                                'documents'][exp_2]['id'] == actual_fe_release[
                                                                'releases'][0]['parties'][od]['persones'][act][
                                                                'businessFunctions'][act_1]['documents'][act_2]['id']:
                                                                expected_bf_doc_was_sorted.append(
                                                                    expected_persones_list[exp][
                                                                        'businessFunctions'][exp_1]['documents'][exp_2])
                                                    expected_persones_list[exp]['businessFunctions'][exp_1][
                                                        'documents'] = expected_bf_doc_was_sorted

                                                expected_bf_was_sorted.append(expected_persones_list[exp][
                                                                                  'businessFunctions'][exp_1])
                                    expected_persones_list[exp]['businessFunctions'] = expected_bf_was_sorted
                                    expected_persones_was_sorted.append(expected_persones_list[exp])
                    else:
                        actual_fe_release['releases'][0]['parties'][od]['persones'] = list()
                        for act in range(len(actual_fe_release['releases'][0]['parties'][od]['persones'])):
                            for exp in range(len(expected_persones_list)):
                                if expected_persones_list[exp]['id'] == \
                                        actual_fe_release['releases'][0]['parties'][od]['persones'][act]['id']:
                                    expected_bf_was_sorted = list()
                                    for act_1 in range(
                                            len(actual_fe_release['releases'][0]['parties'][od]['persones'][act][
                                                    'businessFunctions'])):
                                        for exp_1 in range(len(expected_persones_list[exp]['businessFunctions'])):
                                            if expected_persones_list[exp]['businessFunctions'][exp_1]['type'] == \
                                                    actual_fe_release['releases'][0]['parties'][od]['persones'][act][
                                                        'businessFunctions'][act_1]['type'] and \
                                                    expected_persones_list[exp]['businessFunctions'][exp_1][
                                                        'jobTitle'] == \
                                                    actual_fe_release['releases'][0]['parties'][od]['persones'][act][
                                                        'businessFunctions'][act_1]['jobTitle'] and \
                                                    expected_persones_list[exp]['businessFunctions'][exp_1]['period'] == \
                                                    actual_fe_release['releases'][0]['parties'][od]['persones'][act][
                                                        'businessFunctions'][act_1]['period']:
                                                # Set terminal id for 'persones[*].businessFucntions[*].id':
                                                # try:
                                                #     """Set permanent id."""
                                                #     is_permanent_id_correct = is_it_uuid(
                                                #         actual_fe_release['releases'][0]['parties'][od]['persones'][
                                                #             act]['businessFunctions'][act_1]['id']
                                                #     )
                                                #     if is_permanent_id_correct is True:
                                                #         expected_persones_list[exp]['businessFunctions'][exp_1]['id'] = \
                                                #             actual_fe_release['releases'][0]['parties'][od][
                                                #                 'persones'][act]['businessFunctions'][act_1]['id']
                                                #     else:
                                                #         ValueError(f"The 'releases[0].parties[{od}].persones[{act}."
                                                #                    f"businessFunctions[{act_1}].id' must be uuid.")
                                                # except KeyError:
                                                #     KeyError(f"Mismatch key into path 'releases[0].parties[{od}]."
                                                #              f"persones[{act}.businessFunctions[{act_1}].id'.")

                                                if "documents" in actual_fe_release['releases'][0]['parties'][od][
                                                    'persones'][act]['businessFunctions'][act_1] and \
                                                        "documents" in expected_persones_list[exp][
                                                    'businessFunctions'][exp_1]:
                                                    expected_bf_doc_was_sorted = list()
                                                    for act_2 in range(len(actual_fe_release['releases'][0][
                                                                               'parties'][od]['persones'][act][
                                                                               'businessFunctions'][act_1][
                                                                               'documents'])):
                                                        for exp_2 in range(len(expected_persones_list[exp][
                                                                                   'businessFunctions'][exp_1][
                                                                                   'documents'])):
                                                            if expected_persones_list[exp]['businessFunctions'][exp_1][
                                                                'documents'][exp_2]['id'] == actual_fe_release[
                                                                'releases'][0]['parties'][od]['persones'][act][
                                                                'businessFunctions'][act_1]['documents'][act_2]['id']:
                                                                expected_bf_doc_was_sorted.append(
                                                                    expected_persones_list[exp][
                                                                        'businessFunctions'][exp_1]['documents'][exp_2])
                                                    expected_persones_list[exp]['businessFunctions'][exp_1][
                                                        'documents'] = expected_bf_doc_was_sorted

                                                expected_bf_was_sorted.append(expected_persones_list[exp][
                                                                                  'businessFunctions'][exp_1])
                                    expected_persones_list[exp]['businessFunctions'] = expected_bf_was_sorted
                                    expected_persones_was_sorted.append(expected_persones_list[exp])
            expected_persones_list = expected_persones_was_sorted

            for od in range(len(self.__expected_fe_release['releases'][0]['parties'])):
                if self.__expected_fe_release['releases'][0]['parties'][od]['roles'][0] == "buyer":
                    self.__expected_fe_release['releases'][0]['parties'][od]['persones'] = expected_persones_list
        else:
            self.__expected_fe_release['releases'][0]['parties'] = previous_fe_release['releases'][0]['parties']

        """Prepare 'tender' object for expected FE release: releases[0].tender"""
        self.__expected_fe_release['releases'][0]['tender']['id'] = previous_fe_release['releases'][0]['tender']['id']
        self.__expected_fe_release['releases'][0]['tender']['status'] = \
            previous_fe_release['releases'][0]['tender']['status']
        self.__expected_fe_release['releases'][0]['tender']['statusDetails'] = \
            previous_fe_release['releases'][0]['tender']['statusDetails']
        self.__expected_fe_release['releases'][0]['tender']['criteria'] = \
            previous_fe_release['releases'][0]['tender']['criteria']

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

        """Prepare 'invitations' array, depends on parameter into 'submission.rules'"""
        need_to_return_invitation = get_parameter_from_submission_rules(
            connect_to_submission, country, pmd, "all", "returnInvitations"
        )
        need_to_return_invitation = json.loads(need_to_return_invitation.lower())

        if need_to_return_invitation is False:
            del self.__expected_fe_release['releases'][0]['invitations']
        else:
            self.__expected_fe_release['releases'][0]['invitations'] = previous_fe_release['releases'][0]['invitations']

        """Prepare 'contracts' array: """
        self.__expected_fe_release['releases'][0]['contracts'] = previous_fe_release['releases'][0]['contracts']

        """Prepare 'qualifications' array for expected FE release: releases[0].qualification"""
        self.__expected_fe_release['releases'][0]['qualifications'] = \
            previous_fe_release['releases'][0]['qualifications']

        """Prepare 'submission' object for expected FE release: releases[0].submission"""
        self.__expected_fe_release['releases'][0]['submissions']['details'] = \
            previous_fe_release['releases'][0]['submissions']['details']

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

        """Enrich 'parties' array for expected FA release: releases[0].parties"""
        self.__expected_fa_release['releases'][0]['parties'] = previous_fa_release['releases'][0]['parties']

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
