"""Prepare the expected release of the create expenditure item process, budget."""
import copy

from data_collection.for_test_createEI_process.ei_release_full_model import *
from functions_collection.some_functions import get_value_from_cpvs_dictionary_csv, is_it_uuid, \
    get_value_from_cpv_dictionary_xls, get_value_from_classification_unit_dictionary_csv, \
    get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv


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

    def build_expected_ei_release(self, payload, message_for_platform, actual_ei_release):
        """Build EI release."""

        """Enrich general attribute for expected EI release"""
        self.expected_ei_release['uri'] = f"{self.metadata_budget_url}/{message_for_platform['data']['ocid']}/" \
                                          f"{message_for_platform['data']['outcomes']['ei'][0]['id']}"

        self.expected_ei_release['version'] = "1.1"
        self.expected_ei_release['extensions'] = self.extensions
        self.expected_ei_release['publisher']['name'] = self.publisher_name
        self.expected_ei_release['publisher']['uri'] = self.publisher_uri
        self.expected_ei_release['license'] = "http://opendefinition.org/licenses/"
        self.expected_ei_release['publicationPolicy'] = "http://opendefinition.org/licenses/"

        # FR.COM-3.5.6: Set created date for release.
        self.expected_ei_release['publishedDate'] = message_for_platform['data']['operationDate']

        """Enrich general attribute for expected EI release: releases[0]"""
        # FR.COM-3.5.2: Set ocid.
        self.expected_ei_release['releases'][0]['ocid'] = message_for_platform['data']['outcomes']['ei'][0]['id']

        # FR.COM-3.5.4: Set id.
        self.expected_ei_release['releases'][0]['id'] = f"{message_for_platform['data']['outcomes']['ei'][0]['id']}-" \
                                                        f"{actual_ei_release['releases'][0]['id'][29:42]}"

        # FR.COM-14.2.2: Set date.
        self.expected_ei_release['releases'][0]['date'] = message_for_platform['data']['operationDate']

        # FR.COM-3.5.7: Set tag.
        self.expected_ei_release['releases'][0]['tag'] = ["compiled"]

        # FR.COM-3.5.8: Set initiationType.
        self.expected_ei_release['releases'][0]['initiationType'] = "tender"

        # FR.COM-3.5.9: Set language.
        self.expected_ei_release['releases'][0]['language'] = self.language

        """Enrich attribute for expected EI release: releases[0].planning"""
        # FR.COM-14.2.12: Set id.
        self.expected_ei_release['releases'][0]['planning']['budget']['id'] = self.tender_classification_id

        # FR.COM-14.2.14: Set period.
        self.expected_ei_release['releases'][0]['planning']['budget']['period']['startDate'] = \
            payload['planning']['budget']['period']['startDate']
        self.expected_ei_release['releases'][0]['planning']['budget']['period']['endDate'] = \
            payload['planning']['budget']['period']['endDate']

        # FR.COM-14.2.15: Set amount.
        if "amount" in payload['planning']['budget']:
            self.expected_ei_release['releases'][0]['planning']['budget']['amount']['amount'] = \
                payload['planning']['budget']['amount']['amount']
            self.expected_ei_release['releases'][0]['planning']['budget']['amount']['currency'] = \
                payload['planning']['budget']['amount']['currency']
        else:
            del self.expected_ei_release['releases'][0]['planning']['budget']['amount']

        # FR.COM-14.2.13: Set rationale.
        if "rationale" in payload['planning']:
            self.expected_ei_release['releases'][0]['planning']['rationale'] = payload['planning']['rationale']
        else:
            del self.expected_ei_release['releases'][0]['planning']['rationale']

        """Enrich attribute for expected EI release: releases[0].parties"""
        # According to actions of the 'budgetCreateEI' delegate.
        buyer_role_array = list()
        buyer_role_array.append(copy.deepcopy(self.expected_ei_release['releases'][0]['parties'][0]))

        buyer_role_array[0]['id'] = f"{payload['buyer']['identifier']['scheme']}-" \
                                    f"{payload['buyer']['identifier']['id']}"

        buyer_role_array[0]['name'] = payload['buyer']['name']
        buyer_role_array[0]['identifier']['scheme'] = payload['buyer']['identifier']['scheme']
        buyer_role_array[0]['identifier']['id'] = payload['buyer']['identifier']['id']
        buyer_role_array[0]['identifier']['legalName'] = payload['buyer']['identifier']['legalName']

        if "uri" in payload['buyer']['identifier']:
            buyer_role_array[0]['identifier']['uri'] = payload['buyer']['identifier']['uri']
        else:
            del buyer_role_array[0]['identifier']['uri']

        buyer_role_array[0]['address']['streetAddress'] = payload['buyer']['address']['streetAddress']

        if "postalCode" in payload['buyer']['address']:
            buyer_role_array[0]['address']['postalCode'] = payload['buyer']['address']['postalCode']
        else:
            del buyer_role_array[0]['address']['postalCode']

        # Prepare addressDetails object for party with buyer role.
        try:
            buyer_country_data = get_value_from_country_csv(
                country=payload['buyer']['address']['addressDetails']['country']['id'],
                language=self.language
            )
            expected_buyer_country_object = [{
                "scheme": buyer_country_data[2].upper(),
                "id": payload['buyer']['address']['addressDetails']['country']['id'],
                "description": buyer_country_data[1],
                "uri": buyer_country_data[3]
            }]

            buyer_region_data = get_value_from_region_csv(
                region=payload['buyer']['address']['addressDetails']['region']['id'],
                country=payload['buyer']['address']['addressDetails']['country']['id'],
                language=self.language
            )
            expected_buyer_region_object = [{
                "scheme": buyer_region_data[2],
                "id": payload['buyer']['address']['addressDetails']['region']['id'],
                "description": buyer_region_data[1],
                "uri": buyer_region_data[3]
            }]

            if payload['buyer']['address']['addressDetails']['locality']['scheme'] == "CUATM":

                buyer_locality_data = get_value_from_locality_csv(
                    locality=payload['buyer']['address']['addressDetails']['locality']['id'],
                    region=payload['buyer']['address']['addressDetails']['region']['id'],
                    country=payload['buyer']['address']['addressDetails']['country']['id'],
                    language=self.language
                )
                expected_buyer_locality_object = [{
                    "scheme": buyer_locality_data[2],
                    "id": payload['buyer']['address']['addressDetails']['locality']['id'],
                    "description": buyer_locality_data[1],
                    "uri": buyer_locality_data[3]
                }]
            else:
                expected_buyer_locality_object = [{
                    "scheme": payload['buyer']['address']['addressDetails']['locality']['scheme'],
                    "id": payload['buyer']['address']['addressDetails']['locality']['id'],
                    "description": payload['buyer']['address']['addressDetails']['locality']['description']
                }]

            buyer_role_array[0]['address']['addressDetails']['country'] = expected_buyer_country_object[0]
            buyer_role_array[0]['address']['addressDetails']['region'] = expected_buyer_region_object[0]
            buyer_role_array[0]['address']['addressDetails']['locality'] = expected_buyer_locality_object[0]
        except ValueError:
            ValueError(
                "Impossible to prepare addressDetails object for party with buyer role.")

        if "additionalIdentifiers" in payload['buyer']:
            for q_1 in range(len(payload['buyer']['additionalIdentifiers'])):
                buyer_role_array[0]['additionalIdentifiers'][q_1]['scheme'] = \
                    payload['buyer']['additionalIdentifiers'][q_1]['scheme']

                buyer_role_array[0]['additionalIdentifiers'][q_1]['id'] = \
                    payload['buyer']['additionalIdentifiers'][q_1]['id']

                buyer_role_array[0]['additionalIdentifiers'][q_1]['legalName'] = \
                    payload['buyer']['additionalIdentifiers'][q_1]['legalName']

                buyer_role_array[0]['additionalIdentifiers'][q_1]['uri'] = \
                    payload['buyer']['additionalIdentifiers'][q_1]['uri']
        else:
            del buyer_role_array[0]['additionalIdentifiers']

        if "faxNumber" in payload['buyer']['contactPoint']:
            buyer_role_array[0]['contactPoint']['faxNumber'] = payload['buyer']['contactPoint']['faxNumber']
        else:
            del buyer_role_array[0]['contactPoint']['faxNumber']

        if "url" in payload['buyer']['contactPoint']:
            buyer_role_array[0]['contactPoint']['url'] = payload['buyer']['contactPoint']['url']
        else:
            del buyer_role_array[0]['contactPoint']['url']

        buyer_role_array[0]['contactPoint']['name'] = payload['buyer']['contactPoint']['name']
        buyer_role_array[0]['contactPoint']['email'] = payload['buyer']['contactPoint']['email']
        buyer_role_array[0]['contactPoint']['telephone'] = payload['buyer']['contactPoint']['telephone']

        if "details" in payload['buyer']:
            if "typeOfBuyer" in payload['buyer']['details']:
                buyer_role_array[0]['details']['typeOfBuyer'] = payload['buyer']['details']['typeOfBuyer']
            else:
                del buyer_role_array['buyer']['details']['typeOfBuyer']

            if "mainGeneralActivity" in payload['buyer']['details']:

                buyer_role_array[0]['details']['mainGeneralActivity'] = \
                    payload['buyer']['details']['mainGeneralActivity']
            else:
                del buyer_role_array[0]['details']['mainGeneralActivity']

            if "mainSectoralActivity" in payload['buyer']['details']:

                buyer_role_array[0]['details']['mainSectoralActivity'] = \
                    payload['buyer']['details']['mainSectoralActivity']
            else:
                del buyer_role_array[0]['details']['mainSectoralActivity']
        else:
            del buyer_role_array[0]['details']

        buyer_role_array[0]['roles'] = ["buyer"]
        self.expected_ei_release['releases'][0]['parties'] = buyer_role_array

        """Enrich attribute for expected EI release: releases[0].tender"""
        # According to actions of the 'budgetCreateEI' delegate.

        # FR.COM-14.2.9: Set items.
        if "items" in payload['tender']:
            try:
                # Build the releases.tender.items array.
                new_items_array = list()
                for q_0 in range(len(payload['tender']['items'])):

                    new_items_array.append(copy.deepcopy(
                        self.expected_ei_release['releases'][0]['tender']['items'][0]))

                    # Enrich or delete optional fields:
                    if "additionalClassifications" in payload['tender']['items'][q_0]:
                        new_item_additional_classifications_array = list()
                        for q_1 in range(len(payload['tender']['items'][q_0]['additionalClassifications'])):
                            new_item_additional_classifications_array.append(copy.deepcopy(
                                self.expected_ei_release['releases'][0]['tender']['items'][0][
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

                    # FR.COM-14.2.10: Set id.
                    try:
                        is_permanent_id_correct = is_it_uuid(
                            actual_ei_release['releases'][0]['tender']['items'][q_0]['id']
                        )
                        if is_permanent_id_correct is True:

                            new_items_array[q_0]['id'] = \
                                actual_ei_release['releases'][0]['tender']['items'][q_0]['id']
                        else:
                            new_items_array[q_0]['id'] = \
                                f"FR.COM-14.2.10: the 'releases[0].tender.items[{q_0}].id' must be uuid."
                    except KeyError:
                        KeyError(f"Mismatch key into path 'releases[0].tender.items[{q_0}].id'")

                    new_items_array[q_0]['description'] = payload['tender']['items'][q_0]['description']

                    expected_cpv_data = get_value_from_cpv_dictionary_xls(
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

                        if payload['tender']['items'][q_0]['deliveryAddress']['addressDetails'][
                                'locality']['scheme'] == "CUATM":

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

                        new_items_array[q_0]['deliveryAddress']['addressDetails']['country'] = \
                            expected_item_country_object[0]

                        new_items_array[q_0]['deliveryAddress']['addressDetails']['region'] = \
                            expected_item_region_object[0]

                        new_items_array[q_0]['deliveryAddress']['addressDetails']['locality'] = \
                            expected_item_locality_object[0]
                    except ValueError:
                        ValueError("Impossible to prepare addressDetails object for items array")

                self.expected_ei_release['releases'][0]['tender']['items'] = new_items_array
            except ValueError:
                ValueError("Impossible to build the expected releases.tender.items array.")
        else:
            del self.expected_ei_release['releases'][0]['tender']['items']

        # FR.COM-14.2.6: Set description.
        if "description" in payload['tender']:
            self.expected_ei_release['releases'][0]['tender']['description'] = payload['tender']['description']
        else:
            del self.expected_ei_release['releases'][0]['tender']['description']

        # FR.COM-14.2.3: Set id.
        try:
            is_permanent_id_correct = is_it_uuid(actual_ei_release['releases'][0]['tender']['id'])
            if is_permanent_id_correct is True:

                self.expected_ei_release['releases'][0]['tender']['id'] = \
                    actual_ei_release['releases'][0]['tender']['id']
            else:
                ValueError(f"The 'releases[0].tender.id' must be uuid.")
        except KeyError:
            KeyError("Mismatch key into path 'releases[0].tender.id'")

        # FR.COM-14.2.5: Set title.
        self.expected_ei_release['releases'][0]['tender']['title'] = payload['tender']['title']

        # FR.COM-14.2.4: Set state.
        self.expected_ei_release['releases'][0]['tender']['status'] = "planning"

        # FR.COM-14.2.8:  Set mainProcurementCategory.
        try:
            expected_main_procurement_category = None
            if \
                    self.tender_classification_id[0:2] == "03" or \
                    self.tender_classification_id[0] == "1" or \
                    self.tender_classification_id[0] == "2" or \
                    self.tender_classification_id[0] == "3" or \
                    self.tender_classification_id[0:2] == "44" or \
                    self.tender_classification_id[0:2] == "48":
                expected_main_procurement_category = "goods"

            elif \
                    self.tender_classification_id[0:2] == "45":
                expected_main_procurement_category = "works"

            elif \
                    self.tender_classification_id[0] == "5" or \
                    self.tender_classification_id[0] == "6" or \
                    self.tender_classification_id[0] == "7" or \
                    self.tender_classification_id[0] == "8" or \
                    self.tender_classification_id[0:2] == "92" or \
                    self.tender_classification_id[0:2] == "98":
                expected_main_procurement_category = "services"

            else:
                ValueError("Check your tender.classification.id")

            self.expected_ei_release['releases'][0]['tender']['mainProcurementCategory'] = \
                expected_main_procurement_category

        except KeyError:
            KeyError("Could not parse tender.classification.id.")

        # FR.COM-14.2.7:  Set classification.id.
        try:
            expected_cpv_data = get_value_from_cpv_dictionary_xls(
                cpv=self.tender_classification_id,
                language=self.language
            )

            self.expected_ei_release['releases'][0]['tender']['classification']['id'] = expected_cpv_data[0]
            self.expected_ei_release['releases'][0]['tender']['classification']['description'] = expected_cpv_data[1]
            self.expected_ei_release['releases'][0]['tender']['classification']['scheme'] = "CPV"
        except ValueError:
            ValueError("FR.COM-14.2.7: impossible to set tender.classification object.")

        """Enrich attribute for expected EI release: releases[0].buyer"""
        # According to actions of the 'budgetCreateEI' delegate.

        # FR.COM-14.2.11: Set buyer.
        self.expected_ei_release['releases'][0]['buyer']['id'] = \
            f"{payload['buyer']['identifier']['scheme']}-{payload['buyer']['identifier']['id']}"

        self.expected_ei_release['releases'][0]['buyer']['name'] = payload['buyer']['name']

        return self.expected_ei_release
