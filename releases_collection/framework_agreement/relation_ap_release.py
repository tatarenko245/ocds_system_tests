"""Prepare the expected releases of the relation aggregated plan process, framework agreement procedures."""
import copy

from functions_collection.some_functions import is_it_uuid, get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv


class RelationAggregatedPlanRelease:
    """This class creates instance of release."""

    def __init__(self, environment, language, actual_message, cpid, ocid, cp, pn, actual_pn_release,
                 previous_pn_release, actual_ms_release, previous_ms_release, actual_ap_release, previous_ap_release,
                 actual_fa_release, previous_fa_release, list_of_pn_payload, list_of_ei_payload):

        self.__environment = environment
        self.__language = language
        self.__actual_message = actual_message
        self.__cpid = cpid
        self.__ocid = ocid
        self.__cp = cp
        self.__pn = pn
        self.__actual_pn_release = actual_pn_release
        self.__previous_pn_release = previous_pn_release
        self.__actual_ms_release = actual_ms_release
        self.__previous_ms_release = previous_ms_release
        self.__actual_ap_release = actual_ap_release
        self.__previous_ap_release = previous_ap_release
        self.__actual_fa_release = actual_fa_release
        self.__previous_fa_release = previous_fa_release
        self.__list_of_pn_payload = list_of_pn_payload
        self.__list_of_ei_payload = list_of_ei_payload

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
            ValueError("Check your environment: You must use 'dev' or 'sandbox' environment in pytest command")

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
                    "id": f"{self.__pn}-{self.__actual_pn_release['releases'][0]['id'][46:59]}",
                    "date": actual_message['data']['operationDate'],
                    "tag": self.__previous_pn_release['releases'][0]['tag'],
                    "initiationType": self.__previous_pn_release['releases'][0]['initiationType'],
                    "language": self.__previous_pn_release['releases'][0]['language'],
                    "tender": {
                        "id": self.__previous_pn_release['releases'][0]['tender']['id'],
                        "status": self.__previous_pn_release['releases'][0]['tender']['status'],
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
                    "id": f"{self.__ocid}-{self.__actual_ap_release['releases'][0]['id'][46:59]}",
                    "date": self.__actual_message['data']['operationDate'],
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
                    "id": f"{self.__cp}-{self.__previous_ms_release['releases'][0]['id'][29:42]}",
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
                    "id": f"{self.__cpid}-{self.__actual_fa_release['releases'][0]['id'][29:42]}",
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
                            "amount": 0.00,
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

        old_parties = self.__previous_ap_release['releases'][0]['parties']

        # Prepare 'releases[0].parties' array:
        new_parties = list()
        for p_0 in range(len(self.__list_of_ei_payload)):
            new_parties.append(copy.deepcopy(
                self.__expected_ap_release['releases'][0]['parties'][0]
            ))

            new_parties[p_0]['id'] = f"{self.__list_of_ei_payload[p_0]['buyer']['identifier']['scheme']}-" \
                                     f"{self.__list_of_ei_payload[p_0]['buyer']['identifier']['id']}"

            new_parties[p_0]['name'] = self.__list_of_ei_payload[p_0]['buyer']['name']
            new_parties[p_0]['identifier']['scheme'] = self.__list_of_ei_payload[p_0]['buyer']['identifier']['scheme']
            new_parties[p_0]['identifier']['id'] = self.__list_of_ei_payload[p_0]['buyer']['identifier']['id']

            new_parties[p_0]['identifier']['legalName'] = \
                self.__list_of_ei_payload[p_0]['buyer']['identifier']['legalName']

            if "uri" in self.__list_of_ei_payload[p_0]['buyer']['identifier']:
                new_parties[p_0]['identifier']['uri'] = self.__list_of_ei_payload[p_0]['buyer']['identifier']['uri']
            else:
                del new_parties[p_0]['identifier']['uri']

            new_parties[p_0]['address']['streetAddress'] = \
                self.__list_of_ei_payload[p_0]['buyer']['address']['streetAddress']

            if "postalCode" in self.__list_of_ei_payload[p_0]['buyer']['address']:
                new_parties[p_0]['address']['postalCode'] = \
                    self.__list_of_ei_payload[p_0]['buyer']['address']['postalCode']
            else:
                del new_parties[p_0]['address']['postalCode']

            try:
                """
                Prepare expected 'addressDetails' object for party with 'role'= ['client'].
                """
                country_data = get_value_from_country_csv(
                    country=self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails']['country']['id'],
                    language=self.__language
                )

                expected_country_object = [{
                    "scheme": country_data[2],
                    "id": self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails']['country']['id'],
                    "description": country_data[1],
                    "uri": country_data[3]
                }]

                region_data = get_value_from_region_csv(
                    region=self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails']['region']['id'],
                    country=self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails']['country']['id'],
                    language=self.__language
                )
                expected_region_object = [{
                    "scheme": region_data[2],
                    "id": self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails']['region']['id'],
                    "description": region_data[1],
                    "uri": region_data[3]
                }]

                if self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails']['locality']['scheme'] == \
                        "CUATM":
                    locality_data = get_value_from_locality_csv(
                        locality=self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails']['locality']['id'],
                        region=self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails']['region']['id'],
                        country=self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails']['country']['id'],
                        language=self.__language
                    )

                    expected_locality_object = [{
                        "scheme": locality_data[2],
                        "id": self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails']['locality']['id'],
                        "description": locality_data[1],
                        "uri": locality_data[3]
                    }]

                else:
                    expected_locality_object = [{
                        "scheme": self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails'][
                            'locality']['scheme'],
                        "id": self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails'][
                            'locality']['id'],
                        "description": self.__list_of_ei_payload[p_0]['buyer']['address']['addressDetails'][
                            'locality']['description']
                    }]

                new_parties[p_0]['address']['addressDetails']['country'] = expected_country_object[0]
                new_parties[p_0]['address']['addressDetails']['region'] = expected_region_object[0]
                new_parties[p_0]['address']['addressDetails']['locality'] = expected_locality_object[0]
            except ValueError:
                ValueError("Impossible to prepare expected 'addressDetails' object for party "
                                 "with 'role'= ['client'].")

            if "additionalIdentifiers" in self.__list_of_ei_payload[p_0]['buyer']:
                for a_0 in range(len(new_parties[p_0]['additionalIdentifiers'])):
                    if "uri" in new_parties[p_0]['additionalIdentifiers'][a_0]:
                        new_parties[p_0]['additionalIdentifiers'][a_0]['uri'] = \
                            self.__list_of_ei_payload[p_0]['buyer']['additionalIdentifiers'][a_0]['uri']
                    else:
                        del new_parties[p_0]['additionalIdentifiers'][a_0]['uri']

                    new_parties[p_0]['additionalIdentifiers'][a_0]['scheme'] = \
                        self.__list_of_ei_payload[p_0]['buyer']['additionalIdentifiers'][a_0]['scheme']

                    new_parties[p_0]['additionalIdentifiers'][a_0]['id'] = \
                        self.__list_of_ei_payload[p_0]['buyer']['additionalIdentifiers'][a_0]['id']

                    new_parties[p_0]['additionalIdentifiers'][a_0]['legalName'] = \
                        self.__list_of_ei_payload[p_0]['buyer']['additionalIdentifiers'][a_0]['legalName']
            else:
                del new_parties[p_0]['additionalIdentifiers']

            new_parties[p_0]['contactPoint']['name'] = self.__list_of_ei_payload[p_0]['buyer']['contactPoint']['name']
            new_parties[p_0]['contactPoint']['email'] = self.__list_of_ei_payload[p_0]['buyer']['contactPoint']['email']

            new_parties[p_0]['contactPoint']['telephone'] = \
                self.__list_of_ei_payload[p_0]['buyer']['contactPoint']['telephone']

            if "faxNumber" in self.__list_of_ei_payload[p_0]['buyer']['contactPoint']:
                new_parties[p_0]['contactPoint']['faxNumber'] = \
                    self.__list_of_ei_payload[p_0]['buyer']['contactPoint']['faxNumber']
            else:
                del new_parties[p_0]['contactPoint']['faxNumber']

            if "url" in self.__list_of_ei_payload[p_0]['buyer']['contactPoint']:
                new_parties[p_0]['contactPoint']['url'] = \
                    self.__list_of_ei_payload[p_0]['buyer']['contactPoint']['url']
            else:
                del new_parties[p_0]['contactPoint']['url']

            if "details" in self.__list_of_ei_payload[p_0]['buyer']:
                if "typeOfBuyer" in self.__list_of_ei_payload[p_0]['buyer']['details']:
                    new_parties[p_0]['details']['typeOfBuyer'] = \
                        self.__list_of_ei_payload[p_0]['buyer']['details']['typeOfBuyer']
                else:
                    del new_parties[p_0]['details']['typeOfBuyer']

                if "mainGeneralActivity" in self.__list_of_ei_payload[p_0]['buyer']['details']:
                    new_parties[p_0]['details']['mainGeneralActivity'] = \
                        self.__list_of_ei_payload[p_0]['buyer']['details']['mainGeneralActivity']
                else:
                    del new_parties[p_0]['details']['mainGeneralActivity']

                if "mainSectoralActivity" in self.__list_of_ei_payload[p_0]['buyer']['details']:
                    new_parties[p_0]['details']['mainSectoralActivity'] = \
                        self.__list_of_ei_payload[p_0]['buyer']['details']['mainSectoralActivity']
                else:
                    del new_parties[p_0]['details']['mainSectoralActivity']
            else:
                del new_parties[p_0]['details']

            new_parties[p_0]['roles'] = ["client"]

        # Sort objects:
        expected_parties = list()

        for n in range(len(new_parties)):
            for o in range(len(old_parties)):
                if new_parties[n]['id'] == old_parties[o]['id']:
                    del new_parties[n]

        parties = old_parties + new_parties

        for act in range(len(self.__actual_ap_release['releases'][0]['parties'])):
            for exp in range(len(parties)):
                if self.__actual_ap_release['releases'][0]['parties'][act]['id'] == parties[exp]['id']:
                    expected_parties.append(parties[exp])

        self.__expected_ap_release['releases'][0]['parties'] = expected_parties

        # Prepare 'release[0].relatedProcesses' array:
        old_related_processes = self.__previous_ap_release['releases'][0]['relatedProcesses']
        new_related_processes = list()
        for n in range(1):
            new_related_processes.append(copy.deepcopy(
                self.__expected_ap_release['releases'][0]['relatedProcesses'][0]
            ))

            new_related_processes[n]['relationship'] = ["x_scope"]
            new_related_processes[n]['scheme'] = "ocid"
            new_related_processes[n]['identifier'] = self.__pn
            new_related_processes[n]['uri'] = f"{self.__metadata_tender_url}/{self.__cp}/{self.__pn}"

        # Set permanent id:
        temp_actual_related_processes = copy.deepcopy(self.__actual_ap_release['releases'][0]['relatedProcesses'])
        temp_expected_related_processes = copy.deepcopy(new_related_processes)

        for act in range(len(self.__actual_pn_release['releases'][0]['relatedProcesses'])):
            del temp_actual_related_processes[act]['id']
        for exp in range(len(new_related_processes)):
            del temp_expected_related_processes[exp]['id']

        for act in range(len(self.__actual_ap_release['releases'][0]['relatedProcesses'])):
            for exp in range(len(new_related_processes)):
                if temp_expected_related_processes[exp] == temp_actual_related_processes[act]:
                    try:
                        """Set permanent id."""
                        is_permanent_id_correct = is_it_uuid(
                            self.__actual_ap_release['releases'][0]['relatedProcesses'][act]['id']
                        )
                        if is_permanent_id_correct is True:
                            new_related_processes[exp]['id'] = \
                                self.__actual_ap_release['releases'][0]['relatedProcesses'][act]['id']
                        else:
                            ValueError(f"The 'releases[0].relatedProcesses[{act}].id' must be uuid.")
                    except KeyError:
                        KeyError(f"Mismatch key into path 'releases[0].relatedProcesses[{act}].id'")

        # Sort objects:
        expected_related_processes = list()
        temp_related_processes = old_related_processes + new_related_processes
        for act in range(len(self.__actual_ap_release['releases'][0]['relatedProcesses'])):
            for exp in range(len(temp_related_processes)):

                if temp_related_processes[exp]['id'] == \
                        self.__actual_ap_release['releases'][0]['relatedProcesses'][act]['id']:
                    expected_related_processes.append(temp_related_processes[exp])

        self.__expected_ap_release['releases'][0]['relatedProcesses'] = expected_related_processes
        return self.__expected_ap_release

    def build_expected_fa_release(self):
        """Build FA release."""

        if "procurementMethodRationale" in self.__actual_fa_release['releases'][0]['tender']:

            self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale'] = \
                self.__previous_fa_release['releases'][0]['tender']['procurementMethodRationale']
        else:
            del self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale']

        self.__expected_fa_release['releases'][0]['relatedProcesses'] = \
            self.__previous_fa_release['releases'][0]['relatedProcesses']

        try:
            """
            Prepare expected 'tender.value.amount' attribute.
            Sum amount from budgetBreakdown, because lots array wasn't presented into pn_1_payload.
            Sum amount from budgetBreakdown, because lots array wasn't presented into pn_2_payload.
            """
            amount_from_pn_payload = list()
            for p in range(len(self.__list_of_pn_payload)):
                if "lots" in self.__list_of_pn_payload[p]['tender']:
                    for lo in range(len(self.__list_of_pn_payload[p]['tender']['lots'])):
                        amount_from_pn_payload.append(
                            self.__list_of_pn_payload[p]['tender']['lots'][lo]['value']['amount']
                        )

                else:
                    for budget in range(len(self.__list_of_pn_payload[p]['planning']['budget']['budgetBreakdown'])):
                        amount_from_pn_payload.append(
                            self.__list_of_pn_payload[p]['planning']['budget']['budgetBreakdown'][budget][
                                'amount']['amount']
                        )

            expected_tender_value_amount = sum(amount_from_pn_payload)
        except ValueError:
            ValueError("Impossible to prepare expected 'tender.value.amount' attribute.")

        self.__expected_fa_release['releases'][0]['tender']['value']['amount'] = expected_tender_value_amount
        return self.__expected_fa_release

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

        self.__expected_pn_release['releases'][0]['relatedProcesses'] = \
            self.__previous_pn_release['releases'][0]['relatedProcesses']
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
