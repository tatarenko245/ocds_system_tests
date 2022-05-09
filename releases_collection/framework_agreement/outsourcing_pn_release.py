"""Prepare the expected releases of the outsourcing planning notice process, framework agreement procedures."""
import copy

from functions_collection.some_functions import is_it_uuid


class OutsourcingPlanningNoticeRelease:
    """This class creates instance of release."""

    def __init__(self, environment, actual_message, cpid, ocid, fa, ap, actual_pn_release, previous_pn_release,
                 actual_ms_release, previous_ms_release, actual_ap_release, previous_ap_release,
                 actual_fa_release, previous_fa_release):

        self.__environment = environment
        self.__actual_message = actual_message
        self.__cpid = cpid
        self.__ocid = ocid
        self.__fa = fa
        self.__ap = ap
        self.__actual_pn_release = actual_pn_release
        self.__previous_pn_release = previous_pn_release
        self.__actual_ms_release = actual_ms_release
        self.__previous_ms_release = previous_ms_release
        self.__actual_ap_release = actual_ap_release
        self.__previous_ap_release = previous_ap_release
        self.__actual_fa_release = actual_fa_release
        self.__previous_fa_release = previous_fa_release

        try:
            if environment == "dev":
                self.__metadata_tender_url = "http://dev.public.eprocurement.systems/tenders"
                self.__metadata_document_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get"
                self.__metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"

            elif environment == "sandbox":
                self.__metadata_tender_url = "http://public.eprocurement.systems/tenders"
                self.__metadata_document_url = "http://storage.eprocurement.systems/get"
                self.__metadata_budget_url = "http://public.eprocurement.systems/budgets"
        except ValueError:
            raise ValueError("Check your environment: You must use 'dev' or 'sandbox' environment in pytest command")

        self.__expected_pn_release = {
            "uri": self.__previous_pn_release['uri'],
            "version": self.__previous_pn_release['version'],
            "extensions": self.__previous_pn_release['extensions'],
            "publisher": {
                "name": self.__previous_pn_release['publisher']['name'],
                "uri": self.__previous_pn_release['publisher']['uri']
            },
            "license": self.__previous_pn_release['license'],
            "publicationPolicy": self.__previous_pn_release['publicationPolicy'],
            "publishedDate": self.__previous_pn_release['publishedDate'],
            "releases": [
                {
                    "ocid": self.__previous_pn_release['releases'][0]['ocid'],
                    "id": f"{self.__ocid}-{self.__actual_pn_release['releases'][0]['id'][46:59]}",
                    "date": actual_message['data']['operationDate'],
                    "tag": self.__previous_pn_release['releases'][0]['tag'],
                    "initiationType": self.__previous_pn_release['releases'][0]['initiationType'],
                    "language": self.__previous_pn_release['releases'][0]['language'],
                    "tender": {
                        "id": self.__previous_pn_release['releases'][0]['tender']['id'],
                        "status": self.__previous_pn_release['releases'][0]['tender']['status'],
                        "statusDetails": "aggregationPending",
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
                                    "id": "",
                                    "name": ""
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
                                "value": {
                                    "amount": 0.0,
                                    "currency": ""
                                },
                                "recurrentProcurement": [
                                    {
                                        "isRecurrent": False
                                    }
                                ],
                                "renewals": [
                                    {
                                        "hasRenewals": False
                                    }
                                ],
                                "variants": [
                                    {
                                        "hasVariants": False
                                    }
                                ],
                                "contractPeriod": {
                                    "startDate": "",
                                    "endDate": ""
                                },
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
                                    },
                                    "description": ""
                                },
                                "options": [
                                    {
                                        "hasOptions": False
                                    }
                                ]
                            }
                        ],
                        "lotGroups": [
                            {
                                "optionToCombine": self.__previous_pn_release['releases'][0]['tender'][
                                    'lotGroups'][0]['optionToCombine']
                            }
                        ],
                        "tenderPeriod": {
                            "startDate": self.__previous_pn_release['releases'][0]['tender'][
                                'tenderPeriod']['startDate']
                        },
                        "hasEnquiries": self.__previous_pn_release['releases'][0]['tender']['hasEnquiries'],
                        "documents": [
                            {
                                "id": "",
                                "documentType": "",
                                "title": "",
                                "description": "",
                                "url": "",
                                "datePublished": "",
                                "relatedLots": [
                                    ""
                                ]
                            }
                        ],
                        "submissionMethod": self.__previous_pn_release['releases'][0]['tender']['submissionMethod'],

                        "submissionMethodDetails": self.__previous_pn_release['releases'][0]['tender'][
                            'submissionMethodDetails'],

                        "submissionMethodRationale": self.__previous_pn_release['releases'][0]['tender'][
                            'submissionMethodRationale'],

                        "requiresElectronicCatalogue": self.__previous_pn_release['releases'][0]['tender'][
                            'requiresElectronicCatalogue']
                    },
                    "hasPreviousNotice": self.__previous_pn_release['releases'][0]['hasPreviousNotice'],

                    "purposeOfNotice": {
                        "isACallForCompetition": self.__previous_pn_release['releases'][0]['purposeOfNotice'][
                            'isACallForCompetition']
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
                    "id": f"{self.__ap}-{self.__actual_ap_release['releases'][0]['id'][46:59]}",
                    "date": self.__previous_ap_release['releases'][0]['date'],
                    "tag": self.__previous_ap_release['releases'][0]['tag'],
                    "language": self.__previous_ap_release['releases'][0]['language'],
                    "initiationType": self.__previous_ap_release['releases'][0]['initiationType'],
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
                        "id": self.__previous_ap_release['releases'][0]['tender']['id'],
                        "status": self.__previous_ap_release['releases'][0]['tender']['status'],
                        "statusDetails": self.__previous_ap_release['releases'][0]['tender']['statusDetails'],
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
                                "datePublished": ""
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

        self.__expected_ms_release = {
            "uri": self.__previous_ms_release['uri'],
            "version": self.__previous_ms_release['version'],
            "extensions": self.__previous_ms_release['extensions'],
            "publisher": {
                "name": self.__previous_ms_release['publisher']['name'],
                "uri": self.__previous_ms_release['publisher']['uri']
            },
            "license": self.__previous_ms_release['license'],
            "publicationPolicy": self.__previous_ms_release['publicationPolicy'],
            "publishedDate": self.__previous_ms_release['publishedDate'],
            "releases": [
                {
                    "ocid": self.__previous_ms_release['releases'][0]['ocid'],
                    "id": f"{self.__cpid}-{self.__previous_ms_release['releases'][0]['id'][29:42]}",
                    "date": self.__previous_ms_release['releases'][0]['date'],
                    "tag": self.__previous_ms_release['releases'][0]['tag'],
                    "language": self.__previous_ms_release['releases'][0]['language'],
                    "initiationType": "tender",
                    "planning": {
                        "budget": {
                            "description": "",
                            "amount": {
                                "amount": 0.0,
                                "currency": ""
                            },
                            "isEuropeanUnionFunded": True,
                            "budgetBreakdown": [
                                {
                                    "id": "",
                                    "description": "",
                                    "amount": {
                                        "amount": 0.0,
                                        "currency": ""
                                    },
                                    "period": {
                                        "startDate": "",
                                        "endDate": ""
                                    },
                                    "sourceParty": {
                                        "id": "",
                                        "name": ""
                                    },
                                    "europeanUnionFunding": {
                                        "projectIdentifier": "",
                                        "projectName": "",
                                        "uri": ""
                                    }
                                }]
                        },
                        "rationale": ""
                    },
                    "tender": {
                        "id": self.__previous_ms_release['releases'][0]['tender']['id'],
                        "title": self.__previous_ms_release['releases'][0]['tender']['title'],
                        "description": self.__previous_ms_release['releases'][0]['tender']['description'],
                        "status": self.__previous_ms_release['releases'][0]['tender']['status'],
                        "statusDetails": self.__previous_ms_release['releases'][0]['tender']['statusDetails'],
                        "value": {
                            "amount": self.__previous_ms_release['releases'][0]['tender']['value']['amount'],
                            "currency": self.__previous_ms_release['releases'][0]['tender']['value']['currency']
                        },
                        "procurementMethod": self.__previous_ms_release['releases'][0]['tender']['procurementMethod'],

                        "procurementMethodDetails": self.__previous_ms_release['releases'][0]['tender'][
                            'procurementMethodDetails'],

                        "procurementMethodRationale": "",

                        "mainProcurementCategory": self.__previous_ms_release['releases'][0]['tender'][
                            'mainProcurementCategory'],

                        "hasEnquiries": self.__previous_ms_release['releases'][0]['tender']['hasEnquiries'],

                        "eligibilityCriteria": self.__previous_ms_release['releases'][0]['tender'][
                            'eligibilityCriteria'],

                        "contractPeriod": {
                            "startDate": "",
                            "endDate": ""
                        },
                        "acceleratedProcedure": {
                            "isAcceleratedProcedure": self.__previous_ms_release['releases'][0]['tender'][
                                'acceleratedProcedure']['isAcceleratedProcedure']
                        },
                        "classification": {
                            "scheme": self.__previous_ms_release['releases'][0]['tender'][
                                'classification']['scheme'],

                            "id": self.__previous_ms_release['releases'][0]['tender'][
                                'classification']['id'],

                            "description": self.__previous_ms_release['releases'][0]['tender'][
                                'classification']['description']
                        },
                        "designContest": {
                            "serviceContractAward": self.__previous_ms_release['releases'][0]['tender'][
                                'designContest']['serviceContractAward']
                        },
                        "electronicWorkflows": {
                            "useOrdering": self.__previous_ms_release['releases'][0]['tender'][
                                'electronicWorkflows']['useOrdering'],

                            "usePayment": self.__previous_ms_release['releases'][0]['tender']['electronicWorkflows'][
                                'usePayment'],
                            "acceptInvoicing": self.__previous_ms_release['releases'][0]['tender'][
                                'electronicWorkflows']['acceptInvoicing']
                        },
                        "jointProcurement": {
                            "isJointProcurement": self.__previous_ms_release['releases'][0]['tender'][
                                'jointProcurement']['isJointProcurement']
                        },
                        "legalBasis": self.__previous_ms_release['releases'][0]['tender']['legalBasis'],
                        "procedureOutsourcing": {
                            "procedureOutsourced": self.__previous_ms_release['releases'][0]['tender'][
                                'procedureOutsourcing']['procedureOutsourced']
                        },
                        "procurementMethodAdditionalInfo": "",

                        "dynamicPurchasingSystem": {
                            "hasDynamicPurchasingSystem": self.__previous_ms_release['releases'][0]['tender'][
                                'dynamicPurchasingSystem']['hasDynamicPurchasingSystem']
                        },
                        "framework": {
                            "isAFramework": self.__previous_ms_release['releases'][0]['tender'][
                                'framework']['isAFramework']
                        }
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
                                        "description": ""
                                    }
                                }
                            },
                            "additionalIdentifiers": [
                                {
                                    "scheme": "",
                                    "id": "",
                                    "legalName": "",
                                    "uri": ""
                                }],
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
                            "roles": [
                                ""]
                        }],
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
                    "id": f"{self.__fa}-{self.__actual_fa_release['releases'][0]['id'][29:42]}",
                    "date": self.__actual_message['data']['operationDate'],
                    "tag": self.__previous_fa_release['releases'][0]['tag'],
                    "initiationType": self.__previous_fa_release['releases'][0]['initiationType'],
                    "language": self.__previous_fa_release['releases'][0]['language'],
                    "tender": {
                        "id": self.__previous_fa_release['releases'][0]['tender']['id'],
                        "title": self.__previous_fa_release['releases'][0]['tender']['title'],
                        "description": self.__previous_fa_release['releases'][0]['tender']['description'],
                        "status": self.__previous_fa_release['releases'][0]['tender']['status'],
                        "statusDetails": self.__previous_fa_release['releases'][0]['tender']['statusDetails'],
                        "hasEnquiries": self.__previous_fa_release['releases'][0]['tender']['hasEnquiries'],
                        "value": {
                            "currency": self.__previous_fa_release['releases'][0]['tender']['value']['currency']
                        },
                        "procurementMethod": self.__previous_fa_release['releases'][0]['tender']['procurementMethod'],

                        "procurementMethodDetails": self.__previous_fa_release['releases'][0]['tender'][
                            'procurementMethodDetails'],

                        "procurementMethodRationale": "",

                        "eligibilityCriteria": self.__previous_fa_release['releases'][0]['tender'][
                            'eligibilityCriteria'],

                        "contractPeriod": {
                            "startDate": self.__previous_fa_release['releases'][0]['tender']['contractPeriod'][
                                'startDate'],

                            "endDate": self.__previous_fa_release['releases'][0]['tender']['contractPeriod'][
                                'endDate']
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

        if "documents" in self.__previous_ap_release['releases'][0]['tender']:
            self.__expected_ap_release['releases'][0]['tender']['documents'] = \
                self.__previous_ap_release['releases'][0]['tender']['documents']
        else:
            del self.__expected_ap_release['releases'][0]['tender']['documents']

        self.__expected_ap_release['releases'][0]['parties'] = self.__previous_ap_release['releases'][0]['parties']

        self.__expected_ap_release['releases'][0]['relatedProcesses'] = \
            self.__previous_ap_release['releases'][0]['relatedProcesses']
        return self.__expected_ap_release

    def build_expected_pn_release(self):
        """Build PN release."""

        if "items" in self.__previous_pn_release['releases'][0]['tender']:
            self.__expected_pn_release['releases'][0]['tender']['items'] = \
                self.__previous_pn_release['releases'][0]['tender']['items']
        else:
            del self.__expected_pn_release['releases'][0]['tender']['items']

        if "lots" in self.__previous_pn_release['releases'][0]['tender']:
            self.__expected_pn_release['releases'][0]['tender']['lots'] = \
                self.__previous_pn_release['releases'][0]['tender']['lots']
        else:
            del self.__expected_pn_release['releases'][0]['tender']['lots']

        if "documents" in self.__previous_pn_release['releases'][0]['tender']:
            self.__expected_pn_release['releases'][0]['tender']['documents'] = \
                self.__previous_pn_release['releases'][0]['tender']['documents']
        else:
            del self.__expected_pn_release['releases'][0]['tender']['documents']

        # Prepare 'release[0].relatedProcesses' array:
        old_related_processes = self.__previous_pn_release['releases'][0]['relatedProcesses']
        new_related_processes = list()
        for n in range(1):
            new_related_processes.append(copy.deepcopy(
                self.__expected_ap_release['releases'][0]['relatedProcesses'][0]
            ))

            new_related_processes[n]['relationship'] = ["framework"]
            new_related_processes[n]['scheme'] = "ocid"
            new_related_processes[n]['identifier'] = self.__fa
            new_related_processes[n]['uri'] = f"{self.__metadata_tender_url}/{self.__fa}/{self.__fa}"

        # Set permanent id:
        temp_actual_related_processes = copy.deepcopy(self.__actual_pn_release['releases'][0]['relatedProcesses'])
        temp_expected_related_processes = copy.deepcopy(new_related_processes)

        for act in range(len(self.__actual_pn_release['releases'][0]['relatedProcesses'])):
            del temp_actual_related_processes[act]['id']
        for exp in range(len(new_related_processes)):
            del temp_expected_related_processes[exp]['id']

        for act in range(len(self.__actual_pn_release['releases'][0]['relatedProcesses'])):
            for exp in range(len(new_related_processes)):
                if temp_expected_related_processes[exp] == temp_actual_related_processes[act]:
                    try:
                        """Set permanent id."""
                        is_permanent_id_correct = is_it_uuid(
                            self.__actual_pn_release['releases'][0]['relatedProcesses'][act]['id']
                        )
                        if is_permanent_id_correct is True:
                            new_related_processes[exp]['id'] = \
                                self.__actual_pn_release['releases'][0]['relatedProcesses'][act]['id']
                        else:
                            raise ValueError(f"The 'releases[0].relatedProcesses[{act}].id' must be uuid.")
                    except KeyError:
                        raise KeyError(f"Mismatch key into path 'releases[0].relatedProcesses[{act}].id'")

        # Sort objects:
        expected_related_processes = list()
        temp_related_processes = old_related_processes + new_related_processes
        for act in range(len(self.__actual_pn_release['releases'][0]['relatedProcesses'])):
            for exp in range(len(temp_related_processes)):

                if temp_related_processes[exp]['id'] == \
                        self.__actual_pn_release['releases'][0]['relatedProcesses'][act]['id']:
                    expected_related_processes.append(temp_related_processes[exp])

        self.__expected_pn_release['releases'][0]['relatedProcesses'] = expected_related_processes
        return self.__expected_pn_release

    def build_expected_ms_release(self):
        """Build MS release."""
        if "procurementMethodRationale" in self.__actual_ms_release['releases'][0]['tender']:

            self.__expected_ms_release['releases'][0]['tender']['procurementMethodRationale'] = \
                self.__previous_ms_release['releases'][0]['tender']['procurementMethodRationale']
        else:
            del self.__expected_ms_release['releases'][0]['tender']['procurementMethodRationale']

        if "contractPeriod" in self.__actual_ms_release['releases'][0]['tender']:

            self.__expected_ms_release['releases'][0]['tender']['contractPeriod'] = \
                self.__previous_ms_release['releases'][0]['tender']['contractPeriod']
        else:
            del self.__expected_ms_release['releases'][0]['tender']['contractPeriod']

        if "procurementMethodAdditionalInfo" in self.__actual_ms_release['releases'][0]['tender']:

            self.__expected_ms_release['releases'][0]['tender']['procurementMethodAdditionalInfo'] = \
                self.__previous_ms_release['releases'][0]['tender']['procurementMethodAdditionalInfo']
        else:
            del self.__expected_ms_release['releases'][0]['tender']['procurementMethodAdditionalInfo']

        self.__expected_ms_release['releases'][0]['relatedProcesses'] = \
            self.__previous_ms_release['releases'][0]['relatedProcesses']

        self.__expected_ms_release['releases'][0]['planning'] = self.__previous_ms_release['releases'][0]['planning']
        self.__expected_ms_release['releases'][0]['parties'] = self.__previous_ms_release['releases'][0]['parties']
        return self.__expected_ms_release

    def build_expected_fa_release(self):
        """Build FA release."""

        if "procurementMethodRationale" in self.__actual_fa_release['releases'][0]['tender']:

            self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale'] = \
                self.__previous_fa_release['releases'][0]['tender']['procurementMethodRationale']
        else:
            del self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale']

        # Prepare 'release[0].relatedProcesses' array:
        old_related_processes = self.__previous_fa_release['releases'][0]['relatedProcesses']
        new_related_processes = list()
        for n in range(1):
            new_related_processes.append(copy.deepcopy(
                self.__expected_fa_release['releases'][0]['relatedProcesses'][0]
            ))

            new_related_processes[n]['relationship'] = ["x_demand"]
            new_related_processes[n]['scheme'] = "ocid"
            new_related_processes[n]['identifier'] = self.__cpid
            new_related_processes[n]['uri'] = f"{self.__metadata_tender_url}/{self.__cpid}/{self.__cpid}"

        # Set permanent id:
        temp_actual_related_processes = copy.deepcopy(self.__actual_fa_release['releases'][0]['relatedProcesses'])
        temp_expected_related_processes = copy.deepcopy(new_related_processes)

        for act in range(len(self.__actual_fa_release['releases'][0]['relatedProcesses'])):
            del temp_actual_related_processes[act]['id']
        for exp in range(len(new_related_processes)):
            del temp_expected_related_processes[exp]['id']

        for act in range(len(self.__actual_fa_release['releases'][0]['relatedProcesses'])):
            for exp in range(len(new_related_processes)):
                if temp_expected_related_processes[exp] == temp_actual_related_processes[act]:
                    try:
                        """Set permanent id."""
                        is_permanent_id_correct = is_it_uuid(
                            self.__actual_fa_release['releases'][0]['relatedProcesses'][act]['id']
                        )
                        if is_permanent_id_correct is True:
                            new_related_processes[exp]['id'] = \
                                self.__actual_fa_release['releases'][0]['relatedProcesses'][act]['id']
                        else:
                            raise ValueError(f"The 'releases[0].relatedProcesses[{act}].id' must be uuid.")
                    except KeyError:
                        raise KeyError(f"Mismatch key into path 'releases[0].relatedProcesses[{act}].id'")

        # Sort objects:
        expected_related_processes = list()
        temp_related_processes = old_related_processes + new_related_processes
        for act in range(len(self.__actual_fa_release['releases'][0]['relatedProcesses'])):
            for exp in range(len(temp_related_processes)):

                if temp_related_processes[exp]['id'] == \
                        self.__actual_fa_release['releases'][0]['relatedProcesses'][act]['id']:
                    expected_related_processes.append(temp_related_processes[exp])

        self.__expected_fa_release['releases'][0]['relatedProcesses'] = expected_related_processes
        return self.__expected_fa_release
