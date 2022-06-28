payload_model = {
    "planning": {
        "rationale": "update ei: planning.rationale",
        "budget": {
            "amount": {
                "amount": 900.00
            }
        }
    },
    "tender": {
        "title": "update ei: tender.title",
        "description": "update ei: tender.description",
        "items": [
            {
                "id": f"update ei: tender.items[{0}].id",
                "description": f"update ei: tender.items[{0}].description",
                "classification": {
                    "id": f"update ei: tender.items[{0}].classification.id",
                    "scheme": "CPV"
                },
                "additionalClassifications": [
                    {
                        "id": f"update ei: tender.items[{0}].additionalClassifications[{0}].id",
                        "scheme": "CPVS"
                    }
                ],
                "quantity": 20.0,
                "unit": "19",
                "deliveryAddress": {
                    "streetAddress": f"update ei: tender.items[{0}].deliveryAddress.streetAddress",
                    "postalCode": f"update ei: tender.items[{0}].deliveryAddress.postalCode",
                    "addressDetails": {
                        "country": {
                            "id": "MD",
                            "description": f"update ei: tender.items[{0}].deliveryAddress.addressDetails.country."
                                           "description",
                            "scheme": "ISO-ALPHA2"
                        },
                        "region": {
                            "id": "2500000",
                            "description": f"update ei: tender.items[{0}].deliveryAddress.addressDetails.region."
                                           "description",
                            "scheme": "CUATM"
                        },
                        "locality": {
                            "id": "2501000",
                            "description": f"update ei: tender.items[{0}].deliveryAddress.addressDetails.locality."
                                           "description",
                            "scheme": "CUATM",
                            "uri": f"update ei: tender.items[{0}].deliveryAddress.addressDetails.locality.uri"
                        }
                    }
                }
            }
        ]
    }
}
