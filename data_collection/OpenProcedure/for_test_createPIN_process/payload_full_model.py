import random

from data_collection.data_constant import qualificationSystemMethod_tuple, reductionCriteria_tuple, legal_basis_tuple, \
    awardCriteria_tuple, awardCriteriaDetails_tuple
from functions_collection.prepare_date import pn_period, enquiry_period, old_period

tenderperiod_startdate = pn_period()
enquiryperiod_enddate = enquiry_period(tenderperiod_startdate)

payload_model = {
    "planning": {
        "rationale": "create pin: planning.rationale",
        "budget": {
            "description": "create pin: planning.description",
            "budgetBreakdown": [
                {
                    "id": "create pin: planning.budgetBreakdown[0].id",
                    "amount": {
                        "amount": 1000.00,
                        "currency": "EUR"
                    },
                    "classifications": {
                        "ei": "test-t1s2t3-MD-1657307654765",
                        "fs": "test-t1s2t3-MD-1657307654765-FS-1657307662948"
                    }
                }
            ]
        }
    },
    "tender": {
        "title": "create pin: tender.title",
        "description": "create pin: tender.description",
        "secondStage": {
            "minimumCandidates": 1.00,
            "maximumCandidates": 5.00
        },
        "otherCriteria": {
            "reductionCriteria": f"{random.choice(reductionCriteria_tuple)}" ,
            "qualificationSystemMethods": [f"{random.choice(qualificationSystemMethod_tuple)}"]
        },
        "classification": {
            "id": "45100000-8",
            "scheme": "CPV"
        },
        "legalBasis": f"{random.choice(legal_basis_tuple)}",
        "procurementMethodRationale": "create pin: tender.procurementMethodRationale",
        "awardCriteria": f"{random.choice(awardCriteria_tuple)}",
        "awardCriteriaDetails": f"{random.choice(awardCriteriaDetails_tuple)}",
        "tenderPeriod": {
            "startDate": tenderperiod_startdate
        },
        "enquiryPeriod": {
            "endDate": enquiryperiod_enddate
        },
        "procurementMethodModalities": ["electronicAuction"],
        "electronicAuctions": {
            "details": [
                {
                    "id": "create pin: tender.electronicAuctions.details[0].id",
                    "relatedLot": "create pin: tender.electronicAuctions.details[0].relatedLot",
                    "electronicAuctionModalities": [
                        {
                            "eligibleMinimumDifference": {
                                "amount": 10.00,
                                "currency": "EUR"
                            }
                        }
                    ]
                }
            ]
        },
        "procuringEntity": {
            "name": "create pin: procuringEntity.name",
            "identifier": {
                "id": "create pin: procuringEntity.identifier.id",
                "legalName": "create pin: procuringEntity.identifier.legalName",
                "scheme": "create pin: procuringEntity.identifier.scheme",
                "uri": "create pin: procuringEntity.identifier.uri"
            },
            "additionalIdentifiers": [
                {
                    "id": "create pin: procuringEntity.additionalIdentifiers[0].id",
                    "legalName": "create pin: procuringEntity.additionalIdentifiers[0].legalName",
                    "scheme": "create pin: procuringEntity.additionalIdentifiers[0].scheme",
                    "uri": "create pin: procuringEntity.additionalIdentifiers[0].uri"
                }
            ],
            "address": {
                "streetAddress": "create pin: procuringEntity.address.streetAddress",
                "postalCode": "create pin: procuringEntity.address.postalCode",
                "addressDetails": {
                    "country": {
                            "id": "MD",
                            "description": "create pin: tender.procuringEntity.address.addressDetails.country."
                                           "description",
                            "scheme": "ISO-ALPHA2"
                        },
                    "region": {
                        "id": "2500000",
                        "description": "create pin: tender.procuringEntity.address.addressDetails.region.description",
                        "scheme": "CUATM"
                    },
                    "locality": {
                        "id": "2501000",
                        "description": "create pin: tender.procuringEntity.address.addressDetails.locality.description",
                        "scheme": "create pin: tender.procuringEntity.address.addressDetails.locality.scheme"
                    }
                }
            },
            "contactPoint": {
                "name": "create pin: procuringEntity.contactPoint.name",
                "email": "create pin: procuringEntity.contactPoint.email",
                "telephone": "create pin: procuringEntity.contactPoint.telephone",
                "faxNumber": "create pin: procuringEntity.contactPoint.faxNumber",
                "url": "create pin: procuringEntity.contactPoint.url"
            },
            "persones": [
                {
                    "title": "create pin: procuringEntity.persones[0].title",
                    "name": "create pin: procuringEntity.persones[0].name",
                    "identifier": {
                        "scheme": "create pin: procuringEntity.persones[0].identifier.scheme",
                        "id": "create pin: procuringEntity.persones[0].identifier.id",
                        "uri": "create pin: procuringEntity.persones[0].identifier.uri"
                    },
                    "businessFunctions": [
                        {
                            "id": "create pin: procuringEntity.persones[0].businessFunctions[0].id",
                            "type": "create pin: procuringEntity.persones[0].businessFunctions[0].type",
                            "jobTitle": "create pin: procuringEntity.persones[0].businessFunctions[0].jobTitle",
                            "period": {
                                "startDate": old_period()[0]
                            },
                            "documents": [
                                {
                                    "id": "create pin: procuringEntity.persones[0].businessFunctions[0].documents[0]."
                                          "startDate",
                                    "title": "create pin: procuringEntity.persones[0].businessFunctions[0]."
                                             "documents[0].title",
                                    "documentType": "regulatoryDocument",
                                    "description": "create pin: procuringEntity.persones[0].businessFunctions[0]."
                                             "documents[0].description"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "criteria": [
            {
                "id": "create pin: tender.criteria[0].id",
                "title": "create pin: tender.criteria[0].title",
                "classification": {
                    "id": "create pin: tender.criteria[0].classification.id",
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
