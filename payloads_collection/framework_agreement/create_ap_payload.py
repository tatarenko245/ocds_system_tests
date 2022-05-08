"""Prepare the expected payloads of the aggregated plan process, framework agreement procedures."""
import copy
import random

from class_collection.document_registration import Document
from data_collection.data_constant import cpv_category_tuple, cpv_goods_high_level_tuple, cpv_works_high_level_tuple, \
    cpv_services_high_level_tuple, currency_tuple, legal_basis_tuple, locality_scheme_tuple, document_type_tuple
from functions_collection.prepare_date import pn_period, contact_period


class AggregatedPlan:
    """This class creates instance of payload."""
    def __init__(self, central_purchasing_body_id, host_to_service, max_duration_of_fa, tender_classification_id=None,
                 currency=None):

        __pn_period = pn_period()
        __contact_period = contact_period(max_duration_of_fa)

        __document_one = Document(host=host_to_service)
        self.__document_one_was_uploaded = __document_one.uploading_document()
        self.__host = host_to_service

        self.__tender_classification_id = tender_classification_id
        if self.__tender_classification_id is None:
            __category = random.choice(cpv_category_tuple)
            if __category == "goods":
                self.__tender_classification_id = random.choice(cpv_goods_high_level_tuple)
            elif __category == "works":
                self.__tender_classification_id = random.choice(cpv_works_high_level_tuple)
            elif __category == "services":
                self.__tender_classification_id = random.choice(cpv_services_high_level_tuple)

        if currency is None:
            currency = f"{random.choice(currency_tuple)}"

        self.__payload = {
            "tender": {
                "title": "create ap: tender.title",
                "description": "create ap: tender.description",
                "legalBasis": f"{random.choice(legal_basis_tuple)}",
                "procurementMethodRationale": "create ap: tender.procurementMethodRationale",
                "classification": {
                    "id": self.__tender_classification_id
                },
                "tenderPeriod": {
                    "startDate": __pn_period
                },
                "procuringEntity": {
                    "name": "create ap: procuringEntity.name",
                    "identifier": {
                        "id": f"{central_purchasing_body_id}",
                        "scheme": "MD-IDNO",
                        "legalName": "create ap: procuringEntity.identifier.legalName",
                        "uri": "create ap: procuringEntity.identifier.uri"
                    },
                    "address": {
                        "streetAddress": "create ap: procuringEntity.address.streetAddress",
                        "postalCode": "create ap: procuringEntity.address.postalCode",
                        "addressDetails": {
                            "country": {
                                "id": "MD"
                            },
                            "region": {
                                "id": "1700000"
                            },
                            "locality": {
                                "scheme": f"{random.choice(locality_scheme_tuple)}",
                                "id": "1701000",
                                "description":
                                    "create ap: tender.procuringEntity.address.addressDetails.locality.description"
                            }
                        }
                    },
                    "additionalIdentifiers": [{
                        "id": "create ap: tender.procuringEntity.additionalIdentifiers.id",
                        "scheme": "create ap: tender.procuringEntity.additionalIdentifiers.scheme",
                        "legalName": "create ap: tender.procuringEntity.additionalIdentifiers.legalName",
                        "uri": "create ap: tender.procuringEntity.additionalIdentifiers.uri"
                    }],
                    "contactPoint": {
                        "name": "create ap: tender.procuringEntity.contactPoint.name",
                        "email": "create ap: tender.procuringEntity.contactPoint.email",
                        "telephone": "create ap: tender.procuringEntity.contactPoint.telephone",
                        "faxNumber": "create ap: tender.procuringEntity.contactPoint.faxNumber",
                        "url": "create ap: tender.procuringEntity.contactPoint.url"
                    }
                },
                "documents": [
                    {
                        "documentType": f"{random.choice(document_type_tuple)}",
                        "id": self.__document_one_was_uploaded[0]["data"]["id"],
                        "title": "create ap: tender.documents.title",
                        "description": "create ap: tender.documents.description"
                    }],
                "contractPeriod": {
                    "startDate": __contact_period[0],
                    "endDate": __contact_period[1]
                },
                "value": {
                    "currency": currency
                }

            }
        }

    def build_payload(self):
        """Build payload."""
        return self.__payload

    def delete_optional_fields(
            self, *args, procuring_entity_additional_identifiers_position=0, document_position=0):
        """Call this method last! Delete option fields from payload."""

        for a in args:
            if a == "tender.procurementMethodRationale":
                del self.__payload['tender']['procurementMethodRationale']

            elif a == "tender.procuringEntity.additionalIdentifiers":
                del self.__payload['tender']['procuringEntity'][
                    'additionalIdentifiers']

            elif a == "tender.procuringEntity.additionalIdentifiers.uri":
                del self.__payload['tender']['procuringEntity'][
                    'additionalIdentifiers'][procuring_entity_additional_identifiers_position]['uri']

            elif a == "tender.procuringEntity.address.postalCode":
                del self.__payload['tender']['procuringEntity']['address']['postalCode']
            elif a == "tender.procuringEntity.contactPoint.faxNumber":
                del self.__payload['tender']['procuringEntity']['contactPoint']['faxNumber']
            elif a == "tender.procuringEntity.contactPoint.url":
                del self.__payload['tender']['procuringEntity']['contactPoint']['url']

            elif a == "tender.documents":
                del self.__payload['tender']['documents']
            elif a == "tender.documents.description":
                del self.__payload['tender']['documents'][document_position]['description']

            else:
                raise KeyError(f"Impossible to delete attribute by path {a}.")

    def customize_tender_procuring_entity_additional_identifiers(
            self, quantity_of_tender_procuring_entity_additional_identifiers):
        """ Customize tender.procuringEntity.additionalIdentifiers array."""

        new_additional_identifiers_array = list()
        for q in range(quantity_of_tender_procuring_entity_additional_identifiers):
            new_additional_identifiers_array.append(
                copy.deepcopy(self.__payload['tender']['procuringEntity']['additionalIdentifiers'][0])
            )

            new_additional_identifiers_array[q]['id'] = \
                f"create fs: tender.procuringEntity.additionalIdentifiers{q}.id"

            new_additional_identifiers_array[q]['scheme'] = \
                f"create fs: tender.procuringEntity.additionalIdentifiers{q}.scheme"

            new_additional_identifiers_array[q]['legalName'] = \
                f"create fs: tender.procuringEntity.additionalIdentifiers{q}.legalName"

            new_additional_identifiers_array[q]['uri'] = \
                f"create fs: tender.procuringEntity.additionalIdentifiers{q}.uri"

        self.__payload['tender']['procuringEntity']['additionalIdentifiers'] = new_additional_identifiers_array

    def customize_tender_documents(self, quantity_of_documents):
        """Customize tender.documents array."""

        new_documents_array = list()
        for q_0 in range(quantity_of_documents):
            new_documents_array.append(copy.deepcopy(self.__payload['tender']['documents'][0]))

            document_two = Document(host=self.__host)
            document_two_was_uploaded = document_two.uploading_document()

            new_documents_array[q_0]['id'] = document_two_was_uploaded[0]["data"]["id"]
            new_documents_array[q_0]['documentType'] = f"{random.choice(document_type_tuple)}"
            new_documents_array[q_0]['title'] = f"create pn: tender.documents{q_0}.title"
            new_documents_array[q_0]['description'] = f"create pn: tender.documents{q_0}.description"

        self.__payload['tender']['documents'] = new_documents_array

    def get_tender_classification_id(self):
        return self.__tender_classification_id

    def __del__(self):
        print(f"The instance of AggregatedPlan class: {__name__} was deleted.")
