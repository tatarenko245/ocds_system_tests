

payload_model = {
    "planning": {
        "rationale": "",
        "budget": {
            "description": "",
            "budgetBreakdown": [
                {
                    "id": "",
                    "amount": {
                        "amount": 0.00,
                        "currency": ""
                    },
                    "classifications": {
                        "ei": "",
                        "fs": ""
                    }
                }
            ]
        }
    },
    "tender": {
        "title": "",
        "description": "create pin: tender.description",
        "classification": {
            "id": "",
            "scheme": ""
        },
        "legalBasis": "",
        "procurementMethodRationale": "",
        "awardCriteria": "",
        "awardCriteriaDetails": "",
        "tenderPeriod": {
            "startDate": ""
        },
        "enquiryPeriod": {
            "endDate": ""
        },
        "procurementMethodModalities": [""],
        "electronicAuctions": {
            "details": [
                {
                    "id": "",
                    "relatedLot": "",
                    "electronicAuctionModalities": [
                        {
                            "eligibleMinimumDifference": {
                                "amount": 0.00,
                                "currency": ""
                            }
                        }
                    ]
                }
            ]
        },
        "procuringEntity": {
            "name": "",
            "identifier": {
                "id": "",
                "legalName": "",
                "scheme": "",
                "uri": ""
            },
            "additionalIdentifiers": [
                {
                    "id": "",
                    "legalName": "",
                    "scheme": "",
                    "uri": ""
                }
            ],
            "address": {
                "streetAddress": "",
                "postalCode": "",
                "addressDetails": {
                    "country": {
                            "id": "",
                            "description": "",
                            "scheme": ""
                        },
                    "region": {
                        "id": "",
                        "description": "",
                        "scheme": ""
                    },
                    "locality": {
                        "id": "",
                        "description": "",
                        "scheme": ""
                    }
                }
            },
            "contactPoint": {
                "name": "",
                "email": "",
                "telephone": "",
                "faxNumber": "",
                "url": ""
            },
            "persones": [
                {
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
                                    "title": "",
                                    "documentType": "",
                                    "description": ""
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "criteria": [
            {
                "id": "",
                "title": "",
                "classification": {
                    "id": "",
                    "scheme": ""
                },
                "description": "",
                "relatesTo": "",
                "relatedItem": "",
                "requirementGroups": [
                    {
                        "id": "",
                        "description": "",
                        "requirements": [
                            {
                                "id": "",
                                "title": "",
                                "dataType": "",
                                "description": "",
                                "period": {
                                    "startDate": "",
                                    "endDate": ""
                                },
                                "expectedValue": "",
                                "minValue": 0.00,
                                "maxValue": 0.00,
                                "eligibleEvidences": [
                                    {
                                        "id": "",
                                        "title": "",
                                        "description": "",
                                        "type": "",
                                        "relatedDocument": {
                                            "id": ""
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "conversions": [
            {
                "id": "",
                "relatedItem": "",
                "relatesTo": "",
                "description": "",
                "rationale": "",
                "coefficients": [
                    {
                        "value": "",
                        "id": "",
                        "coefficient": 1.0
                    }
                ]
            }
        ],
        "targets": [
            {
                "id": "",
                "title": "",
                "relatesTo": "",
                "relatedItem": "",
                "observations": [
                    {
                        "id": "",
                        "period": {
                            "startDate": "",
                            "endDate": ""
                        },
                        "measure": "",
                        'unit': {
                            "id": ""
                        },
                        "dimensions": {
                            "requirementClassIdPR": ""
                        },
                        "notes": "",
                        "relatedRequirementId": ""
                    }
                ]
            }
        ],
        "lots": [
            {
                "id": "",
                "internalId": "",
                "title": "",
                "description": "",
                "value": {
                    "amount": 0.00,
                    "currency": ""
                },
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
                                "id": "",
                                "description": "",
                                "scheme": ""
                            },
                            "region": {
                                "id": "",
                                "description": "",
                                "scheme": ""
                            },
                            "locality": {
                                "id": "",
                                "description": "",
                                "scheme": ""
                            }
                        }
                    },
                    "description": ""
                },
                "hasOptions": True,
                "options": [
                    {
                        "description": "",
                        "period": {
                            "durationInDays": 365,
                            "startDate": "",
                            "endDate": "",
                            "maxExtentDate": ""
                        }
                    }
                ],
                "hasRecurrence": True,
                "recurrence": {
                    "dates": [
                        {
                            "startDate": ""
                        }
                    ],
                    "description": ""
                },
                "hasRenewal": True,
                "renewal": {
                    "description": "",
                    "minimumRenewals": 0.00,
                    "maximumRenewals": 0.00,
                    "period": {
                        "durationInDays": 0.00,
                        "startDate": "",
                        "endDate": "",
                        "maxExtentDate": ""
                    }
                }
            }
        ],
        "items": [
            {
                "id": "",
                "internalId": "",
                "classification": {
                    "id": "",
                    "scheme": ""
                },
                "additionalClassifications": [
                    {
                        "id": "",
                        "scheme": ""
                    }
                ],
                "quantity": 0.00,
                "unit": {
                    "id": ""
                },
                "description": "",
                "relatedLot": ""
            }
        ],
        "documents": [
            {
                "id": "",
                "title": "",
                "documentType": "",
                "description": "",
                "relatedLots": [
                    ""
                ]
            }
        ]
    }
}
