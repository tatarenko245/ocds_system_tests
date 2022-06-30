"""Prepare the expected release of the update expenditure item process, budget."""
import copy

from data_collection.for_test_createEI_process.ei_release_full_model import *
from functions_collection.some_functions import get_value_from_cpvs_dictionary_csv, is_it_uuid, \
    get_value_from_classification_unit_dictionary_csv, \
    get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv, get_value_from_cpv_dictionary_csv


class ExpenditureItemRelease:
    """This class creates instance of release."""

    def __init__(self, environment, language, tender_classification_id):

        self.environment = environment
        self.language = language
        self.tender_classification_id = tender_classification_id
        self.expected_ei_release = copy.deepcopy(release_model)

        try:
            if environment == "dev":
                self.metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"

                self.extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"
                ]

                self.publisher_name = "M-Tender"
                self.publisher_uri = "https://www.mtender.gov.md"

            elif environment == "sandbox":
                self.metadata_budget_url = "http://public.eprocurement.systems/budgets"

                self.extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.json"
                ]

                self.publisher_name = "Viešųjų pirkimų tarnyba"
                self.publisher_uri = "https://vpt.lrv.lt"

        except ValueError:
            raise ValueError("Check your environment: You must use 'dev' or 'sandbox' environment.")

    def build_expected_ei_release(self, payload, message_for_platform, actual_ei_release, previous_ei_release):
        """Build EI release."""

        """Enrich general attribute for expected EI release"""
        # FR-10.3.1.3: get value from previous release.
        self.expected_ei_release['uri'] = previous_ei_release['uri']
        self.expected_ei_release['version'] = previous_ei_release['version']
        self.expected_ei_release['extensions'] = previous_ei_release['extensions']
        self.expected_ei_release['publisher']['name'] = previous_ei_release['publisher']['name']
        self.expected_ei_release['publisher']['uri'] = previous_ei_release['publisher']['uri']
        self.expected_ei_release['license'] = previous_ei_release['license']
        self.expected_ei_release['publicationPolicy'] = previous_ei_release['publicationPolicy']
        self.expected_ei_release['publishedDate'] = previous_ei_release['publishedDate']

        """Enrich general attribute for expected EI release: releases[0]"""
        # FR-10.3.1.3: get value from previous release.
        self.expected_ei_release['releases'][0]['ocid'] = previous_ei_release['releases'][0]['ocid']

        self.expected_ei_release['releases'][0]['id'] = f"{previous_ei_release['releases'][0]['id'][:28]}-" \
                                                        f"{actual_ei_release['releases'][0]['id'][29:42]}"

        self.expected_ei_release['releases'][0]['tag'] = previous_ei_release['releases'][0]['tag']
        self.expected_ei_release['releases'][0]['initiationType'] = previous_ei_release['releases'][0]['initiationType']
        self.expected_ei_release['releases'][0]['language'] = previous_ei_release['releases'][0]['language']

        # FR-10.3.1.1: Set date.
        self.expected_ei_release['releases'][0]['date'] = message_for_platform['data']['operationDate']

        """Enrich attribute for expected EI release: releases[0].planning"""
        # FR-10.3.1.3: get value from previous release.
        self.expected_ei_release['releases'][0]['planning']['budget']['id'] = \
            previous_ei_release['releases'][0]['planning']['budget']['id']

        self.expected_ei_release['releases'][0]['planning']['budget']['period']['startDate'] = \
            previous_ei_release['releases'][0]['planning']['budget']['period']['startDate']

        self.expected_ei_release['releases'][0]['planning']['budget']['period']['endDate'] = \
            previous_ei_release['releases'][0]['planning']['budget']['period']['endDate']

        if "planning" in payload:
            # Set planning.rationale:
            # FR.COM-14.1.2: is present in payload.
            if "rationale" in payload['planning']:
                self.expected_ei_release['releases'][0]['planning']['rationale'] = payload['planning']['rationale']
            # FR.COM-14.1.1: isn't present in payload.
            else:
                # FR-10.3.1.3: get value from previous release.
                if "rationale" in previous_ei_release['releases'][0]['planning']:
                    self.expected_ei_release['releases'][0]['planning']['rationale'] = \
                        previous_ei_release['releases'][0]['planning']['rationale']
                else:
                    del self.expected_ei_release['releases'][0]['planning']['rationale']

            if "budget" in payload['planning']:
                # Set amount:
                # FR.COM-14.1.3: is present in payload.
                if "amount" in payload['planning']['budget']:

                    self.expected_ei_release['releases'][0]['planning']['budget']['amount']['amount'] = \
                        payload['planning']['budget']['amount']['amount']

                    self.expected_ei_release['releases'][0]['planning']['budget']['amount']['currency'] = \
                        previous_ei_release['releases'][0]['planning']['budget']['amount']['currency']
                else:
                    # FR-10.3.1.3: get value from previous release.
                    if "amount" in previous_ei_release['releases'][0]['planning']['budget']:
                        self.expected_ei_release['releases'][0]['planning']['budget']['amount'] = \
                            previous_ei_release['releases'][0]['planning']['budget']['amount']
                    else:
                        del self.expected_ei_release['releases'][0]['planning']['budget']['amount']
            else:
                # FR-10.3.1.3: get value from previous release.
                if "amount" in previous_ei_release['releases'][0]['planning']['budget']:
                    self.expected_ei_release['releases'][0]['planning']['budget']['amount'] = \
                        previous_ei_release['releases'][0]['planning']['budget']['amount']
                else:
                    del self.expected_ei_release['releases'][0]['planning']['budget']['amount']
        else:
            # FR-10.3.1.3: get value from previous release.
            if "planning" in previous_ei_release['releases'][0]:
                self.expected_ei_release['releases'][0]['planning'] = previous_ei_release['releases'][0]['planning']
            else:
                del self.expected_ei_release['releases'][0]['planning']

        """Enrich attribute for expected EI release: releases[0].parties"""
        # BR-10.3.1.1: Set parties.
        self.expected_ei_release['releases'][0]['parties'] = previous_ei_release['releases'][0]['parties']

        """Enrich attribute for expected EI release: releases[0].tender"""
        # FR-10.3.1.3: get value from previous release.
        self.expected_ei_release['releases'][0]['tender']['id'] = previous_ei_release['releases'][0]['tender']['id']

        self.expected_ei_release['releases'][0]['tender']['status'] = \
            previous_ei_release['releases'][0]['tender']['status']

        self.expected_ei_release['releases'][0]['tender']['mainProcurementCategory'] = \
            previous_ei_release['releases'][0]['tender']['mainProcurementCategory']

        self.expected_ei_release['releases'][0]['tender']['classification']['id'] = \
            previous_ei_release['releases'][0]['tender']['classification']['id']

        self.expected_ei_release['releases'][0]['tender']['classification']['description'] = \
            previous_ei_release['releases'][0]['tender']['classification']['description']

        self.expected_ei_release['releases'][0]['tender']['classification']['scheme'] = \
            previous_ei_release['releases'][0]['tender']['classification']['scheme']

        # Set title.
        # FR.COM-14.1.4: is present in payload.
        if "title" in payload['tender']:
            self.expected_ei_release['releases'][0]['tender']['title'] = payload['tender']['title']
        else:
            # FR-10.3.1.3: get value from previous release.
            if "title" in previous_ei_release['releases'][0]['tender']:

                self.expected_ei_release['releases'][0]['tender']['title'] = \
                    previous_ei_release['releases'][0]['tender']['title']
            else:
                del self.expected_ei_release['releases'][0]['tender']['title']

        # Set description.
        # FR.COM-14.1.5, FR.COM-14.1.6: is present in payload.
        if "description" in payload['tender']:
            self.expected_ei_release['releases'][0]['tender']['description'] = payload['tender']['description']
        else:
            # FR-10.3.1.3: get value from previous release.
            if "description" in previous_ei_release['releases'][0]['tender']:

                self.expected_ei_release['releases'][0]['tender']['description'] = \
                    previous_ei_release['releases'][0]['tender']['description']
            else:
                del self.expected_ei_release['releases'][0]['tender']['description']

        # Set items.
        if "items" in previous_ei_release['releases'][0]['tender']:
            if "items" in payload['tender']:
                previous_items_array = previous_ei_release['releases'][0]['tender']['items']

                # Check what kind of the item object is present into payload (old or new).
                previous_release_items_id = list()
                for q in range(len(previous_items_array)):
                    previous_release_items_id.append(previous_items_array[q]['id'])

                payload_items_id = list()
                for q in range(len(payload['tender']['items'])):
                    payload_items_id.append(payload['tender']['items'][q]['id'])

                expected_items_array = list()

                # Get items objects from previous release, which should be copied with data from previous release.
                items_id_for_copied = list(set(previous_release_items_id) - set(payload_items_id))

                for i in range(len(items_id_for_copied)):
                    for previous in range(len(previous_items_array)):
                        if items_id_for_copied[i] == previous_items_array[previous]['id']:
                            expected_items_array.append(previous_items_array[previous])

                # Get items objects from previous release, which should be update with data from payload or
                # which should be copied with data from previous release.
                items_id_for_updating = list(set(previous_release_items_id) & set(payload_items_id))

                for i in range(len(items_id_for_updating)):
                    for actual in range(len(payload['tender']['items'])):
                        for previous in range(len(previous_items_array)):
                            if items_id_for_updating[i] == payload['tender']['items'][actual]['id'] == \
                                    previous_items_array[previous]['id']:

                                # FR.COM-14.1.9: Update description.
                                previous_items_array[previous]['description'] = \
                                    payload['tender']['items'][actual]['description']

                                # FR.COM-14.1.10: Update additionalClassifications.
                                if "additionalClassifications" in payload['tender']['items'][actual]:
                                    expected_additionalclassifications_array = list()

                                    # Check what kind of the additionalClassification object is present into
                                    # payload (old or new).
                                    previous_release_additionalclassification_id = list()

                                    for q in range(len(previous_items_array[previous]['additionalClassifications'])):
                                        previous_release_additionalclassification_id.append(
                                            previous_items_array[previous]['additionalClassifications'][q]['id']
                                        )

                                    payload_additionalclassification_id = list()
                                    for q in range(len(
                                            payload['tender']['items'][actual]['additionalClassifications']
                                            )
                                    ):
                                        payload_additionalclassification_id.append(
                                            payload['tender']['items'][actual]['additionalClassifications'][q]['id']
                                        )

                                    # Get additionalClassifications objects of item from payload,
                                    # which should be copied to actual release with data from previous release.
                                    additionalclassification_id_for_copied = list(
                                        set(previous_release_additionalclassification_id) -
                                        set(payload_additionalclassification_id)
                                    )

                                    for y in range(len(additionalclassification_id_for_copied)):
                                        for q in range(len(
                                                previous_items_array[previous]['additionalClassifications']
                                                )
                                        ):
                                            if additionalclassification_id_for_copied[y] == \
                                                    previous_items_array[previous]['additionalClassifications'][q][
                                                        'id']:

                                                expected_additionalclassifications_array.append(
                                                    previous_items_array[previous]['additionalClassifications'][q]
                                                )

                                    # Get additionalClassifications objects of item from payload,
                                    # which should be add to actual release with data from payload.
                                    additionalclassification_id_for_add = list(
                                        set(payload_additionalclassification_id) -
                                        set(previous_release_additionalclassification_id)
                                    )

                                    for y in range(len(additionalclassification_id_for_add)):
                                        for q in range(len(
                                                payload['tender']['items'][actual]['additionalClassifications']
                                                )
                                        ):
                                            if additionalclassification_id_for_add[y] == \
                                                    payload['tender']['items'][actual]['additionalClassifications'][q][
                                                        'id']:

                                                additionalclassification_object = copy.deepcopy(
                                                    release_model['releases'][0]['tender']['items'][0][
                                                        'additionalClassifications'][0]
                                                )

                                                expected_cpvs_data = get_value_from_cpvs_dictionary_csv(
                                                    cpvs=payload['tender']['items'][actual][
                                                        'additionalClassifications'][q]['id'],
                                                    language=self.language
                                                )

                                                additionalclassification_object['scheme'] = payload['tender'][
                                                    'items'][actual]['additionalClassifications'][q]['scheme']

                                                additionalclassification_object['id'] = expected_cpvs_data[0]
                                                additionalclassification_object['description'] = expected_cpvs_data[2]

                                                expected_additionalclassifications_array.append(
                                                    additionalclassification_object
                                                )

                                    # Sort objects in expected additionalClassifications array.
                                    for a_0 in range(len(actual_ei_release['releases'][0]['tender']['items'])):
                                        if actual_ei_release['releases'][0]['tender']['items'][a_0]['id'] == \
                                                previous_items_array[previous]['id']:

                                            temp_array = list()

                                            for a_1 in range(len(
                                                    actual_ei_release['releases'][0]['tender']['items'][a_0][
                                                        'additionalClassifications']
                                                    )
                                            ):

                                                for e_1 in range(len(expected_additionalclassifications_array)):

                                                    if actual_ei_release['releases'][0]['tender']['items'][a_0][
                                                            'additionalClassifications'][a_1]['id'] == \
                                                            expected_additionalclassifications_array[e_1]['id']:

                                                        temp_array.append(expected_additionalclassifications_array[e_1])

                                            expected_additionalclassifications_array = temp_array

                                    # Set additionalClassifications.
                                    previous_items_array[previous]['additionalClassifications'] = \
                                        expected_additionalclassifications_array

                                else:
                                    # FR-10.3.1.3: get value from previous release.
                                    if "additionalClassifications" in \
                                            previous_ei_release['releases'][0]['tender']['items'][previous]:

                                        self.expected_ei_release['releases'][0]['tender']['items'][previous][
                                            'additionalClassifications'] = \
                                            previous_ei_release['releases'][0]['tender']['items'][previous][
                                            'additionalClassifications']
                                    else:
                                        del self.expected_ei_release['releases'][0]['tender']['items'][previous][
                                            'additionalClassifications']

                                # FR.COM-14.1.11: Update quantity.
                                previous_items_array[previous]['quantity'] = \
                                    payload['tender']['items'][actual]['quantity']

                                # FR.COM-14.1.12: Update unit.
                                expected_unit_data = get_value_from_classification_unit_dictionary_csv(
                                    unit_id=payload['tender']['items'][actual]['unit']['id'],
                                    language=self.language
                                )

                                previous_items_array[previous]['unit']['id'] = expected_unit_data[0]
                                previous_items_array[previous]['unit']['name'] = expected_unit_data[1]

                                # FR.COM-14.1.13: Update deliveryAddress.
                                previous_items_array[previous]['deliveryAddress']['streetAddress'] = \
                                    payload['tender']['items'][actual]['deliveryAddress']['streetAddress']

                                if "postalCode" in payload['tender']['items'][actual]['deliveryAddress']:

                                    previous_items_array[previous]['deliveryAddress']['postalCode'] = \
                                        payload['tender']['items'][actual]['deliveryAddress']['postalCode']

                                # Prepare addressDetails object for items array.
                                try:
                                    item_country_data = get_value_from_country_csv(

                                        country=payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                            'country']['id'],
                                        language=self.language
                                    )
                                    expected_item_country_object = [{
                                        "scheme": item_country_data[2].upper(),
                                        "id": payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                            'country']['id'],

                                        "description": item_country_data[1],
                                        "uri": item_country_data[3]
                                    }]

                                    item_region_data = get_value_from_region_csv(

                                        region=payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                            'region']['id'],
                                        country=payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                            'country']['id'],
                                        language=self.language
                                    )
                                    expected_item_region_object = [{
                                        "scheme": item_region_data[2],

                                        "id": payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                            'region']['id'],

                                        "description": item_region_data[1],
                                        "uri": item_region_data[3]
                                    }]

                                    if "locality" in payload['tender']['items'][actual]['deliveryAddress'][
                                            'addressDetails']:

                                        if payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                                'locality']['scheme'] != "other":

                                            item_locality_data = get_value_from_locality_csv(

                                                locality=payload['tender']['items'][actual]['deliveryAddress'][
                                                    'addressDetails']['locality']['id'],
                                                region=payload['tender']['items'][actual]['deliveryAddress'][
                                                    'addressDetails']['region']['id'],
                                                country=payload['tender']['items'][actual]['deliveryAddress'][
                                                    'addressDetails']['country']['id'],
                                                language=self.language
                                            )
                                            expected_item_locality_object = [{
                                                "scheme": item_locality_data[2],

                                                "id": payload['tender']['items'][actual]['deliveryAddress'][
                                                    'addressDetails']['locality']['id'],

                                                "description": item_locality_data[1],
                                                "uri": item_locality_data[3]
                                            }]
                                        else:
                                            expected_item_locality_object = [{

                                                "scheme":
                                                    payload['tender']['items'][actual]['deliveryAddress'][
                                                        'addressDetails']['locality']['scheme'],

                                                "id": payload['tender']['items'][actual]['deliveryAddress'][
                                                    'addressDetails']['locality']['id'],

                                                "description": payload['tender']['items'][actual]['deliveryAddress'][
                                                    'addressDetails']['locality']['description']
                                            }]

                                        previous_items_array[previous]['deliveryAddress']['addressDetails'][
                                            'locality'] = expected_item_locality_object[0]
                                    else:
                                        del previous_items_array[previous]['deliveryAddress']['addressDetails'][
                                            'locality']

                                    previous_items_array[previous]['deliveryAddress']['addressDetails']['country'] = \
                                        expected_item_country_object[0]

                                    previous_items_array[previous]['deliveryAddress']['addressDetails']['region'] = \
                                        expected_item_region_object[0]
                                except ValueError:
                                    ValueError("Impossible to prepare addressDetails object for items array")

                                expected_items_array.append(previous_items_array[previous])

                # Get items objects from payload, which should be add to actual release with data from payload.
                items_id_for_add = list(set(payload_items_id) - set(previous_release_items_id))

                for i in range(len(items_id_for_add)):
                    for actual in range(len(payload['tender']['items'])):
                        if items_id_for_add[i] == payload['tender']['items'][actual]['id']:

                            new_item_object = copy.deepcopy(release_model['releases'][0]['tender']['items'][0])

                            new_item_object['description'] = payload['tender']['items'][actual]['description']

                            expected_cpv_data = get_value_from_cpv_dictionary_csv(
                                cpv=payload['tender']['items'][actual]['classification']['id'],
                                language=self.language
                            )
                            new_item_object['classification']['scheme'] = "CPV"
                            new_item_object['classification']['id'] = expected_cpv_data[0]
                            new_item_object['classification']['description'] = expected_cpv_data[1]

                            if "additionalClassifications" in payload['tender']['items'][actual]:
                                new_item_additional_classifications_array = list()

                                for q_1 in range(len(payload['tender']['items'][actual]['additionalClassifications'])):
                                    new_item_additional_classifications_array.append(copy.deepcopy(
                                        release_model['releases'][0]['tender']['items'][0][
                                            'additionalClassifications'][0]))

                                    expected_cpvs_data = get_value_from_cpvs_dictionary_csv(
                                        cpvs=payload['tender']['items'][actual]['additionalClassifications'][q_1]['id'],
                                        language=self.language
                                    )

                                    new_item_additional_classifications_array[q_1]['scheme'] = "CPVS"
                                    new_item_additional_classifications_array[q_1]['id'] = expected_cpvs_data[0]

                                    new_item_additional_classifications_array[q_1]['description'] = \
                                        expected_cpvs_data[2]

                                new_item_object['additionalClassifications'] = new_item_additional_classifications_array
                            else:
                                del new_item_object['additionalClassifications']

                            new_item_object['quantity'] = int(float(
                                payload['tender']['items'][actual]['quantity']
                            ))

                            expected_unit_data = get_value_from_classification_unit_dictionary_csv(
                                unit_id=payload['tender']['items'][actual]['unit']['id'],
                                language=self.language
                            )

                            new_item_object['unit']['id'] = expected_unit_data[0]
                            new_item_object['unit']['name'] = expected_unit_data[1]

                            new_item_object['deliveryAddress']['streetAddress'] = \
                                payload['tender']['items'][actual]['deliveryAddress']['streetAddress']

                            if "postalCode" in payload['tender']['items'][actual]['deliveryAddress']:
                                new_item_object['deliveryAddress']['postalCode'] = \
                                    payload['tender']['items'][actual]['deliveryAddress']['postalCode']
                            else:
                                del new_item_object['deliveryAddress']['postalCode']

                            # Prepare addressDetails object for items array.
                            try:
                                item_country_data = get_value_from_country_csv(

                                    country=payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                        'country']['id'],
                                    language=self.language
                                )
                                expected_item_country_object = [{
                                    "scheme": item_country_data[2].upper(),
                                    "id": payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                        'country']['id'],

                                    "description": item_country_data[1],
                                    "uri": item_country_data[3]
                                }]

                                item_region_data = get_value_from_region_csv(

                                    region=payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                        'region']['id'],
                                    country=payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                        'country']['id'],
                                    language=self.language
                                )
                                expected_item_region_object = [{
                                    "scheme": item_region_data[2],

                                    "id": payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                        'region']['id'],

                                    "description": item_region_data[1],
                                    "uri": item_region_data[3]
                                }]

                                if "locality" in payload['tender']['items'][actual]['deliveryAddress'][
                                        'addressDetails']:
                                    if payload['tender']['items'][actual]['deliveryAddress']['addressDetails'][
                                            'locality']['scheme'] != "other":

                                        item_locality_data = get_value_from_locality_csv(

                                            locality=payload['tender']['items'][actual]['deliveryAddress'][
                                                'addressDetails']['locality']['id'],
                                            region=payload['tender']['items'][actual]['deliveryAddress'][
                                                'addressDetails']['region']['id'],
                                            country=payload['tender']['items'][actual]['deliveryAddress'][
                                                'addressDetails']['country']['id'],
                                            language=self.language
                                        )
                                        expected_item_locality_object = [{
                                            "scheme": item_locality_data[2],

                                            "id": payload['tender']['items'][actual]['deliveryAddress'][
                                                'addressDetails'][
                                                'locality']['id'],

                                            "description": item_locality_data[1],
                                            "uri": item_locality_data[3]
                                        }]
                                    else:
                                        expected_item_locality_object = [{

                                            "scheme": payload['tender']['items'][actual]['deliveryAddress'][
                                                'addressDetails'][
                                                'locality']['scheme'],

                                            "id": payload['tender']['items'][actual]['deliveryAddress'][
                                                'addressDetails'][
                                                'locality']['id'],

                                            "description": payload['tender']['items'][actual]['deliveryAddress'][
                                                'addressDetails']['locality']['description']
                                        }]

                                    new_item_object['deliveryAddress']['addressDetails']['locality'] = \
                                        expected_item_locality_object[0]
                                else:
                                    del new_item_object['deliveryAddress']['addressDetails']['locality']

                                new_item_object['deliveryAddress']['addressDetails']['country'] = \
                                    expected_item_country_object[0]

                                new_item_object['deliveryAddress']['addressDetails']['region'] = \
                                    expected_item_region_object[0]
                            except ValueError:
                                ValueError("Impossible to prepare addressDetails object for items array")

                            if new_item_object['id'] == "":
                                # FR.COM-14.1.7: Set id.
                                for a in range(len(actual_ei_release['releases'][0]['tender']['items'])):
                                    if actual_ei_release['releases'][0]['tender']['items'][a]['description'] == \
                                            new_item_object['description']:

                                        try:
                                            is_permanent_id_correct = is_it_uuid(
                                                actual_ei_release['releases'][0]['tender']['items'][a]['id']
                                            )
                                            if is_permanent_id_correct is True:

                                                new_item_object['id'] = \
                                                    actual_ei_release['releases'][0]['tender']['items'][a]['id']
                                            else:
                                                new_item_object['id'] = \
                                                    f"FR.COM-14.1.7: the 'releases[0].tender.items[{a}].id' " \
                                                    f"must be uuid."
                                        except KeyError:
                                            KeyError(f"Mismatch key into path 'releases[0].tender.items[{a}].id'")
                            expected_items_array.append(new_item_object)

                # Sort objects in expected items array.
                temp_array = list()
                for a in range(len(actual_ei_release['releases'][0]['tender']['items'])):
                    for e in range(len(expected_items_array)):

                        if actual_ei_release['releases'][0]['tender']['items'][a]['id'] == \
                                expected_items_array[e]['id']:

                            temp_array.append(expected_items_array[e])

                expected_items_array = temp_array

                self.expected_ei_release['releases'][0]['tender']['items'] = expected_items_array
            else:
                self.expected_ei_release['releases'][0]['tender']['items'] = \
                    previous_ei_release['releases'][0]['tender']['items']
        else:
            # FR.COM-14.1.8: Add new items.
            if "items" in payload['tender']:
                try:
                    # Build the releases.tender.items array.
                    new_items_array = list()
                    for q_0 in range(len(payload['tender']['items'])):

                        new_items_array.append(copy.deepcopy(
                            release_model['releases'][0]['tender']['items'][0]))

                        # Enrich or delete optional fields:
                        if "additionalClassifications" in payload['tender']['items'][q_0]:
                            new_item_additional_classifications_array = list()
                            for q_1 in range(len(payload['tender']['items'][q_0]['additionalClassifications'])):
                                new_item_additional_classifications_array.append(copy.deepcopy(
                                    release_model['releases'][0]['tender']['items'][0][
                                        'additionalClassifications'][0]))

                                expected_cpvs_data = get_value_from_cpvs_dictionary_csv(
                                    cpvs=payload['tender']['items'][q_0]['additionalClassifications'][q_1]['id'],
                                    language=self.language
                                )

                                new_item_additional_classifications_array[q_1]['scheme'] = "CPVS"
                                new_item_additional_classifications_array[q_1]['id'] = expected_cpvs_data[0]
                                new_item_additional_classifications_array[q_1]['description'] = expected_cpvs_data[2]

                            new_items_array[q_0]['additionalClassifications'] = \
                                new_item_additional_classifications_array
                        else:
                            del new_items_array[q_0]['additionalClassifications']

                        # FR.COM-14.1.7: Set id.
                        try:
                            is_permanent_id_correct = is_it_uuid(
                                actual_ei_release['releases'][0]['tender']['items'][q_0]['id']
                            )
                            if is_permanent_id_correct is True:

                                new_items_array[q_0]['id'] = \
                                    actual_ei_release['releases'][0]['tender']['items'][q_0]['id']
                            else:
                                new_items_array[q_0]['id'] = \
                                    f"FR.COM-14.1.7: the 'releases[0].tender.items[{q_0}].id' must be uuid."
                        except KeyError:
                            KeyError(f"Mismatch key into path 'releases[0].tender.items[{q_0}].id'")

                        new_items_array[q_0]['description'] = payload['tender']['items'][q_0]['description']

                        expected_cpv_data = get_value_from_cpv_dictionary_csv(
                            cpv=payload['tender']['items'][q_0]['classification']['id'],
                            language=self.language
                        )
                        new_items_array[q_0]['classification']['scheme'] = "CPV"
                        new_items_array[q_0]['classification']['id'] = expected_cpv_data[0]
                        new_items_array[q_0]['classification']['description'] = expected_cpv_data[1]
                        new_items_array[q_0]['quantity'] = int(float(payload['tender']['items'][q_0]['quantity']))

                        expected_unit_data = get_value_from_classification_unit_dictionary_csv(
                            unit_id=payload['tender']['items'][q_0]['unit']['id'],
                            language=self.language
                        )

                        new_items_array[q_0]['unit']['id'] = expected_unit_data[0]
                        new_items_array[q_0]['unit']['name'] = expected_unit_data[1]

                        new_items_array[q_0]['deliveryAddress']['streetAddress'] = \
                            payload['tender']['items'][q_0]['deliveryAddress']['streetAddress']

                        if "postalCode" in payload['tender']['items'][q_0]['deliveryAddress']:

                            new_items_array[q_0]['deliveryAddress']['postalCode'] = \
                                payload['tender']['items'][q_0]['deliveryAddress']['postalCode']
                        else:
                            del new_items_array[q_0]['deliveryAddress']['postalCode']

                        # Prepare addressDetails object for items array.
                        try:
                            item_country_data = get_value_from_country_csv(

                                country=payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'country']['id'],
                                language=self.language
                            )
                            expected_item_country_object = [{
                                "scheme": item_country_data[2].upper(),
                                "id": payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'country']['id'],

                                "description": item_country_data[1],
                                "uri": item_country_data[3]
                            }]

                            item_region_data = get_value_from_region_csv(

                                region=payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'region']['id'],
                                country=payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'country']['id'],
                                language=self.language
                            )
                            expected_item_region_object = [{
                                "scheme": item_region_data[2],

                                "id": payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                    'region']['id'],

                                "description": item_region_data[1],
                                "uri": item_region_data[3]
                            }]

                            if "locality" in payload['tender']['items'][q_0]['deliveryAddress']['addressDetails']:
                                if payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                        'locality']['scheme'] != "other":

                                    item_locality_data = get_value_from_locality_csv(

                                        locality=payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                            'locality']['id'],
                                        region=payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                            'region']['id'],
                                        country=payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                            'country']['id'],
                                        language=self.language
                                    )
                                    expected_item_locality_object = [{
                                        "scheme": item_locality_data[2],

                                        "id": payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                            'locality']['id'],

                                        "description": item_locality_data[1],
                                        "uri": item_locality_data[3]
                                    }]
                                else:
                                    expected_item_locality_object = [{

                                        "scheme": payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                            'locality']['scheme'],

                                        "id": payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                            'locality']['id'],

                                        "description": payload['tender']['items'][q_0]['deliveryAddress'][
                                            'addressDetails']['locality']['description']
                                    }]

                                new_items_array[q_0]['deliveryAddress']['addressDetails']['locality'] = \
                                    expected_item_locality_object[0]
                            else:
                                del new_items_array[q_0]['deliveryAddress']['addressDetails']['locality']

                            new_items_array[q_0]['deliveryAddress']['addressDetails']['country'] = \
                                expected_item_country_object[0]

                            new_items_array[q_0]['deliveryAddress']['addressDetails']['region'] = \
                                expected_item_region_object[0]
                        except ValueError:
                            ValueError("Impossible to prepare addressDetails object for items array")

                    self.expected_ei_release['releases'][0]['tender']['items'] = new_items_array
                except ValueError:
                    ValueError("Impossible to build the expected releases.tender.items array.")
            else:
                del self.expected_ei_release['releases'][0]['tender']['items']

        """Enrich attribute for expected EI release: releases[0].buyer"""
        # FR-10.3.1.3: get value from previous release.

        self.expected_ei_release['releases'][0]['buyer']['id'] = previous_ei_release['releases'][0]['buyer']['id']
        self.expected_ei_release['releases'][0]['buyer']['name'] = previous_ei_release['releases'][0]['buyer']['name']

        return self.expected_ei_release
