payload_model = {
    "tender": {
        "title": "create ei: tender.title",
        "description": "create ei: tender.description",
        "classification": {
            "id": "45100000-8",
            "scheme": "CPV"
        },
        "items": [
            {
                "id": f"create ei: tender.items[{0}].id",
                "description": f"create ei: tender.items[{0}].description",
                "classification": {
                    "id": "45112420-5",
                    "scheme": "CPV"
                },
                "additionalClassifications": [
                    {
                        "id": "AA01-1",
                        "scheme": "CPVS"
                    }
                ],
                "deliveryAddress": {
                    "streetAddress": f"create ei: tender.items[{0}].deliveryAddress.streetAddress",
                    "postalCode": f"create ei: tender.items[{0}].deliveryAddress.postalCode",
                    "addressDetails": {
                        "country": {
                            "id": "MD",
                            "description": f"create ei: tender.items[{0}].deliveryAddress.addressDetails.country."
                                           "description",
                            "scheme": "ISO-ALPHA2"
                        },
                        "region": {
                            "id": "2500000",
                            "description": f"create ei: tender.items[{0}].deliveryAddress.addressDetails.region."
                                           "description",
                            "scheme": "CUATM"
                        },
                        "locality": {
                            "id": "2501000",
                            "description": f"create ei: tender.items[{0}].deliveryAddress.addressDetails.locality."
                                           "description",
                            "scheme": "CUATM",
                            "uri": f"create ei: tender.items[{0}].deliveryAddress.addressDetails.locality.uri"
                        }
                    }
                },
                "quantity": 10.0,
                "unit": {
                    "id": "18"
                }
            }
        ]
    },
    "planning": {
        "budget": {
            "period": {
                "startDate": "2022-06-23T15:05:41Z",
                "endDate": "2022-09-21T15:05:41Z"
            },
            "amount": {
                "amount": 1000.00,
                "currency": "EUR"
            }
        },
        "rationale": "create ei: planning.rationale"
    },
    "buyer": {
        "name": "create ei: buyer.name",
        "identifier": {
            "id": "0",
            "scheme": "MD-IDNO",
            "legalName": "create ei: buyer.identifier.legalName",
            "uri": "create ei: buyer.identifier.uri"
        },
        "address": {
            "streetAddress": "create ei: buyer.address.streetAddress",
            "postalCode": "create ei: buyer.address.postalCode",
            "addressDetails": {
                "country": {
                    "id": "MD",
                    "description": "create ei: buyer.address.addressDetails.country.description",
                    "scheme": "ISO-ALPHA2"
                },
                "region": {
                    "id": "1700000",
                    "description": "create ei: buyer.address.addressDetails.region.description",
                    "scheme": "CUATM"
                },
                "locality": {
                    "scheme": "CUATM",
                    "id": "1701000",
                    "description": "create ei: buyer.address.addressDetails.locality.description",
                    "uri": "create ei: buyer.address.addressDetails.locality.uri"
                }
            }
        },
        "additionalIdentifiers": [
            {
                "id": "create ei buyer.additionalIdentifiers0.id",
                "scheme": "create ei buyer.additionalIdentifiers0.scheme",
                "legalName": "create ei buyer.additionalIdentifiers0.legalName",
                "uri": "create ei buyer.additionalIdentifiers0.uri"
            }
        ],
        "contactPoint": {
            "name": "create ei: buyer.contactPoint.name",
            "email": "create ei: buyer.contactPoint.email",
            "telephone": "create ei: buyer.contactPoint.telephone",
            "faxNumber": "create ei: buyer.contactPoint.faxNumber",
            "url": "create ei: buyer.contactPoint.url"
        },
        "details": {
            "typeOfBuyer": "REGIONAL_AUTHORITY",
            "mainGeneralActivity": "EDUCATION",
            "mainSectoralActivity": "EXPLORATION_EXTRACTION_GAS_OIL"
        }
    }
}
