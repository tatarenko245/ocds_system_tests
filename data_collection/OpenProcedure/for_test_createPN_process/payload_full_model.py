payload_model = {
    "planning": {
        "rationale": "create pn: planning.rationale",
        "budget": {
            "description": "create pn: planning.description.description",
            "budgetBreakdown": [
                {
                    "id": fs_id,
                    "amount": {
                        "amount": amount,
                        "currency": currency
                    }
                }
            ]
        }
    },
    "tender": {
        "title": "create pn: tender.title",
        "description": "create pn: tender.description",
        "legalBasis": f"{random.choice(legal_basis_tuple)}",
        "procurementMethodRationale": "create pn: tender.procurementMethodRationale",
        "procurementMethodAdditionalInfo": "create pn: tender.procurementMethodAdditionalInfo",
        "tenderPeriod":
            {
                "startDate": __pn_period
            },
        "procuringEntity": {
            "name": "create pn: tender.procuringEntity.name",
            "identifier": {
                "id": "create pn: tender.procuringEntity.identifier.id",
                "scheme": "MD-IDNO",
                "legalName": "create pn: tender.procuringEntity.identifier.legalName",
                "uri": "create pn: tender.procuringEntity.identifier.uri",
            },
            "address": {
                "streetAddress": "create pn: tender.procuringEntity.address.streetAddress",
                "postalCode": "create pn: tender.procuringEntity.address.postalCode",
                "addressDetails": {
                    "country": {
                        "id": "MD"
                    },
                    "region": {
                        "id": region_id,
                    },
                    "locality": {
                        "scheme": f"{random.choice(locality_scheme_tuple)}",
                        "id": locality_id,
                        "description": "create pn: tender.procuringEntity.address.addressDetails.description"
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
                "name": "create pn: tender.procuringEntity.contactPoint.name",
                "email": "create pn: tender.procuringEntity.contactPoint.email",
                "telephone": "create pn: tender.procuringEntity.contactPoint.telephone",
                "faxNumber": "create pn: tender.procuringEntity.contactPoint.faxNumber",
                "url": "create pn: tender.procuringEntity.contactPoint.url",
            }},
        "lots": [
            {
                "id": "0",
                "internalId": "create pn: tender.lots0.internalId",
                "title": "create pn: tender.lots0.title",
                "description": "create pn: tender.lots0.description",
                "value": {
                    "amount": amount,
                    "currency": currency
                },
                "contractPeriod": {
                    "startDate": __contact_period[0],
                    "endDate": __contact_period[1]
                },
                "placeOfPerformance": {
                    "address": {
                        "streetAddress": "create pn: tender.lots0.deliveryAddress.streetAddress",
                        "postalCode": "create ei: tender.lots0.deliveryAddress.postalCode",
                        "addressDetails": {
                            "country": {
                                "id": "MD"
                            },
                            "region": {
                                "id": "3400000"
                            },
                            "locality": {
                                "id": "3401000",
                                "description":
                                    "create ei: tender.lots0.deliveryAddress.addressDetails.locality.uri",
                                "scheme": f"{random.choice(locality_scheme_tuple)}",
                                "uri": "create ei: tender.lots0.deliveryAddress.addressDetails.locality.uri"
                            }
                        }
                    },
                    "description": "create pn: tender.lots0.placeOfPerformance.description"
                }
            }],
        "items": [
            {
                "id": "0",
                "internalId": "create pn: tender.items0.internalId",
                "classification": {
                    "id": item_classification_id
                },
                "additionalClassifications": [
                    {
                        "id": "AA12-4"
                    }
                ],
                "quantity": "10.989",
                "unit": {
                    "id": "10"
                },
                "description": "create ei: tender.items0.description",
                "relatedLot": "0"
            }],
        "documents": [
            {
                "documentType": f"{random.choice(documentType_tuple)}",
                "id": self.__document_one_was_uploaded[0]["data"]["id"],
                "title": "create pn: tender.documents.title",
                "description": "create pn: tender.documents.description",
                "relatedLots": ["0"]
            }]
    }
}
