"""Prepare the expected payloads of the planning notice process, framework agreement procedures."""
import copy
import random

from class_collection.document_registration import Document
from data_collection.data_constant import cpv_goods_low_level_03_tuple, cpv_goods_low_level_1_tuple, \
    cpv_goods_low_level_2_tuple, cpv_goods_low_level_3_tuple, cpv_goods_low_level_44_tuple, \
    cpv_goods_low_level_48_tuple, cpv_works_low_level_45_tuple, cpv_services_low_level_5_tuple, \
    cpv_services_low_level_6_tuple, cpv_services_low_level_7_tuple, cpv_services_low_level_8_tuple, \
    cpv_services_low_level_92_tuple, cpv_services_low_level_98_tuple, legal_basis_tuple, locality_scheme_tuple, \
    documentType_tuple, unit_id_tuple, cpvs_tuple, region_id_tuple
from functions_collection.prepare_date import pn_period, contact_period
from functions_collection.some_functions import generate_items_array, generate_lots_array, \
    get_locality_id_according_with_region_id


class PlanningNoticePayload:
    """This class creates instance of payload."""

    def __init__(self, fs_id, amount, currency, tender_classification_id, host_to_service):

        __pn_period = pn_period()
        __contact_period = contact_period()

        __document_one = Document(host=host_to_service)
        self.__document_one_was_uploaded = __document_one.uploading_document()

        self.__amount = amount
        self.__currency = currency
        self.__tender_classification_id = tender_classification_id
        self.__host = host_to_service
        item_classification_id = None
        try:
            if tender_classification_id[0:3] == "031":
                item_classification_id = random.choice(cpv_goods_low_level_03_tuple)
            elif tender_classification_id[0:3] == "146":
                item_classification_id = random.choice(cpv_goods_low_level_1_tuple)
            elif tender_classification_id[0:3] == "221":
                item_classification_id = random.choice(cpv_goods_low_level_2_tuple)
            elif tender_classification_id[0:3] == "301":
                item_classification_id = random.choice(cpv_goods_low_level_3_tuple)
            elif tender_classification_id[0:3] == "444":
                item_classification_id = random.choice(cpv_goods_low_level_44_tuple)
            elif tender_classification_id[0:3] == "482":
                item_classification_id = random.choice(cpv_goods_low_level_48_tuple)
            elif tender_classification_id[0:3] == "451":
                item_classification_id = random.choice(cpv_works_low_level_45_tuple)
            elif tender_classification_id[0:3] == "515":
                item_classification_id = random.choice(cpv_services_low_level_5_tuple)
            elif tender_classification_id[0:3] == "637":
                item_classification_id = random.choice(cpv_services_low_level_6_tuple)
            elif tender_classification_id[0:3] == "713":
                item_classification_id = random.choice(cpv_services_low_level_7_tuple)
            elif tender_classification_id[0:3] == "851":
                item_classification_id = random.choice(cpv_services_low_level_8_tuple)
            elif tender_classification_id[0:3] == "923":
                item_classification_id = random.choice(cpv_services_low_level_92_tuple)
            elif tender_classification_id[0:3] == "983":
                item_classification_id = random.choice(cpv_services_low_level_98_tuple)
        except ValueError:
            ValueError("Check tender_classification_id")

        self.__payload = {
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

    def build_payload(self):
        """Build payload."""
        return self.__payload

    def delete_optional_fields(
            self, *args, lot_position=0, item_position=0, additional_classification_position=0, document_position=0):
        """Call this method last! Delete option fields from payload."""

        for a in args:
            if a == "planning.rationale":
                del self.__payload['planning']['rationale']
            elif a == "planning.budget.description":
                del self.__payload['planning']['budget']['description']

            elif a == "tender.procurementMethodRationale":
                del self.__payload['tender']['procurementMethodRationale']
            elif a == "tender.procurementMethodAdditionalInfo":
                del self.__payload['tender']['procurementMethodAdditionalInfo']

            elif a == "tender.lots":
                del self.__payload['tender']['lots']
            elif a == "tender.lots.internalId":
                del self.__payload['tender']['lots'][lot_position]['internalId']
            elif a == "tender.lots.placeOfPerformance.address.postalCode":
                del self.__payload['tender']['lots'][lot_position]['placeOfPerformance']['address']['postalCode']
            elif a == "tender.lots.placeOfPerformance.description":
                del self.__payload['tender']['lots'][lot_position]['placeOfPerformance']['description']

            elif a == "tender.items":
                del self.__payload['tender']['items']
            elif a == "tender.items.internalId":
                del self.__payload['tender']['items'][item_position]['internalId']
            elif a == "tender.items.additionalClassifications":
                del self.__payload['tender']['items'][item_position]['additionalClassifications']
            elif a == f"tender.items.additionalClassifications[{additional_classification_position}]":

                del self.__payload['tender']['items'][item_position][
                    'additionalClassifications'][additional_classification_position]
            elif a == "tender.documents":
                del self.__payload['tender']['documents']
            elif a == "tender.documents.description":
                del self.__payload['tender']['documents'][document_position]['description']
            elif a == "tender.documents.relatedLots":
                del self.__payload['tender']['documents'][document_position]["relatedLots"]
            else:
                KeyError(f"Impossible to delete attribute by path {a}.")

    def get_lots_id_from_payload(self):
        """Get lots.id from payload."""

        lot_id_list = list()
        for q in range(len(self.__payload['tender']['lots'])):
            lot_id_list.append(self.__payload['tender']['lots'][q]['id'])
        return lot_id_list

    def customize_planning_budget_budget_breakdown(self, list_of_fs_id):
        """Customize planning.budget.budgetBreakdown array."""

        new_budget_breakdown_array = list()
        for q in range(len(list_of_fs_id)):
            new_budget_breakdown_array.append(copy.deepcopy(self.__payload['planning']['budget']['budgetBreakdown'][0]))
            new_budget_breakdown_array[q]['id'] = list_of_fs_id[q]

            new_budget_breakdown_array[q]['amount']['amount'] = round(self.__amount / len(list_of_fs_id), 2)

            new_budget_breakdown_array[q]['amount']['currency'] = self.__currency

        self.__payload['planning']['budget']['budgetBreakdown'] = new_budget_breakdown_array

    def customize_tender_items(self, lot_id_list, quantity_of_items, quantity_of_items_additional_classifications):
        """
        The max quantity of items must be 5, because it depends on cpvs_tuple from data_of_enum.
        The quantity of lot_id_list must be equal the quantity_of_items.
        """
        new_items_array = generate_items_array(
            quantity_of_object=quantity_of_items,
            item_object=copy.deepcopy(self.__payload['tender']['items'][0]),
            tender_classification_id=self.__tender_classification_id
        )

        for q_0 in range(quantity_of_items):

            new_items_array[q_0]['internalId'] = f"create pn: tender.items{q_0}.internalId"
            new_items_array[q_0]['description'] = f"create pn: tender.items{q_0}.description"
            new_items_array[q_0]['unit']['id'] = f"{random.choice(unit_id_tuple)}"

            list_of_additional_classification_id = list()
            for q_1 in range(quantity_of_items_additional_classifications):
                new_items_array[q_0]['additionalClassifications'].append(
                    copy.deepcopy(self.__payload['tender']['items'][0]['additionalClassifications'][0]))

                while len(list_of_additional_classification_id) < quantity_of_items_additional_classifications:
                    additional_classification_id = f"{random.choice(cpvs_tuple)}"
                    if additional_classification_id not in list_of_additional_classification_id:
                        list_of_additional_classification_id.append(additional_classification_id)

            for q_1 in range(quantity_of_items_additional_classifications):

                new_items_array[q_0]['additionalClassifications'][q_1]['id'] = \
                    list_of_additional_classification_id[q_1]

            new_items_array[q_0]['relatedLot'] = lot_id_list[q_0]

        self.__payload['tender']['items'] = new_items_array

    def customize_tender_lots(self, quantity_of_lots):
        """Customize tender.lots array."""

        new_lots_array = generate_lots_array(
            quantity_of_object=quantity_of_lots,
            lot_object=copy.deepcopy(self.__payload['tender']['lots'][0])
        )
        for q_0 in range(quantity_of_lots):

            new_lots_array[q_0]['internalId'] = f"create pn: tender.lots{q_0}.internalId"
            new_lots_array[q_0]['title'] = f"create pn: tender.lotss{q_0}.title"
            new_lots_array[q_0]['description'] = f"create pn: tender.lots{q_0}.description"
            new_lots_array[q_0]['value']['amount'] = round(self.__amount / quantity_of_lots, 2)
            new_lots_array[q_0]['value']['currency'] = self.__currency

            __contact_period = contact_period()
            new_lots_array[q_0]['contractPeriod']['startDate'] = __contact_period[0]
            new_lots_array[q_0]['contractPeriod']['endDate'] = __contact_period[1]

            new_lots_array[q_0]['placeOfPerformance']['streetAddress'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.streetAddress"

            new_lots_array[q_0]['placeOfPerformance']['postalCode'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.postalCode"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['region']['id'] = \
                f"{random.choice(region_id_tuple)}"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['id'] = \
                get_locality_id_according_with_region_id(
                    new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['region']['id'])

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['scheme'] = \
                f"{random.choice(locality_scheme_tuple)}"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['description'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.address.addressDetails.locality.description"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['uri'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.address.addressDetails.locality.uri"

            new_lots_array[q_0]['placeOfPerformance']['description'] = \
                f"create pn: tender.lots{q_0}.placeOfPerformance.description"

        self.__payload['tender']['lots'] = new_lots_array

    def customize_tender_documents(self, lot_id_list, quantity_of_documents):
        """
        The quantity of lot_id_list must be equal the quantity_of_documents.
        """
        new_documents_array = list()
        for q_0 in range(quantity_of_documents):
            new_documents_array.append(copy.deepcopy(self.__payload['tender']['documents'][0]))

            document_two = Document(host=self.__host)
            document_two_was_uploaded = document_two.uploading_document()

            new_documents_array[q_0]['id'] = document_two_was_uploaded[0]["data"]["id"]
            new_documents_array[q_0]['documentType'] = f"{random.choice(documentType_tuple)}"
            new_documents_array[q_0]['title'] = f"create pn: tender.documents{q_0}.title"
            new_documents_array[q_0]['description'] = f"create pn: tender.documents{q_0}.description"

            new_documents_array[q_0]['relatedLots'] = [lot_id_list[q_0]]

        self.__payload['tender']['documents'] = new_documents_array

    def __del__(self):
        print(f"The instance of PlanningNoticePayload class: {__name__} was deleted.")
