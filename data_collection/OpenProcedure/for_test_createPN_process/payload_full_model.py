"""This is payload full data model for Create PN process."""

payload_model = {
    "planning": {
        "rationale": "",
        "budget": {
            "description": "",
            "budgetBreakdown": [
                {
                    "id": "",
                    "amount": {
                        "amount": "",
                        "currency": ""
                    }
                }
            ]
        }
    },
    "tender": {
        "title": "",
        "description": "",
        "legalBasis": "",
        "procurementMethodRationale": "",
        "procurementMethodAdditionalInfo": "",
        "tenderPeriod":
            {
                "startDate": ""
            },
        "procuringEntity": {
            "name": "",
            "identifier": {
                "id": "",
                "scheme": "",
                "legalName": "",
                "uri": "",
            },
            "address": {
                "streetAddress": "",
                "postalCode": "",
                "addressDetails": {
                    "country": {
                        "scheme": "",
                        "id": "",
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
                        "description": "",
                        "uri": ""
                    }
                }
            },
            "additionalIdentifiers": [
                {
                    "id": "",
                    "legalName": "",
                    "scheme": "",
                    "uri": ""
                }
            ],
            "contactPoint": {
                "name": "",
                "email": "",
                "telephone": "",
                "faxNumber": "",
                "url": "",
            }},
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
                                "scheme": "",
                                "id": "",
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
                                "description": "",
                                "uri": ""
                            }
                        }
                    },
                    "description": ""
                }
            }],
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
                "quantity": "",
                "unit": {
                    "id": ""
                },
                "description": "",
                "relatedLot": ""
            }],
        "documents": [
            {
                "documentType": "",
                "id": "",
                "title": "",
                "description": "",
                "relatedLots": [""]
            }]
    }
}
