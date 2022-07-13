"""This is full release data model for PIN release."""

release_model = {
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
                "secondStage": {
                    "minimumCandidates": 0.00,
                    "maximumCandidates": 0.00
                },
                "otherCriteria": {
                    "reductionCriteria": "",
                    "qualificationSystemMethods": [""]
                },
                "classification": {
                    "scheme": "",
                    "id": "",
                    "description": ""
                },
                "awardCriteria": "",
                "awardCriteriaDetails": "",
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
                        }
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
                "procurementMethodModalities": [""],
                "hasEnquiries": False,
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
                                        "status": "",
                                        "datePublished": "",
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
