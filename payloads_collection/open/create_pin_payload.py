"""Prepare the expected payloads of the prior information notice process, open procedures."""
import copy
import json
import random
import uuid

from class_collection.document_registration import Document
from class_collection.prepare_criteria_array import CriteriaArray
from data_collection.OpenProcedure.for_test_createPIN_process.payload_full_model import payload_model
from data_collection.data_constant import documentType_tuple, unit_id_tuple, cpvs_tuple, legal_basis_tuple,\
    awardCriteria_tuple, awardCriteriaDetails_tuple, person_title_tuple, business_function_type_2_tuple
from functions_collection.cassandra_methods import get_value_from_ocds_budgetrules, get_value_from_auctions_auctionrules
from functions_collection.mdm_methods import get_standard_criteria

from functions_collection.prepare_date import pn_period, contact_period, enquiry_period, old_period
from functions_collection.some_functions import generate_items_array, generate_lots_array, \
    get_affordable_schemes, set_eligibility_evidences_unique_temporary_id, set_criteria_array_unique_temporary_id, \
    generate_conversions_array, set_conversions_unique_temporary_id


class PriorInformationNoticePayload:
    """This class creates instance of payload."""

    def __init__(self, environment: str, language: str, host_to_service: str, country: str, amount: float or int,
                 currency: str, tender_classification_id: str, procurinentity_id: str = "55",
                 procurinentity_scheme: str = None):

        self.host = host_to_service
        self.country = country
        self.affordable_schemes = get_affordable_schemes(country)
        self.amount = amount
        self.currency = currency

        self.tender_classification_id = tender_classification_id
        self.tenderperiod_startdate = pn_period()
        self.enquiryperiod_enddate = enquiry_period(self.tenderperiod_startdate)

        # Get all 'standard' criteria from eMDM service.
        self.standard_criteria = get_standard_criteria(environment, self.country, language)

        self.payload = copy.deepcopy(payload_model)

        # Set regular value for some attribute
        self.payload['planning']['rationale'] = "create pin: planning.rationale"
        self.payload['planning']['budget']['description'] = "create pin: planning.description"
        self.payload['planning']['budget']['description'] = "create pin: planning.budgetBreakdown[0].id"

        self.payload['tender']['title'] = "create pin: tender.title"
        self.payload['tender']['description'] = "create pin: tender.description"
        self.payload['tender']['classification']['id'] = self.tender_classification_id
        self.payload['tender']['classification']['scheme'] = "CPV"
        self.payload['tender']['legalBasis'] = f"{random.choice(legal_basis_tuple)}"
        self.payload['tender']['procurementMethodRationale'] = "create pin: tender.procurementMethodRationale"
        self.payload['tender']['awardCriteria'] = f"{random.choice(awardCriteria_tuple)}"
        self.payload['tender']['awardCriteriaDetails'] = f"{random.choice(awardCriteriaDetails_tuple)}"
        self.payload['tender']['tenderPeriod']['startDate'] = self.tenderperiod_startdate
        self.payload['tender']['enquiryPeriod']['endDate'] = self.enquiryperiod_enddate

        self.payload['tender']['procuringEntity']['name'] = "create pin: procuringEntity.name"
        self.payload['tender']['procuringEntity']['identifier']['id'] = procurinentity_id

        self.payload['tender']['procuringEntity']['identifier']['legalName'] = \
            "create pin: procuringEntity.identifier.legalName"

        if procurinentity_scheme is None:
            procurinentity_scheme = self.affordable_schemes[0]

        self.payload['tender']['procuringEntity']['identifier']['scheme'] = procurinentity_scheme

        self.payload['tender']['procuringEntity']['identifier']['uri'] = "create pin: procuringEntity.identifier.uri"

        self.payload['tender']['procuringEntity']['address']['streetAddress'] = \
            "create pin: procuringEntity.address.streetAddress"

        self.payload['tender']['procuringEntity']['address']['postalCode'] = \
            "create pin: procuringEntity.address.postalCode"

        self.payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'] = self.country

        self.payload['tender']['procuringEntity']['address']['addressDetails']['country']['scheme'] = \
            self.affordable_schemes[1]

        self.payload['tender']['procuringEntity']['address']['addressDetails']['country']['description'] = \
            "create pin: tender.procuringEntity.address.addressDetails.country.description"

        self.payload['tender']['procuringEntity']['address']['addressDetails']['region']['scheme'] = \
            self.affordable_schemes[2]

        self.payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'] = \
            self.affordable_schemes[3]

        self.payload['tender']['procuringEntity']['address']['addressDetails']['region']['description'] = \
            "create pin: tender.procuringEntity.address.addressDetails.region.description"

        self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] = \
            self.affordable_schemes[4]

        self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'] = \
            self.affordable_schemes[5]

        self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['description'] = \
            "create pin: tender.procuringEntity.address.addressDetails.locality.description"

        self.payload['tender']['procuringEntity']['contactPoint']['name'] = \
            "create pin: procuringEntity.contactPoint.name"

        self.payload['tender']['procuringEntity']['contactPoint']['email'] = \
            "create pin: procuringEntity.contactPoint.email"

        self.payload['tender']['procuringEntity']['contactPoint']['telephone'] = \
            "create pin: procuringEntity.contactPoint.telephone"

        self.payload['tender']['procuringEntity']['contactPoint']['faxNumber'] = \
            "create pin: procuringEntity.contactPoint.faxNumber"

        self.payload['tender']['procuringEntity']['contactPoint']['url'] = \
            "create pin: procuringEntity.contactPoint.url"

    def build_payload(self):
        """Build payload, based on full data model."""

        # According with 'VR.COM-1.60.35' rule, at least one clasification.id of 'items' array,
        # should be equal by 4 first digits of tender.classification.id
        self.payload['tender']['items'][0]['classification']['id'] = self.tender_classification_id

        if self.payload['tender']['awardCriteria'] == "priceOnly":
            # VR.COM-1.60.36: Set awardCriteriaDetails.
            self.payload['tender']['awardCriteriaDetails'] = "automated"

            # VR.COM-1.60.58: del conversion.
            del self.payload['tender']['conversions']
        return self.payload

    def delete_optional_fields(
            self, *args, pe_additionalidentifiers_position: int = 0, pe_persones_position: int = 0,
            pe_persones_bf_position: int = 0, pe_persones_bf_documents_position: int = 0, criteria_position: int = 0,
            conversion_position: int = 0, target_position: int = 0, lot_position: int = 0,
            lot_options_position: int = 0, lot_recurrence_dates_position: int = 0, item_position: int = 0,
            item_additionalclassification_position: int = 0, document_position: int = 0,
            target_observation_position: int = 0):
        """Call this method last! Delete option fields from payload."""

        for a in args:
            if a == "planning.rationale":
                del self.payload['planning']['rationale']

            elif a == "planning.budget.description":
                del self.payload['planning']['budget']['description']

            elif a == "tender.procurementMethodRationale":
                del self.payload['tender']['procurementMethodRationale']

            elif a == "tender.enquiryPeriod":
                del self.payload['tender']['enquiryPeriod']

            elif a == "tender.procurementMethodModalities":
                del self.payload['tender']['procurementMethodModalities']

            elif a == "tender.electronicAuctions":
                del self.payload['tender']['electronicAuctions']

            elif a == "tender.procuringEntity.identifier.uri":
                del self.payload['tender']['procuringEntity']['identifier']['uri']

            elif a == "tender.procuringEntity.additionalIdentifiers":
                del self.payload['tender']['procuringEntity']['additionalIdentifiers']

            elif a == "tender.procuringEntity.additionalIdentifiers[?]":
                del self.payload['tender']['procuringEntity']['additionalIdentifiers'][
                    pe_additionalidentifiers_position]

            elif a == "tender.procuringEntity.additionalIdentifiers[?].uri":
                del self.payload['tender']['procuringEntity'][
                    'additionalIdentifiers'][pe_additionalidentifiers_position]['uri']

            elif a == "tender.procuringEntity.address.postalCode":
                del self.payload['tender']['procuringEntity']['address']['postalCode']

            elif a == "tender.procuringEntity.contactPoint.faxNumber":
                del self.payload['tender']['procuringEntity']['contactPoint']['faxNumber']

            elif a == "tender.procuringEntity.contactPoint.url":
                del self.payload['tender']['procuringEntity']['contactPoint']['url']

            elif a == "tender.procuringEntity.persones":
                del self.payload['tender']['procuringEntity']['persones']

            elif a == "tender.procuringEntity.persones[?]":
                del self.payload['tender']['procuringEntity']['persones'][pe_persones_position]

            elif a == "tender.procuringEntity.persones[?].identifier.uri":
                del self.payload['tender']['procuringEntity']['persones'][pe_persones_position]['identifier']['uri']

            elif a == "tender.procuringEntity.persones[?].businessFunctions[?].documents":
                del self.payload['tender']['procuringEntity']['persones'][pe_persones_position][
                    'businessFunctions'][pe_persones_bf_position]['documents']

            elif a == "tender.procuringEntity.persones[?].businessFunctions[?].documents[?]":
                del self.payload['tender']['procuringEntity']['persones'][pe_persones_position][
                    'businessFunctions'][pe_persones_bf_position]['documents'][pe_persones_bf_documents_position]

            elif a == "tender.procuringEntity.persones[?].businessFunctions[?].documents[?].description":
                del self.payload['tender']['procuringEntity']['persones'][pe_persones_position][
                    'businessFunctions'][pe_persones_bf_position]['documents'][pe_persones_bf_documents_position][
                    'description']

            elif a == "tender.criteria":
                del self.payload['tender']['criteria']

            elif a == "tender.criteria[?]":
                del self.payload['tender']['criteria'][criteria_position]

            elif a == "tender.conversions":
                del self.payload['tender']['conversions']

            elif a == "tender.conversions[?]":
                del self.payload['tender']['conversions'][conversion_position]

            elif a == "tender.conversions[?].description":
                del self.payload['tender']['conversions'][conversion_position]['description']

            elif a == "tender.targets":
                del self.payload['tender']['targets']

            elif a == "tender.targets[?]":
                del self.payload['tender']['targets'][target_position]

            elif a == "tender.targets[?].relatedItem":
                del self.payload['tender']['targets'][target_position]['relatedItem']

            elif a == "tender.targets[?].observations.period":
                del self.payload['tender']['targets'][target_position]['observations']['period']

            elif a == "tender.targets[?].observations.period.startDate":
                del self.payload['tender']['targets'][target_position]['observations']['period']['startDate']

            elif a == "tender.targets[?].observations[?].period.endDate":
                del self.payload['tender']['targets'][target_position]['observations'][target_observation_position][
                    'period']['endDate']

            elif a == "tender.targets[?].unit":
                del self.payload['tender']['targets'][target_position]['unit']

            elif a == "tender.targets[?].dimensions":
                del self.payload['tender']['targets'][target_position]['dimensions']

            elif a == "tender.targets[?].relatedRequirementId":
                del self.payload['tender']['targets'][target_position]['relatedRequirementId']

            elif a == "tender.lots":
                del self.payload['tender']['lots']

            elif a == "tender.lots[?]":
                del self.payload['tender']['lots'][{lot_position}]

            elif a == "tender.lots[?].internalId":
                del self.payload['tender']['lots'][lot_position]['internalId']

            elif a == "tender.lots[?].placeOfPerformance.address.postalCode":
                del self.payload['tender']['lots'][lot_position]['placeOfPerformance']['address']['postalCode']

            elif a == "tender.lots[?].placeOfPerformance.description":
                del self.payload['tender']['lots'][lot_position]['placeOfPerformance']['description']

            elif a == "tender.lots[?].hasOptions":
                del self.payload['tender']['lots'][lot_position]['hasOptions']

            elif a == "tender.lots[?].options":
                del self.payload['tender']['lots'][lot_position]['options']

            elif a == "tender.lots[?].options[?]":
                del self.payload['tender']['lots'][lot_position]['options'][lot_options_position]

            elif a == "tender.lots[?].options[?].description":
                del self.payload['tender']['lots'][lot_position]['options'][lot_options_position]['description']

            elif a == "tender.lots[?].options[?].period":
                del self.payload['tender']['lots'][lot_position]['options'][lot_options_position]['period']

            elif a == "tender.lots[?].options[?].period.durationInDays":
                del self.payload['tender']['lots'][lot_position]['options'][lot_options_position]['period'][
                    'durationInDays']

            elif a == "tender.lots[?].options[?].period.startDate":
                del self.payload['tender']['lots'][lot_position]['options'][lot_options_position]['period'][
                    'startDate']

            elif a == "tender.lots[?].options[?].period.endDate":
                del self.payload['tender']['lots'][lot_position]['options'][lot_options_position]['period']['endDate']

            elif a == "tender.lots[?].options[?].period.maxExtentDate":
                del self.payload['tender']['lots'][lot_position]['options'][lot_options_position]['period'][
                    'maxExtentDate']

            elif a == "tender.lots[?].hasRecurrence":
                del self.payload['tender']['lots'][lot_position]['hasRecurrence']

            elif a == "tender.lots[?].recurrence":
                del self.payload['tender']['lots'][lot_position]['recurrence']

            elif a == "tender.lots[?].recurrence.dates":
                del self.payload['tender']['lots'][lot_position]['recurrence']['dates']

            elif a == "tender.lots[?].recurrence.dates[?]":
                del self.payload['tender']['lots'][lot_position]['recurrence']['dates'][lot_recurrence_dates_position]

            elif a == "tender.lots[?].recurrence.dates[?].startDate":
                del self.payload['tender']['lots'][lot_position]['recurrence']['dates'][
                    lot_recurrence_dates_position]['startDate']

            elif a == "tender.lots[?].recurrence.description":
                del self.payload['tender']['lots'][lot_position]['recurrence']['description']

            elif a == "tender.lots[?].hasRenewal":
                del self.payload['tender']['lots'][lot_position]['hasRenewal']

            elif a == "tender.lots[?].renewal":
                del self.payload['tender']['lots'][lot_position]['renewal']

            elif a == "tender.lots[?].renewal.description":
                del self.payload['tender']['lots'][lot_position]['renewal']['description']

            elif a == "tender.lots[?].renewal.minimumRenewals":
                del self.payload['tender']['lots'][lot_position]['renewal']['minimumRenewals']

            elif a == "tender.lots[?].renewal.maximumRenewals":
                del self.payload['tender']['lots'][lot_position]['renewal']['maximumRenewals']

            elif a == "tender.lots[?].renewal.period":
                del self.payload['tender']['lots'][lot_position]['renewal']['period']

            elif a == "tender.lots[?].renewal.period.durationInDays":
                del self.payload['tender']['lots'][lot_position]['renewal']['period']['durationInDays']

            elif a == "tender.lots[?].renewal.period.startDate":
                del self.payload['tender']['lots'][lot_position]['renewal']['period']['startDate']

            elif a == "tender.lots[?].renewal.period.endDate":
                del self.payload['tender']['lots'][lot_position]['renewal']['period']['endDate']

            elif a == "tender.lots[?].renewal.period.maxExtentDate":
                del self.payload['tender']['lots'][lot_position]['renewal']['period']['maxExtentDate']

            elif a == "tender.items":
                del self.payload['tender']['items']

            elif a == "tender.items[?]":
                del self.payload['tender']['items'][item_position]

            elif a == "tender.items[?].internalId":
                del self.payload['tender']['items'][item_position]['internalId']

            elif a == "tender.items[?].additionalClassifications":
                del self.payload['tender']['items'][item_position]['additionalClassifications']

            elif a == "tender.items[?].additionalClassifications[?]":
                del self.payload['tender']['items'][item_position][
                    'additionalClassifications'][item_additionalclassification_position]

            elif a == "tender.documents":
                del self.payload['tender']['documents']

            elif a == "tender.documents[?]":
                del self.payload['tender']['documents'][document_position]

            elif a == "tender.documents[?].description":
                del self.payload['tender']['documents'][document_position]['description']

            elif a == "tender.documents[?].relatedLots":
                del self.payload['tender']['documents'][document_position]["relatedLots"]

            else:
                KeyError(f"Impossible to delete attribute by path {a}.")

    def get_lots_id_from_payload(self):
        """Get lots.id from payload."""

        lot_id_list = list()
        for q in range(len(self.payload['tender']['lots'])):
            lot_id_list.append(self.payload['tender']['lots'][q]['id'])
        return lot_id_list

    def get_items_id_from_payload(self):
        """Get items.id from payload."""

        item_id_list = list()
        for q in range(len(self.payload['tender']['items'])):
            item_id_list.append(self.payload['tender']['items'][q]['id'])
        return item_id_list

    def customize_planning_budget_budgetbreakdown(self, connect_to_ocds: str, list_of_classifications: list):
        """Customize planning.budget.budgetBreakdown array."""

        # Since we work with two country Moldova and Litua, we should to correct some attribute.
        # It depends on country value and according to payload data model from documentation.
        presence_fs = json.loads(
            get_value_from_ocds_budgetrules(connect_to_ocds, f"{self.country}-createPin", "presenceClassificationFS")
        )

        new_budget_breakdown_array = list()
        for q_0 in range(len(list_of_classifications)):
            new_budget_breakdown_array.append(copy.deepcopy(self.payload['planning']['budget']['budgetBreakdown'][0]))

            new_budget_breakdown_array[q_0]['id'] = str(uuid.uuid4())
            new_budget_breakdown_array[q_0]['amount']['amount'] = round(self.amount / len(list_of_classifications), 2)
            new_budget_breakdown_array[q_0]['amount']['currency'] = self.currency

            new_budget_breakdown_array[q_0]['classifications']['ei'] = list_of_classifications[q_0]['ei']

            if presence_fs is False:
                del new_budget_breakdown_array[q_0]['classifications']['fs']
            elif presence_fs is True:
                new_budget_breakdown_array[q_0]['classifications']['fs'] = list_of_classifications[q_0]['fs']
            else:
                raise ValueError(f"Error in payload! Invalid SQL request: 'ocds.budget_rules'.")

        self.payload['planning']['budget']['budgetBreakdown'] = new_budget_breakdown_array

    def customize_tender_items(self, quantity_of_items: int, quantity_of_items_additionalclassifications: int):
        """
        The max quantity of items must be 5, because it depends on cpvs_tuple from data_of_enum.
        The quantity of lot_id_list must be equal the quantity_of_items.
        """

        lot_id_list = self.get_lots_id_from_payload()

        new_items_array = generate_items_array(
            quantity_of_object=quantity_of_items,
            item_object=copy.deepcopy(self.payload['tender']['items'][0]),
            tender_classification_id=self.tender_classification_id
        )

        for q_0 in range(quantity_of_items):

            new_items_array[q_0]['classification']['scheme'] = "CPV"
            new_items_array[q_0]['internalId'] = f"create pin: tender.items{q_0}.internalId"
            new_items_array[q_0]['description'] = f"create pin: tender.items{q_0}.description"
            new_items_array[q_0]['quantity'] = 5+q_0
            new_items_array[q_0]['unit']['id'] = f"{random.choice(unit_id_tuple)}"

            list_of_additional_classification_id = list()
            del new_items_array[q_0]['additionalClassifications'][0]
            for q_1 in range(quantity_of_items_additionalclassifications):
                new_items_array[q_0]['additionalClassifications'].append(
                    copy.deepcopy(self.payload['tender']['items'][0]['additionalClassifications'][0]))

                while len(list_of_additional_classification_id) < quantity_of_items_additionalclassifications:
                    additional_classification_id = f"{random.choice(cpvs_tuple)}"
                    if additional_classification_id not in list_of_additional_classification_id:
                        list_of_additional_classification_id.append(additional_classification_id)

            for q_1 in range(quantity_of_items_additionalclassifications):
                new_items_array[q_0]['additionalClassifications'][q_1]['id'] = \
                    list_of_additional_classification_id[q_1]

                new_items_array[q_0]['additionalClassifications'][q_1]['scheme'] = "CPVS"

            new_items_array[q_0]['relatedLot'] = lot_id_list[q_0]

        self.payload['tender']['items'] = new_items_array

    def customize_tender_lots(self, quantity_of_lots: int, quantity_of_options: int, quantity_of_recurrence_dates: int,
                              quantity_of_renewal: int):
        """Customize tender.lots array."""

        new_lots_array = generate_lots_array(
            quantity_of_object=quantity_of_lots,
            lot_object=copy.deepcopy(self.payload['tender']['lots'][0])
        )
        for q_0 in range(quantity_of_lots):
            new_lots_array[q_0]['internalId'] = f"create pin: tender.lots{q_0}.internalId"
            new_lots_array[q_0]['title'] = f"create pin: tender.lotss{q_0}.title"
            new_lots_array[q_0]['description'] = f"create pin: tender.lots{q_0}.description"
            new_lots_array[q_0]['value']['amount'] = round(self.amount / quantity_of_lots, 2)
            new_lots_array[q_0]['value']['currency'] = self.currency

            _contact_period = contact_period()
            new_lots_array[q_0]['contractPeriod']['startDate'] = _contact_period[0]
            new_lots_array[q_0]['contractPeriod']['endDate'] = _contact_period[1]

            new_lots_array[q_0]['placeOfPerformance']['address']['streetAddress'] = \
                f"create pin: tender.lots{q_0}.placeOfPerformance.streetAddress"

            new_lots_array[q_0]['placeOfPerformance']['address']['postalCode'] = \
                f"create pin: tender.lots{q_0}.placeOfPerformance.postalCode"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['country']['id'] = self.country

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['country']['scheme'] = \
                self.affordable_schemes[1]

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['country']['description'] = \
                f"create pin: tender.lots[{q_0}].placeOfPerformance.address.addressDetails.country.description"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['region']['scheme'] = \
                self.affordable_schemes[2]

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['region']['id'] = \
                self.affordable_schemes[3]

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['region']['description'] = \
                f"create pin: tender.lots[{q_0}].placeOfPerformance.address.addressDetails.region.description"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['scheme'] = \
                self.affordable_schemes[4]

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['id'] = \
                self.affordable_schemes[5]

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['description'] = \
                f"create pin: tender.lots{q_0}.placeOfPerformance.address.addressDetails.locality.description"

            new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']['uri'] = \
                f"create pin: tender.lots{q_0}.placeOfPerformance.address.addressDetails.locality.uri"

            new_lots_array[q_0]['placeOfPerformance']['description'] = \
                f"create pin: tender.lots{q_0}.placeOfPerformance.description"

            if quantity_of_options > 0:
                new_lots_array[q_0]['hasOptions'] = True

                options_array = list()
                for q_1 in range(quantity_of_options):
                    options_object = copy.deepcopy(self.payload['tender']['lots'][q_0]['options'][0])

                    if "description" in options_object:
                        options_object['description'] = f"create pin: tender.lots{q_0}.options[{q_1}].description"

                    if "period" in options_object:
                        if "durationInDays" in options_object:
                            options_object['period']['durationInDays'] = 90

                        if "startDate" in options_object['period']:
                            options_object['period']['startDate'] = new_lots_array[q_0]['contractPeriod']['startDate']

                        if "endDate" in options_object['period']:
                            options_object['period']['endDate'] = new_lots_array[q_0]['contractPeriod']['endDate']

                        if "maxExtentDate" in options_object['period']:
                            options_object['period']['maxExtentDate'] = new_lots_array[q_0]['contractPeriod']['endDate']
                    options_array.append(options_object)

                new_lots_array[q_0]['options'] = options_array
            else:
                new_lots_array[q_0]['hasOptions'] = False
                del new_lots_array[q_0]['options']

            if quantity_of_recurrence_dates > 0:
                new_lots_array[q_0]['hasRecurrence'] = True

                if "description" in new_lots_array[q_0]['recurrence']:
                    new_lots_array[q_0]['recurrence']['description'] = \
                        f"create pin: tender.lots{q_0}.recurrence.description"

                if "dates" in new_lots_array[q_0]['recurrence']:
                    recurrence_dates_array = list()
                    for q_1 in range(quantity_of_recurrence_dates):
                        recurrence_dates_object = copy.deepcopy(
                            self.payload['tender']['lots'][q_0]['recurrence']['dates'][0]
                        )

                        if "startDate" in recurrence_dates_object:
                            recurrence_dates_object['startDate'] = new_lots_array[q_0]['contractPeriod']['startDate']

                        recurrence_dates_array.append(recurrence_dates_object)

                    new_lots_array[q_0]['recurrence']['dates'] = recurrence_dates_array
            else:
                new_lots_array[q_0]['hasRecurrence'] = False
                del new_lots_array[q_0]['recurrence']

            if quantity_of_renewal == 1:
                new_lots_array[q_0]['hasRenewal'] = True
                if "description" in new_lots_array[q_0]['renewal']:
                    new_lots_array[q_0]['renewal']['description'] = f"create pin: tender.lots{q_0}.renewal.description"

                if "minimumRenewals" in new_lots_array[q_0]['renewal']:
                    new_lots_array[q_0]['renewal']['minimumRenewals'] = q_0 + 1.23

                if "maximumRenewals" in new_lots_array[q_0]['renewal']:
                    new_lots_array[q_0]['renewal']['maximumRenewals'] = q_0 + 2.24

                if "period" in new_lots_array[q_0]['renewal']:
                    if "durationInDays" in new_lots_array[q_0]['renewal']['period']:
                        new_lots_array[q_0]['renewal']['period']['durationInDays'] = 7.7

                    if "startDate" in new_lots_array[q_0]['renewal']['period']:
                        new_lots_array[q_0]['renewal']['period']['startDate'] = \
                            new_lots_array[q_0]['contractPeriod']['startDate']

                    if "endDate" in new_lots_array[q_0]['renewal']['period']:
                        new_lots_array[q_0]['renewal']['period']['endDate'] = \
                            new_lots_array[q_0]['contractPeriod']['endDate']

                    if "maxExtentDate" in new_lots_array[q_0]['renewal']['period']:
                        new_lots_array[q_0]['renewal']['period']['maxExtentDate'] = \
                            new_lots_array[q_0]['contractPeriod']['endDate']

            else:
                new_lots_array[q_0]['hasRenewal'] = False
                del new_lots_array[q_0]['renewal']

        self.payload['tender']['lots'] = new_lots_array

    def customize_tender_electronicauctions_object(self, connect_to_auctions, pmd):
        """Call this method after customize 'tender.lots' array"""

        # Since we work with two country Moldova and Litua, we should to correct some attribute.
        # It depends on country value and according to VR.COM-18.1.15.

        max_allowable_bid_change_for_auction = json.loads(get_value_from_auctions_auctionrules(
            connect_to_auctions, f"{self.country}-{pmd}-createPin", "maxAllowableBidChangeForAuction"))['percent']/100

        self.payload['tender']['procurementMethodModalities'] = ['electronicAuction']
        electronic_auctions_object = copy.deepcopy(self.payload['tender']['electronicAuctions'])
        del electronic_auctions_object['details'][0]

        for q_0 in range(len(self.payload['tender']['lots'])):
            electronic_auctions_object['details'].append(copy.deepcopy(
                self.payload['tender']['electronicAuctions']['details'][0]
            ))

            electronic_auctions_object['details'][q_0]['id'] = f"{q_0}"
            electronic_auctions_object['details'][q_0]['relatedLot'] = self.payload['tender']['lots'][q_0]['id']

            # 'electronicAuctionModalities' array must contain only one object
            electronic_auctions_object['details'][q_0]['electronicAuctionModalities'][0]['eligibleMinimumDifference'][
                'amount'] = round(self.payload['tender']['lots'][q_0]['value']['amount'] *
                                  max_allowable_bid_change_for_auction, 2)

            electronic_auctions_object['details'][q_0]['electronicAuctionModalities'][0]['eligibleMinimumDifference'][
                'currency'] = self.currency

        self.payload['tender']['electronicAuctions'] = electronic_auctions_object

    def customize_tender_documents(self, quantity_of_documents: int):
        """
        The quantity of lot_id_list must be equal the quantity_of_documents.
        """

        lot_id_list = self.get_lots_id_from_payload()

        new_documents_array = list()
        for q_0 in range(quantity_of_documents):
            new_documents_array.append(copy.deepcopy(self.payload['tender']['documents'][0]))

            document_two = Document(host=self.host)
            document_two_was_uploaded = document_two.uploading_document()

            new_documents_array[q_0]['id'] = document_two_was_uploaded[0]["data"]["id"]
            new_documents_array[q_0]['documentType'] = f"{random.choice(documentType_tuple)}"
            new_documents_array[q_0]['title'] = f"create pin: tender.documents{q_0}.title"

            if "description" in new_documents_array[q_0]:
                new_documents_array[q_0]['description'] = f"create pin: tender.documents{q_0}.description"

            if "relatedLots" in new_documents_array[q_0]:
                new_documents_array[q_0]['relatedLots'] = [lot_id_list[q_0]]

        ee_documents_array = list()
        if "criteria" in self.payload['tender']:
            for e_0 in range(len(self.payload['tender']['criteria'])):
                for e_1 in range(len(self.payload['tender']['criteria'][e_0]['requirementGroups'])):

                    for e_2 in range(len(self.payload['tender']['criteria'][e_0]['requirementGroups'][e_1][
                                             'requirements'])):

                        if "eligibleEvidences" in self.payload['tender']['criteria'][e_0][
                                'requirementGroups'][e_1]['requirements'][e_2]:

                            for e_3 in range(len(self.payload['tender']['criteria'][e_0][
                                                     'requirementGroups'][e_1]['requirements'][e_2][
                                                     'eligibleEvidences'])):

                                if "relatedDocument" in self.payload['tender']['criteria'][e_0][
                                        'requirementGroups'][e_1]['requirements'][e_2]['eligibleEvidences'][e_3]:
                                    ee_document_object = copy.deepcopy(
                                        self.payload['tender']['documents'][0])

                                    ee_document_object['id'] = \
                                        self.payload['tender']['criteria'][e_0]['requirementGroups'][e_1][
                                            'requirements'][e_2]['eligibleEvidences'][e_3]['relatedDocument']['id']

                                    ee_document_object['documentType'] = f"{random.choice(documentType_tuple)}"

                                    ee_document_object['title'] = \
                                        f"create fe: tender.documents{len(ee_documents_array)}.title"

                                    ee_document_object['description'] = \
                                        f"create fe: tender.documents{len(ee_documents_array)}." \
                                        f"description"

                                    del ee_document_object['relatedLots']
                                    ee_documents_array.append(ee_document_object)

        self.payload['tender']['documents'] = new_documents_array + ee_documents_array

    def customize_tender_procuringentity_additionalidentifiers(
            self, quantity_of_tender_procuring_entity_additional_identifiers: int):
        """ Customize tender.procuringEntity.additionalIdentifiers array."""

        new_additional_identifiers_array = list()
        for q in range(quantity_of_tender_procuring_entity_additional_identifiers):
            new_additional_identifiers_array.append(
                copy.deepcopy(self.payload['tender']['procuringEntity']['additionalIdentifiers'][0])
            )

            new_additional_identifiers_array[q]['id'] = \
                f"create fs: tender.procuringEntity.additionalIdentifiers{q}.id"

            new_additional_identifiers_array[q]['scheme'] = \
                f"create fs: tender.procuringEntity.additionalIdentifiers{q}.scheme"

            new_additional_identifiers_array[q]['legalName'] = \
                f"create fs: tender.procuringEntity.additionalIdentifiers{q}.legalName"

            new_additional_identifiers_array[q]['uri'] = \
                f"create fs: tender.procuringEntity.additionalIdentifiers{q}.uri"

        self.payload['tender']['procuringEntity']['additionalIdentifiers'] = new_additional_identifiers_array

    def customize_tender_procuringentity_bf_persones_array(
            self, quantity_of_persones_objects: int, quantity_of_bf_objects: int, quantity_of_documents_objects: int,
            person_title: str = None, businessfunctions_type: str = None):
        """Add new oblects to tender.procuringEntity.persones array."""

        if person_title is None:
            person_title = f"{random.choice(person_title_tuple)}"
        else:
            person_title = person_title

        if businessfunctions_type is None:
            businessfunctions_type = f"{random.choice(business_function_type_2_tuple)}"
        else:
            businessfunctions_type = businessfunctions_type

        businessfunctions_period_startdate = old_period()[0]

        persones_array = list()
        for q_0 in range(quantity_of_persones_objects):
            persones_array.append(copy.deepcopy(
                self.payload['tender']['procuringEntity']['persones'][0]
            ))

            persones_array[q_0]['title'] = person_title
            persones_array[q_0]['name'] = f"create pin: tender.procuringEntity.persones[{q_0}].name"
            persones_array[q_0]['identifier']['scheme'] = self.affordable_schemes[0]
            persones_array[q_0]['identifier']['id'] = f"create pin: tender.procuringEntity.persones[{q_0}].id"
            persones_array[q_0]['identifier']['uri'] = f"create pin: tender.procuringEntity.persones[{q_0}].uri"

            persones_array[q_0]['businessFunctions'] = list()
            for q_1 in range(quantity_of_bf_objects):

                persones_array[q_0]['businessFunctions'].append(copy.deepcopy(
                    self.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0])
                )

                persones_array[q_0]['businessFunctions'][q_1]['id'] = f"{q_1}"
                persones_array[q_0]['businessFunctions'][q_1]['type'] = businessfunctions_type

                persones_array[q_0]['businessFunctions'][q_1]['jobTitle'] = \
                    f"create pin: tender.procuringEntity.persones[{q_0}].['businessFunctions'][{q_1}].jobTitle"

                persones_array[q_0]['businessFunctions'][q_1]['period']['startDate'] = \
                    businessfunctions_period_startdate

                persones_array[q_0]['businessFunctions'][q_1]['documents'] = list()
                for q_2 in range(quantity_of_documents_objects):
                    persones_array[q_0]['businessFunctions'][q_1]['documents'].append(copy.deepcopy(
                        self.payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0][
                            'documents'][0])
                    )

                    document_three = Document(host=self.host)
                    document_three_was_uploaded = document_three.uploading_document()

                    persones_array[q_0]['businessFunctions'][q_1]['documents'][q_2]['id'] = \
                        document_three_was_uploaded[0]["data"]["id"]

                    persones_array[q_0]['businessFunctions'][q_1]['documents'][q_2]['documentType'] = \
                        "regulatoryDocument"

                    persones_array[q_0]['businessFunctions'][q_1]['documents'][q_2]['title'] = \
                        f"amend fe: tender.procuringEntity.persones[{q_0}].['businessFunctions'][{q_1}]." \
                        f"documents[{q_2}.title"

                    persones_array[q_0]['businessFunctions'][q_1]['documents'][q_2]['description'] = \
                        f"amend fe: tender.procuringEntity.persones[{q_0}].['businessFunctions'][{q_1}]." \
                        f"documents[{q_2}.description"

        self.payload['tender']['procuringEntity']['persones'] = persones_array

    def prepare_exclusion_criteria(self, *args, language: str, environment: str, criteria_relates_to: str,
                                   criteria_related_item: str = None):
        # Prepare 'exclusion' criteria for payload.

        some_criteria = CriteriaArray(
            host_to_service=self.host,
            country=self.country,
            language=language,
            environment=environment,
            quantity_of_criteria_objects=len(self.standard_criteria[1]),
            quantity_of_requirement_groups_objects=1,
            quantity_of_requirements_objects=2,
            quantity_of_eligible_evidences_objects=2,
            type_of_standard_criteria=1
        )

        # Delete redundant attributes: 'minValue', 'maxValue', because attribute ' expectedValue' will be used.
        some_criteria.delete_optional_fields(*args)

        some_criteria.prepare_criteria_array(criteria_relates_to, criteria_related_item)
        some_criteria.set_unique_temporary_id_for_eligible_evidences()
        some_criteria.set_unique_temporary_id_for_criteria()
        exclusion_criteria_array = some_criteria.build_criteria_array()
        return exclusion_criteria_array

    def prepare_selection_criteria(self, *args, language: str, environment: str, criteria_relates_to: str,
                                   criteria_related_item: str = None):
        # Prepare 'selection' criteria for payload.

        some_criteria = CriteriaArray(
            host_to_service=self.host,
            country=self.country,
            language=language,
            environment=environment,
            quantity_of_criteria_objects=len(self.standard_criteria[2]),
            quantity_of_requirement_groups_objects=2,
            quantity_of_requirements_objects=2,
            quantity_of_eligible_evidences_objects=2,
            type_of_standard_criteria=2
        )

        # Delete redundant attributes: 'minValue', 'maxValue', because attribute ' expectedValue' will be used.
        some_criteria.delete_optional_fields(*args)

        some_criteria.prepare_criteria_array(criteria_relates_to, criteria_related_item)
        some_criteria.set_unique_temporary_id_for_eligible_evidences()
        some_criteria.set_unique_temporary_id_for_criteria()
        selection_criteria_array = some_criteria.build_criteria_array()
        return selection_criteria_array

    def prepare_other_criteria(self, *args, language: str, environment: str, criteria_relates_to: str,
                               criteria_related_item: str = None):
        # Prepare 'other' criteria for payload.

        some_criteria = CriteriaArray(
            host_to_service=self.host,
            country=self.country,
            language=language,
            environment=environment,
            quantity_of_criteria_objects=len(self.standard_criteria[3]),
            quantity_of_requirement_groups_objects=2,
            quantity_of_requirements_objects=2,
            quantity_of_eligible_evidences_objects=2,
            type_of_standard_criteria=3
        )

        # Delete redundant attributes: 'minValue', 'maxValue', because attribute ' expectedValue' will be used.
        some_criteria.delete_optional_fields(*args)

        some_criteria.prepare_criteria_array(
            criteria_relates_to, criteria_related_item
        )
        some_criteria.set_unique_temporary_id_for_eligible_evidences()
        some_criteria.set_unique_temporary_id_for_criteria()
        other_criteria_array = some_criteria.build_criteria_array()
        return other_criteria_array

    def customize_tender_criteria(self, exclusion_criteria_array: list, selection_criteria_array: list,
                                  other_criteria_array: list):
        """Customize tender.criteria array."""

        # Prepare new criteria array.
        new_criteria_array = exclusion_criteria_array + selection_criteria_array + other_criteria_array
        new_criteria_array = set_eligibility_evidences_unique_temporary_id(new_criteria_array)
        new_criteria_array = set_criteria_array_unique_temporary_id(new_criteria_array)

        self.payload['tender']['criteria'] = new_criteria_array

    def prepare_selection_conversions(self, selection_criteria_array: list):
        """Prepare conversion array"""

        requirements_objects = list()
        for o in selection_criteria_array:
            if "id" in o:
                for o_1 in o['requirementGroups']:
                    if "id" in o_1:
                        for o_2 in o_1['requirements']:
                            if "id" in o_2:
                                requirements_objects.append(o_2['id'])
        quantity_of_requirements_objects = len(requirements_objects)

        conversion_object = {}
        conversion_object.update(copy.deepcopy(self.payload['tender']['conversions'][0]))
        conversion_object['id'] = "0"
        conversion_object['relatesTo'] = "requirement"
        conversion_object['rationale'] = "create pin: tender.conversion.rationale"

        if "description" in conversion_object:
            conversion_object['description'] = "create pin: tender.conversion.description"

        conversion_object['coefficients'] = [{}, {}]

        conversion_object['coefficients'][0].update(copy.deepcopy(
            self.payload['tender']['conversions'][0]['coefficients'][0]
        ))

        conversion_object['coefficients'][1].update(copy.deepcopy(
            self.payload['tender']['conversions'][0]['coefficients'][0]
        ))

        conversion_object['coefficients'][0]['id'] = "create cnonpn: tender.conversion.coefficients.id"
        conversion_object['coefficients'][0]['value'] = 0.99
        conversion_object['coefficients'][0]['coefficient'] = 1
        conversion_object['coefficients'][1]['id'] = "create cnonpn: tender.conversion.coefficients.id"
        conversion_object['coefficients'][1]['value'] = 99.99
        conversion_object['coefficients'][1]['coefficient'] = 0.99

        # Limited by math -> 0.99 ^ 22 = 0.8
        if quantity_of_requirements_objects >= 22:
            quantity = 21
        else:
            quantity = quantity_of_requirements_objects

        conversion_array_for_selection_criteria = generate_conversions_array(
            quantity_of_conversion_object=quantity,
            conversion_object=conversion_object,
            requirements_array=requirements_objects
        )
        return conversion_array_for_selection_criteria

    def prepare_other_conversions(self, other_criteria_array: list):
        """Prepare conversion array"""

        requirements_objects = list()
        for o in other_criteria_array:
            if "id" in o:
                for o_1 in o['requirementGroups']:
                    if "id" in o_1:
                        for o_2 in o_1['requirements']:
                            if "id" in o_2:
                                requirements_objects.append(o_2['id'])
        quantity_of_requirements_objects = len(requirements_objects)

        conversion_object = {}
        conversion_object.update(copy.deepcopy(self.payload['tender']['conversions'][0]))
        conversion_object['id'] = "0"
        conversion_object['relatesTo'] = "requirement"
        conversion_object['rationale'] = "create pin: tender.conversion.rationale"

        if "description" in conversion_object:
            conversion_object['description'] = "create pin: tender.conversion.description"

        conversion_object['coefficients'] = [{}, {}]

        conversion_object['coefficients'][0].update(copy.deepcopy(
            self.payload['tender']['conversions'][0]['coefficients'][0]
        ))

        conversion_object['coefficients'][1].update(copy.deepcopy(
            self.payload['tender']['conversions'][0]['coefficients'][0]
        ))

        conversion_object['coefficients'][0]['id'] = "create cnonpn: tender.conversion.coefficients[0].id"
        conversion_object['coefficients'][0]['value'] = True
        conversion_object['coefficients'][0]['coefficient'] = 0.99
        conversion_object['coefficients'][1]['id'] = "create cnonpn: tender.conversion.coefficients[1].id"
        conversion_object['coefficients'][1]['value'] = False
        conversion_object['coefficients'][1]['coefficient'] = 1

        if quantity_of_requirements_objects >= 1:
            quantity = 1
        else:
            quantity = quantity_of_requirements_objects
        conversion_array_for_other_criteria = generate_conversions_array(
            quantity_of_conversion_object=quantity,
            conversion_object=conversion_object,
            requirements_array=requirements_objects
        )
        return conversion_array_for_other_criteria

    def customize_tender_conversions(self, selection_conversions_array: list, other_conversions_array: list):
        """Customize tender.conversions array.
        According to VR.COM-1.60.79, conversion shouldn't relate with CRITERION.EXCLUSION."""

        # Prepare new conversions array.
        conversions_array = selection_conversions_array + other_conversions_array

        new_conversions_array = set_conversions_unique_temporary_id(conversions_array)
        self.payload['tender']['conversions'] = new_conversions_array

    def customize_tender_targets(self, quantity_of_observations: int = 1, **targets_dict: dict):
        """Customize tender.targets array"""

        targets_list = list()
        for q_0 in range(len(targets_dict['targets_dict']['relatedItems'])):

            targets_list.append(copy.deepcopy(
                self.payload['tender']['targets'][0]
            ))

            targets_list[q_0]['id'] = f"{q_0}"
            targets_list[q_0]['title'] = f"create pin: tender.targets[{q_0}].title"
            targets_list[q_0]['relatesTo'] = targets_dict['targets_dict']['relatesTo']

            if "relatedItem" in targets_list[q_0]:
                targets_list[q_0]['relatedItem'] = targets_dict['targets_dict']['relatedItems'][q_0]

            observations_list = list()
            for q_1 in range(quantity_of_observations):
                observations_list.append(copy.deepcopy(
                    self.payload['tender']['targets'][0]['observations'][0]
                ))

                observations_list[q_1]['id'] = f"{q_1}"

                observation_period = contact_period()
                observations_list[q_1]['period']['startDate'] = observation_period[0]
                observations_list[q_1]['period']['endDate'] = observation_period[1]
                observations_list[q_1]['measure'] = True
                observations_list[q_1]['unit']['id'] = f"{random.choice(unit_id_tuple)}"

                observations_list[q_1]['dimensions']['requirementClassIdPR'] = \
                    f"create pin: tender.targets[{q_0}].observations[{q_1}].dimensions.requirementClassIdPR"

                observations_list[q_1]['notes'] = f"create pin: tender.targets[{q_0}].observations[{q_1}].notes"

                observations_list[q_1]['relatedRequirementId'] = \
                    self.payload['tender']['criteria'][q_1]['requirementGroups'][0]['requirements'][0]['id']

            targets_list[q_0]['observations'] = observations_list
        self.payload['tender']['targets'] = targets_list

    def __del__(self):
        print(f"The instance of PlanPayload class: {__name__} was deleted.")
