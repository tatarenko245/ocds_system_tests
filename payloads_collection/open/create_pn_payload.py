"""Prepare the expected payloads of the planning notice process, open procedures."""
import copy
import random

from class_collection.document_registration import Document
from data_collection.OpenProcedure.for_test_createPN_process.payload_full_model import payload_model
from data_collection.data_constant import legal_basis_tuple, documentType_tuple, unit_id_tuple, cpvs_tuple
from functions_collection.prepare_date import pn_period, contact_period
from functions_collection.some_functions import generate_items_array, generate_lots_array, get_affordable_schemes


class PlanningNoticePayload:
    """This class creates instance of payload."""

    def __init__(self, country: str, amount: float, currency: str, procuringentity_id: str):

        self.country = country
        self.amount = amount
        self.currency = currency

        self.affordable_schemes = get_affordable_schemes(self.country)
        self.payload = copy.deepcopy(payload_model)

        self.payload['planning']['rationale'] = "create pn: planning.rationale"
        self.payload['planning']['budget']['description'] = "create pn: planning.description.description"

        self.payload['tender']['title'] = "create pn: tender.title"
        self.payload['tender']['description'] = "create pn: tender.description"
        self.payload['tender']['legalBasis'] = f"{random.choice(legal_basis_tuple)}"
        self.payload['tender']['procurementMethodRationale'] = "create pn: tender.procurementMethodRationale"
        self.payload['tender']['procurementMethodAdditionalInfo'] = "create pn: tender.procurementMethodAdditionalInfo"
        self.payload['tender']['tenderPeriod']['startDate'] = pn_period()
        self.payload['tender']['procuringEntity']['name'] = "create pn: tender.procuringEntity.name"
        self.payload['tender']['procuringEntity']['identifier']['id'] = procuringentity_id
        self.payload['tender']['procuringEntity']['identifier']['scheme'] = self.affordable_schemes[0]

        self.payload['tender']['procuringEntity']['identifier']['legalName'] = \
            "create pn: tender.procuringEntity.identifier.legalName"

        self.payload['tender']['procuringEntity']['identifier']['uri'] = \
            "create pn: tender.procuringEntity.identifier.uri"

        self.payload['tender']['procuringEntity']['address']['streetAddress'] = \
            "create pn: tender.procuringEntity.address.streetAddress"

        self.payload['tender']['procuringEntity']['address']['postalCode'] = \
            "create pn: tender.procuringEntity.address.postalCode"

        self.payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = country
        self.payload['tender']['procuringEntity']['address']['addressDetails']['country']['scheme'] = \
            self.affordable_schemes[1]

        self.payload['tender']['procuringEntity']['address']['addressDetails']['country']['description'] = \
            "create pn: tender.procuringEntity.address.addressDetails.country.description"

        self.payload['tender']['procuringEntity']['address']['addressDetails']['region']['scheme'] = \
            self.affordable_schemes[2]

        self.payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = \
            self.affordable_schemes[3]

        self.payload['tender']['procuringEntity']['address']['addressDetails']['region']['description'] = \
            "create pn: tender.procuringEntity.address.addressDetails.region.description"

        self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = \
            self.affordable_schemes[4]

        self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = \
            self.affordable_schemes[5]

        self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['description'] = \
            "create pn: tender.procuringEntity.address.addressDetails.locality.description"

        self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['uri'] = \
            "create pn: tender.procuringEntity.address.addressDetails.locality.uri"

        self.payload['tender']['procuringEntity']['contactPoint']['name'] = \
            "create pn: tender.procuringEntity.contactPoint.name"

        self.payload['tender']['procuringEntity']['contactPoint']['email'] = \
            "create pn: tender.procuringEntity.contactPoint.email"

        self.payload['tender']['procuringEntity']['contactPoint']['telephone'] = \
            "create pn: tender.procuringEntity.contactPoint.telephone"

        self.payload['tender']['procuringEntity']['contactPoint']['faxNumber'] = \
            "create pn: tender.procuringEntity.contactPoint.faxNumber"

        self.payload['tender']['procuringEntity']['contactPoint']['url'] = \
            "create pn: tender.procuringEntity.contactPoint.url"

    def build_payload(self):
        """Build payload."""

        return self.payload

    def delete_optional_fields(
            self, *args, lot_position: int = 0, item_position: int = 0, additional_classification_position: int = 0,
            document_position: int = 0, pe_additional_identifiers_position: int = 0):
        """Call this method last! Delete option fields from payload."""

        for a in args:
            if a == "planning.rationale":
                del self.payload['planning']['rationale']
            elif a == "planning.budget.description":
                del self.payload['planning']['budget']['description']

            elif a == "tender.procurementMethodRationale":
                del self.payload['tender']['procurementMethodRationale']
            elif a == "tender.procurementMethodAdditionalInfo":
                del self.payload['tender']['procurementMethodAdditionalInfo']

            elif a == "tender.procuringEntity.identifier.uri":
                del self.payload['tender']['procuringEntity']['identifier']['uri']
            elif a == "tender.procuringEntity.additionalIdentifiers":
                del self.payload['tender']['procuringEntity']['additionalIdentifiers']
            elif a == "tender.procuringEntity.additionalIdentifiers.uri":
                del self.payload['tender']['procuringEntity']['additionalIdentifiers'][
                    pe_additional_identifiers_position]['uri']
            elif a == "tender.procuringEntity.address.postalCode":
                del self.payload['tender']['procuringEntity']['address']['postalCode']

            elif a == "tender.lots":
                del self.payload['tender']['lots']
            elif a == "tender.lots.internalId":
                del self.payload['tender']['lots'][lot_position]['internalId']
            elif a == "tender.lots.placeOfPerformance.address.postalCode":
                del self.payload['tender']['lots'][lot_position]['placeOfPerformance']['address']['postalCode']
            elif a == "tender.lots.placeOfPerformance.description":
                del self.payload['tender']['lots'][lot_position]['placeOfPerformance']['description']

            elif a == "tender.items":
                del self.payload['tender']['items']
            elif a == "tender.items.internalId":
                del self.payload['tender']['items'][item_position]['internalId']
            elif a == "tender.items.additionalClassifications":
                del self.payload['tender']['items'][item_position]['additionalClassifications']
            elif a == f"tender.items.additionalClassifications[{additional_classification_position}]":

                del self.payload['tender']['items'][item_position][
                    'additionalClassifications'][additional_classification_position]
            elif a == "tender.documents":
                del self.payload['tender']['documents']
            elif a == "tender.documents.description":
                del self.payload['tender']['documents'][document_position]['description']
            elif a == "tender.documents.relatedLots":
                del self.payload['tender']['documents'][document_position]["relatedLots"]
            else:
                KeyError(f"Impossible to delete attribute by path {a}.")

    def get_lots_id_from_payload(self):
        """Get lots.id from payload."""

        lot_id_list = list()
        for q in range(len(self.payload['tender']['lots'])):
            lot_id_list.append(self.payload['tender']['lots'][q]['id'])
        return lot_id_list

    def customize_planning_budget_budget_breakdown(self, list_of_fs_id: list):
        """Customize planning.budget.budgetBreakdown array."""

        new_budget_breakdown_array = list()
        for q in range(len(list_of_fs_id)):
            new_budget_breakdown_array.append(copy.deepcopy(self.payload['planning']['budget']['budgetBreakdown'][0]))
            new_budget_breakdown_array[q]['id'] = list_of_fs_id[q]

            new_budget_breakdown_array[q]['amount']['amount'] = round(self.amount / len(list_of_fs_id), 2)

            new_budget_breakdown_array[q]['amount']['currency'] = self.currency

        self.payload['planning']['budget']['budgetBreakdown'] = new_budget_breakdown_array

    def customize_tender_items(self, tender_classification_id: str, lot_id_list: list, quantity_of_items: int,
                               quantity_of_items_additional_classifications: int):
        """
        The max quantity of items must be 5, because it depends on cpvs_tuple from data_of_enum.
        The quantity of lot_id_list must be equal the quantity_of_items.
        """
        new_items_array = generate_items_array(
            quantity_of_object=quantity_of_items,
            item_object=copy.deepcopy(self.payload['tender']['items'][0]),
            tender_classification_id=tender_classification_id
        )

        for q_0 in range(quantity_of_items):

            new_items_array[q_0]['classification']['scheme'] = "CPV"
            new_items_array[q_0]['internalId'] = f"create pn: tender.items{q_0}.internalId"
            new_items_array[q_0]['description'] = f"create pn: tender.items{q_0}.description"
            new_items_array[q_0]['unit']['id'] = f"{random.choice(unit_id_tuple)}"
            new_items_array[q_0]['quantity'] = f"{100.01+q_0}"
            del new_items_array[q_0]['additionalClassifications'][0]

            list_of_additional_classification_id = list()
            for q_1 in range(quantity_of_items_additional_classifications):
                new_items_array[q_0]['additionalClassifications'].append(
                    copy.deepcopy(self.payload['tender']['items'][0]['additionalClassifications'][0]))

                while len(list_of_additional_classification_id) < quantity_of_items_additional_classifications:
                    additional_classification_id = f"{random.choice(cpvs_tuple)}"
                    if additional_classification_id not in list_of_additional_classification_id:
                        list_of_additional_classification_id.append(additional_classification_id)

            for q_1 in range(quantity_of_items_additional_classifications):
                new_items_array[q_0]['additionalClassifications'][q_1]['id'] = \
                    list_of_additional_classification_id[q_1]

                new_items_array[q_0]['additionalClassifications'][q_1]['scheme'] = "CPVS"

            new_items_array[q_0]['relatedLot'] = lot_id_list[q_0]

        self.payload['tender']['items'] = new_items_array

    def customize_tender_lots(self, quantity_of_lots: int):
        """Customize tender.lots array."""

        new_lots_array = generate_lots_array(
            quantity_of_object=quantity_of_lots,
            lot_object=copy.deepcopy(self.payload['tender']['lots'][0])
        )
        for q_0 in range(quantity_of_lots):
            new_lots_array[q_0]['internalId'] = f"create pn: tender.lots{q_0}.internalId"
            new_lots_array[q_0]['title'] = f"create pn: tender.lotss{q_0}.title"
            new_lots_array[q_0]['description'] = f"create pn: tender.lots{q_0}.description"
            new_lots_array[q_0]['value']['amount'] = round(self.amount / quantity_of_lots, 2)
            new_lots_array[q_0]['value']['currency'] = self.currency

            lot_contact_period = contact_period()
            new_lots_array[q_0]['contractPeriod']['startDate'] = lot_contact_period[0]
            new_lots_array[q_0]['contractPeriod']['endDate'] = lot_contact_period[1]

            new_lots_array[q_0]['placeOfPerformance']['address']['streetAddress'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.address.streetAddress"

            new_lots_array[q_0]['placeOfPerformance']['address']['postalCode'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.address.postalCode"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['country']['id'] = self.country
            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['country']['scheme'] = \
                self.affordable_schemes[1]

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['country']['description'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.address.addressDetails.country.description"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['region']['scheme'] = \
                self.affordable_schemes[2]

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['region']['id'] = \
                self.affordable_schemes[3]

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['region']['description'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.address.addressDetails.region.description"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['scheme'] = \
                self.affordable_schemes[4]

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['id'] = \
                self.affordable_schemes[5]

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['description'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.address.addressDetails.locality.description"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['uri'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.address.addressDetails.locality.uri"

            new_lots_array[q_0]['placeOfPerformance']['description'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.description"

        self.payload['tender']['lots'] = new_lots_array

    def customize_tender_documents(self, host: str, lot_id_list: list, quantity_of_documents: int):
        """
        The quantity of lot_id_list must be equal the quantity_of_documents.
        """
        new_documents_array = list()
        for q_0 in range(quantity_of_documents):
            new_documents_array.append(copy.deepcopy(self.payload['tender']['documents'][0]))

            document_two = Document(host)
            document_two_was_uploaded = document_two.uploading_document()

            new_documents_array[q_0]['id'] = document_two_was_uploaded[0]["data"]["id"]
            new_documents_array[q_0]['documentType'] = f"{random.choice(documentType_tuple)}"
            new_documents_array[q_0]['title'] = f"create pn: tender.documents{q_0}.title"
            new_documents_array[q_0]['description'] = f"create pn: tender.documents{q_0}.description"

            new_documents_array[q_0]['relatedLots'] = [lot_id_list[q_0]]

        self.payload['tender']['documents'] = new_documents_array

    def customize_tender_procuring_entity_additional_identifiers(
            self, quantity_of_tender_procuring_entity_additional_identifiers: int):
        """ Customize tender.procuringEntity.additionalIdentifiers array."""

        new_additional_identifiers_array = list()
        for q in range(quantity_of_tender_procuring_entity_additional_identifiers):
            new_additional_identifiers_array.append(
                copy.deepcopy(self.payload['tender']['procuringEntity']['additionalIdentifiers'][0])
            )

            new_additional_identifiers_array[q]['id'] = \
                f"create pn: tender.procuringEntity.additionalIdentifiers{q}.id"

            new_additional_identifiers_array[q]['scheme'] = \
                f"create pn: tender.procuringEntity.additionalIdentifiers{q}.scheme"

            new_additional_identifiers_array[q]['legalName'] = \
                f"create pn: tender.procuringEntity.additionalIdentifiers{q}.legalName"

            new_additional_identifiers_array[q]['uri'] = \
                f"create pn: tender.procuringEntity.additionalIdentifiers{q}.uri"

        self.payload['tender']['procuringEntity']['additionalIdentifiers'] = new_additional_identifiers_array

    def __del__(self):
        print(f"The instance of PlanPayload class: {__name__} was deleted.")
