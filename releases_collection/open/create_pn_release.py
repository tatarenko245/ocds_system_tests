"""Prepare the expected releases of the planning notice process, open procedures."""
import copy
import json

from data_collection.OpenProcedure.for_test_createPN_process.release_full_model import pn_release_model, \
    ms_release_model
from functions_collection.some_functions import is_it_uuid, get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv, get_value_from_cpvs_dictionary_csv, get_value_from_cpv_dictionary_xls, \
    get_value_from_classification_unit_dictionary_csv, generate_tender_classification_id, get_sum_of_lot, \
    get_contract_period_for_ms_release, get_unique_party_from_list_by_id


class PlanningNoticeRelease:
    """This class creates instance of release."""

    def __init__(self, environment, language, pmd, pn_payload, actual_message):

        self.environment = environment
        self.language = language
        self.pmd = pmd
        self.pn_payload = pn_payload
        self.actual_message = actual_message
        self.metadata_document_url = None
        try:
            if environment == "dev":
                self.metadata_tender_url = "http://dev.public.eprocurement.systems/tenders"

                self.extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"
                ]

                self.publisher_name = "M-Tender"
                self.publisher_uri = "https://www.mtender.gov.md"
                self.metadata_document_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get"
                self.metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"

            elif environment == "sandbox":
                self.metadata_tender_url = "http://public.eprocurement.systems/tenders"

                self.extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.json"
                ]

                self.publisher_name = "Viešųjų pirkimų tarnyba"
                self.publisher_uri = "https://vpt.lrv.lt"
                self.metadata_document_url = "http://storage.eprocurement.systems/get"
                self.metadata_budget_url = "http://public.eprocurement.systems/budgets"
        except ValueError:
            ValueError("Check your environment: You must use 'dev' or 'sandbox' environment in pytest command")

        self.expected_pn_release = copy.deepcopy(pn_release_model)
        self.expected_ms_release = copy.deepcopy(ms_release_model)

    def build_expected_pn_release(self, actual_pn_release):
        """Build PN release."""

        """Enrich general attribute for expected PN release"""
        self.expected_pn_release['uri'] = \
            f"{self.metadata_tender_url}/{self.actual_message['data']['ocid']}/" \
            f"{self.actual_message['data']['outcomes']['pn'][0]['id']}"

        self.expected_pn_release['version'] = "1.1"
        self.expected_pn_release['extensions'] = self.extensions
        self.expected_pn_release['publisher']['name'] = self.publisher_name
        self.expected_pn_release['publisher']['uri'] = self.publisher_uri
        self.expected_pn_release['license'] = "http://opendefinition.org/licenses/"
        self.expected_pn_release['publicationPolicy'] = "http://opendefinition.org/licenses/"
        self.expected_pn_release['publishedDate'] = self.actual_message['data']['operationDate']

        """Enrich general attribute for expected PN release: releases[0]"""
        self.expected_pn_release['releases'][0]['ocid'] = self.actual_message['data']['outcomes']['pn'][0]['id']

        self.expected_pn_release['releases'][0]['id'] = \
            f"{self.actual_message['data']['outcomes']['pn'][0]['id']}-" \
            f"{actual_pn_release['releases'][0]['id'][46:59]}"

        self.expected_pn_release['releases'][0]['date'] = self.actual_message['data']['operationDate']
        self.expected_pn_release['releases'][0]['tag'] = ["planning"]
        self.expected_pn_release['releases'][0]['language'] = self.language
        self.expected_pn_release['releases'][0]['initiationType'] = "tender"
        self.expected_pn_release['releases'][0]['hasPreviousNotice'] = False
        self.expected_pn_release['releases'][0]['purposeOfNotice']['isACallForCompetition'] = False

        """Enrich 'tender' object for expected PN release: releases[0].tender"""
        try:
            """Set permanent id."""
            is_permanent_id_correct = is_it_uuid(actual_pn_release['releases'][0]['tender']['id'])
            if is_permanent_id_correct is True:

                self.expected_pn_release['releases'][0]['tender']['id'] = \
                    actual_pn_release['releases'][0]['tender']['id']
            else:
                ValueError(f"The 'releases[0].tender.id' must be uuid.")
        except KeyError:
            KeyError(f"Mismatch key into path 'releases[0].tender.id'.")

        self.expected_pn_release['releases'][0]['tender']['status'] = "planning"
        self.expected_pn_release['releases'][0]['tender']['statusDetails'] = "planning"

        # Prepare lots array.
        if "lots" in self.pn_payload['tender']:
            # BR-3.1.1, BR-3.1.5,
            try:
                """
                Build the releases.tender.lots array.
                """
                new_lots_array = list()
                for q_0 in range(len(self.pn_payload['tender']['lots'])):
                    new_lots_array.append(copy.deepcopy(self.expected_pn_release['releases'][0]['tender']['lots'][0]))

                    # Enrich or delete optional fields:
                    if "internalId" in self.pn_payload['tender']['lots'][q_0]:
                        new_lots_array[q_0]['internalId'] = self.pn_payload['tender']['lots'][q_0]['internalId']
                    else:
                        del new_lots_array[q_0]['internalId']

                    if "postalCode" in self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address']:

                        new_lots_array[q_0]['placeOfPerformance']['address']['postalCode'] = \
                            self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address']['postalCode']
                    else:
                        del new_lots_array[q_0]['placeOfPerformance']['address']['postalCode']

                    if "description" in self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']:

                        new_lots_array[q_0]['placeOfPerformance']['description'] = \
                            self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['description']
                    else:
                        del new_lots_array[q_0]['placeOfPerformance']['description']

                    # Enrich required fields:
                    is_permanent_lot_id_correct = is_it_uuid(
                        actual_pn_release['releases'][0]['tender']['lots'][q_0]['id'])

                    if is_permanent_lot_id_correct is True:
                        new_lots_array[q_0]['id'] = actual_pn_release['releases'][0]['tender']['lots'][q_0]['id']
                    else:
                        ValueError(f"The relases0.tender.lots{q_0}.id must be uuid.")

                    new_lots_array[q_0]['title'] = self.pn_payload['tender']['lots'][q_0]['title']
                    new_lots_array[q_0]['description'] = self.pn_payload['tender']['lots'][q_0]['description']
                    new_lots_array[q_0]['status'] = "planning"
                    new_lots_array[q_0]['statusDetails'] = "empty"
                    new_lots_array[q_0]['value']['amount'] = self.pn_payload['tender']['lots'][q_0]['value']['amount']
                    new_lots_array[q_0]['value']['currency'] = self.pn_payload['tender']['lots'][q_0]['value'][
                        'currency']

                    new_lots_array[q_0]['contractPeriod']['startDate'] = \
                        self.pn_payload['tender']['lots'][q_0]['contractPeriod']['startDate']

                    new_lots_array[q_0]['contractPeriod']['endDate'] = \
                        self.pn_payload['tender']['lots'][q_0]['contractPeriod']['endDate']

                    new_lots_array[q_0]['placeOfPerformance']['address']['streetAddress'] = \
                        self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address']['streetAddress']

                    try:
                        """
                        Prepare releases.tender.lots.placeOfPerformance.address.addressDetails object.
                        """
                        lot_country_data = get_value_from_country_csv(
                            country=self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                'addressDetails']['country']['id'],

                            language=self.language
                        )
                        expected_lot_country_object = [{
                            "scheme": lot_country_data[2],

                            "id":
                                self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                    'addressDetails'][
                                    'country']['id'],

                            "description": lot_country_data[1],
                            "uri": lot_country_data[3]
                        }]

                        lot_region_data = get_value_from_region_csv(
                            region=self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                'addressDetails']['region']['id'],

                            country=self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                'addressDetails']['country']['id'],

                            language=self.language
                        )
                        expected_lot_region_object = [{
                            "scheme": lot_region_data[2],

                            "id":
                                self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                    'addressDetails'][
                                    'region']['id'],

                            "description": lot_region_data[1],
                            "uri": lot_region_data[3]
                        }]

                        if self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'locality']['scheme'] != "other":

                            lot_locality_data = get_value_from_locality_csv(

                                locality=self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                    'addressDetails']['locality']['id'],

                                region=self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                    'addressDetails']['region']['id'],

                                country=self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                    'addressDetails']['country']['id'],

                                language=self.language
                            )
                            expected_lot_locality_object = [{
                                "scheme": lot_locality_data[2],

                                "id": self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                    'addressDetails'][
                                    'locality']['id'],

                                "description": lot_locality_data[1],
                                "uri": lot_locality_data[3]
                            }]
                        else:
                            expected_lot_locality_object = [{
                                "scheme":
                                    self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                        'addressDetails'][
                                        'locality']['scheme'],

                                "id": self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                    'addressDetails'][
                                    'locality']['id'],

                                "description":
                                    self.pn_payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                        'addressDetails'][
                                        'locality']['description']
                            }]

                        new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails'][
                            'country'] = expected_lot_country_object[0]
                        new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails'][
                            'region'] = expected_lot_region_object[0]
                        new_lots_array[q_0]['placeOfPerformance']['address']['addressDetails'][
                            'locality'] = expected_lot_locality_object[0]
                    except ValueError:
                        ValueError(
                            "Impossible to prepare the expected releases.tender.lots.placeOfPerformance.address."
                            "addressDetails object.")
                self.expected_pn_release['releases'][0]['tender']['lots'] = new_lots_array
            except ValueError:
                ValueError("Impossible to build the expected releases.tender.lots array.")
        else:
            del self.expected_pn_release['releases'][0]['tender']['lots']

        # Prepare items array.
        if "items" in self.pn_payload['tender']:
            try:
                """
                Build the releases.tender.items array.
                """
                new_items_array = list()
                for q_0 in range(len(self.pn_payload['tender']['items'])):

                    new_items_array.append(copy.deepcopy(
                        self.expected_pn_release['releases'][0]['tender']['items'][0]))

                    # Enrich or delete optional fields:
                    if "internalId" in self.pn_payload['tender']['items'][q_0]:
                        new_items_array[q_0]['internalId'] = self.pn_payload['tender']['items'][q_0]['internalId']
                    else:
                        del new_items_array[q_0]['internalId']

                    if "additionalClassifications" in self.pn_payload['tender']['items'][q_0]:
                        new_item_additional_classifications_array = list()
                        for q_1 in range(len(self.pn_payload['tender']['items'][q_0]['additionalClassifications'])):
                            new_item_additional_classifications_array.append(copy.deepcopy(
                                self.expected_pn_release['releases'][0]['tender']['items'][0][
                                    'additionalClassifications'][0]))

                            expected_cpvs_data = get_value_from_cpvs_dictionary_csv(
                                cpvs=self.pn_payload['tender']['items'][q_0]['additionalClassifications'][q_1]['id'],
                                language=self.language
                            )

                            new_item_additional_classifications_array[q_1]['scheme'] = "CPVS"
                            new_item_additional_classifications_array[q_1]['id'] = expected_cpvs_data[0]
                            new_item_additional_classifications_array[q_1]['description'] = expected_cpvs_data[2]

                        new_items_array[q_0]['additionalClassifications'] = \
                            new_item_additional_classifications_array
                    else:
                        del new_items_array[q_0]['additionalClassifications']

                    # Enrich required fields:
                    is_permanent_item_id_correct = is_it_uuid(
                        actual_pn_release['releases'][0]['tender']['items'][q_0]['id'])

                    if is_permanent_item_id_correct is True:
                        new_items_array[q_0]['id'] = actual_pn_release['releases'][0]['tender']['items'][q_0][
                            'id']
                    else:
                        ValueError(f"The relases[0].tender.items[{q_0}].id must be uuid.")

                    new_items_array[q_0]['description'] = self.pn_payload['tender']['items'][q_0]['description']

                    expected_cpv_data = get_value_from_cpv_dictionary_xls(
                        cpv=self.pn_payload['tender']['items'][q_0]['classification']['id'],
                        language=self.language
                    )

                    new_items_array[q_0]['classification']['scheme'] = "CPV"
                    new_items_array[q_0]['classification']['id'] = expected_cpv_data[0]
                    new_items_array[q_0]['classification']['description'] = expected_cpv_data[1]
                    new_items_array[q_0]['quantity'] = float(self.pn_payload['tender']['items'][q_0]['quantity'])

                    expected_unit_data = get_value_from_classification_unit_dictionary_csv(
                        unit_id=self.pn_payload['tender']['items'][q_0]['unit']['id'],
                        language=self.language
                    )

                    new_items_array[q_0]['unit']['id'] = expected_unit_data[0]
                    new_items_array[q_0]['unit']['name'] = expected_unit_data[1]

                    new_items_array[q_0]['relatedLot'] = \
                        actual_pn_release['releases'][0]['tender']['lots'][q_0]['id']

                self.expected_pn_release['releases'][0]['tender']['items'] = new_items_array
            except ValueError:
                ValueError("Impossible to build the expected releases.tender.items array.")
        else:
            del self.expected_pn_release['releases'][0]['tender']['items']

        # Prepare documents array
        if "documents" in self.pn_payload['tender']:
            try:
                """
                Build the releases.tender.documents array.
                """
                new_documents_array = list()
                for q_0 in range(len(self.pn_payload['tender']['documents'])):

                    new_documents_array.append(copy.deepcopy(
                        self.expected_pn_release['releases'][0]['tender']['documents'][0]))

                    # Enrich or delete optional fields:
                    if "description" in self.pn_payload['tender']['documents'][q_0]:
                        new_documents_array[q_0]['description'] = self.pn_payload['tender']['documents'][q_0][
                            'description']
                    else:
                        del new_documents_array[q_0]['description']

                    if "relatedLots" in self.pn_payload['tender']['documents'][q_0]:

                        new_documents_array[q_0]['relatedLots'] = \
                            [actual_pn_release['releases'][0]['tender']['lots'][q_0]['id']]
                    else:
                        del new_documents_array[q_0]['relatedLots']

                    # Enrich required fields:
                    new_documents_array[q_0]['id'] = self.pn_payload['tender']['documents'][q_0]['id']
                    new_documents_array[q_0]['documentType'] = self.pn_payload['tender']['documents'][q_0][
                        'documentType']
                    new_documents_array[q_0]['title'] = self.pn_payload['tender']['documents'][q_0]['title']

                    new_documents_array[q_0]['url'] = \
                        f"{self.metadata_document_url}/{self.pn_payload['tender']['documents'][q_0]['id']}"

                    new_documents_array[q_0]['datePublished'] = self.actual_message['data']['operationDate']
                self.expected_pn_release['releases'][0]['tender']['documents'] = new_documents_array
            except ValueError:
                ValueError("Impossible to build the expected releases.tender.documents array.")
        else:
            del self.expected_pn_release['releases'][0]['tender']['documents']

        self.expected_pn_release['releases'][0]['tender']['lotGroups'][0]['optionToCombine'] = False

        self.expected_pn_release['releases'][0]['tender']['tenderPeriod']['startDate'] = \
            self.pn_payload['tender']['tenderPeriod']['startDate']

        self.expected_pn_release['releases'][0]['tender']['submissionMethod'][0] = "electronicSubmission"

        self.expected_pn_release['releases'][0]['tender']['submissionMethodDetails'] = \
            "Lista platformelor: achizitii, ebs, licitatie, yptender"

        self.expected_pn_release['releases'][0]['tender']['submissionMethodRationale'][0] = \
            "Ofertele vor fi primite prin intermediul unei platforme electronice de achiziții publice"

        """Enrich 'relatedProcesses' object for expected PN release: releases[0].relatedProcesses"""
        try:
            """Set permanent id."""
            is_permanent_id_correct = is_it_uuid(actual_pn_release['releases'][0]['relatedProcesses'][0]['id'])
            if is_permanent_id_correct is True:
                self.expected_pn_release['releases'][0]['relatedProcesses'][0]['id'] = \
                    actual_pn_release['releases'][0]['relatedProcesses'][0]['id']
            else:
                ValueError(f"The 'releases[0].relatedProcesses[0].id' must be uuid.")
        except KeyError:
            KeyError(f"Mismatch key into path 'releases[0].relatedProcesses[0].id'.")

        self.expected_pn_release['releases'][0]['relatedProcesses'][0]['relationship'][0] = "parent"
        self.expected_pn_release['releases'][0]['relatedProcesses'][0]['scheme'] = "ocid"

        self.expected_pn_release['releases'][0]['relatedProcesses'][0]['identifier'] = \
            self.actual_message['data']['ocid']

        self.expected_pn_release['releases'][0]['relatedProcesses'][0]['uri'] = \
            f"{self.metadata_tender_url}/{self.actual_message['data']['ocid']}/" \
            f"{self.actual_message['data']['ocid']}"

        return self.expected_pn_release

    def build_expected_ms_release(self, ei_payload, ei_message, fs_payloads_list, fs_message_list,
                                  tender_classification_id, actual_ms_release):
        """ Build MS release."""

        """Enrich general attribute for expected MS release"""
        self.expected_ms_release['uri'] = \
            f"{self.metadata_tender_url}/{self.actual_message['data']['ocid']}/{self.actual_message['data']['ocid']}"

        self.expected_ms_release['version'] = "1.1"
        self.expected_ms_release['extensions'] = self.extensions
        self.expected_ms_release['publisher']['name'] = self.publisher_name
        self.expected_ms_release['publisher']['uri'] = self.publisher_uri
        self.expected_ms_release['license'] = "http://opendefinition.org/licenses/"
        self.expected_ms_release['publicationPolicy'] = "http://opendefinition.org/licenses/"
        self.expected_ms_release['publishedDate'] = self.actual_message['data']['operationDate']

        """Enrich general attribute for expected MS release: releases[0]"""
        self.expected_ms_release['releases'][0]['ocid'] = self.actual_message['data']['ocid']

        self.expected_ms_release['releases'][0]['id'] = \
            f"{self.actual_message['data']['ocid']}-{actual_ms_release['releases'][0]['id'][29:42]}"

        self.expected_ms_release['releases'][0]['date'] = self.actual_message['data']['operationDate']
        self.expected_ms_release['releases'][0]['tag'] = ["compiled"]
        self.expected_ms_release['releases'][0]['language'] = self.language
        self.expected_ms_release['releases'][0]['initiationType'] = "tender"

        """Enrich 'planning' object for expected MS release: releases[0].planning"""
        if "rationale" in self.pn_payload['planning']:
            self.expected_ms_release['releases'][0]['planning']['rationale'] = self.pn_payload['planning'][
                'rationale']
        else:
            del self.expected_ms_release['releases'][0]['planning']['rationale']

        if "description" in self.pn_payload['planning']['budget']:

            self.expected_ms_release['releases'][0]['planning']['budget']['description'] = \
                self.pn_payload['planning']['budget']['description']
        else:
            del self.expected_ms_release['releases'][0]['planning']['budget']['description']

        if "procurementMethodRationale" in self.pn_payload['tender']:

            self.expected_ms_release['releases'][0]['tender']['procurementMethodRationale'] = \
                self.pn_payload['tender']['procurementMethodRationale']
        else:
            del self.expected_ms_release['releases'][0]['tender']['procurementMethodRationale']

        if "procurementMethodAdditionalInfo" in self.pn_payload['tender']:

            self.expected_ms_release['releases'][0]['tender']['procurementMethodAdditionalInfo'] = \
                self.pn_payload['tender']['procurementMethodAdditionalInfo']
        else:
            del self.expected_ms_release['releases'][0]['tender']['procurementMethodAdditionalInfo']

        sum_of_budget_breakdown_amount_list = list()
        new_budget_breakdown_array = list()
        for q_0 in range(len(self.pn_payload['planning']['budget']['budgetBreakdown'])):

            new_budget_breakdown_array.append(copy.deepcopy(
                self.expected_ms_release['releases'][0]['planning']['budget']['budgetBreakdown'][0]))

            new_budget_breakdown_array[q_0]['id'] = \
                self.pn_payload['planning']['budget']['budgetBreakdown'][q_0]['id']

            if "description" in fs_payloads_list[q_0]['planning']['budget']:

                new_budget_breakdown_array[q_0]['description'] = \
                    fs_payloads_list[q_0]['planning']['budget']['description']
            else:
                del new_budget_breakdown_array[q_0]['description']

            new_budget_breakdown_array[q_0]['amount']['amount'] = \
                round(self.pn_payload['planning']['budget']['budgetBreakdown'][q_0]['amount']['amount'], 2)

            sum_of_budget_breakdown_amount_list.append(new_budget_breakdown_array[q_0]['amount']['amount'])

            new_budget_breakdown_array[q_0]['amount']['currency'] = \
                fs_payloads_list[q_0]['planning']['budget']['amount']['currency']

            new_budget_breakdown_array[q_0]['period']['startDate'] = \
                fs_payloads_list[q_0]['planning']['budget']['period']['startDate']

            new_budget_breakdown_array[q_0]['period']['endDate'] = \
                fs_payloads_list[q_0]['planning']['budget']['period']['endDate']

            if "buyer" in fs_payloads_list[q_0]:
                new_budget_breakdown_array[q_0]['sourceParty']['id'] = \
                    f"{fs_payloads_list[q_0]['buyer']['identifier']['scheme']}-" \
                    f"{fs_payloads_list[q_0]['buyer']['identifier']['id']}"

                new_budget_breakdown_array[q_0]['sourceParty']['name'] = fs_payloads_list[q_0]['buyer']['name']
            else:

                new_budget_breakdown_array[q_0]['sourceParty']['id'] = \
                    f"{ei_payload['buyer']['identifier']['scheme']}-" \
                    f"{ei_payload['buyer']['identifier']['id']}"

                new_budget_breakdown_array[q_0]['sourceParty']['name'] = ei_payload['buyer']['name']

            if "europeanUnionFunding" in fs_payloads_list[q_0]['planning']['budget']:

                new_budget_breakdown_array[q_0]['europeanUnionFunding'] = \
                    fs_payloads_list[q_0]['planning']['budget']['europeanUnionFunding']

                if "uri" in fs_payloads_list[q_0]['planning']['budget']['europeanUnionFunding']:

                    new_budget_breakdown_array[q_0]['europeanUnionFunding']['uri'] = \
                        fs_payloads_list[q_0]['planning']['budget']['europeanUnionFunding']['uri']
                else:
                    del new_budget_breakdown_array[q_0]['europeanUnionFunding']['uri']
            else:
                del new_budget_breakdown_array[q_0]['europeanUnionFunding']

        for i in range(len(fs_payloads_list)):
            if fs_payloads_list[i]['planning']['budget']['isEuropeanUnionFunded'] is True:
                self.expected_ms_release['releases'][0]['planning']['budget']['isEuropeanUnionFunded'] = True
            else:
                self.expected_ms_release['releases'][0]['planning']['budget']['isEuropeanUnionFunded'] = False

        self.expected_ms_release['releases'][0]['planning']['budget']['budgetBreakdown'] = new_budget_breakdown_array

        self.expected_ms_release['releases'][0]['planning']['budget']['amount']['amount'] = \
            round(sum(sum_of_budget_breakdown_amount_list), 2)

        self.expected_ms_release['releases'][0]['planning']['budget']['amount']['currency'] = \
            self.pn_payload['planning']['budget']['budgetBreakdown'][0]['amount']['currency']

        """Enrich 'tender' object for expected MS release: releases[0].tender"""
        # Set id.
        try:
            is_permanent_id_correct = is_it_uuid(
                actual_ms_release['releases'][0]['tender']['id']
            )
            if is_permanent_id_correct is True:

                self.expected_ms_release['releases'][0]['tender']['id'] = \
                    actual_ms_release['releases'][0]['tender']['id']
            else:
                self.expected_ms_release['releases'][0]['tender']['id'] = f"The 'releases[0].tender.id' must be uuid."
        except KeyError:
            KeyError(f"Mismatch key into path 'releases[0].tender.id'")

        # Set state.
        self.expected_ms_release['releases'][0]['tender']['status'] = "planning"
        self.expected_ms_release['releases'][0]['tender']['statusDetails'] = "planning"

        # Set title.
        self.expected_ms_release['releases'][0]['tender']['title'] = self.pn_payload['tender']['title']

        # Set description.
        self.expected_ms_release['releases'][0]['tender']['description'] = self.pn_payload['tender']['description']

        # Set procurementMethod.
        self.expected_ms_release['releases'][0]['tender']['procurementMethod'] = "open"

        # Set procurementMethodDetails.
        if self.pmd == "TEST_OT":
            self.expected_ms_release['releases'][0]['tender']['procurementMethodDetails'] = "testOpenTender"
        elif self.pmd == "OT":
            self.expected_ms_release['releases'][0]['tender']['procurementMethodDetails'] = "openTender"
        elif self.pmd == "TEST_SV":
            self.expected_ms_release['releases'][0]['tender']['procurementMethodDetails'] = "testSmallTender"
        elif self.pmd == "SV":
            self.expected_ms_release['releases'][0]['tender']['procurementMethodDetails'] = "smallTender"
        elif self.pmd == "TEST_MV":
            self.expected_ms_release['releases'][0]['tender']['procurementMethodDetails'] = "testMicroTender"
        elif self.pmd == "MV":
            self.expected_ms_release['releases'][0]['tender']['procurementMethodDetails'] = "microTender"
        else:
            self.expected_ms_release['releases'][0]['tender']['procurementMethodDetails'] = "Unknown pmd."

        # Set procuringEntity.
        self.expected_ms_release['releases'][0]['tender']['procuringEntity']['id'] = \
            f"{self.pn_payload['tender']['procuringEntity']['identifier']['scheme']}-" \
            f"{self.pn_payload['tender']['procuringEntity']['identifier']['id']}"

        self.expected_ms_release['releases'][0]['tender']['procuringEntity']['name'] = \
            self.pn_payload['tender']['procuringEntity']['name']

        # Set items array.
        if "items" in self.pn_payload['tender']:

            expected_cpv_data = get_value_from_cpv_dictionary_xls(
                cpv=generate_tender_classification_id(self.pn_payload['tender']['items']),
                language=self.language
            )
        else:
            expected_cpv_data = get_value_from_cpv_dictionary_xls(
                cpv=tender_classification_id,
                language=self.language
            )

        # Set classification.
        self.expected_ms_release['releases'][0]['tender']['classification']['id'] = expected_cpv_data[0]
        self.expected_ms_release['releases'][0]['tender']['classification']['description'] = expected_cpv_data[1]
        self.expected_ms_release['releases'][0]['tender']['classification']['scheme'] = "CPV"

        # Set legalBasis.
        self.expected_ms_release['releases'][0]['tender']['legalBasis'] = self.pn_payload['tender']['legalBasis']

        # Set mainProcurementCategory, depends on tender.classification.id.
        if \
                tender_classification_id[0:2] == "03" or \
                        tender_classification_id[0] == "1" or \
                        tender_classification_id[0] == "2" or \
                        tender_classification_id[0] == "3" or \
                        tender_classification_id[0:2] == "44" or \
                        tender_classification_id[0:2] == "48":
            expected_main_procurement_category = "goods"

        elif \
                tender_classification_id[0:2] == "45":
            expected_main_procurement_category = "works"

        elif \
                tender_classification_id[0] == "5" or \
                        tender_classification_id[0] == "6" or \
                        tender_classification_id[0] == "7" or \
                        tender_classification_id[0] == "8" or \
                        tender_classification_id[0:2] == "92" or \
                        tender_classification_id[0:2] == "98":
            expected_main_procurement_category = "services"

        else:
            expected_main_procurement_category = "Unknown tender.classification.id"

        self.expected_ms_release['releases'][0]['tender']['mainProcurementCategory'] = \
            expected_main_procurement_category

        # Set eligibilityCriteria.
        if self.language == "RO":
            expected_eligibility_criteria = "Regulile generale privind naționalitatea și originea, precum și " \
                                            "alte criterii de eligibilitate sunt enumerate în " \
                                            "Ghidul practic privind procedurile de contractare " \
                                            "a acțiunilor externe ale UE (PRAG)"
        elif self.language == "EN":
            expected_eligibility_criteria = "The general rules on nationality and origin, " \
                                            "as well as other eligibility criteria are listed " \
                                            "in the Practical Guide to Contract Procedures for EU " \
                                            "External Actions (PRAG)"
        else:
            expected_eligibility_criteria = "Unknown language."

        self.expected_ms_release['releases'][0]['tender']['eligibilityCriteria'] = expected_eligibility_criteria

        # Set value.
        if "lots" in self.pn_payload['tender']:

            self.expected_ms_release['releases'][0]['tender']['value']['amount'] = \
                round(get_sum_of_lot(lots_array=self.pn_payload['tender']['lots']), 2)

            self.expected_ms_release['releases'][0]['tender']['value']['currency'] = \
                self.pn_payload['tender']['lots'][0]['value']['currency']

            expected_contract_period = get_contract_period_for_ms_release(
                lots_array=self.pn_payload['tender']['lots'])

            self.expected_ms_release['releases'][0]['tender']['contractPeriod']['startDate'] = \
                expected_contract_period[0]

            self.expected_ms_release['releases'][0]['tender']['contractPeriod']['endDate'] = \
                expected_contract_period[1]
        else:
            self.expected_ms_release['releases'][0]['tender']['value']['amount'] = round(
                sum(sum_of_budget_breakdown_amount_list), 2)

            self.expected_ms_release['releases'][0]['tender']['value']['currency'] = \
                self.pn_payload['planning']['budget']['budgetBreakdown'][0]['amount']['currency']

            del self.expected_ms_release['releases'][0]['tender']['contractPeriod']

        """Enrich 'parties' object for expected MS release: releases[0].parties"""
        buyer_role_array = list()
        payer_role_array = list()
        funder_role_array = list()
        procuringentity_role_array = list()

        # Prepare party with procuringEntity role.
        procuringentity_role_array.append(copy.deepcopy(self.expected_ms_release['releases'][0]['parties'][0]))
        procuringentity_role_array[0]['id'] = f"{self.pn_payload['tender']['procuringEntity']['identifier']['scheme']}-" \
                                              f"{self.pn_payload['tender']['procuringEntity']['identifier']['id']}"

        procuringentity_role_array[0]['name'] = self.pn_payload['tender']['procuringEntity']['name']
        procuringentity_role_array[0]['identifier']['scheme'] = \
        self.pn_payload['tender']['procuringEntity']['identifier']['scheme']
        procuringentity_role_array[0]['identifier']['id'] = self.pn_payload['tender']['procuringEntity']['identifier'][
            'id']
        procuringentity_role_array[0]['identifier']['legalName'] = \
        self.pn_payload['tender']['procuringEntity']['identifier']['legalName']
        procuringentity_role_array[0]['address']['streetAddress'] = \
        self.pn_payload['tender']['procuringEntity']['address']['streetAddress']

        if "postalCode" in self.pn_payload['tender']['procuringEntity']['address']:
            procuringentity_role_array[0]['address']['postalCode'] = \
            self.pn_payload['tender']['procuringEntity']['address']['postalCode']
        else:
            del procuringentity_role_array[0]['address']['postalCode']

        # Prepare addressDetails object for party with procuringEntity role.
        procuringentity_country_data = get_value_from_country_csv(
            country=ei_payload['buyer']['address']['addressDetails']['country']['id'],
            language=self.language
        )
        expected_procuringentity_country_object = [{
            "scheme": procuringentity_country_data[2],
            "id": self.pn_payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
            "description": procuringentity_country_data[1],
            "uri": procuringentity_country_data[3]
        }]

        procuringentity_region_data = get_value_from_region_csv(
            region=ei_payload['buyer']['address']['addressDetails']['region']['id'],
            country=ei_payload['buyer']['address']['addressDetails']['country']['id'],
            language=self.language
        )
        expected_procuringentity_region_object = [{
            "scheme": procuringentity_region_data[2],
            "id": self.pn_payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
            "description": procuringentity_region_data[1],
            "uri": procuringentity_region_data[3]
        }]

        if self.pn_payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] != "other":

            procuringentity_locality_data = get_value_from_locality_csv(
                locality=self.pn_payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],
                region=self.pn_payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
                country=self.pn_payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
                language=self.language
            )
            expected_procuringentity_locality_object = [{
                "scheme": procuringentity_locality_data[2],
                "id": self.pn_payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],
                "description": procuringentity_locality_data[1],
                "uri": procuringentity_locality_data[3]
            }]
        else:
            expected_procuringentity_locality_object = [{
                "scheme": self.pn_payload['tender']['procuringEntity']['address']['addressDetails']['locality'][
                    'scheme'],
                "id": self.pn_payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],

                "description": self.pn_payload['tender']['procuringEntity']['address']['addressDetails'][
                    'locality']['description']
            }]

        procuringentity_role_array[0]['address']['addressDetails']['country'] = \
            expected_procuringentity_country_object[0]

        procuringentity_role_array[0]['address']['addressDetails']['region'] = \
            expected_procuringentity_region_object[0]

        procuringentity_role_array[0]['address']['addressDetails']['locality'] = \
            expected_procuringentity_locality_object[0]

        if "uri" in self.pn_payload['tender']['procuringEntity']['identifier']:

            procuringentity_role_array[0]['identifier']['uri'] = self.pn_payload['tender']['procuringEntity'][
                'identifier']['uri']
        else:
            del procuringentity_role_array[0]['identifier']['uri']

        if "additionalIdentifiers" in self.pn_payload['tender']['procuringEntity']:
            del procuringentity_role_array[0]['additionalIdentifiers'][0]
            additional_identifiers = list()
            for q_1 in range(len(self.pn_payload['tender']['procuringEntity']['additionalIdentifiers'])):
                additional_identifiers.append(copy.deepcopy(
                    self.expected_ms_release['releases'][0]['parties'][0]['additionalIdentifiers'][0]
                ))

                additional_identifiers[q_1]['scheme'] = \
                    self.pn_payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['scheme']

                additional_identifiers[q_1]['id'] = \
                    self.pn_payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['id']

                additional_identifiers[q_1]['legalName'] = \
                    self.pn_payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['legalName']

                additional_identifiers[q_1]['uri'] = \
                    self.pn_payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['uri']

                procuringentity_role_array[0]['additionalIdentifiers'] = additional_identifiers
        else:
            del procuringentity_role_array[0]['additionalIdentifiers']

        if "faxNumber" in self.pn_payload['tender']['procuringEntity']['contactPoint']:

            procuringentity_role_array[0]['contactPoint']['faxNumber'] = \
                self.pn_payload['tender']['procuringEntity']['contactPoint']['faxNumber']
        else:
            del procuringentity_role_array[0]['contactPoint']['faxNumber']

        if "url" in self.pn_payload['tender']['procuringEntity']['contactPoint']:

            procuringentity_role_array[0]['contactPoint']['url'] = \
                self.pn_payload['tender']['procuringEntity']['contactPoint']['url']
        else:
            del procuringentity_role_array[0]['contactPoint']['url']

        procuringentity_role_array[0]['contactPoint']['name'] = \
            self.pn_payload['tender']['procuringEntity']['contactPoint']['name']

        procuringentity_role_array[0]['contactPoint']['email'] = \
            self.pn_payload['tender']['procuringEntity']['contactPoint']['email']

        procuringentity_role_array[0]['contactPoint']['telephone'] = \
            self.pn_payload['tender']['procuringEntity']['contactPoint']['telephone']

        procuringentity_role_array[0]['roles'] = ["procuringEntity"]

        # Prepare party with buyer role.
        buyer_role_array.append(copy.deepcopy(self.expected_ms_release['releases'][0]['parties'][0]))

        buyer_role_array[0]['id'] = f"{ei_payload['buyer']['identifier']['scheme']}-" \
                                    f"{ei_payload['buyer']['identifier']['id']}"

        buyer_role_array[0]['name'] = ei_payload['buyer']['name']
        buyer_role_array[0]['identifier']['scheme'] = ei_payload['buyer']['identifier']['scheme']
        buyer_role_array[0]['identifier']['id'] = ei_payload['buyer']['identifier']['id']
        buyer_role_array[0]['identifier']['legalName'] = ei_payload['buyer']['identifier']['legalName']
        buyer_role_array[0]['address']['streetAddress'] = ei_payload['buyer']['address']['streetAddress']

        if "postalCode" in ei_payload['buyer']['address']:
            buyer_role_array[0]['address']['postalCode'] = ei_payload['buyer']['address']['postalCode']
        else:
            del buyer_role_array[0]['address']['postalCode']

        # Prepare addressDetails object for party with buyer role.
        buyer_country_data = get_value_from_country_csv(
            country=ei_payload['buyer']['address']['addressDetails']['country']['id'],
            language=self.language
        )
        expected_buyer_country_object = [{
            "scheme": buyer_country_data[2],
            "id": ei_payload['buyer']['address']['addressDetails']['country']['id'],
            "description": buyer_country_data[1],
            "uri": buyer_country_data[3]
        }]

        buyer_region_data = get_value_from_region_csv(
            region=ei_payload['buyer']['address']['addressDetails']['region']['id'],
            country=ei_payload['buyer']['address']['addressDetails']['country']['id'],
            language=self.language
        )
        expected_buyer_region_object = [{
            "scheme": buyer_region_data[2],
            "id": ei_payload['buyer']['address']['addressDetails']['region']['id'],
            "description": buyer_region_data[1],
            "uri": buyer_region_data[3]
        }]

        if ei_payload['buyer']['address']['addressDetails']['locality']['scheme'] != "other":

            buyer_locality_data = get_value_from_locality_csv(
                locality=ei_payload['buyer']['address']['addressDetails']['locality']['id'],
                region=ei_payload['buyer']['address']['addressDetails']['region']['id'],
                country=ei_payload['buyer']['address']['addressDetails']['country']['id'],
                language=self.language
            )
            expected_buyer_locality_object = [{
                "scheme": buyer_locality_data[2],
                "id": ei_payload['buyer']['address']['addressDetails']['locality']['id'],
                "description": buyer_locality_data[1],
                "uri": buyer_locality_data[3]
            }]
        else:
            expected_buyer_locality_object = [{
                "scheme": ei_payload['buyer']['address']['addressDetails']['locality']['scheme'],
                "id": ei_payload['buyer']['address']['addressDetails']['locality']['id'],
                "description": ei_payload['buyer']['address']['addressDetails']['locality']['description']
            }]

        buyer_role_array[0]['address']['addressDetails']['country'] = expected_buyer_country_object[0]
        buyer_role_array[0]['address']['addressDetails']['region'] = expected_buyer_region_object[0]
        buyer_role_array[0]['address']['addressDetails']['locality'] = expected_buyer_locality_object[0]

        if "uri" in ei_payload['buyer']['identifier']:
            buyer_role_array[0]['identifier']['uri'] = ei_payload['buyer']['identifier']['uri']
        else:
            del buyer_role_array[0]['identifier']['uri']

        if "additionalIdentifiers" in ei_payload['buyer']:
            del buyer_role_array[0]['additionalIdentifiers'][0]
            additional_identifiers = list()
            for q_1 in range(len(ei_payload['buyer']['additionalIdentifiers'])):
                additional_identifiers.append(copy.deepcopy(
                    self.expected_ms_release['releases'][0]['parties'][0]['additionalIdentifiers'][0]
                ))

                additional_identifiers[q_1]['scheme'] = \
                    ei_payload['buyer']['additionalIdentifiers'][q_1]['scheme']

                additional_identifiers[q_1]['id'] = \
                    ei_payload['buyer']['additionalIdentifiers'][q_1]['id']

                additional_identifiers[q_1]['legalName'] = \
                    ei_payload['buyer']['additionalIdentifiers'][q_1]['legalName']

                additional_identifiers[q_1]['uri'] = \
                    ei_payload['buyer']['additionalIdentifiers'][q_1]['uri']

                buyer_role_array[0]['additionalIdentifiers'] = additional_identifiers
        else:
            del buyer_role_array[0]['additionalIdentifiers']

        if "faxNumber" in ei_payload['buyer']['contactPoint']:
            buyer_role_array[0]['contactPoint']['faxNumber'] = ei_payload['buyer']['contactPoint']['faxNumber']
        else:
            del buyer_role_array[0]['contactPoint']['faxNumber']

        if "url" in ei_payload['buyer']['contactPoint']:
            buyer_role_array[0]['contactPoint']['url'] = ei_payload['buyer']['contactPoint']['url']
        else:
            del buyer_role_array[0]['contactPoint']['url']

        buyer_role_array[0]['contactPoint']['name'] = ei_payload['buyer']['contactPoint']['name']
        buyer_role_array[0]['contactPoint']['email'] = ei_payload['buyer']['contactPoint']['email']
        buyer_role_array[0]['contactPoint']['telephone'] = ei_payload['buyer']['contactPoint']['telephone']

        if "details" in ei_payload['buyer']:
            if "typeOfBuyer" in ei_payload['buyer']['details']:
                buyer_role_array[0]['details']['typeOfBuyer'] = ei_payload['buyer']['details']['typeOfBuyer']
            else:
                del buyer_role_array['buyer']['details']['typeOfBuyer']

            if "mainGeneralActivity" in ei_payload['buyer']['details']:

                buyer_role_array[0]['details']['mainGeneralActivity'] = \
                    ei_payload['buyer']['details']['mainGeneralActivity']
            else:
                del buyer_role_array[0]['details']['mainGeneralActivity']

            if "mainSectoralActivity" in ei_payload['buyer']['details']:

                buyer_role_array[0]['details']['mainSectoralActivity'] = \
                    ei_payload['buyer']['details']['mainSectoralActivity']
            else:
                del buyer_role_array[0]['details']['mainSectoralActivity']
        else:
            del buyer_role_array[0]['details']

        buyer_role_array[0]['roles'] = ["buyer"]

        # Prepare party with funder role.
        for q_2 in range(len(fs_payloads_list)):
            if "buyer" in fs_payloads_list[q_2]:
                funder_role_array.append(copy.deepcopy(self.expected_ms_release['releases'][0]['parties'][0]))

                funder_role_array[q_2]['id'] = f"{fs_payloads_list[q_2]['buyer']['identifier']['scheme']}-" \
                                               f"{fs_payloads_list[q_2]['buyer']['identifier']['id']}"

                funder_role_array[q_2]['name'] = fs_payloads_list[q_2]['buyer']['name']
                funder_role_array[q_2]['identifier']['scheme'] = fs_payloads_list[q_2]['buyer']['identifier']['scheme']
                funder_role_array[q_2]['identifier']['id'] = fs_payloads_list[q_2]['buyer']['identifier']['id']

                funder_role_array[q_2]['identifier']['legalName'] = \
                    fs_payloads_list[q_2]['buyer']['identifier']['legalName']

                funder_role_array[q_2]['address']['streetAddress'] = fs_payloads_list[q_2]['buyer']['address'][
                    'streetAddress']

                if "postalCode" in fs_payloads_list[q_2]['buyer']['address']:

                    funder_role_array[q_2]['address']['postalCode'] = \
                        fs_payloads_list[q_2]['buyer']['address']['postalCode']
                else:
                    del funder_role_array[q_2]['address']['postalCode']

                # Prepare addressDetails object for party with funder role.
                funder_country_data = get_value_from_country_csv(
                    country=fs_payloads_list[q_2]['buyer']['address']['addressDetails']['country']['id'],
                    language=self.language
                )
                expected_funder_country_object = [{
                    "scheme": funder_country_data[2],
                    "id": fs_payloads_list[q_2]['buyer']['address']['addressDetails']['country']['id'],
                    "description": funder_country_data[1],
                    "uri": funder_country_data[3]
                }]

                funder_region_data = get_value_from_region_csv(
                    region=fs_payloads_list[q_2]['buyer']['address']['addressDetails']['region']['id'],
                    country=fs_payloads_list[q_2]['buyer']['address']['addressDetails']['country']['id'],
                    language=self.language
                )
                expected_funder_region_object = [{
                    "scheme": funder_region_data[2],
                    "id": fs_payloads_list[q_2]['buyer']['address']['addressDetails']['region']['id'],
                    "description": funder_region_data[1],
                    "uri": funder_region_data[3]
                }]

                if fs_payloads_list[q_2]['buyer']['address']['addressDetails']['locality']['scheme'] != "other":

                    funder_locality_data = get_value_from_locality_csv(
                        locality=fs_payloads_list[q_2]['buyer']['address']['addressDetails']['locality']['id'],
                        region=fs_payloads_list[q_2]['buyer']['address']['addressDetails']['region']['id'],
                        country=fs_payloads_list[q_2]['buyer']['address']['addressDetails']['country']['id'],
                        language=self.language
                    )
                    expected_funder_locality_object = [{
                        "scheme": funder_locality_data[2],
                        "id": fs_payloads_list[q_2]['buyer']['address']['addressDetails']['locality']['id'],
                        "description": funder_locality_data[1],
                        "uri": funder_locality_data[3]
                    }]
                else:
                    expected_funder_locality_object = [{
                        "scheme": fs_payloads_list[q_2]['buyer']['address']['addressDetails']['locality']['scheme'],
                        "id": fs_payloads_list[q_2]['buyer']['address']['addressDetails']['locality']['id'],

                        "description":
                            fs_payloads_list[q_2]['buyer']['address']['addressDetails']['locality']['description']
                    }]

                funder_role_array[q_2]['address']['addressDetails']['country'] = expected_funder_country_object[0]
                funder_role_array[q_2]['address']['addressDetails']['region'] = expected_funder_region_object[0]
                funder_role_array[q_2]['address']['addressDetails']['locality'] = expected_funder_locality_object[0]

                if "uri" in fs_payloads_list[q_2]['buyer']['identifier']:
                    funder_role_array[q_2]['identifier']['uri'] = fs_payloads_list[q_2]['buyer']['identifier']['uri']
                else:
                    del funder_role_array[q_2]['identifier']['uri']

                if "additionalIdentifiers" in fs_payloads_list[q_2]['buyer']:
                    del funder_role_array[q_2]['additionalIdentifiers'][0]
                    additional_identifiers = list()
                    for q_3 in range(len(fs_payloads_list[q_2]['buyer']['additionalIdentifiers'])):
                        additional_identifiers.append(copy.deepcopy(
                            self.expected_ms_release['releases'][0]['parties'][0]['additionalIdentifiers'][0]
                        ))

                        additional_identifiers[q_3]['scheme'] = \
                            fs_payloads_list[q_2]['buyer']['additionalIdentifiers'][q_3]['scheme']

                        additional_identifiers[q_3]['id'] = \
                            fs_payloads_list[q_2]['buyer']['additionalIdentifiers'][q_3]['id']

                        additional_identifiers[q_3]['legalName'] = \
                            fs_payloads_list[q_2]['buyer']['additionalIdentifiers'][q_3]['legalName']

                        additional_identifiers[q_3]['uri'] = \
                            fs_payloads_list[q_2]['buyer']['additionalIdentifiers'][q_3]['uri']

                        funder_role_array[q_2]['additionalIdentifiers'] = additional_identifiers
                else:
                    del funder_role_array[q_2]['additionalIdentifiers']

                if "faxNumber" in fs_payloads_list[q_2]['buyer']['contactPoint']:

                    funder_role_array[q_2]['contactPoint']['faxNumber'] = \
                        fs_payloads_list[q_2]['buyer']['contactPoint']['faxNumber']
                else:
                    del funder_role_array[q_2]['contactPoint']['faxNumber']

                if "url" in fs_payloads_list[q_2]['buyer']['contactPoint']:
                    funder_role_array[q_2]['contactPoint']['url'] = fs_payloads_list[q_2]['buyer']['contactPoint'][
                        'url']
                else:
                    del funder_role_array[q_2]['contactPoint']['url']

                funder_role_array[q_2]['contactPoint']['name'] = \
                    fs_payloads_list[q_2]['buyer']['contactPoint']['name']

                funder_role_array[q_2]['contactPoint']['email'] = \
                    fs_payloads_list[q_2]['buyer']['contactPoint']['email']

                funder_role_array[q_2]['contactPoint']['telephone'] = \
                    fs_payloads_list[q_2]['buyer']['contactPoint']['telephone']

                del funder_role_array[q_2]['details']
                funder_role_array[q_2]['roles'] = ["funder"]

        # Prepare party with payer role.
        for q_3 in range(len(fs_payloads_list)):
            payer_role_array.append(copy.deepcopy(self.expected_ms_release['releases'][0]['parties'][0]))

            payer_role_array[q_3]['id'] = \
                f"{fs_payloads_list[q_3]['tender']['procuringEntity']['identifier']['scheme']}-" \
                f"{fs_payloads_list[q_3]['tender']['procuringEntity']['identifier']['id']}"

            payer_role_array[q_3]['name'] = fs_payloads_list[q_3]['tender']['procuringEntity']['name']

            payer_role_array[q_3]['identifier']['scheme'] = \
                fs_payloads_list[q_3]['tender']['procuringEntity']['identifier']['scheme']

            payer_role_array[q_3]['identifier']['id'] = \
                fs_payloads_list[q_3]['tender']['procuringEntity']['identifier']['id']

            payer_role_array[q_3]['identifier']['legalName'] = \
                fs_payloads_list[q_3]['tender']['procuringEntity']['identifier']['legalName']

            payer_role_array[q_3]['address']['streetAddress'] = \
                fs_payloads_list[q_3]['tender']['procuringEntity']['address']['streetAddress']

            if "postalCode" in fs_payloads_list[q_3]['tender']['procuringEntity']['address']:

                payer_role_array[q_3]['address']['postalCode'] = \
                    fs_payloads_list[q_3]['tender']['procuringEntity']['address']['postalCode']
            else:
                del payer_role_array[q_3]['address']['postalCode']

            # Prepare addressDetails object for party with payer role.
            payer_country_data = get_value_from_country_csv(
                country=fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                    'country']['id'],

                language=self.language
            )
            expected_payer_country_object = [{
                "scheme": payer_country_data[2],

                "id": fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                    'country']['id'],

                "description": payer_country_data[1],
                "uri": payer_country_data[3]
            }]

            payer_region_data = get_value_from_region_csv(
                region=fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                    'region']['id'],

                country=fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                    'country']['id'],

                language=self.language
            )
            expected_payer_region_object = [{
                "scheme": payer_region_data[2],

                "id": fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                    'region']['id'],

                "description": payer_region_data[1],
                "uri": payer_region_data[3]
            }]

            if fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                'locality']['scheme'] != "other":

                payer_locality_data = get_value_from_locality_csv(
                    locality=fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                        'locality']['id'],

                    region=fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                        'region']['id'],

                    country=fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                        'country']['id'],

                    language=self.language
                )
                expected_payer_locality_object = [{
                    "scheme": payer_locality_data[2],
                    "id": fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                        'locality']['id'],

                    "description": payer_locality_data[1],
                    "uri": payer_locality_data[3]
                }]
            else:
                expected_payer_locality_object = [{
                    "scheme": fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                        'locality']['scheme'],

                    "id": fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                        'locality']['id'],

                    "description": fs_payloads_list[q_3]['tender']['procuringEntity']['address']['addressDetails'][
                        'locality']['description']
                }]

            payer_role_array[q_3]['address']['addressDetails']['country'] = expected_payer_country_object[0]
            payer_role_array[q_3]['address']['addressDetails']['region'] = expected_payer_region_object[0]
            payer_role_array[q_3]['address']['addressDetails']['locality'] = expected_payer_locality_object[0]

            if "uri" in fs_payloads_list[q_3]['tender']['procuringEntity']['identifier']:

                payer_role_array[q_3]['identifier']['uri'] = \
                    fs_payloads_list[q_3]['tender']['procuringEntity']['identifier']['uri']
            else:
                del payer_role_array[q_3]['identifier']['uri']

            if "additionalIdentifiers" in fs_payloads_list[q_3]['tender']['procuringEntity']:
                del payer_role_array[q_3]['additionalIdentifiers'][0]
                additional_identifiers = list()
                for q_4 in range(len(fs_payloads_list[q_3]['tender']['procuringEntity']['additionalIdentifiers'])):
                    additional_identifiers.append(copy.deepcopy(
                        self.expected_ms_release['releases'][0]['parties'][0]['additionalIdentifiers'][0]
                    ))

                    additional_identifiers[q_4]['scheme'] = \
                        fs_payloads_list[q_3]['tender']['procuringEntity']['additionalIdentifiers'][q_4]['scheme']

                    additional_identifiers[q_4]['id'] = \
                        fs_payloads_list[q_3]['tender']['procuringEntity']['additionalIdentifiers'][q_4]['id']

                    additional_identifiers[q_4]['legalName'] = \
                        fs_payloads_list[q_3]['tender']['procuringEntity']['additionalIdentifiers'][q_4]['legalName']

                    additional_identifiers[q_4]['uri'] = \
                        fs_payloads_list[q_3]['tender']['procuringEntity']['additionalIdentifiers'][q_4]['uri']

                    payer_role_array[q_3]['additionalIdentifiers'] = additional_identifiers
            else:
                del payer_role_array[q_3]['additionalIdentifiers']

            if "faxNumber" in fs_payloads_list[q_3]['tender']['procuringEntity']['contactPoint']:

                payer_role_array[q_3]['contactPoint']['faxNumber'] = \
                    fs_payloads_list[q_3]['tender']['procuringEntity']['contactPoint']['faxNumber']
            else:
                del payer_role_array[q_3]['contactPoint']['faxNumber']

            if "url" in fs_payloads_list[q_3]['tender']['procuringEntity']['contactPoint']:

                payer_role_array[q_3]['contactPoint']['url'] = \
                    fs_payloads_list[q_3]['tender']['procuringEntity']['contactPoint']['url']
            else:
                del payer_role_array[q_3]['contactPoint']['url']

            payer_role_array[q_3]['contactPoint']['name'] = \
                fs_payloads_list[q_3]['tender']['procuringEntity']['contactPoint']['name']

            payer_role_array[q_3]['contactPoint']['email'] = \
                fs_payloads_list[q_3]['tender']['procuringEntity']['contactPoint']['email']

            payer_role_array[q_3]['contactPoint']['telephone'] = \
                fs_payloads_list[q_3]['tender']['procuringEntity']['contactPoint']['telephone']

            del payer_role_array[q_3]['details']
            payer_role_array[q_3]['roles'] = ["payer"]

        # Get unique 'parties' array for buyer role.
        unique_buyer_role_array = get_unique_party_from_list_by_id(buyer_role_array)
        unique_buyer_id_array = list()
        for buyer in range(len(unique_buyer_role_array)):
            unique_buyer_id_array.append(unique_buyer_role_array[buyer]['id'])

        # Get unique 'parties' array for payer role.
        unique_payer_role_array = get_unique_party_from_list_by_id(payer_role_array)
        unique_payer_id_array = list()
        for payer in range(len(unique_payer_role_array)):
            unique_payer_id_array.append(unique_payer_role_array[payer]['id'])

        # Get unique 'parties' array for funder role.
        unique_funder_role_array = get_unique_party_from_list_by_id(funder_role_array)
        unique_funder_id_array = list()
        for funder in range(len(unique_funder_role_array)):
            unique_funder_id_array.append(unique_funder_role_array[funder]['id'])

        # Get unique 'parties' array for procuringEntity role.
        unique_procuringentity_role_array = get_unique_party_from_list_by_id(procuringentity_role_array)
        unique_procuringentity_id_array = list()
        for procuringentity in range(len(unique_procuringentity_role_array)):
            unique_procuringentity_id_array.append(unique_procuringentity_role_array[procuringentity]['id'])

        # Prepare temporary 'parties' array for specific role.
        temp_parties_with_buyer_role_array = list()
        temp_parties_with_payer_role_array = list()
        temp_parties_with_funder_role_array = list()
        temp_parties_with_procuringentity_role_array = list()

        # Compare organizations with 'funder' and 'procuringEntity' role.
        same_id_into_procuringentity_and_funder = list(
            set(unique_procuringentity_id_array) & set(unique_funder_id_array)
        )

        if len(same_id_into_procuringentity_and_funder) > 0:
            for funder in range(len(unique_funder_role_array)):
                for i_1 in range(len(same_id_into_procuringentity_and_funder)):
                    for procuringentity in range(len(unique_procuringentity_role_array)):
                        if unique_funder_role_array[funder]['id'] == same_id_into_procuringentity_and_funder[i_1] == \
                                unique_procuringentity_role_array[procuringentity]['id']:
                            unique_funder_role_array[funder]['roles'] = \
                                unique_funder_role_array[funder]['roles'] + \
                                unique_procuringentity_role_array[procuringentity]['roles']

                            temp_parties_with_funder_role_array.append(unique_funder_role_array[funder])

                    for procuringentity in range(len(unique_procuringentity_role_array)):
                        if unique_funder_role_array[funder]['id'] != same_id_into_procuringentity_and_funder[i_1]:
                            temp_parties_with_procuringentity_role_array.append(
                                unique_procuringentity_role_array[procuringentity]
                            )

                        if unique_funder_role_array[funder]['id'] != same_id_into_procuringentity_and_funder[i_1]:
                            temp_parties_with_funder_role_array.append(unique_payer_role_array[funder])
        else:
            temp_parties_with_procuringentity_role_array = unique_procuringentity_role_array
            temp_parties_with_funder_role_array = unique_funder_role_array

        unique_parties_id_array = list()
        for funder in range(len(temp_parties_with_funder_role_array)):
            unique_parties_id_array.append(temp_parties_with_funder_role_array[funder]['id'])

        # Compare organizations with 'payer' and 'funder' role.
        same_id_into_payer_and_funder = list(set(unique_payer_id_array) & set(unique_parties_id_array))

        if len(same_id_into_payer_and_funder) > 0:
            for payer in range(len(unique_payer_role_array)):
                for i_1 in range(len(same_id_into_payer_and_funder)):
                    for funder in range(len(unique_parties_id_array)):
                        if unique_payer_role_array[payer]['id'] == same_id_into_payer_and_funder[i_1] == \
                                unique_parties_id_array[funder]['id']:
                            unique_payer_role_array[payer]['roles'] = \
                                unique_payer_role_array[payer]['roles'] + unique_parties_id_array[funder]['roles']

                            temp_parties_with_payer_role_array.append(unique_payer_role_array[payer])

                    for funder in range(len(unique_funder_role_array)):
                        if unique_payer_role_array[payer]['id'] != same_id_into_payer_and_funder[i_1]:
                            temp_parties_with_payer_role_array.append(unique_payer_role_array[payer])

                        if unique_parties_id_array[funder]['id'] != same_id_into_payer_and_funder[i_1]:
                            temp_parties_with_funder_role_array.append(unique_parties_id_array[funder])
        else:
            temp_parties_with_payer_role_array = unique_payer_role_array
            temp_parties_with_funder_role_array = temp_parties_with_funder_role_array

        unique_parties_id_array = list()
        for payer in range(len(temp_parties_with_payer_role_array)):
            unique_parties_id_array.append(temp_parties_with_payer_role_array[payer]['id'])

        # --
        # Compare organizations with 'payer' and 'procuringEntity' role.
        same_id_into_procuringentity_and_funder = list(
            set(unique_procuringentity_id_array) & set(unique_funder_id_array)
        )

        if len(same_id_into_procuringentity_and_funder) > 0:
            for funder in range(len(unique_funder_role_array)):
                for i_1 in range(len(same_id_into_procuringentity_and_funder)):
                    for procuringentity in range(len(unique_procuringentity_role_array)):
                        if unique_funder_role_array[funder]['id'] == same_id_into_procuringentity_and_funder[i_1] == \
                                unique_procuringentity_role_array[procuringentity]['id']:
                            unique_funder_role_array[funder]['roles'] = \
                                unique_funder_role_array[funder]['roles'] + \
                                unique_procuringentity_role_array[procuringentity]['roles']

                            temp_parties_with_funder_role_array.append(unique_funder_role_array[funder])

                    for procuringentity in range(len(unique_procuringentity_role_array)):
                        if unique_funder_role_array[funder]['id'] != same_id_into_procuringentity_and_funder[i_1]:
                            temp_parties_with_procuringentity_role_array.append(
                                unique_procuringentity_role_array[procuringentity]
                            )

                        if unique_funder_role_array[funder]['id'] != same_id_into_procuringentity_and_funder[i_1]:
                            temp_parties_with_funder_role_array.append(unique_payer_role_array[funder])
        else:
            temp_parties_with_procuringentity_role_array = unique_procuringentity_role_array
            temp_parties_with_funder_role_array = unique_funder_role_array

        unique_parties_id_array = list()
        for funder in range(len(temp_parties_with_funder_role_array)):
            unique_parties_id_array.append(temp_parties_with_funder_role_array[funder]['id'])
        # =====
        # Compare organizations with 'buyer' and 'payer' role.
        same_id_into_buyer_and_payer = \
            list(set(unique_buyer_id_array) & set(unique_parties_id_array))

        permanent_parties_with_buyer_role_array = list()
        permanent_parties_with_payer_role_array = list()
        permanent_parties_with_funder_role_array = list()

        if len(same_id_into_buyer_and_payer) > 0:
            for buyer in range(len(unique_buyer_role_array)):
                for i_1 in range(len(same_id_into_buyer_and_payer)):
                    for payer in range(len(temp_parties_with_payer_role_array)):

                        if unique_buyer_role_array[buyer]['id'] == same_id_into_buyer_and_payer[i_1] == \
                                temp_parties_with_payer_role_array[payer]['id']:
                            unique_buyer_role_array[buyer]['roles'] = \
                                unique_buyer_role_array[buyer]['roles'] + temp_parties_with_payer_role_array[payer][
                                    'roles']

                            temp_parties_with_buyer_role_array.append(unique_buyer_role_array[buyer])

                    for payer in range(len(temp_parties_with_payer_role_array)):
                        if temp_parties_with_payer_role_array[payer]['id'] != same_id_into_buyer_and_payer[i_1]:
                            permanent_parties_with_payer_role_array.append(temp_parties_with_payer_role_array[payer])
        else:
            temp_parties_with_buyer_role_array = unique_buyer_role_array
            permanent_parties_with_payer_role_array = temp_parties_with_payer_role_array

        unique_parties_id_array = list()
        for funder in range(len(temp_parties_with_funder_role_array)):
            unique_parties_id_array.append(temp_parties_with_funder_role_array[funder]['id'])

        unique_buyer_id_array = list()
        for buyer in range(len(temp_parties_with_buyer_role_array)):
            unique_buyer_id_array.append(temp_parties_with_buyer_role_array[buyer]['id'])

        # Compare organizations with 'buyer' and 'funder' role.
        same_id_into_buyer_and_funder = \
            list(set(unique_buyer_id_array) & set(unique_parties_id_array))

        if len(same_id_into_buyer_and_funder) > 0:
            for buyer in range(len(temp_parties_with_buyer_role_array)):
                for i_1 in range(len(same_id_into_buyer_and_funder)):
                    for funder in range(len(temp_parties_with_funder_role_array)):

                        if temp_parties_with_buyer_role_array[buyer]['id'] == same_id_into_buyer_and_funder[i_1] == \
                                temp_parties_with_funder_role_array[funder]['id']:
                            temp_parties_with_buyer_role_array[buyer]['roles'] = \
                                temp_parties_with_buyer_role_array[buyer]['roles'] + \
                                temp_parties_with_funder_role_array[funder]['roles']

                            permanent_parties_with_buyer_role_array.append(temp_parties_with_buyer_role_array[buyer])

                    for funder in range(len(temp_parties_with_funder_role_array)):
                        if temp_parties_with_funder_role_array[funder]['id'] != same_id_into_buyer_and_funder[i_1]:
                            permanent_parties_with_funder_role_array.append(temp_parties_with_funder_role_array[funder])
        else:
            permanent_parties_with_buyer_role_array = temp_parties_with_buyer_role_array
            permanent_parties_with_funder_role_array = temp_parties_with_funder_role_array

        parties_array = \
            permanent_parties_with_buyer_role_array + permanent_parties_with_payer_role_array + \
            permanent_parties_with_funder_role_array

        expected_parties_array = list()
        if len(actual_ms_release['releases'][0]['parties']) == len(parties_array):
            for act in range(len(actual_ms_release['releases'][0]['parties'])):
                for exp in range(len(parties_array)):
                    if parties_array[exp]['id'] == actual_ms_release['releases'][0]['parties'][act]['id']:
                        expected_parties_array.append(parties_array[exp])
        else:
            ValueError("Quantity of objects into actual ms release doesn't equal "
                       "quantity of objects into prepared parties array")

        self.expected_ms_release['releases'][0]['parties'] = expected_parties_array

        """Enrich 'relatedProcesses' object for expected MS release: releases[0].relatedProcesses"""
        new_related_processes_array = list()
        for q_0 in range(2):
            new_related_processes_array.append(
                copy.deepcopy(self.expected_ms_release['releases'][0]['relatedProcesses'][0])
            )

        new_related_processes_array[0]['relationship'] = ["planning"]
        new_related_processes_array[0]['scheme'] = "ocid"
        new_related_processes_array[0]['identifier'] = self.actual_message['data']['outcomes']['pn'][0]['id']

        new_related_processes_array[0]['uri'] = \
            f"{self.metadata_tender_url}/{self.actual_message['data']['ocid']}/" \
            f"{self.actual_message['data']['outcomes']['pn'][0]['id']}"

        new_related_processes_array[1]['relationship'] = ["x_expenditureItem"]
        new_related_processes_array[1]['scheme'] = "ocid"
        new_related_processes_array[1]['identifier'] = ei_message['data']['outcomes']['ei'][0]['id']

        new_related_processes_array[1]['uri'] = \
            f"{self.metadata_budget_url}/{ei_message['data']['outcomes']['ei'][0]['id']}/" \
            f"{ei_message['data']['outcomes']['ei'][0]['id']}"

        fs_related_processes_array = list()
        for q_0 in range(len(fs_message_list)):
            fs_related_processes_array.append(
                copy.deepcopy(self.expected_ms_release['releases'][0]['relatedProcesses'][0])
            )

            fs_related_processes_array[q_0]['relationship'] = ["x_fundingSource"]
            fs_related_processes_array[q_0]['scheme'] = "ocid"

            fs_related_processes_array[q_0]['identifier'] = \
                fs_message_list[q_0]['data']['outcomes']['fs'][0]['id']

            fs_related_processes_array[q_0]['uri'] = \
                f"{self.metadata_budget_url}/{ei_message['data']['outcomes']['ei'][0]['id']}/" \
                f"{fs_message_list[q_0]['data']['outcomes']['fs'][0]['id']}"

        expected_related_processes_array = new_related_processes_array + fs_related_processes_array
        if len(actual_ms_release['releases'][0]['relatedProcesses']) == len(expected_related_processes_array):
            for act in range(len(actual_ms_release['releases'][0]['relatedProcesses'])):
                for exp in range(len(expected_related_processes_array)):

                    is_permanent_releatedprocess_id_correct = is_it_uuid(
                        actual_ms_release['releases'][0]['relatedProcesses'][act]['id'])

                    if is_permanent_releatedprocess_id_correct is True:

                        if actual_ms_release['releases'][0]['relatedProcesses'][act]['identifier'] == \
                                expected_related_processes_array[exp]['identifier']:
                            expected_related_processes_array[exp]['id'] = \
                                actual_ms_release['releases'][0]['relatedProcesses'][act]['id']
                    else:
                        ValueError(f"The relases0.relatedProcess.id must be uuid.")
        else:
            ValueError("The quantity of actual relatedProcesses array != "
                       "quantity of expected relatedProcess array")

        self.expected_ms_release['releases'][0]['relatedProcesses'] = expected_related_processes_array
        return self.expected_ms_release
