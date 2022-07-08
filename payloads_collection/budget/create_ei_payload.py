import copy
import json
import random

from data_collection.data_constant import typeOfBuyer_tuple, mainGeneralActivity_tuple, \
    mainSectoralActivity_tuple, unit_id_tuple, cpvs_tuple
from data_collection.for_test_createEI_process.payload_full_model import *
from functions_collection.cassandra_methods import get_value_from_ocds_budgetrules
from functions_collection.prepare_date import ei_period
from functions_collection.some_functions import generate_items_array, get_affordable_schemes


class CreateExpenditureItemPayload:
    def __init__(self, connect_to_ocds, country, buyer_id, tender_classification_id, amount, currency):

        affordable_schemes = get_affordable_schemes(country)
        __ei_period = ei_period()
        self.__tender_classification_id = tender_classification_id
        self.__payload = copy.deepcopy(payload_model)
        self.__country = country

        # Since we work with two country Moldova and Litua, we should to correct some attribute.
        # It depends on country value and according to payload data model from documentation.
        presence_ei_amount = json.loads(
            get_value_from_ocds_budgetrules(connect_to_ocds, f"{country}-createEI", "presenceEIAmount")
        )

        if presence_ei_amount is False:
            del self.__payload['planning']['budget']['amount']
        elif presence_ei_amount is True:
            self.__payload['planning']['budget']['amount']['amount'] = amount
            self.__payload['planning']['budget']['amount']['currency'] = currency
        else:
            raise ValueError(f"Error in payload! Invalid SQL request: 'ocds.budget_rules'.")

        self.__payload['tender']['classification']['id'] = tender_classification_id

        self.__payload['tender']['items'][0]['classification']['id'] = tender_classification_id
        self.__payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['scheme'] = \
            affordable_schemes[1]
        self.__payload['tender']['items'][0]['deliveryAddress']['addressDetails']['country']['id'] = country
        self.__payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['scheme'] = \
            affordable_schemes[2]
        self.__payload['tender']['items'][0]['deliveryAddress']['addressDetails']['region']['id'] = \
            affordable_schemes[3]
        self.__payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = \
            affordable_schemes[4]
        self.__payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['id'] = \
            affordable_schemes[5]

        self.__payload['planning']['budget']['period']['startDate'] = __ei_period[0]
        self.__payload['planning']['budget']['period']['endDate'] = __ei_period[1]

        self.__payload['buyer']['identifier']['id'] = f"{buyer_id}"
        self.__payload['buyer']['identifier']['scheme'] = affordable_schemes[0]
        self.__payload['buyer']['address']['addressDetails']['country']['scheme'] = affordable_schemes[1]
        self.__payload['buyer']['address']['addressDetails']['country']['id'] = country
        self.__payload['buyer']['address']['addressDetails']['region']['scheme'] = affordable_schemes[2]
        self.__payload['buyer']['address']['addressDetails']['region']['id'] = affordable_schemes[3]
        self.__payload['buyer']['address']['addressDetails']['locality']['scheme'] = affordable_schemes[4]
        self.__payload['buyer']['address']['addressDetails']['locality']['id'] = affordable_schemes[5]
        self.__payload['buyer']['details']['typeOfBuyer'] = f"{random.choice(typeOfBuyer_tuple)}"
        self.__payload['buyer']['details']['mainGeneralActivity'] = f"{random.choice(mainGeneralActivity_tuple)}"
        self.__payload['buyer']['details']['mainSectoralActivity'] = f"{random.choice(mainSectoralActivity_tuple)}"

    def build_payload(self):

        # For business needs: Republic of Moldova uses the specific payload model.
        if self.__country == "MD":
            del self.__payload['tender']['classification']['scheme']

            if "items" in self.__payload['tender']:
                for i in range(len(self.__payload['tender']['items'])):
                    del self.__payload['tender']['items'][i]['classification']['scheme']

                    if "additionalClassifications" in self.__payload['tender']['items'][i]:
                        for a in range(len(self.__payload['tender']['items'][i]['additionalClassifications'])):
                            del self.__payload['tender']['items'][i]['additionalClassifications'][a]['scheme']

                    del self.__payload['tender']['items'][i]['deliveryAddress']['addressDetails'][
                        'country']['description']
                    del self.__payload['tender']['items'][i]['deliveryAddress']['addressDetails'][
                        'country']['scheme']

                    del self.__payload['tender']['items'][i]['deliveryAddress']['addressDetails'][
                        'region']['description']
                    del self.__payload['tender']['items'][i]['deliveryAddress']['addressDetails'][
                        'region']['scheme']

            del self.__payload['buyer']['address']['addressDetails']['country']['description']
            del self.__payload['buyer']['address']['addressDetails']['country']['scheme']
            del self.__payload['buyer']['address']['addressDetails']['region']['description']
            del self.__payload['buyer']['address']['addressDetails']['region']['scheme']

        return self.__payload

    def get_tender_classification_id(self):
        return self.__tender_classification_id

    def delete_optional_fields(self, *args, item_position=0, additional_classification_position=0,
                               buyer_additional_identifiers_position=0):
        """Call this method last, but before 'build_payload' method! Delete option fields from payload."""

        for a in args:
            if a == "tender.description":
                del self.__payload['tender']['description']

            elif a == "tender.items":
                del self.__payload['tender']['items']
            elif a == "tender.items.additionalClassifications":
                del self.__payload['tender']['items'][item_position]['additionalClassifications']
            elif a == f"tender.items.additionalClassifications[{additional_classification_position}]":

                del self.__payload['tender']['items'][item_position][
                    'additionalClassifications'][additional_classification_position]

            elif a == "tender.items.deliveryAddress.streetAddress":
                del self.__payload['tender']['items'][item_position]['deliveryAddress']['streetAddress']
            elif a == "tender.items.deliveryAddress.postalCode":
                del self.__payload['tender']['items'][item_position]['deliveryAddress']['postalCode']
            elif a == "tender.items.deliveryAddress.addressDetails.locality":
                del self.__payload['tender']['items'][item_position]['deliveryAddress']['addressDetails']['locality']
            elif a == "tender.items.deliveryAddress.addressDetails.locality.uri":
                del self.__payload['tender']['items'][item_position]['deliveryAddress']['addressDetails']['locality'][
                    'uri']

            elif a == "planning.rationale":
                del self.__payload['planning']['rationale']

            elif a == "buyer.identifier.uri":
                del self.__payload['buyer']['identifier']['uri']
            elif a == "buyer.address.postalCode":
                del self.__payload['buyer']['address']['postalCode']
            elif a == "buyer.additionalIdentifiers":
                del self.__payload['buyer']['additionalIdentifiers']
            elif a == "buyer.additionalIdentifiers.uri":
                del self.__payload['buyer']['additionalIdentifiers'][buyer_additional_identifiers_position]['uri']
            elif a == "buyer.contactPoint.faxNumber":
                del self.__payload['buyer']['contactPoint']['faxNumber']
            elif a == "buyer.contactPoint.url":
                del self.__payload['buyer']['contactPoint']['url']
            elif a == "buyer.details":
                del self.__payload['buyer']['details']
            elif a == "buyer.details.typeOfBuyer":
                del self.__payload['buyer']['details']['typeOfBuyer']
            elif a == "buyer.details.mainGeneralActivity":
                del self.__payload['buyer']['details']['mainGeneralActivity']
            elif a == "buyer.details.mainSectoralActivity":
                del self.__payload['buyer']['details']['mainSectoralActivity']

            else:
                KeyError(f"Impossible to delete attribute by path {a}.")

    def customize_tender_items(self, quantity_of_items, quantity_of_items_additional_classifications):
        """
        The max quantity of items must be 5, because it depends on cpvs_tuple from data_of_enum.
        """
        new_items_array = generate_items_array(
            quantity_of_object=quantity_of_items,
            item_object=copy.deepcopy(self.__payload['tender']['items'][0]),
            tender_classification_id=self.__tender_classification_id
        )

        for q_0 in range(quantity_of_items):

            affordable_schemes = get_affordable_schemes(self.__country)

            new_items_array[q_0]['description'] = f"create ei: tender.items[{q_0}].description"

            new_items_array[q_0]['deliveryAddress']['streetAddress'] = \
                f"create ei: tender.items[{q_0}].deliveryAddress.streetAddress"

            new_items_array[q_0]['deliveryAddress']['postalCode'] = \
                f"create ei: tender.items[{q_0}].deliveryAddress.postalCode"

            new_items_array[q_0]['deliveryAddress']['addressDetails']['country']['scheme'] = affordable_schemes[1]
            new_items_array[q_0]['deliveryAddress']['addressDetails']['region']['scheme'] = affordable_schemes[2]
            new_items_array[q_0]['deliveryAddress']['addressDetails']['region']['id'] = affordable_schemes[3]
            new_items_array[q_0]['deliveryAddress']['addressDetails']['locality']['scheme'] = affordable_schemes[4]
            new_items_array[q_0]['deliveryAddress']['addressDetails']['locality']['id'] = affordable_schemes[5]

            new_items_array[q_0]['unit']['id'] = f"{random.choice(unit_id_tuple)}"
            del new_items_array[q_0]['additionalClassifications'][0]

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

        self.__payload['tender']['items'] = new_items_array

    def customize_buyer_additional_identifiers(self, quantity_of_buyer_additional_identifiers):
        new_additional_identifiers_array = list()
        for q in range(quantity_of_buyer_additional_identifiers):
            new_additional_identifiers_array.append(copy.deepcopy(self.__payload['buyer']['additionalIdentifiers'][0]))
            new_additional_identifiers_array[q]['id'] = f"create ei: buyer.additionalIdentifiers{q}.id"
            new_additional_identifiers_array[q]['scheme'] = f"create ei: buyer.additionalIdentifiers{q}.scheme"
            new_additional_identifiers_array[q]['legalName'] = f"create ei: buyer.additionalIdentifiers{q}.legalName"
            new_additional_identifiers_array[q]['uri'] = f"create ei: buyer.additionalIdentifiers{q}.uri"

        self.__payload['buyer']['additionalIdentifiers'] = new_additional_identifiers_array

    def __del__(self):
        print(f"The instance of ExpenditureItemPayload class: {__name__} was deleted.")
