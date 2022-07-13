"""This is full release data model for PN release."""

pn_release_model = {
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
                                        "description": ""
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
                        "optionToCombine": False
                    }
                ],
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
                        "datePublished": "",
                        "relatedLots": [
                            ""
                        ]
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
                        "parent"
                    ],
                    "scheme": "",
                    "identifier": "",
                    "uri": ""
                }
            ]
        }
    ]
}

ms_release_model = {
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
    "publicationPolicy": "h",
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
                        }
                    ]
                },
                "rationale": ""
            },
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
                "hasEnquiries": False,
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
                "procurementMethodAdditionalInfo": "",
                "dynamicPurchasingSystem": {
                    "hasDynamicPurchasingSystem": False
                },
                "framework": {
                    "isAFramework": False
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
