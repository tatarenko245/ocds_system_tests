import copy
import random

from jsonschema import validate

from data_collection.data_constant import locality_scheme_tuple, typeOfBuyer_tuple, mainGeneralActivity_tuple, \
    mainSectoralActivity_tuple, region_id_tuple, unit_id_tuple, cpvs_tuple
from data_collection.for_test_createEI_process.payload_full_model import *
from functions_collection.prepare_date import ei_period
from functions_collection.some_functions import generate_items_array, get_locality_id_according_with_region_id
from payloads_collection.budget.temp_ei_scheme import ei_payload_scheme


class ExpenditureItemPayload:
    def __init__(self, country, buyer_id, tender_classification_id, amount=None, currency=None):

        __ei_period = ei_period()
        self.__tender_classification_id = tender_classification_id
        self.__payload = payload_model

        # Since we work with two country Moldova and Litua, we should to correct some attribute.
        # It depends on country value and according with payload data model from documentation.
        if country == "MD":
            del self.__payload['planning']['budget']['amount']
        elif country == "LT":
            self.__payload['planning']['budget']['amount']['amount'] = amount
            self.__payload['planning']['budget']['amount']['currency'] = currency
        else:
            raise ValueError(f"Error in payload! Invalid country value. Actual country = {country}")

        self.__payload['tender']['classification']['id'] = tender_classification_id
        self.__payload['tender']['items'][0]['classification']['id'] = tender_classification_id
        self.__payload['tender']['items'][0]['deliveryAddress']['addressDetails']['locality']['scheme'] = \
            f"{random.choice(locality_scheme_tuple)}"
        self.__payload['planning']['budget']['period']['startDate'] = __ei_period[0]
        self.__payload['planning']['budget']['period']['endDate'] = __ei_period[1]
        self.__payload['buyer']['identifier']['id'] = f"{buyer_id}"
        self.__payload['buyer']['address']['addressDetails']['locality']['scheme'] = \
            f"{random.choice(locality_scheme_tuple)}"
        self.__payload['buyer']['details']['typeOfBuyer'] = f"{random.choice(typeOfBuyer_tuple)}"
        self.__payload['buyer']['details']['mainGeneralActivity'] = f"{random.choice(mainGeneralActivity_tuple)}"
        self.__payload['buyer']['details']['mainSectoralActivity'] = f"{random.choice(mainSectoralActivity_tuple)}"

    def build_payload(self):
        validate(self.__payload, ei_payload_scheme['paths']['/do/ei']['post']['requestBody']['content'][
            'application/json']['schema'])

        return self.__payload

    def get_tender_classification_id(self):
        return self.__tender_classification_id

    def delete_optional_fields(self, *args):
        """Call this method last, but before 'build_payload' method! Delete option fields from payload."""
        for a in args:
            del self.__payload[a]

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

            new_items_array[q_0]['description'] = f"create ei: tender.items{q_0}.description"

            new_items_array[q_0]['deliveryAddress']['streetAddress'] = \
                f"create ei: tender.items{q_0}.deliveryAddress.streetAddress"

            new_items_array[q_0]['deliveryAddress']['postalCode'] = \
                f"create ei: tender.items{q_0}.deliveryAddress.postalCode"

            new_items_array[q_0]['deliveryAddress']['addressDetails']['region']['id'] = \
                f"{random.choice(region_id_tuple)}"

            new_items_array[q_0]['deliveryAddress']['addressDetails']['locality']['id'] = \
                get_locality_id_according_with_region_id(
                    new_items_array[q_0]['deliveryAddress']['addressDetails']['region']['id'])

            new_items_array[q_0]['deliveryAddress']['addressDetails']['locality']['scheme'] = \
                f"{random.choice(locality_scheme_tuple)}"

            new_items_array[q_0]['deliveryAddress']['addressDetails']['locality']['description'] = \
                f"create ei: tender.items{q_0}.deliveryAddress.addressDetails.locality.description"

            new_items_array[q_0]['deliveryAddress']['addressDetails']['locality']['uri'] = \
                f"create ei: tender.items{q_0}.deliveryAddress.addressDetails.locality.uri"

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
