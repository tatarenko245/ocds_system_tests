"""Prepare the expected releases of the complete qualification process, framework agreement procedures."""
import json

from functions_collection.cassandra_methods import get_parameter_from_submission_rules


class CompleteQualificationRelease:
    """This class creates instance of release."""

    def __init__(self, actual_message, ocid):
        self.__actual_message = actual_message
        self.__ocid = ocid

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
                            "date": "",
                            "status": "",
                            "statusDetails": "",
                            "isFrameworkOrDynamic": False
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
        self.__expected_fe_release['releases'][0]['date'] = self.__actual_message['data']['operationDate']
        self.__expected_fe_release['releases'][0]['tag'] = previous_fe_release['releases'][0]['tag']
        self.__expected_fe_release['releases'][0]['language'] = previous_fe_release['releases'][0]['language']
        self.__expected_fe_release['releases'][0]['initiationType'] = \
            previous_fe_release['releases'][0]['initiationType']
        self.__expected_fe_release['releases'][0]['hasPreviousNotice'] = \
            previous_fe_release['releases'][0]['hasPreviousNotice']
        self.__expected_fe_release['releases'][0]['purposeOfNotice']['isACallForCompetition'] = \
            previous_fe_release['releases'][0]['purposeOfNotice']['isACallForCompetition']

        """Prepare 'preQualification' object for expected FE release: releases[0].preQualification: FR.COM-7.23.1"""
        self.__expected_fe_release['releases'][0]['preQualification']['period'] = \
            previous_fe_release['releases'][0]['preQualification']['period']
        self.__expected_fe_release['releases'][0]['preQualification']['qualificationPeriod']['startDate'] = \
            previous_fe_release['releases'][0]['preQualification']['qualificationPeriod']['startDate']
        self.__expected_fe_release['releases'][0]['preQualification']['qualificationPeriod']['endDate'] = \
            self.__actual_message['data']['operationDate']

        """Prepare 'parties' array for expected FE release: releases[0].parties:
        https://ustudio.atlassian.net/wiki/spaces/ES/pages/652148737/10.0.5.5+eDossier#
        dossierGetSubmissionsForTendering -> dossierGetSubmissionsForTendering -> 
        ???????? ???processInfo.operationType??? = ???completeQualification??? ?????????????????? ???????????????? ???invitedCandidate???"""
        self.__expected_fe_release['releases'][0]['parties'] = previous_fe_release['releases'][0]['parties']
        temp_relatedsubmission_list = list()
        for q in range(len(previous_fe_release['releases'][0]['qualifications'])):
            if previous_fe_release['releases'][0]['qualifications'][q]['status'] == "pending" and \
                    previous_fe_release['releases'][0]['qualifications'][q]['statusDetails'] == "active":
                temp_relatedsubmission_list.append(
                    previous_fe_release['releases'][0]['qualifications'][q]['relatedSubmission']
                )
        for q in range(len(temp_relatedsubmission_list)):
            for s in range(len(previous_fe_release['releases'][0]['submissions']['details'])):
                if previous_fe_release['releases'][0]['submissions']['details'][s]['id'] == \
                        temp_relatedsubmission_list[q]:
                    for can in range(len(
                            previous_fe_release['releases'][0]['submissions']['details'][s]['candidates'])):
                        for party in range(len(self.__expected_fe_release['releases'][0]['parties'])):
                            if previous_fe_release['releases'][0]['submissions']['details'][s][
                                    'candidates'][can]['id'] == self.__expected_fe_release['releases'][0][
                                    'parties'][party]['id']:
                                self.__expected_fe_release['releases'][0]['parties'][party]['roles'].append(
                                    "invitedCandidate"
                                )

        """Prepare 'tender' object for expected FE release: releases[0].tender:
        Subprocess Modify Tender -> if operationType = completeQualification"""
        self.__expected_fe_release['releases'][0]['tender']['id'] = previous_fe_release['releases'][0]['tender']['id']
        self.__expected_fe_release['releases'][0]['tender']['status'] = "active"
        self.__expected_fe_release['releases'][0]['tender']['statusDetails'] = "evaluation"
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

        """Prepare 'contracts' array"""
        self.__expected_fe_release['releases'][0]['contracts'] = previous_fe_release['releases'][0]['contracts']

        """Prepare 'qualifications' array for expected FE release: releases[0].qualification: FR.COM-7.26.1,"""
        self.__expected_fe_release['releases'][0]['qualifications'] = \
            previous_fe_release['releases'][0]['qualifications']
        for q in range(len(self.__expected_fe_release['releases'][0]['qualifications'])):
            if self.__expected_fe_release['releases'][0]['qualifications'][q]['status'] == "pending" and \
                    self.__expected_fe_release['releases'][0]['qualifications'][q]['statusDetails'] == "active":
                self.__expected_fe_release['releases'][0]['qualifications'][q]['status'] = "active"
                self.__expected_fe_release['releases'][0]['qualifications'][q]['statusDetails'] = "basedOnHumanDecision"
            elif self.__expected_fe_release['releases'][0]['qualifications'][q]['status'] == "pending" and \
                    self.__expected_fe_release['releases'][0]['qualifications'][q]['statusDetails'] == "unsuccessful":
                self.__expected_fe_release['releases'][0]['qualifications'][q]['status'] = "unsuccessful"
                self.__expected_fe_release['releases'][0]['qualifications'][q]['statusDetails'] = "basedOnHumanDecision"

        """Prepare 'submission' object for expected FE release: releases[0].submission: FR.COM-5.18.1"""
        self.__expected_fe_release['releases'][0]['submissions']['details'] = \
            previous_fe_release['releases'][0]['submissions']['details']

        for s in range(len(self.__expected_fe_release['releases'][0]['submissions']['details'])):
            if self.__expected_fe_release['releases'][0]['submissions']['details'][s]['status'] == "pending":
                self.__expected_fe_release['releases'][0]['submissions']['details'][s]['status'] = "withdrawn"

        for s in range(len(self.__expected_fe_release['releases'][0]['submissions']['details'])):
            if self.__expected_fe_release['releases'][0]['submissions']['details'][s]['status'] == "withdrawn":
                for q in range(len(self.__expected_fe_release['releases'][0]['qualifications'])):
                    if self.__expected_fe_release['releases'][0]['qualifications'][q]['status'] == "unsuccessful":
                        if self.__expected_fe_release['releases'][0]['qualifications'][q]['relatedSubmission'] == \
                                self.__expected_fe_release['releases'][0]['submissions']['details'][s]['id']:
                            self.__expected_fe_release['releases'][0]['submissions']['details'][s][
                                'status'] = "disqualified"

                    elif self.__expected_fe_release['releases'][0]['qualifications'][q]['status'] == "active":
                        if self.__expected_fe_release['releases'][0]['qualifications'][q]['relatedSubmission'] == \
                                self.__expected_fe_release['releases'][0]['submissions']['details'][s]['id']:
                            self.__expected_fe_release['releases'][0]['submissions']['details'][s][
                                'status'] = "valid"
            else:
                ValueError(f"The value of 'submissions.details[{s}].status' is invalid: "
                           f"{self.__expected_fe_release['releases'][0]['submissions']['details'][s]['status']}")

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
