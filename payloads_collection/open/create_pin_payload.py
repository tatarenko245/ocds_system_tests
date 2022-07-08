"""Prepare the expected payloads of the prior information notice process, open procedures."""
import copy
import json
import random

from class_collection.document_registration import Document
from data_collection.data_constant import cpv_goods_low_level_03_tuple, cpv_goods_low_level_1_tuple, \
    cpv_goods_low_level_2_tuple, cpv_goods_low_level_3_tuple, cpv_goods_low_level_44_tuple, \
    cpv_goods_low_level_48_tuple, cpv_works_low_level_45_tuple, cpv_services_low_level_5_tuple, \
    cpv_services_low_level_6_tuple, cpv_services_low_level_7_tuple, cpv_services_low_level_8_tuple, \
    cpv_services_low_level_92_tuple, cpv_services_low_level_98_tuple, legal_basis_tuple, locality_scheme_tuple, \
    documentType_tuple, unit_id_tuple, cpvs_tuple, region_id_tuple
from data_collection.for_test_createPIN_process.payload_full_model import payload_model
from functions_collection.cassandra_methods import get_value_from_ocds_budgetrules
from functions_collection.prepare_date import pn_period, contact_period
from functions_collection.some_functions import generate_items_array, generate_lots_array, \
    get_locality_id_according_with_region_id


class PriorInformationNoticePayload:
    """This class creates instance of payload."""

    def __init__(
            self, connect_to_ocds, country, amount, currency, tender_classification_id, host_to_service, fs_id=None):

        self.__payload = copy.deepcopy(payload_model)

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

    def build_payload(self):
        """Build payload."""

        return self.__payload

    def delete_optional_fields(
            self, *args, pe_additionalidentifiers_position=0, pe_persones_position=0, pe_persones_bf_position=0,
            pe_persones_bf_documents_position=0, criteria_position=0, conversion_position=0, target_position=0,
            lot_position=0, lot_options_position=0, lot_recurrence_dates_position=0, item_position=0,
            item_additionalclassification_position=0, document_position=0):
        """Call this method last! Delete option fields from payload."""

        for a in args:
            if a == "planning.rationale":
                del self.__payload['planning']['rationale']

            elif a == "planning.budget.description":
                del self.__payload['planning']['budget']['description']

            elif a == "tender.secondStage":
                del self.__payload['tender']['secondStage']

            elif a == "tender.secondStage.minimumCandidates":
                del self.__payload['tender']['secondStage']['minimumCandidates']

            elif a == "tender.secondStage.maximumCandidates":
                del self.__payload['tender']['secondStage']['maximumCandidates']

            elif a == "tender.otherCriteria":
                del self.__payload['tender']['otherCriteria']

            elif a == "tender.procurementMethodRationale":
                del self.__payload['tender']['procurementMethodRationale']

            elif a == "tender.enquiryPeriod":
                del self.__payload['tender']['enquiryPeriod']

            elif a == "tender.procurementMethodModalities":
                del self.__payload['tender']['procurementMethodModalities']

            elif a == "tender.electronicAuctions":
                del self.__payload['tender']['electronicAuctions']

            elif a == "tender.procuringEntity.identifier.uri":
                del self.__payload['tender']['procuringEntity']['identifier']['uri']

            elif a == "tender.procuringEntity.additionalIdentifiers":
                del self.__payload['tender']['procuringEntity']['additionalIdentifiers']

            elif a == f"tender.procuringEntity.additionalIdentifiers[{pe_additionalidentifiers_position}]":
                del self.__payload['tender']['procuringEntity']['additionalIdentifiers'][
                    pe_additionalidentifiers_position]

            elif a == f"tender.procuringEntity.additionalIdentifiers[{pe_additionalidentifiers_position}].uri":
                del self.__payload['tender']['procuringEntity'][
                    'additionalIdentifiers'][pe_additionalidentifiers_position]['uri']

            elif a == "tender.procuringEntity.address.postalCode":
                del self.__payload['tender']['procuringEntity']['address']['postalCode']

            elif a == "tender.procuringEntity.contactPoint.faxNumber":
                del self.__payload['tender']['procuringEntity']['contactPoint']['faxNumber']

            elif a == "tender.procuringEntity.contactPoint.url":
                del self.__payload['tender']['procuringEntity']['contactPoint']['url']

            elif a == "tender.procuringEntity.persones":
                del self.__payload['tender']['procuringEntity']['persones']

            elif a == f"tender.procuringEntity.persones[{pe_persones_position}]":
                del self.__payload['tender']['procuringEntity']['persones'][pe_persones_position]

            elif a == f"tender.procuringEntity.persones[{pe_persones_position}].identifier.uri":
                del self.__payload['tender']['procuringEntity']['persones'][pe_persones_position]['identifier']['uri']

            elif a == f"tender.procuringEntity.persones[{pe_persones_position}].businessFunctions" \
                      f"[{pe_persones_bf_position}].documents":
                del self.__payload['tender']['procuringEntity']['persones'][pe_persones_position][
                    'businessFunctions'][pe_persones_bf_position]['documents']

            elif a == f"tender.procuringEntity.persones[{pe_persones_position}].businessFunctions" \
                      f"[{pe_persones_bf_position}].documents[{pe_persones_bf_documents_position}]":
                del self.__payload['tender']['procuringEntity']['persones'][pe_persones_position][
                    'businessFunctions'][pe_persones_bf_position]['documents'][pe_persones_bf_documents_position]

            elif a == f"tender.procuringEntity.persones[{pe_persones_position}].businessFunctions" \
                      f"[{pe_persones_bf_position}].documents[{pe_persones_bf_documents_position}].description":
                del self.__payload['tender']['procuringEntity']['persones'][pe_persones_position][
                    'businessFunctions'][pe_persones_bf_position]['documents'][pe_persones_bf_documents_position][
                    'description']

            elif a == "tender.criteria":
                del self.__payload['tender']['criteria']

            elif a == f"tender.criteria[{criteria_position}]":
                del self.__payload['tender']['criteria'][criteria_position]

            elif a == "tender.conversions":
                del self.__payload['tender']['conversions']

            elif a == f"tender.conversions[{conversion_position}]":
                del self.__payload['tender']['conversions'][conversion_position]

            elif a == f"tender.conversions[{conversion_position}].description":
                del self.__payload['tender']['conversions'][conversion_position]['description']

            elif a == "tender.targets":
                del self.__payload['tender']['targets']

            elif a == f"tender.targets[{target_position}]":
                del self.__payload['tender']['targets'][target_position]

            elif a == f"tender.targets[{target_position}].relatedItem":
                del self.__payload['tender']['targets'][target_position]['relatedItem']

            elif a == f"tender.targets[{target_position}].observations.period":
                del self.__payload['tender']['targets'][target_position]['observations']['period']

            elif a == f"tender.targets[{target_position}].observations.period.startDate":
                del self.__payload['tender']['targets'][target_position]['observations']['period']['startDate']

            elif a == f"tender.targets[{target_position}].observations.period.endDate":
                del self.__payload['tender']['targets'][target_position]['observations']['period']['endDate']

            elif a == f"tender.targets[{target_position}].unit":
                del self.__payload['tender']['targets'][target_position]['unit']

            elif a == f"tender.targets[{target_position}].dimensions":
                del self.__payload['tender']['targets'][target_position]['dimensions']

            elif a == f"tender.targets[{target_position}].relatedRequirementId":
                del self.__payload['tender']['targets'][target_position]['relatedRequirementId']

            elif a == "tender.lots":
                del self.__payload['tender']['lots']

            elif a == f"tender.lots[{lot_position}]":
                del self.__payload['tender']['lots'][{lot_position}]

            elif a == f"tender.lots[{lot_position}].internalId":
                del self.__payload['tender']['lots'][lot_position]['internalId']

            elif a == f"tender.lots[{lot_position}].placeOfPerformance.address.postalCode":
                del self.__payload['tender']['lots'][lot_position]['placeOfPerformance']['address']['postalCode']

            elif a == f"tender.lots[{lot_position}].placeOfPerformance.description":
                del self.__payload['tender']['lots'][lot_position]['placeOfPerformance']['description']

            elif a == f"tender.lots[{lot_position}].hasOptions":
                del self.__payload['tender']['lots'][lot_position]['hasOptions']

            elif a == f"tender.lots[{lot_position}].options[{lot_options_position}]":
                del self.__payload['tender']['lots'][lot_position]['options'][lot_options_position]

            elif a == f"tender.lots[{lot_position}].options[{lot_options_position}].description":
                del self.__payload['tender']['lots'][lot_position]['options'][lot_options_position]['description']

            elif a == f"tender.lots[{lot_position}].options[{lot_options_position}].period":
                del self.__payload['tender']['lots'][lot_position]['options'][lot_options_position]['period']

            elif a == f"tender.lots[{lot_position}].options[{lot_options_position}].period.durationInDays":
                del self.__payload['tender']['lots'][lot_position]['options'][lot_options_position]['period'][
                    'durationInDays']

            elif a == f"tender.lots[{lot_position}].options[{lot_options_position}].period.startDate":
                del self.__payload['tender']['lots'][lot_position]['options'][lot_options_position]['period'][
                    'startDate']

            elif a == f"tender.lots[{lot_position}].options[{lot_options_position}].period.endDate":
                del self.__payload['tender']['lots'][lot_position]['options'][lot_options_position]['period']['endDate']

            elif a == f"tender.lots[{lot_position}].options[{lot_options_position}].period.maxExtentDate":
                del self.__payload['tender']['lots'][lot_position]['options'][lot_options_position]['period'][
                    'maxExtentDate']

            elif a == f"tender.lots[{lot_position}].hasRecurrence":
                del self.__payload['tender']['lots'][lot_position]['hasRecurrence']

            elif a == f"tender.lots[{lot_position}].recurrence.dates":
                del self.__payload['tender']['lots'][lot_position]['recurrence']['dates']

            elif a == f"tender.lots[{lot_position}].recurrence.dates[{lot_recurrence_dates_position}]":
                del self.__payload['tender']['lots'][lot_position]['recurrence']['dates'][lot_recurrence_dates_position]

            elif a == f"tender.lots[{lot_position}].recurrence.dates[" \
                      f"{lot_recurrence_dates_position}].startDate":
                del self.__payload['tender']['lots'][lot_position]['recurrence']['dates'][
                    lot_recurrence_dates_position]['startDate']

            elif a == f"tender.lots[{lot_position}].recurrence.description":
                del self.__payload['tender']['lots'][lot_position]['recurrence']['description']

            elif a == f"tender.lots[{lot_position}].hasRenewal.":
                del self.__payload['tender']['lots'][lot_position]['haRenewal']

            elif a == f"tender.lots[{lot_position}].renewal.description":
                del self.__payload['tender']['lots'][lot_position]['renewal']['description']

            elif a == f"tender.lots[{lot_position}].renewal.minimumRenewals":
                del self.__payload['tender']['lots'][lot_position]['renewal']['minimumRenewals']

            elif a == f"tender.lots[{lot_position}].renewal.maximumRenewals":
                del self.__payload['tender']['lots'][lot_position]['renewal']['maximumRenewals']

            elif a == f"tender.lots[{lot_position}].renewal.period":
                del self.__payload['tender']['lots'][lot_position]['renewal']['period']

            elif a == f"tender.lots[{lot_position}].renewal.period.durationInDays":
                del self.__payload['tender']['lots'][lot_position]['renewal']['period']['durationInDays']

            elif a == f"tender.lots[{lot_position}].renewal.period.startDate":
                del self.__payload['tender']['lots'][lot_position]['renewal']['period']['startDate']

            elif a == f"tender.lots[{lot_position}].renewal.period.endDate":
                del self.__payload['tender']['lots'][lot_position]['renewal']['period']['endDate']

            elif a == f"tender.lots[{lot_position}].renewal.period.maxExtentDate":
                del self.__payload['tender']['lots'][lot_position]['renewal']['period']['maxExtentDate']

            elif a == "tender.items":
                del self.__payload['tender']['items']

            elif a == f"tender.items[{item_position}]":
                del self.__payload['tender']['items'][item_position]

            elif a == "tender.items.internalId":
                del self.__payload['tender']['items'][item_position]['internalId']

            elif a == "tender.items.additionalClassifications":
                del self.__payload['tender']['items'][item_position]['additionalClassifications']

            elif a == f"tender.items.additionalClassifications[{item_additionalclassification_position}]":
                del self.__payload['tender']['items'][item_position][
                    'additionalClassifications'][item_additionalclassification_position]

            elif a == "tender.documents":
                del self.__payload['tender']['documents']

            elif a == f"tender.documents[{document_position}]":
                del self.__payload['tender']['documents'][document_position]

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

    def customize_planning_budget_budget_breakdown(self, list_of_classifications: list):
        """Customize planning.budget.budgetBreakdown array."""

        # Since we work with two country Moldova and Litua, we should to correct some attribute.
        # It depends on country value and according to payload data model from documentation.
        # presence_fs = json.loads(
        #     get_value_from_ocds_budgetrules(connect_to_ocds, f"{country}-createEI", "presenceClassificationFS")
        # )

        # Тимчасове рішення - видалити рядок, що нижче
        presence_fs = True

        new_budget_breakdown_array = list()
        for q_0 in range(len(list_of_classifications)):
            new_budget_breakdown_array.append(copy.deepcopy(self.__payload['planning']['budget']['budgetBreakdown'][0]))

            new_budget_breakdown_array[q_0]['id'] = f"{q_0}"
            new_budget_breakdown_array[q_0]['amount'] = round(self.__amount / len(list_of_classifications), 2)
            new_budget_breakdown_array[q_0]['amount'] = self.__currency

            new_budget_breakdown_array[q_0]['classifications']['ei'] = list_of_classifications[q_0]['ei']

            if presence_fs is False:
                del new_budget_breakdown_array[q_0]['classifications']['fs']
            elif presence_fs is True:
                new_budget_breakdown_array[q_0]['classifications']['fs'] = list_of_classifications[q_0]['fs']
            else:
                raise ValueError(f"Error in payload! Invalid SQL request: 'ocds.budget_rules'.")

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

    def __del__(self):
        print(f"The instance of PlanPayload class: {__name__} was deleted.")
