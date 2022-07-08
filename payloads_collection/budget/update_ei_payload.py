import copy
import json
import random
import re

from data_collection.Budget.for_test_updateEI_process.payload_full_model import payload_model
from data_collection.data_constant import unit_id_tuple, cpvs_tuple


from functions_collection.cassandra_methods import get_value_from_ocds_budgetrules
from functions_collection.prepare_date import ei_period
from functions_collection.some_functions import generate_items_array, get_affordable_schemes


class UpdateExpenditureItemPayload:
    def __init__(self, connect_to_ocds, country, tender_classification_id, amount):

        __ei_period = ei_period()
        self.__tender_classification_id = tender_classification_id
        self.__payload = copy.deepcopy(payload_model)
        self.__country = country

        # Since we work with two country Moldova and Litua, we should to correct some attribute.
        # It depends on country value and according with payload data model from documentation.
        presence_ei_amount = json.loads(
            get_value_from_ocds_budgetrules(connect_to_ocds, f"{country}-updateEI", "presenceEIAmount")
        )

        if presence_ei_amount is False:
            # If delete 'self.__payload['planning']['budget']['amount']', service return error.
            del self.__payload['planning']['budget']
        elif presence_ei_amount is True:
            self.__payload['planning']['budget']['amount']['amount'] = amount
        else:
            raise ValueError(f"Error in payload! Invalid SQL request: 'ocds.budget_rules'.")

        del self.__payload['tender']['items']

    def build_payload(self):

        # For business needs: Republic of Moldova uses the specific payload model.
        if self.__country == "MD":

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

        return self.__payload

    def delete_optional_fields(self, *args, item_position=0, additional_classification_position=0):
        """Call this method last, but before 'build_payload' method! Delete option fields from payload."""

        for a in args:
            if a == "planning":
                del self.__payload['planning']
            elif a == "planning.rationale":
                del self.__payload['planning']['rationale']
            elif a == "planning.budget":
                del self.__payload['planning']['budget']

            elif a == "tender":
                del self.__payload['tender']
            elif a == "tender.description":
                del self.__payload['tender']['description']
            elif a == "tender.title":
                del self.__payload['tender']['title']
            elif a == "tender.items":
                del self.__payload['tender']['items']
            elif a == f"tender.items[{item_position}]":
                del self.__payload['tender']['items'][{item_position}]
            elif a == f"tender.items[{item_position}].additionalClassifications":
                del self.__payload['tender']['items'][item_position]['additionalClassifications']
            elif a == f"tender.items[{item_position}].additionalClassifications[{additional_classification_position}]":
                del self.__payload['tender']['items'][item_position][
                    'additionalClassifications'][additional_classification_position]
            elif a == f"tender.items[{item_position}].deliveryAddress.streetAddress":
                del self.__payload['tender']['items'][item_position]['deliveryAddress']['streetAddress']
            elif a == f"tender.items[{item_position}].deliveryAddress.postalCode":
                del self.__payload['tender']['items'][item_position]['deliveryAddress']['postalCode']
            elif a == f"tender.items[{item_position}].deliveryAddress.addressDetails.locality":
                del self.__payload['tender']['items'][item_position]['deliveryAddress']['addressDetails']['locality']
            elif a == f"tender.items[{item_position}].deliveryAddress.addressDetails.locality.uri":
                del self.__payload['tender']['items'][item_position]['deliveryAddress']['addressDetails']['locality'][
                    'uri']

            else:
                KeyError(f"Impossible to delete attribute by path {a}.")

    def add_new_tender_items(self, quantity_of_items, quantity_of_new_additional_classifications):
        """
        The max quantity of items must be 5, because it depends on cpvs_tuple from data_of_enum.
        """
        item_object = copy.deepcopy(payload_model['tender']['items'][0])
        affordable_schemes = get_affordable_schemes(self.__country)

        item_object['classification']['id'] = self.__tender_classification_id
        item_object['deliveryAddress']['addressDetails']['country']['scheme'] = affordable_schemes[1]
        item_object['deliveryAddress']['addressDetails']['country']['id'] = self.__country
        item_object['deliveryAddress']['addressDetails']['region']['scheme'] = affordable_schemes[2]
        item_object['deliveryAddress']['addressDetails']['region']['id'] = affordable_schemes[3]
        item_object['deliveryAddress']['addressDetails']['locality']['scheme'] = affordable_schemes[4]
        item_object['deliveryAddress']['addressDetails']['locality']['id'] = affordable_schemes[5]

        new_items_array = generate_items_array(
            quantity_of_object=quantity_of_items,
            item_object=copy.deepcopy(item_object),
            tender_classification_id=self.__tender_classification_id
        )

        for q_0 in range(quantity_of_items):

            affordable_schemes = get_affordable_schemes(self.__country)

            new_items_array[q_0]['description'] = f"update ei: tender.items[{q_0}].description"

            new_items_array[q_0]['deliveryAddress']['streetAddress'] = \
                f"update ei: tender.items[{q_0}].deliveryAddress.streetAddress"

            new_items_array[q_0]['deliveryAddress']['postalCode'] = \
                f"update ei: tender.items[{q_0}].deliveryAddress.postalCode"

            new_items_array[q_0]['deliveryAddress']['addressDetails']['country']['scheme'] = affordable_schemes[1]
            new_items_array[q_0]['deliveryAddress']['addressDetails']['region']['scheme'] = affordable_schemes[2]
            new_items_array[q_0]['deliveryAddress']['addressDetails']['region']['id'] = affordable_schemes[3]
            new_items_array[q_0]['deliveryAddress']['addressDetails']['locality']['scheme'] = affordable_schemes[4]
            new_items_array[q_0]['deliveryAddress']['addressDetails']['locality']['id'] = affordable_schemes[5]

            new_items_array[q_0]['unit']['id'] = f"{random.choice(unit_id_tuple)}"
            del new_items_array[q_0]['additionalClassifications'][0]

            list_of_additional_classification_id = list()
            for q_1 in range(quantity_of_new_additional_classifications):
                new_items_array[q_0]['additionalClassifications'].append(
                    copy.deepcopy(payload_model['tender']['items'][0]['additionalClassifications'][0]))

                while len(list_of_additional_classification_id) < quantity_of_new_additional_classifications:
                    additional_classification_id = f"{random.choice(cpvs_tuple)}"
                    if additional_classification_id not in list_of_additional_classification_id:
                        list_of_additional_classification_id.append(additional_classification_id)

            for q_1 in range(quantity_of_new_additional_classifications):
                new_items_array[q_0]['additionalClassifications'][q_1]['id'] = \
                    list_of_additional_classification_id[q_1]

        if "items" not in self.__payload['tender']:
            self.__payload['tender']['items'] = list()

        self.__payload['tender']['items'] += new_items_array

    def update_old_tender_items(
            self, *previous_item_id, previous_items_list, quantity_of_new_additional_classifications):

        for i in previous_item_id:
            for previous_item in range(len(previous_items_list)):
                if i == previous_items_list[previous_item]['id']:
                    previous_item_object = copy.deepcopy(previous_items_list[previous_item])

                    # If previous_items_list was got from release, should delete redundant attribute,
                    # according to payload data model.
                    if "description" in previous_item_object['classification']:
                        del previous_item_object['classification']['description']

                    previous_item_object['description'] = f"update ei: tender.items[{i}].description"
                    previous_item_object['quantity'] = 44.44

                    # Set new unit.id.
                    unit_id = copy.deepcopy(previous_item_object['unit']['id'])
                    while unit_id == previous_item_object['unit']['id']:
                        unit_id = f"{random.choice(unit_id_tuple)}"
                    previous_item_object['unit']['id'] = unit_id

                    # If previous_items_list was got from release, should delete redundant attribute,
                    # according to payload data model.
                    if "name" in previous_item_object['unit']:
                        del previous_item_object['unit']['name']

                    # Add additionalClassifications, if 'additionalClassifications' array
                    # isn't present into previous item object
                    # and add unique object, if 'additionalClassifications' array is present into previous item object.

                    if "additionalClassifications" not in previous_item_object:
                        new_additionalclassifications = list()

                        list_of_additional_classification_id = list()
                        for q_1 in range(quantity_of_new_additional_classifications):
                            new_additionalclassifications.append(
                                copy.deepcopy(payload_model['tender']['items'][0]['additionalClassifications'][0])
                            )

                            while len(list_of_additional_classification_id) < \
                                    quantity_of_new_additional_classifications:

                                additional_classification_id = f"{random.choice(cpvs_tuple)}"
                                if additional_classification_id not in list_of_additional_classification_id:
                                    list_of_additional_classification_id.append(additional_classification_id)

                        for q_1 in range(quantity_of_new_additional_classifications):
                            new_additionalclassifications[q_1]['id'] = list_of_additional_classification_id[q_1]

                        previous_item_object['additionalClassifications'] = new_additionalclassifications

                    else:
                        additionalclassifications_identifier = set()
                        for q_1 in range(len(previous_item_object['additionalClassifications'])):
                            identifier = \
                                f"{previous_item_object['additionalClassifications'][q_1]['scheme']}-" \
                                f"{previous_item_object['additionalClassifications'][q_1]['id']}"

                            additionalclassifications_identifier.add(identifier)

                        base_quantity = len(additionalclassifications_identifier)
                        base_additionalclassifications_identifier = copy.deepcopy(
                            additionalclassifications_identifier
                        )
                        while len(additionalclassifications_identifier) != \
                                base_quantity + quantity_of_new_additional_classifications:

                            new_additionalclassification_id = f"{random.choice(cpvs_tuple)}"
                            new_identifier = \
                                f"{previous_item_object['additionalClassifications'][0]['scheme']}-" \
                                f"{new_additionalclassification_id}"

                            additionalclassifications_identifier.add(new_identifier)

                        diff_identifier = list(
                            additionalclassifications_identifier - base_additionalclassifications_identifier
                        )

                        expected_additionalclassifications_list = list()
                        for q_1 in range(len(diff_identifier)):
                            expected_additionalclassifications_list.append(copy.deepcopy(
                                payload_model['tender']['items'][0]['additionalClassifications'][0]
                            ))

                            pattern = f"{previous_item_object['additionalClassifications'][0]['scheme']}"
                            add_class_scheme = re.search(pattern, diff_identifier[q_1]).group()
                            add_class_id = re.split(add_class_scheme, diff_identifier[q_1])[1][1:]

                            expected_additionalclassifications_list[q_1]['id'] = add_class_id
                            expected_additionalclassifications_list[q_1]['scheme'] = add_class_scheme

                        previous_item_object['additionalClassifications'] = expected_additionalclassifications_list

                    # Set random deliveryAddress object.
                    previous_item_object['deliveryAddress'] = copy.deepcopy(
                        payload_model['tender']['items'][0]['deliveryAddress']
                    )

                    previous_item_object['deliveryAddress']['streetAddress'] = \
                        f"update ei: tender.items[{i}].deliveryAddress.streetAddress"

                    previous_item_object['deliveryAddress']['postalCode'] = \
                        f"update ei: tender.items[{i}].deliveryAddress.postalCode"

                    affordable_schemes = get_affordable_schemes(self.__country)

                    previous_item_object['deliveryAddress']['addressDetails']['country']['id'] = self.__country
                    previous_item_object['deliveryAddress']['addressDetails']['region']['scheme'] = \
                        affordable_schemes[2]

                    previous_item_object['deliveryAddress']['addressDetails']['region']['id'] = \
                        affordable_schemes[3]

                    previous_item_object['deliveryAddress']['addressDetails']['locality']['scheme'] = \
                        affordable_schemes[4]

                    previous_item_object['deliveryAddress']['addressDetails']['locality']['id'] = affordable_schemes[5]

                    if "items" not in self.__payload['tender']:
                        self.__payload['tender']['items'] = list()

                    self.__payload['tender']['items'].append(previous_item_object)

    def __del__(self):
        print(f"The instance of ExpenditureItemPayload class: {__name__} was deleted.")
