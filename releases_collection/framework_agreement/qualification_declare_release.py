"""Prepare the expected releases of the qualification declare non conflict of inretest process,
framework agreement procedures."""
import copy
import json

from functions_collection.some_functions import is_it_uuid


class QualificationDeclareRelease:
    """This class creates instance of release."""

    def __init__(self, environment, country, language, pmd, actual_message, host_for_service, cpid, ocid,
                 qualification_declare_payload):
        self.__country = country
        self.__pmd = pmd
        self.__language = language
        self.__actual_message = actual_message
        self.__host = host_for_service
        self.__cpid = cpid
        self.__ocid = ocid
        self.__payload = qualification_declare_payload
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
                                }]
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

    def build_expected_fe_release(self, previous_fe_release, actual_fe_release, qualification_id):
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
            previous_fe_release['releases'][0]['preQualification']['qualificationPeriod']['startDate']

        """Prepare 'parties' array for expected FE release: releases[0].parties"""
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

        """Prepare 'submission' object for expected FE release: releases[0].submission"""
        self.__expected_fe_release['releases'][0]['submissions']['details'] = \
            previous_fe_release['releases'][0]['submissions']['details']

        """Prepare 'qualifications' array for expected FE release: releases[0].qualification"""
        expected_qualifications_array = copy.deepcopy(previous_fe_release['releases'][0]['qualifications'])
        for q in range(len(expected_qualifications_array)):
            if expected_qualifications_array[q]['id'] == qualification_id:
                if "requirementResponses" not in expected_qualifications_array[q]:
                    expected_qualifications_array[q].update(
                        {
                            "requirementResponses": []
                        }
                    )

                requirement_response = copy.deepcopy(
                    self.__expected_fe_release['releases'][0]['qualifications'][0]['requirementResponses'][0])
                requirement_response['value'] = self.__payload['requirementResponse']['value']

                requirement_response['requirement']['id'] = \
                    self.__payload['requirementResponse']['requirement']['id']

                requirement_response['responder']['id'] = \
                    f"{self.__payload['requirementResponse']['responder']['identifier']['scheme']}-" \
                    f"{self.__payload['requirementResponse']['responder']['identifier']['id']}"

                requirement_response['responder']['name'] = \
                    self.__payload['requirementResponse']['responder']['name']

                requirement_response['relatedTenderer']['id'] = \
                    self.__payload['requirementResponse']['relatedTenderer']['id']

                expected_qualifications_array[q]['requirementResponses'].append(requirement_response)

                for act_0 in range(len(actual_fe_release['releases'][0]['qualifications'])):
                    for act_1 in range(len(actual_fe_release['releases'][0]['qualifications'][act_0][
                                               'requirementResponses'])):
                        if requirement_response['requirement']['id'] == actual_fe_release['releases'][0][
                            'qualifications'][act_0]['requirementResponses'][act_1]['requirement']['id'] and \
                                requirement_response['responder']['id'] == actual_fe_release['releases'][0][
                            'qualifications'][act_0]['requirementResponses'][act_1]['responder']['id'] and \
                                requirement_response['responder']['name'] == actual_fe_release['releases'][0][
                            'qualifications'][act_0]['requirementResponses'][act_1]['responder']['name'] and \
                                requirement_response['relatedTenderer']['id'] == actual_fe_release['releases'][0][
                                'qualifications'][act_0]['requirementResponses'][act_1]['relatedTenderer']['id']:
                            requirement_response['id'] = actual_fe_release['releases'][0][
                                'qualifications'][act_0]['requirementResponses'][act_1]['id']
        self.__expected_fe_release['releases'][0]['qualifications'] = expected_qualifications_array

        """Prepare 'relatedProcesses' array for expected FE release: releases[0].relatedProcesses"""
        self.__expected_fe_release['releases'][0]['relatedProcesses'] = \
            previous_fe_release['releases'][0]['relatedProcesses']
        return self.__expected_fe_release

    def build_expected_fa_release(self, previous_fe_release, previous_fa_release, actual_fa_release):
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
        self.__expected_fa_release['releases'][0]['id'] = \
            f"{self.__cpid}-{actual_fa_release['releases'][0]['id'][29:42]}"
        self.__expected_fa_release['releases'][0]['date'] = self.__actual_message['data']['operationDate']
        self.__expected_fa_release['releases'][0]['tag'] = previous_fa_release['releases'][0]['tag']
        self.__expected_fa_release['releases'][0]['language'] = previous_fa_release['releases'][0]['language']
        self.__expected_fa_release['releases'][0]['initiationType'] = \
            previous_fa_release['releases'][0]['initiationType']

        """Enrich 'parties' array for expected FA release: releases[0].parties: FR.COM-1.9.1, FR-10.1.4.1, 
        FR-10.1.4.2, FR-10.1.4.3, FR-10.1.4.4, FR-10.1.4.5, FR-10.1.4.6, FR-10.1.4.7, FR-10.1.4.8, FR-10.1.4.9"""
        expected_parties_object = None
        if "parties" in previous_fa_release['releases'][0]:
            for i in range(len(previous_fa_release['releases'][0]['parties'])):
                if previous_fa_release['releases'][0]['parties'][i]['roles'] == ['procuringEntity']:
                    expected_parties_object = copy.deepcopy(previous_fa_release['releases'][0]['parties'][i])
        else:
            for i in range(len(previous_fe_release['releases'][0]['parties'])):
                if previous_fe_release['releases'][0]['parties'][i]['roles'] == ['procuringEntity']:
                    expected_parties_object = copy.deepcopy(previous_fe_release['releases'][0]['parties'][i])

        if "persones" in expected_parties_object:
            for p in range(len(expected_parties_object['persones'])):
                if expected_parties_object['persones'][p]['id'] == \
                        f"{self.__payload['requirementResponse']['responder']['identifier']['scheme']}-" \
                        f"{self.__payload['requirementResponse']['responder']['identifier']['id']}":
                    expected_parties_object['persones'][p]['title'] = \
                        self.__payload['requirementResponse']['responder']['title']
                    expected_parties_object['persones'][p]['name'] = \
                        self.__payload['requirementResponse']['responder']['name']
                    if "uri" in self.__payload['requirementResponse']['responder']['identifier']:
                        expected_parties_object['persones'][p]['identifier']['uri'] = \
                            self.__payload['requirementResponse']['responder']['identifier']['uri']

                    old_bf_id = list()
                    for ebf in range(len(expected_parties_object['persones'][p]['businessFunctions'])):
                        old_bf_id.append(expected_parties_object['persones'][p]['businessFunctions'][ebf]['id'])

                    new_bf_id = list()
                    for pbf in range(len(self.__payload['requirementResponse']['responder']['businessFunctions'])):
                        new_bf_id.append(self.__payload['requirementResponse']['responder'][
                                             'businessFunctions'][pbf]['id'])

                    # Check same id:
                    bf_same_id = list(set(new_bf_id) & set(old_bf_id))

                    # Check different id:
                    bf_diff_id = list(set(new_bf_id) - set(old_bf_id))

                    if len(bf_same_id) > 0:
                        for i in range(len(bf_same_id)):
                            for ebf in range(len(expected_parties_object['persones'][p]['businessFunctions'])):
                                for pbf in range(len(self.__payload['requirementResponse']['responder'][
                                                         'businessFunctions'])):
                                    if expected_parties_object['persones'][p]['businessFunctions'][ebf]['id'] == \
                                            self.__payload['requirementResponse']['responder'][
                                                'businessFunctions'][pbf]['id'] == bf_same_id[i]:

                                        expected_parties_object['persones'][p]['businessFunctions'][ebf]['type'] = \
                                            self.__payload['requirementResponse']['responder'][
                                                'businessFunctions'][pbf]['type']

                                        expected_parties_object['persones'][p]['businessFunctions'][ebf]['jobTitle'] = \
                                            self.__payload['requirementResponse']['responder'][
                                                'businessFunctions'][pbf]['jobTitle']

                                        expected_parties_object['persones'][p]['businessFunctions'][ebf]['period'][
                                            'startDate'] = self.__payload['requirementResponse']['responder'][
                                            'businessFunctions'][pbf]['period']['startDate']

                                        old_bf_doc_id = list()
                                        if "documents" in expected_parties_object['persones'][p][
                                                'businessFunctions'][ebf]:

                                            old_bf_doc_id = list()
                                            for ebf_d in range(len(expected_parties_object['persones'][p][
                                                                       'businessFunctions'][ebf]['documents'])):
                                                old_bf_doc_id.append(
                                                    expected_parties_object['persones'][p][
                                                        'businessFunctions'][ebf]['documents'][ebf_d]['id'])

                                        new_bf_doc_id = list()
                                        if "documents" in self.__payload['requirementResponse']['responder'][
                                                'businessFunctions'][pbf]:

                                            new_bf_doc_id = list()
                                            for pbf_d in range(len(self.__payload['requirementResponse']['responder'][
                                                                       'businessFunctions'][pbf]['documents'])):
                                                new_bf_doc_id.append(
                                                    self.__payload['requirementResponse']['responder'][
                                                        'businessFunctions'][pbf]['documents'][pbf_d]['id'])

                                        # Check same id:
                                        bf_doc_same_id = list(set(new_bf_doc_id) & set(old_bf_doc_id))

                                        # Check different id:
                                        bf_doc_diff_id = list(set(new_bf_doc_id) - set(old_bf_doc_id))

                                        if len(bf_doc_same_id) > 0:
                                            for y in range(len(bf_doc_same_id)):

                                                for ebf_d in range(len(expected_parties_object['persones'][p][
                                                                           'businessFunctions'][ebf]['documents'])):

                                                    for pbf_d in range(len(self.__payload['requirementResponse'][
                                                                               'responder']['businessFunctions'][pbf][
                                                                               'documents'])):

                                                        if expected_parties_object['persones'][p][
                                                            'businessFunctions'][ebf]['documents'][ebf_d]['id'] == \
                                                                self.__payload['requirementResponse']['responder'][
                                                                    'businessFunctions'][pbf][
                                                                    'documents'][pbf_d]['id'] == bf_doc_same_id[y]:

                                                            expected_parties_object['persones'][p][
                                                                'businessFunctions'][ebf]['documents'][ebf_d][
                                                                'title'] = self.__payload['requirementResponse'][
                                                                'responder']['businessFunctions'][pbf][
                                                                'documents'][pbf_d]['title']

                                                            if "description" in self.__payload['requirementResponse'][
                                                                'responder']['businessFunctions'][pbf][
                                                                    'documents'][pbf_d]:
                                                                expected_parties_object['persones'][p][
                                                                    'businessFunctions'][ebf]['documents'][ebf_d][
                                                                    'description'] = self.__payload[
                                                                    'requirementResponse']['responder'][
                                                                    'businessFunctions'][pbf]['documents'][pbf_d][
                                                                    'description']
                                        if len(bf_doc_diff_id) > 0:

                                            for y in range(len(bf_doc_diff_id)):
                                                for pbf_d in range(len(
                                                        self.__payload['requirementResponse'][
                                                            'responder']['businessFunctions'][pbf]['documents'])):

                                                    if bf_doc_diff_id[y] == self.__payload['requirementResponse'][
                                                            'responder']['businessFunctions'][pbf][
                                                            'documents'][pbf_d]['id']:

                                                        new_bf_document = copy.deepcopy(
                                                            self.__expected_fa_release['releases'][0]['parties'][0][
                                                                'persones'][0]['businessFunctions'][0]['documents'][0]
                                                        )
                                                        new_bf_document['id'] = self.__payload['requirementResponse'][
                                                            'responder']['businessFunctions'][pbf][
                                                            'documents'][pbf_d]['id']

                                                        new_bf_document['title'] = \
                                                            self.__payload['requirementResponse'][
                                                            'responder']['businessFunctions'][pbf][
                                                            'documents'][pbf_d]['title']

                                                        new_bf_document['type'] = \
                                                            self.__payload['requirementResponse'][
                                                            'responder']['businessFunctions'][pbf][
                                                            'documents'][pbf_d]['type']

                                                        if "description" in self.__payload['requirementResponse'][
                                                            'responder']['businessFunctions'][pbf][
                                                                'documents'][pbf_d]:

                                                            new_bf_document['description'] = \
                                                                self.__payload['requirementResponse'][
                                                                'responder']['businessFunctions'][pbf][
                                                                'documents'][pbf_d]['description']

                                                        else:
                                                            del new_bf_document['description']

                                                        new_bf_document['uri'] = \
                                                            f"{self.__metadata_document_url}/{new_bf_document['id']}"

                                                        new_bf_document['datePublished'] = \
                                                            self.__actual_message['data']['operationDate']

                                                        expected_parties_object['persones'][p][
                                                            'businessFunctions'][ebf]['documents'].append(
                                                            new_bf_document)
                    if len(bf_diff_id) > 0:
                        for i in range(len(bf_diff_id)):
                            for pbf in range(len(
                                    self.__payload['requirementResponse']['responder']['businessFunctions'])):

                                if bf_diff_id[i] == self.__payload['requirementResponse'][
                                        'responder']['businessFunctions'][pbf]['id']:

                                    new_bf = copy.deepcopy(
                                        self.__expected_fa_release['releases'][0]['parties'][0][
                                            'persones'][0]['businessFunctions'][0]
                                    )

                                    new_bf['type'] = self.__payload['requirementResponse'][
                                        'responder']['businessFunctions'][pbf]['type']

                                    new_bf['jobTitle'] = self.__payload['requirementResponse'][
                                        'responder']['businessFunctions'][pbf]['jobTitle']

                                    new_bf['period']['startDate'] = self.__payload['requirementResponse'][
                                        'responder']['businessFunctions'][pbf]['period']['startDate']

                                    del new_bf['documents'][0]
                                    if "documents" in self.__payload['requirementResponse'][
                                            'responder']['businessFunctions'][pbf]:
                                        new_bf_documents_array = list()
                                        for pbf_d in range(len(self.__payload['requirementResponse'][
                                                'responder']['businessFunctions'][pbf]['documents'])):

                                            new_bf_documents_array.append(copy.deepcopy(
                                                self.__expected_fa_release['releases'][0]['parties'][0][
                                                    'persones'][0]['businessFunctions'][0]['documents'][0]
                                            ))

                                            new_bf_documents_array[pbf_d]['id'] = \
                                                self.__payload['requirementResponse']['responder'][
                                                    'businessFunctions'][pbf]['documents'][pbf_d]['id']

                                            new_bf_documents_array[pbf_d]['title'] = \
                                                self.__payload['requirementResponse']['responder'][
                                                    'businessFunctions'][pbf]['documents'][pbf_d]['title']

                                            new_bf_documents_array[pbf_d]['type'] = \
                                                self.__payload['requirementResponse']['responder'][
                                                    'businessFunctions'][pbf]['documents'][pbf_d]['type']

                                            if "description" in self.__payload['requirementResponse'][
                                                    'responder']['businessFunctions'][pbf][
                                                    'documents'][pbf_d]:

                                                new_bf_documents_array[pbf_d]['description'] = \
                                                    self.__payload['requirementResponse']['responder'][
                                                        'businessFunctions'][pbf]['documents'][pbf_d]['description']
                                            else:
                                                del new_bf_documents_array[pbf_d]['description']

                                            new_bf_documents_array[pbf_d]['uri'] = \
                                                f"{self.__metadata_document_url}/{new_bf_documents_array[pbf_d]['id']}"

                                            new_bf_documents_array[pbf_d]['datePublished'] = \
                                                self.__actual_message['data']['operationDate']
                                        new_bf['documents'] = new_bf_documents_array
                                    else:
                                        del new_bf['documents']
                                    expected_parties_object['persones'][p]['businessFunctions'].append(new_bf)
        else:
            expected_parties_object.update(
                {
                    "persones": []
                }
            )

            expected_persones = copy.deepcopy(self.__expected_fa_release['releases'][0]['parties'][0]['persones'][0])
            expected_persones['id'] = \
                f"{self.__payload['requirementResponse']['responder']['identifier']['scheme']}-" \
                f"{self.__payload['requirementResponse']['responder']['identifier']['id']}"

            expected_persones['title'] = self.__payload['requirementResponse']['responder']['title']
            expected_persones['name'] = self.__payload['requirementResponse']['responder']['name']

            expected_persones['identifier']['scheme'] = \
                self.__payload['requirementResponse']['responder']['identifier']['scheme']

            expected_persones['identifier']['id'] = \
                self.__payload['requirementResponse']['responder']['identifier']['id']

            if "uri" in self.__payload['requirementResponse']['responder']['identifier']:
                expected_persones['identifier']['uri'] = self.__payload['requirementResponse']['responder'][
                    'identifier']['uri']
            else:
                del expected_persones['identifier']['uri']

            del expected_persones['businessFunctions'][0]
            for pbf in range(len(self.__payload['requirementResponse']['responder']['businessFunctions'])):
                new_bf = copy.deepcopy(
                    self.__expected_fa_release['releases'][0]['parties'][0]['persones'][0]['businessFunctions'][0]
                )
                new_bf['type'] = self.__payload['requirementResponse'][
                    'responder']['businessFunctions'][pbf]['type']

                new_bf['jobTitle'] = self.__payload['requirementResponse'][
                    'responder']['businessFunctions'][pbf]['jobTitle']

                new_bf['period']['startDate'] = self.__payload['requirementResponse'][
                    'responder']['businessFunctions'][pbf]['period']['startDate']

                del new_bf['documents'][0]
                if "documents" in self.__payload['requirementResponse']['responder']['businessFunctions'][pbf]:
                    new_bf_documents_array = list()
                    for pbf_d in range(len(self.__payload['requirementResponse'][
                                               'responder']['businessFunctions'][pbf]['documents'])):
                        new_bf_documents_array.append(copy.deepcopy(
                            self.__expected_fa_release['releases'][0]['parties'][0][
                                'persones'][0]['businessFunctions'][0]['documents'][0]
                        ))

                        new_bf_documents_array[pbf_d]['id'] = \
                            self.__payload['requirementResponse']['responder'][
                                'businessFunctions'][pbf]['documents'][pbf_d]['id']

                        new_bf_documents_array[pbf_d]['title'] = \
                            self.__payload['requirementResponse']['responder'][
                                'businessFunctions'][pbf]['documents'][pbf_d]['title']

                        new_bf_documents_array[pbf_d]['type'] = \
                            self.__payload['requirementResponse']['responder'][
                                'businessFunctions'][pbf]['documents'][pbf_d]['type']

                        if "description" in self.__payload['requirementResponse'][
                                'responder']['businessFunctions'][pbf]['documents'][pbf_d]:

                            new_bf_documents_array[pbf_d]['description'] = \
                                self.__payload['requirementResponse']['responder'][
                                    'businessFunctions'][pbf]['documents'][pbf_d]['description']
                        else:
                            del new_bf_documents_array[pbf_d]['description']

                        new_bf_documents_array[pbf_d]['uri'] = \
                            f"{self.__metadata_document_url}/{new_bf_documents_array[pbf_d]['id']}"

                        new_bf_documents_array[pbf_d]['datePublished'] = \
                            self.__actual_message['data']['operationDate']

                    new_bf['documents'] = new_bf_documents_array
                else:
                    del new_bf['documents']
                expected_persones['businessFunctions'].append(new_bf)
            expected_parties_object['persones'].append(expected_persones)

        self.__expected_fa_release['releases'][0]['parties'] = [expected_parties_object]

        # Sort objects into persones, businessFunctions, documents:
        expected_persones_was_sorted = list()
        for od in range(len(actual_fa_release['releases'][0]['parties'])):
            if actual_fa_release['releases'][0]['parties'][od]['roles'][0] == "procuringEntity":
                for act in range(len(actual_fa_release['releases'][0]['parties'][od]['persones'])):
                    for exp in range(len(expected_parties_object['persones'])):
                        if expected_parties_object['persones'][exp]['id'] == \
                                actual_fa_release['releases'][0]['parties'][od]['persones'][act]['id']:
                            expected_bf_was_sorted = list()
                            for act_1 in range(
                                    len(actual_fa_release['releases'][0]['parties'][od]['persones'][act][
                                            'businessFunctions'])):
                                for exp_1 in range(len(expected_parties_object['persones'][exp]['businessFunctions'])):
                                    if expected_parties_object['persones'][exp]['businessFunctions'][exp_1][
                                        'type'] == actual_fa_release['releases'][0]['parties'][od][
                                        'persones'][act]['businessFunctions'][act_1]['type'] and \
                                            expected_parties_object['persones'][exp][
                                                'businessFunctions'][exp_1]['jobTitle'] == \
                                            actual_fa_release['releases'][0]['parties'][od]['persones'][act][
                                                'businessFunctions'][act_1]['jobTitle'] and \
                                            expected_parties_object['persones'][exp][
                                                'businessFunctions'][exp_1]['period'] == \
                                            actual_fa_release['releases'][0]['parties'][od]['persones'][act][
                                                'businessFunctions'][act_1]['period']:
                                        # Set terminal id for 'persones[*].businessFucntions[*].id':
                                        try:
                                            """Set permanent id."""
                                            is_permanent_id_correct = is_it_uuid(
                                                actual_fa_release['releases'][0]['parties'][od]['persones'][
                                                    act]['businessFunctions'][act_1]['id']
                                            )
                                            if is_permanent_id_correct is True:
                                                expected_parties_object['persones'][exp][
                                                    'businessFunctions'][exp_1]['id'] = \
                                                    actual_fa_release['releases'][0]['parties'][od][
                                                        'persones'][act]['businessFunctions'][act_1]['id']
                                            else:
                                                ValueError(f"The 'releases[0].parties[{od}].persones[{act}."
                                                           f"businessFunctions[{act_1}].id' must be uuid.")
                                        except KeyError:
                                            KeyError(f"Mismatch key into path 'releases[0].parties[{od}]."
                                                     f"persones[{act}.businessFunctions[{act_1}].id'.")

                                        if "documents" in actual_fa_release['releases'][0]['parties'][od][
                                            'persones'][act]['businessFunctions'][act_1] and \
                                                "documents" in expected_parties_object['persones'][exp][
                                                'businessFunctions'][exp_1]:
                                            expected_bf_doc_was_sorted = list()
                                            for act_2 in range(len(actual_fa_release['releases'][0][
                                                                       'parties'][od]['persones'][act][
                                                                       'businessFunctions'][act_1]['documents'])):
                                                for exp_2 in range(len(expected_parties_object['persones'][exp][
                                                                           'businessFunctions'][exp_1][
                                                                           'documents'])):
                                                    if expected_parties_object['persones'][exp][
                                                            'businessFunctions'][exp_1][
                                                            'documents'][exp_2]['id'] == actual_fa_release[
                                                            'releases'][0]['parties'][od]['persones'][act][
                                                            'businessFunctions'][act_1]['documents'][act_2]['id']:
                                                        expected_bf_doc_was_sorted.append(
                                                            expected_parties_object['persones'][exp][
                                                                'businessFunctions'][exp_1]['documents'][exp_2])
                                            expected_parties_object['persones'][exp]['businessFunctions'][exp_1][
                                                'documents'] = expected_bf_doc_was_sorted

                                        expected_bf_was_sorted.append(expected_parties_object['persones'][exp][
                                                                          'businessFunctions'][exp_1])

                            expected_parties_object['persones'][exp]['businessFunctions'] = expected_bf_was_sorted
                            expected_persones_was_sorted.append(expected_parties_object['persones'][exp])

        expected_persones_list = expected_persones_was_sorted

        for od in range(len(self.__expected_fa_release['releases'][0]['parties'])):
            if self.__expected_fa_release['releases'][0]['parties'][od]['roles'][0] == "procuringEntity":
                self.__expected_fa_release['releases'][0]['parties'][od]['persones'] = expected_persones_list

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
