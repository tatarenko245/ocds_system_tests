""""Prepare the expected release of the create pin process, open procedure."""
import copy

import requests

from data_collection.OpenProcedure.for_test_createPIN_process.release_full_model import pi_release_model, \
    ms_release_model
from data_collection.data_constant import affordable_shemes
from functions_collection.some_functions import is_it_uuid, get_value_from_cpv_dictionary_csv, \
    get_value_from_classification_unit_dictionary_csv, get_value_from_cpvs_dictionary_csv, get_value_from_country_csv, \
    get_value_from_region_csv, get_value_from_locality_csv, get_value_from_code_translation_csv, \
    get_unique_party_from_list_by_id, get_contract_period_for_ms_release, \
    get_value_from_cpv_dictionary_xls, generate_tender_classification_id


class CreatePriorInformationNoticeRelease:
    """This class creates instance of release."""

    def __init__(self, environment, country, language, tender_classification_id, payload, message_for_platform):

        self.environment = environment
        self.country = country
        self.language = language
        self.tender_classification_id = tender_classification_id
        self.payload = payload
        self.message_for_platform = message_for_platform
        self.expected_pi_release = copy.deepcopy(pi_release_model)
        self.expected_ms_release = copy.deepcopy(ms_release_model)

        for c in range(len(affordable_shemes['data'])):
            if affordable_shemes['data'][c]['country'] == country:
                self.items_additionalclassifications_scheme = affordable_shemes['data'][c][
                    'items_additionalclassifications_scheme'][0]

        try:
            if environment == "dev":
                self.metadata_budget_url = "http://dev.public.eprocurement.systems/tenders"

                self.extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.js"
                ]

                self.publisher_name = "M-Tender"
                self.publisher_uri = "https://www.mtender.gov.md"
                self.metadata_document_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get"
                self.metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"
                self.metadata_tender_url = "http://dev.public.eprocurement.systems/tenders"

            elif environment == "sandbox":
                self.metadata_budget_url = "http://public.eprocurement.systems/tenders"

                self.extensions = [
                    "https://raw.githubusercontent.com/open-contracting/ocds_bid_extension/v1.1.1/extension.json",
                    "https://raw.githubusercontent.com/open-contracting/ocds_enquiry_extension/v1.1.1/extension.json"
                ]

                self.publisher_name = "Viešųjų pirkimų tarnyba"
                self.publisher_uri = "https://vpt.lrv.lt"
                self.metadata_document_url = "http://storage.eprocurement.systems/get"
                self.metadata_budget_url = "http://public.eprocurement.systems/budgets"
                self.metadata_tender_url = "http://dev.public.eprocurement.systems/tenders"

        except ValueError:
            raise ValueError("Check your environment: You must use 'dev' or 'sandbox' environment.")

    def build_expected_pi_release(self, actual_pi_release):
        """Build PI release."""

        """Enrich general attribute for expected PI release"""
        self.expected_pi_release['uri'] = \
            f"{self.metadata_tender_url}/{self.message_for_platform['data']['ocid'][:28]}/" \
            f"{self.message_for_platform['data']['outcomes']['pin'][0]['id']}"

        self.expected_pi_release['version'] = "1.1"
        self.expected_pi_release['extensions'] = self.extensions
        self.expected_pi_release['publisher']['name'] = self.publisher_name
        self.expected_pi_release['publisher']['uri'] = self.publisher_uri
        self.expected_pi_release['license'] = "http://opendefinition.org/licenses/"
        self.expected_pi_release['publicationPolicy'] = "http://opendefinition.org/licenses/"

        # FR.COM-3.4.6 Set created date for release.
        self.expected_pi_release['publishedDate'] = self.message_for_platform['data']['operationDate']

        """Enrich general attribute for expected PI release: releases[0]"""
        # FR.COM-3.4.2: Set ocid.
        self.expected_pi_release['releases'][0]['ocid'] = self.message_for_platform['data']['outcomes']['pin'][0]['id']

        # FR.COM-3.4.4: Set id.
        self.expected_pi_release['releases'][0]['id'] = \
            f"{self.message_for_platform['data']['outcomes']['pin'][0]['id']}-" \
            f"{actual_pi_release['releases'][0]['id'][46:59]}"

        # FR.COM-1.62.6: Set date.
        self.expected_pi_release['releases'][0]['date'] = self.message_for_platform['data']['operationDate']

        # FR.COM-3.4.7: Set tag.
        self.expected_pi_release['releases'][0]['tag'] = ["planning"]

        # FR.COM-3.4.8: Set initiationType.
        self.expected_pi_release['releases'][0]['initiationType'] = "tender"

        # FR.COM-3.4.11: Set language.
        self.expected_pi_release['releases'][0]['language'] = self.language

        """Enrich attribute for expected PI release: releases[0].tender"""
        # FR.COM-1.62.4: Set id.
        try:
            is_permanent_id_correct = is_it_uuid(
                actual_pi_release['releases'][0]['tender']['id']
            )
            if is_permanent_id_correct is True:

                self.expected_pi_release['releases'][0]['tender']['id'] = \
                    actual_pi_release['releases'][0]['tender']['id']
            else:
                self.expected_pi_release['releases'][0]['tender']['id'] = \
                    f"FR.COM-1.62.4: the 'releases[0].tender.id' must be uuid."
        except KeyError:
            raise KeyError(f"Mismatch key into path 'releases[0].tender.id'")

        # FR.COM-1.62.5: Set status.
        self.expected_pi_release['releases'][0]['tender']['status'] = "planning"

        # FR.COM-1.62.49: Set criteria.
        if "criteria" in self.payload['tender']:
            expected_criteria_array = list()
            for q_0 in range(len(self.payload['tender']['criteria'])):
                expected_criteria_array.append(copy.deepcopy(
                    self.expected_pi_release['releases'][0]['tender']['criteria'][0]
                ))

                # FR.COM-1.62.50: Set id.
                try:
                    is_permanent_id_correct = is_it_uuid(
                        actual_pi_release['releases'][0]['tender']['criteria'][q_0]['id']
                    )
                    if is_permanent_id_correct is True:

                        expected_criteria_array[q_0]['id'] = \
                            actual_pi_release['releases'][0]['tender']['criteria'][q_0]['id']
                    else:
                        expected_criteria_array[q_0]['id'] = \
                            f"FR.COM-1.62.50: the 'releases[0].tender.criteria[{q_0}].id' must be uuid."
                except KeyError:
                    raise KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}].id'")

                # Set title.
                expected_criteria_array[q_0]['title'] = self.payload['tender']['criteria'][q_0]['title']

                # Set source.
                expected_criteria_array[q_0]['source'] = "tenderer"

                # Set description.
                if "description" in self.payload['tender']['criteria'][q_0]:
                    expected_criteria_array[q_0]['description'] = self.payload['tender']['criteria'][q_0]['description']
                else:
                    del expected_criteria_array[q_0]['description']

                # Set relatesTo.
                expected_criteria_array[q_0]['relatesTo'] = self.payload['tender']['criteria'][q_0]['relatesTo']

                # FR.COM-1.62.59: Set relatedItem.
                if "relatedItem" in self.payload['tender']['criteria'][q_0]:
                    try:
                        is_permanent_id_correct = is_it_uuid(
                            actual_pi_release['releases'][0]['tender']['criteria'][q_0]['relatedItem']
                        )
                        if is_permanent_id_correct is True:

                            expected_criteria_array[q_0]['relatedItem'] = \
                                actual_pi_release['releases'][0]['tender']['criteria'][q_0]['relatedItem']
                        else:
                            expected_criteria_array[q_0]['id'] = \
                                f"FR.COM-1.62.59: the 'releases[0].tender.criteria[{q_0}].relatedItem' must be uuid."
                    except KeyError:
                        raise KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}].relatedItem'")
                else:
                    del expected_criteria_array[q_0]['relatedItem']

                # FR.COM-1.62.51: Set classification.
                if "classification" in self.payload['tender']['criteria'][q_0]:
                    expected_criteria_array[q_0]['classification']['scheme'] = \
                        self.payload['tender']['criteria'][q_0]['classification']['scheme']

                    expected_criteria_array[q_0]['classification']['id'] = \
                        self.payload['tender']['criteria'][q_0]['classification']['id']
                else:
                    del expected_criteria_array[q_0]['classification']

                # Set requirementGroups.
                expected_requirementgroups_array = list()
                for q_1 in range(len(self.payload['tender']['criteria'][q_0]['requirementGroups'])):
                    expected_requirementgroups_array.append(copy.deepcopy(
                        self.expected_pi_release['releases'][0]['tender']['criteria'][0]['requirementGroups'][0]
                    ))

                    # FR.COM-1.62.53: Set id.
                    try:
                        is_permanent_id_correct = is_it_uuid(
                            actual_pi_release['releases'][0]['tender']['criteria'][q_0]['requirementGroups'][q_1]['id']
                        )
                        if is_permanent_id_correct is True:

                            expected_requirementgroups_array[q_1]['id'] = \
                                actual_pi_release['releases'][0]['tender']['criteria'][q_0][
                                    'requirementGroups'][q_1]['id']
                        else:
                            expected_requirementgroups_array[q_1]['id'] = \
                                f"FR.COM-1.62.53: the 'releases[0].tender.criteria[{q_0}]." \
                                f"requirementGroups[{q_1}].id' must be uuid."
                    except KeyError:
                        raise KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}]."
                                       f"requirementGroups[{q_1}].id'")

                    # Set description.
                    if "description" in self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1]:
                        expected_requirementgroups_array[q_1]['description'] = \
                            self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['description']
                    else:
                        del expected_requirementgroups_array[q_1]['description']

                    # Set requirements.
                    expected_requirements_array = list()
                    for q_2 in range(len(
                            self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements']
                    )):
                        expected_requirements_array.append(copy.deepcopy(
                            self.expected_pi_release['releases'][0]['tender']['criteria'][0]['requirementGroups'][0][
                                'requirements'][0]
                        ))

                        # FR.COM-1.62.54: Set id.
                        try:
                            is_permanent_id_correct = is_it_uuid(
                                actual_pi_release['releases'][0]['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['id']
                            )
                            if is_permanent_id_correct is True:

                                expected_requirements_array[q_2]['id'] = \
                                    actual_pi_release['releases'][0]['tender']['criteria'][q_0]['requirementGroups'][
                                        q_1]['requirements'][q_2]['id']
                            else:
                                expected_requirements_array[q_2]['id'] = \
                                    f"FR.COM-1.62.54: the 'releases[0].tender.criteria[{q_0}]." \
                                    f"requirementGroups[{q_1}].requirements[{q_2}].id' must be uuid."
                        except KeyError:
                            raise KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}]."
                                           f"requirementGroups[{q_1}].requirements[{q_2}].id'")

                        # Set title.
                        expected_requirements_array[q_2]['title'] = \
                            self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2][
                                'title']

                        # Set dataType.
                        expected_requirements_array[q_2]['dataType'] = \
                            self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2][
                                'dataType']

                        # Set description.
                        if "description" in self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                'requirements'][q_2]:
                            expected_requirements_array[q_2]['description'] = \
                                self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2][
                                    'description']
                        else:
                            del expected_requirements_array[q_2]['description']

                        # Set period.
                        if "period" in self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                'requirements'][q_2]:
                            expected_requirements_array[q_2]['period']['startDate'] = \
                                self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2][
                                    'period']['startDate']

                            expected_requirements_array[q_2]['period']['endDate'] = \
                                self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2][
                                    'period']['endDate']
                        else:
                            del expected_requirements_array[q_2]['period']

                        # Set expectedValue, minValue, maxValue and dataType.
                        if "expectedValue" not in self.payload['tender']['criteria'][q_0][
                                'requirementGroups'][q_1]['requirements'][q_2]:

                            del expected_requirements_array[q_2]['expectedValue']
                        else:
                            expected_requirements_array[q_2]['expectedValue'] = \
                                self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['expectedValue']

                            expected_requirements_array[q_2]['dataType'] = \
                                self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['dataType']

                        if "minValue" not in self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                'requirements'][q_2]:

                            del expected_requirements_array[q_2]['minValue']
                        else:
                            expected_requirements_array[q_2]['minValue'] = \
                                self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['minValue']

                            expected_requirements_array[q_2]['dataType'] = \
                                self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['dataType']

                        if "maxValue" not in self.payload['tender']['criteria'][q_0][
                                'requirementGroups'][q_1]['requirements'][q_2]:

                            del expected_requirements_array[q_2]['maxValue']
                        else:
                            expected_requirements_array[q_2]['maxValue'] = \
                                self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['maxValue']

                            expected_requirements_array[q_2]['dataType'] = \
                                self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['dataType']

                        # FR.COM-1.62.55: Set status.
                        expected_requirements_array[q_2]['status'] = "active"

                        # FR.COM-1.62.56: Set datePublished.
                        expected_requirements_array[q_2]['datePublished'] = \
                            self.message_for_platform['data']['operationDate']

                        # FR.COM-1.62.57: Set eligibleEvidences.
                        if "eligibleEvidences" in self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                'requirements'][q_2]:

                            expected_eligibleevidences_array = list()
                            for q_3 in range(len(
                                    self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['eligibleEvidences']
                            )):
                                expected_eligibleevidences_array.append(copy.deepcopy(
                                    self.expected_pi_release['releases'][0]['tender']['criteria'][0][
                                        'requirementGroups'][0]['requirements'][0]['eligibleEvidences'][0]
                                ))

                                # FR.COM-1.62.58: Set id.
                                try:
                                    is_permanent_id_correct = is_it_uuid(
                                        actual_pi_release['releases'][0]['tender']['criteria'][q_0][
                                            'requirementGroups'][q_1]['requirements'][q_2][
                                            'eligibleEvidences'][q_3]['id']
                                    )
                                    if is_permanent_id_correct is True:

                                        expected_eligibleevidences_array[q_3]['id'] = \
                                            actual_pi_release['releases'][0]['tender']['criteria'][q_0][
                                                'requirementGroups'][q_1]['requirements'][q_2][
                                                'eligibleEvidences'][q_3]['id']
                                    else:
                                        expected_eligibleevidences_array[q_3]['id'] = \
                                            f"FR.COM-1.62.58: the 'releases[0].tender.criteria[{q_0}]." \
                                            f"requirementGroups[{q_1}].requirements[{q_2}].eligibleEvidences[{q_3}]." \
                                            f"id' must be uuid."
                                except KeyError:
                                    raise KeyError(
                                        f"Mismatch key into path 'releases[0].tender.criteria[{q_0}]."
                                        f"requirementGroups[{q_1}].requirements[{q_2}].eligibleEvidences[{q_3}]."
                                        f"id'")

                                # Set title.
                                expected_eligibleevidences_array[q_3]['title'] = \
                                    self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['eligibleEvidences'][q_3]['title']

                                # Set description.
                                if "description" in self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['eligibleEvidences'][q_3]:

                                    expected_eligibleevidences_array[q_3]['description'] = \
                                        self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                            'requirements'][q_2]['eligibleEvidences'][q_3]['description']
                                else:
                                    del expected_eligibleevidences_array[q_3]['description']

                                # Set type.
                                expected_eligibleevidences_array[q_3]['type'] = \
                                    self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['eligibleEvidences'][q_3]['type']

                                # Set relatedDocument.
                                if "relatedDocument" in self.payload['tender']['criteria'][q_0][
                                        'requirementGroups'][q_1]['requirements'][q_2]['eligibleEvidences'][q_3]:

                                    expected_eligibleevidences_array[q_3]['relatedDocument']['id'] = \
                                        self.payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                            'requirements'][q_2]['eligibleEvidences'][q_3]['relatedDocument']['id']
                                else:
                                    del expected_eligibleevidences_array[q_3]['relatedDocument']

                            expected_requirements_array[q_2]['eligibleEvidences'] = expected_eligibleevidences_array
                        else:
                            del expected_requirements_array[q_2]['eligibleEvidences']

                    expected_requirementgroups_array[q_1]['requirements'] = expected_requirements_array
                expected_criteria_array[q_0]['requirementGroups'] = expected_requirementgroups_array
            self.expected_pi_release['releases'][0]['tender']['criteria'] = expected_criteria_array
        else:
            del self.expected_pi_release['releases'][0]['tender']['criteria']

        # FR.COM-1.62.65: Set conversions.
        if "conversions" in self.payload['tender']:
            expected_conversion_array = list()
            for q_0 in range(len(self.payload['tender']['conversions'])):
                expected_conversion_array.append(copy.deepcopy(
                    self.expected_pi_release['releases'][0]['tender']['conversions'][0]
                ))

                # FR.COM-1.62.66: Set id.
                try:
                    is_permanent_id_correct = is_it_uuid(
                        actual_pi_release['releases'][0]['tender']['conversions'][q_0]['id']
                    )
                    if is_permanent_id_correct is True:

                        expected_conversion_array[q_0]['id'] = \
                            actual_pi_release['releases'][0]['tender']['conversions'][q_0]['id']
                    else:
                        expected_conversion_array[q_0]['id'] = \
                            f"FR.COM-1.62.66: the 'releases[0].tender.conversions[{q_0}].id' must be uuid."
                except KeyError:
                    raise KeyError(f"Mismatch key into path 'releases[0].tender.conversions[{q_0}].id'")

                # What a requirement we need?
                actual_requirement = None
                for p_0 in range(len(self.payload['tender']['criteria'])):
                    for p_1 in range(len(self.payload['tender']['criteria'][p_0]['requirementGroups'])):
                        for p_2 in range(len(
                                self.payload['tender']['criteria'][p_0]['requirementGroups'][p_1]['requirements']
                        )):
                            if self.payload['tender']['criteria'][p_0]['requirementGroups'][p_1][
                                'requirements'][p_2]['id'] == self.payload['tender']['conversions'][q_0][
                                    'relatedItem']:
                                # Get the requirement from actual release.
                                actual_requirement = actual_pi_release['releases'][0]['tender']['criteria'][p_0][
                                    'requirementGroups'][p_1]['requirements'][p_2]

                # Set relatedItem.
                expected_conversion_array[q_0]['relatedItem'] = actual_requirement['id']

                # Set relatesTo.
                expected_conversion_array[q_0]['relatesTo'] = "requirement"

                # Set description.
                if "description" in self.payload['tender']['conversions'][q_0]:
                    expected_conversion_array[q_0]['description'] = \
                        self.payload['tender']['conversions'][q_0]['description']
                else:
                    del self.expected_pi_release['releases'][0]['tender']['conversions']

                # Set rationale.
                expected_conversion_array[q_0]['rationale'] = self.payload['tender']['conversions'][q_0]['rationale']

                # Set coefficients.
                expected_coefficients_array = list()
                for q_1 in range(len(self.payload['tender']['conversions'][q_0]['coefficients'])):
                    expected_coefficients_array.append(copy.deepcopy(
                        self.expected_pi_release['releases'][0]['tender']['conversions'][0]['coefficients'][0]
                    ))

                    # FR.COM-1.62.67: Set id.
                    try:
                        is_permanent_id_correct = is_it_uuid(
                            actual_pi_release['releases'][0]['tender']['conversions'][q_0]['coefficients'][q_1]['id']
                        )
                        if is_permanent_id_correct is True:

                            expected_coefficients_array[q_1]['id'] = \
                                actual_pi_release['releases'][0]['tender']['conversions'][q_0][
                                    'coefficients'][q_1]['id']
                        else:
                            expected_coefficients_array[q_1]['id'] = \
                                f"FR.COM-1.62.67: the 'releases[0].tender.conversions[{q_0}].coefficients[{q_1}].id'" \
                                f"must be uuid."
                    except KeyError:
                        raise KeyError(f"Mismatch key into path 'releases[0].tender.conversions[{q_0}]."
                                       f"coefficients[{q_1}].id'")

                    # Set value.
                    expected_coefficients_array[q_1]['value'] = \
                        self.payload['tender']['conversions'][q_0]['coefficients'][q_1]['value']

                    # Set coefficient.
                    expected_coefficients_array[q_1]['coefficient'] = \
                        self.payload['tender']['conversions'][q_0]['coefficients'][q_1]['coefficient']

                expected_conversion_array[q_0]['coefficients'] = expected_coefficients_array
            self.expected_pi_release['releases'][0]['tender']['conversions'] = expected_conversion_array
        else:
            del self.expected_pi_release['releases'][0]['tender']['conversions']

        # FR.COM-1.62.39: Set lots.
        expected_lots_array = list()
        for q_0 in range(len(self.payload['tender']['lots'])):
            expected_lots_array.append(copy.deepcopy(self.expected_pi_release['releases'][0]['tender']['lots'][0]))

            # FR.COM-1.62.40: Set id.
            try:
                is_permanent_id_correct = is_it_uuid(
                    actual_pi_release['releases'][0]['tender']['lots'][q_0]['id']
                )
                if is_permanent_id_correct is True:
                    expected_lots_array[q_0]['id'] = actual_pi_release['releases'][0]['tender']['lots'][q_0]['id']
                else:
                    expected_lots_array[q_0]['id'] = \
                        f"FR.COM-1.62.40: the 'releases[0].tender.lots[{q_0}].id' must be uuid."
            except KeyError:
                raise KeyError(f"Mismatch key into path 'releases[0].tender.lots[{q_0}].id'")

            # Set internalId.
            if "internalId" in self.payload['tender']['lots'][q_0]:
                expected_lots_array[q_0]['internalId'] = self.payload['tender']['lots'][q_0]['internalId']
            else:
                del expected_lots_array[q_0]['internalId']

            # Set title.
            expected_lots_array[q_0]['title'] = self.payload['tender']['lots'][q_0]['title']

            # Set description
            expected_lots_array[q_0]['description'] = self.payload['tender']['lots'][q_0]['description']

            # FR.COM-1.62.41: Set status.
            expected_lots_array[q_0]['status'] = "planning"

            # Set value.
            expected_lots_array[q_0]['value']['amount'] = self.payload['tender']['lots'][q_0]['value']['amount']
            expected_lots_array[q_0]['value']['currency'] = self.payload['tender']['lots'][q_0]['value']['currency']

            # Set contactPeriod.
            expected_lots_array[q_0]['contractPeriod']['startDate'] = \
                self.payload['tender']['lots'][q_0]['contractPeriod']['startDate']

            expected_lots_array[q_0]['contractPeriod']['endDate'] = \
                self.payload['tender']['lots'][q_0]['contractPeriod']['endDate']

            # Set placeOfPerformance.

            # Set streetAddress.
            expected_lots_array[q_0]['placeOfPerformance']['address']['streetAddress'] = \
                self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['streetAddress']

            # Set postalCode.
            if "postalCode" in self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']:

                expected_lots_array[q_0]['placeOfPerformance']['address']['postalCode'] = \
                    self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['postalCode']
            else:
                del expected_lots_array[q_0]['placeOfPerformance']['address']['postalCode']

            # Set addressDetails object for items array.
            try:
                lot_country_data = get_value_from_country_csv(

                    country=self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'country']['id'],
                    language=self.language
                )
                expected_lot_country_object = [{
                    "scheme": lot_country_data[2].upper(),
                    "id": self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'country']['id'],
                    "description": lot_country_data[1],
                    "uri": lot_country_data[3]
                }]

                lot_region_data = get_value_from_region_csv(

                    region=self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'region']['id'],
                    country=self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'country']['id'],
                    language=self.language
                )
                expected_lot_region_object = [{
                    "scheme": lot_region_data[2],
                    "id": self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'region']['id'],
                    "description": lot_region_data[1],
                    "uri": lot_region_data[3]
                }]

                if self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'locality']['scheme'] != "other":

                    lot_locality_data = get_value_from_locality_csv(

                        locality=self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'locality']['id'],
                        region=self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'region']['id'],
                        country=self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'country']['id'],
                        language=self.language
                    )
                    expected_lot_locality_object = [{
                        "scheme": lot_locality_data[2],

                        "id": self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'locality']['id'],
                        "description": lot_locality_data[1],
                        "uri": lot_locality_data[3]
                    }]
                else:
                    expected_lot_locality_object = [{

                        "scheme": self.payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                            'addressDetails']['locality']['scheme'],

                        "id": self.payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'locality']['id'],

                        "description": self.payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                            'addressDetails']['locality']['description']
                    }]

                expected_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality'] = \
                    expected_lot_locality_object[0]

                expected_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['country'] = \
                    expected_lot_country_object[0]

                expected_lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['region'] = \
                    expected_lot_region_object[0]
            except ValueError:
                ValueError("Impossible to prepare addressDetails object for lots array")

            # Set description.
            if "description" in self.payload['tender']['lots'][q_0]['placeOfPerformance']:
                expected_lots_array[q_0]['placeOfPerformance']['description'] = \
                    self.payload['tender']['lots'][q_0]['placeOfPerformance']['description']
            del expected_lots_array[q_0]['placeOfPerformance']['description']

            # Set hasOptions
            if "hasOptions" in self.payload['tender']['lots'][q_0]:
                expected_lots_array[q_0]['hasOptions'] = self.payload['tender']['lots'][q_0]['hasOptions']
            else:
                del expected_lots_array[q_0]['hasOptions']

            # Set options.
            if "options" in self.payload['tender']['lots'][q_0]:
                expected_options_array = list()
                for q_1 in range(len(self.payload['tender']['lots'][q_0]['options'])):
                    expected_options_array.append(copy.deepcopy(
                        self.expected_pi_release['releases'][0]['tender']['lots'][0]['options'][0]
                    ))

                    if "description" in self.payload['tender']['lots'][q_0]['options'][q_1]:
                        expected_options_array[q_1]['description'] = \
                            self.payload['tender']['lots'][q_0]['options'][q_1]['description']
                    else:
                        del expected_options_array[q_1]['description']

                    if "period" in self.payload['tender']['lots'][q_0]['options'][q_1]:
                        if "durationInDays" in self.payload['tender']['lots'][q_0]['options'][q_1]['period']:

                            expected_options_array[q_1]['period']['durationInDays'] = \
                                int(self.payload['tender']['lots'][q_0]['options'][q_1]['period']['durationInDays'])
                        else:
                            del expected_options_array[q_1]['period']['durationInDays']

                        if "startDate" in self.payload['tender']['lots'][q_0]['options'][q_1]['period']:

                            expected_options_array[q_1]['period']['startDate'] = \
                                self.payload['tender']['lots'][q_0]['options'][q_1]['period']['startDate']
                        else:
                            del expected_options_array[q_1]['period']['startDate']

                        if "endDate" in self.payload['tender']['lots'][q_0]['options'][q_1]['period']:

                            expected_options_array[q_1]['period']['endDate'] = \
                                self.payload['tender']['lots'][q_0]['options'][q_1]['period']['endDate']
                        else:
                            del expected_options_array[q_1]['endDate']

                        if "maxExtentDate" in self.payload['tender']['lots'][q_0]['options'][q_1]['period']:

                            expected_options_array[q_1]['period']['maxExtentDate'] = \
                                self.payload['tender']['lots'][q_0]['options'][q_1]['period']['maxExtentDate']
                        else:
                            del expected_options_array[q_1]['period']['maxExtentDate']
                    else:
                        del expected_options_array[q_1]['period']

                expected_lots_array[q_0]['options'] = expected_options_array
            else:
                del expected_lots_array[q_0]['options']

            # Set hasRecurrence
            if "hasRecurrence" in self.payload['tender']['lots'][q_0]:
                expected_lots_array[q_0]['hasRecurrence'] = self.payload['tender']['lots'][q_0]['hasRecurrence']
            else:
                del expected_lots_array[q_0]['hasRecurrence']

            # Set recurrence.
            if "recurrence" in self.payload['tender']['lots'][q_0]:
                if "dates" in self.payload['tender']['lots'][q_0]['recurrence']:
                    expected_dates_array = list()
                    for q_1 in range(len(self.payload['tender']['lots'][q_0]['recurrence']['dates'])):
                        expected_dates_array.append(copy.deepcopy(
                            self.expected_pi_release['releases'][0]['tender']['lots'][0]['recurrence']['dates'][0]
                        ))

                        expected_dates_array[q_1]['startDate'] = \
                            self.payload['tender']['lots'][q_0]['recurrence']['dates'][q_1]['startDate']

                    expected_lots_array[q_0]['recurrence']['dates'] = expected_dates_array
                else:
                    del expected_lots_array[q_0]['recurrence']['dates']

                if "description" in self.payload['tender']['lots'][q_0]['recurrence']:
                    expected_lots_array[q_0]['recurrence']['description'] = \
                        self.payload['tender']['lots'][q_0]['recurrence']['description']
                else:
                    del expected_lots_array[q_0]['recurrence']['description']
            else:
                del expected_lots_array[q_0]['recurrence']

            # Set hasRenewal.
            if "hasRenewal" in self.payload['tender']['lots'][q_0]:
                expected_lots_array[q_0]['hasRenewal'] = self.payload['tender']['lots'][q_0]['hasRenewal']
            else:
                del expected_lots_array[q_0]['hasRenewal']

            # Set renewal.
            if "renewal" in self.payload['tender']['lots'][q_0]:
                if "description" in self.payload['tender']['lots'][q_0]['renewal']:
                    expected_lots_array[q_0]['renewal']['description'] = \
                        self.payload['tender']['lots'][q_0]['renewal']['description']
                else:
                    del expected_lots_array[q_0]['renewal']['description']

                if "minimumRenewals" in self.payload['tender']['lots'][q_0]['renewal']:
                    expected_lots_array[q_0]['renewal']['minimumRenewals'] = \
                        int(self.payload['tender']['lots'][q_0]['renewal']['minimumRenewals'])
                else:
                    del expected_lots_array[q_0]['renewal']['minimumRenewals']

                if "maximumRenewals" in self.payload['tender']['lots'][q_0]['renewal']:
                    expected_lots_array[q_0]['renewal']['maximumRenewals'] = \
                        int(self.payload['tender']['lots'][q_0]['renewal']['maximumRenewals'])
                else:
                    del expected_lots_array[q_0]['renewal']['maximumRenewals']

                if "period" in self.payload['tender']['lots'][q_0]['renewal']:
                    if "durationInDays" in self.payload['tender']['lots'][q_0]['renewal']['period']:

                        expected_lots_array[q_0]['renewal']['period']['durationInDays'] = \
                            int(self.payload['tender']['lots'][q_0]['renewal']['period']['durationInDays'])
                    else:
                        del expected_lots_array[q_0]['renewal']['period']['durationInDays']

                    if "startDate" in self.payload['tender']['lots'][q_0]['renewal']['period']:

                        expected_lots_array[q_0]['renewal']['period']['startDate'] = \
                            self.payload['tender']['lots'][q_0]['renewal']['period']['startDate']
                    else:
                        del expected_lots_array[q_0]['renewal']['period']['startDate']

                    if "endDate" in self.payload['tender']['lots'][q_0]['renewal']['period']:

                        expected_lots_array[q_0]['renewal']['period']['endDate'] = \
                            self.payload['tender']['lots'][q_0]['renewal']['period']['endDate']
                    else:
                        del expected_lots_array[q_0]['renewal']['period']['endDate']

                    if "maxExtentDate" in self.payload['tender']['lots'][q_0]['renewal']['period']:

                        expected_lots_array[q_0]['renewal']['period']['maxExtentDate'] = \
                            self.payload['tender']['lots'][q_0]['renewal']['period']['maxExtentDate']
                    else:
                        del expected_lots_array[q_0]['renewal']['period']['maxExtentDate']
                else:
                    del expected_lots_array[q_0]['renewal']['period']
            else:
                del expected_lots_array[q_0]['renewal']

        self.expected_pi_release['releases'][0]['tender']['lots'] = expected_lots_array

        # FR.COM-1.62.45: Set items.
        expected_items_array = list()

        for q_0 in range(len(self.payload['tender']['items'])):
            expected_items_array.append(copy.deepcopy(self.expected_pi_release['releases'][0]['tender']['items'][0]))

            # FR.COM-1.62.46: Set id.
            try:
                is_permanent_id_correct = is_it_uuid(
                    actual_pi_release['releases'][0]['tender']['items'][q_0]['id']
                )
                if is_permanent_id_correct is True:
                    expected_items_array[q_0]['id'] = actual_pi_release['releases'][0]['tender']['items'][q_0]['id']
                else:
                    expected_items_array[q_0]['id'] = \
                        f"FR.COM-1.62.46: the 'releases[0].tender.items[{q_0}].id' must be uuid."
            except KeyError:
                raise KeyError(f"Mismatch key into path 'releases[0].tender.items[{q_0}].id'")

            # Set internalId.
            if "internalId" in self.payload['tender']['items'][q_0]:
                expected_items_array[q_0]['internalId'] = self.payload['tender']['items'][q_0]['internalId']
            else:
                del self.expected_pi_release['releases'][0]['tender']['items'][q_0]['internalId']

            # Set classification.
            expected_cpv_data = get_value_from_cpv_dictionary_csv(
                cpv=self.payload['tender']['items'][q_0]['classification']['id'],
                language=self.language
            )
            expected_items_array[q_0]['classification']['scheme'] = "CPV"
            expected_items_array[q_0]['classification']['id'] = expected_cpv_data[0]
            expected_items_array[q_0]['classification']['description'] = expected_cpv_data[1]

            # Set additionalClassifications.
            if "additionalClassifications" in self.payload['tender']['items'][q_0]:
                additional_classifications = list()
                for q_1 in range(len(self.payload['tender']['items'][q_0]['additionalClassifications'])):
                    additional_classifications.append(copy.deepcopy(
                        self.expected_pi_release['releases'][0]['tender']['items'][0]['additionalClassifications'][0]
                    ))

                    expected_cpvs_data = get_value_from_cpvs_dictionary_csv(
                        cpvs=self.payload['tender']['items'][q_0]['additionalClassifications'][q_1]['id'],
                        language=self.language
                    )

                    additional_classifications[q_1]['scheme'] = "CPVS"
                    additional_classifications[q_1]['id'] = expected_cpvs_data[0]
                    additional_classifications[q_1]['description'] = expected_cpvs_data[2]

                expected_items_array[q_0]['additionalClassifications'] = additional_classifications
            else:
                del expected_items_array[q_0]['additionalClassifications']

            # Set quantity.
            expected_items_array[q_0]['quantity'] = round(float(self.payload['tender']['items'][q_0]['quantity']), 2)

            # Set unit.
            expected_unit_data = get_value_from_classification_unit_dictionary_csv(
                unit_id=self.payload['tender']['items'][q_0]['unit']['id'],
                language=self.language
            )
            expected_items_array[q_0]['unit']['id'] = expected_unit_data[0]
            expected_items_array[q_0]['unit']['name'] = expected_unit_data[1]

            # Set description.
            expected_items_array[q_0]['description'] = self.payload['tender']['items'][q_0]['description']

            # Set relatedLot.
            expected_items_array[q_0]['relatedLot'] = \
                self.expected_pi_release['releases'][0]['tender']['lots'][q_0]['id']

        self.expected_pi_release['releases'][0]['tender']['items'] = expected_items_array

        # FR.COM-1.62.69: Set documents.
        if "documents" in self.payload['tender']:
            expected_documents_array = list()
            for q_0 in range(len(self.payload['tender']['documents'])):
                expected_documents_array.append(copy.deepcopy(
                    self.expected_pi_release['releases'][0]['tender']['documents'][0]
                ))

                # Set id.
                expected_documents_array[q_0]['id'] = self.payload['tender']['documents'][q_0]['id']

                # Set title.
                expected_documents_array[q_0]['title'] = self.payload['tender']['documents'][q_0]['title']

                # Set documentType.
                expected_documents_array[q_0]['documentType'] = self.payload['tender']['documents'][q_0]['documentType']

                # Set description
                if "description" in self.payload['tender']['documents'][q_0]:
                    expected_documents_array[q_0]['description'] = \
                        self.payload['tender']['documents'][q_0]['description']
                else:
                    del expected_documents_array[q_0]['description']

                # Set url.
                expected_documents_array[q_0]['url'] = \
                    f"{self.metadata_document_url}/{expected_documents_array[q_0]['id']}"

                # Set datePublished.
                expected_documents_array[q_0]['datePublished'] = self.message_for_platform['data']['operationDate']

                # FR.COM-1.62.70: Set relatedLots.
                if "relatedLots" in self.payload['tender']['documents'][q_0]:
                    expected_documents_array[q_0]['relatedLots'] = \
                        [self.expected_pi_release['releases'][0]['tender']['lots'][0]['id']]
                else:
                    del expected_documents_array[q_0]['relatedLots']

            self.expected_pi_release['releases'][0]['tender']['documents'] = expected_documents_array
        else:
            del self.expected_pi_release['releases'][0]['tender']['documents']

        # FR.COM-1.62.60: Set targets.
        if "targets" in self.payload['tender']:
            expected_targets_array = list()
            for q_0 in range(len(self.payload['tender']['targets'])):
                expected_targets_array.append(copy.deepcopy(
                    self.expected_pi_release['releases'][0]['tender']['targets'][0]
                ))

                # FR.COM-1.62.61: Set id.
                try:
                    is_permanent_id_correct = is_it_uuid(
                        actual_pi_release['releases'][0]['tender']['targets'][q_0]['id']
                    )
                    if is_permanent_id_correct is True:

                        expected_targets_array[q_0]['id'] = \
                            actual_pi_release['releases'][0]['tender']['targets'][q_0]['id']
                    else:
                        expected_targets_array[q_0]['id'] = \
                            f"FR.COM-1.62.61: the 'releases[0].tender.targets[{q_0}].id' must be uuid."
                except KeyError:
                    raise KeyError(f"Mismatch key into path 'releases[0].tender.targets[{q_0}].id'")

                # Set title.
                expected_targets_array[q_0]['title'] = self.payload['tender']['targets'][q_0]['title']

                # Set relatesTo.
                expected_targets_array[q_0]['relatesTo'] = self.payload['tender']['targets'][q_0]['relatesTo']

                # FR.COM-1.62.63: Set relatedItem.
                if "relatedItem" in self.payload['tender']['targets'][q_0]:
                    if expected_targets_array[q_0]['relatesTo'] == "lot":
                        expected_targets_array[q_0]['relatedItem'] = \
                            self.expected_pi_release['releases'][0]['tender']['lots'][0]['id']

                    elif expected_targets_array[q_0]['relatesTo'] == "item":
                        expected_targets_array[q_0]['relatedItem'] = \
                            self.expected_pi_release['releases'][0]['tender']['items'][0]['id']

                    else:
                        del expected_targets_array[q_0]['relatedItem']
                else:
                    del expected_targets_array[q_0]['relatedItem']

                # Set observations.
                expected_observations_array = list()
                for q_1 in range(len(self.payload['tender']['targets'][q_0]['observations'])):
                    expected_observations_array.append(copy.deepcopy(
                        self.expected_pi_release['releases'][0]['tender']['targets'][0]['observations'][0]
                    ))

                    # FR.COM-1.62.62: Set id.
                    try:
                        is_permanent_id_correct = is_it_uuid(
                            actual_pi_release['releases'][0]['tender']['targets'][q_0]['observations'][q_1]['id']
                        )
                        if is_permanent_id_correct is True:

                            expected_observations_array[q_1]['id'] = \
                                actual_pi_release['releases'][0]['tender']['targets'][q_0]['observations'][q_1]['id']
                        else:
                            expected_observations_array[q_1]['id'] = \
                                f"FR.COM-1.62.61: the 'releases[0].tender.targets[{q_0}].observations[{q_1}].id' " \
                                f"must be uuid."
                    except KeyError:
                        raise KeyError(
                            f"Mismatch key into path 'releases[0].tender.targets[{q_0}].observations[{q_1}].id'")

                    # Set period.
                    if "period" in self.payload['tender']['targets'][q_0]['observations'][q_1]:

                        # Set startDate.
                        if "startDate" in self.payload['tender']['targets'][q_0]['observations'][q_1]['period']:
                            expected_observations_array[q_1]['period']['startDate'] = \
                                self.payload['tender']['targets'][q_0]['observations'][q_1]['period']['startDate']
                        else:
                            del expected_observations_array[q_1]['period']['startDate']

                        # Set endDate.
                        if "startDate" in self.payload['tender']['targets'][q_0]['observations'][q_1]['period']:
                            expected_observations_array[q_1]['period']['endDate'] = \
                                self.payload['tender']['targets'][q_0]['observations'][q_1]['period']['endDate']
                        else:
                            del expected_observations_array[q_1]['period']['endDate']
                    else:
                        del expected_observations_array[q_1]['period']

                    # Set measure.
                    expected_observations_array[q_1]['measure'] = \
                        self.payload['tender']['targets'][q_0]['observations'][q_1]['measure']

                    # Set unit.
                    expected_unit_data = get_value_from_classification_unit_dictionary_csv(
                        unit_id=self.payload['tender']['targets'][q_0]['observations'][q_1]['unit']['id'],
                        language=self.language
                    )
                    expected_observations_array[q_1]['unit']['id'] = expected_unit_data[0]
                    expected_observations_array[q_1]['unit']['name'] = expected_unit_data[1]

                    # Set dimensions.
                    if "dimensions" in self.payload['tender']['targets'][q_0]['observations'][q_1]:
                        expected_observations_array[q_1]['dimensions'] = \
                            self.payload['tender']['targets'][q_0]['observations'][q_1]['dimensions']
                    else:
                        del expected_observations_array[q_1]['dimensions']

                    # Set notes.
                    expected_observations_array[q_1]['notes'] = \
                        self.payload['tender']['targets'][q_0]['observations'][q_1]['notes']

                    # FR.COM-1.62.64: Set relatedRequirementId.
                    if "relatedRequirementId" in self.payload['tender']['targets'][q_0]['observations'][q_1]:

                        # What a requirement we need?
                        for p_0 in range(len(self.payload['tender']['criteria'])):
                            for p_1 in range(len(self.payload['tender']['criteria'][p_0]['requirementGroups'])):
                                for p_2 in range(len(
                                        self.payload['tender']['criteria'][p_0]['requirementGroups'][p_1][
                                            'requirements']
                                )):
                                    if self.payload['tender']['criteria'][p_0]['requirementGroups'][p_1][
                                            'requirements'][p_2]['id'] == self.payload['tender']['targets'][q_0][
                                            'observations'][q_1]['relatedRequirementId']:
                                        # Get the requirement from actual release.
                                        actual_requirement = \
                                            actual_pi_release['releases'][0]['tender']['criteria'][p_0][
                                                'requirementGroups'][p_1]['requirements'][p_2]

                                        expected_observations_array[q_1]['relatedRequirementId'] = \
                                            actual_requirement['id']
                    else:
                        del expected_observations_array[q_1]['relatedRequirementId']

                expected_targets_array[q_0]['observations'] = expected_observations_array
            self.expected_pi_release['releases'][0]['tender']['targets'] = expected_targets_array
        else:
            del self.expected_pi_release['releases'][0]['tender']['targets']

        # Set electronicAuctions.
        if "electronicAuctions" in self.payload['tender']:
            expected_details_array = list()
            for q_0 in range(len(self.payload['tender']['electronicAuctions']['details'])):
                expected_details_array.append(copy.deepcopy(
                    self.expected_pi_release['releases'][0]['tender']['electronicAuctions']['details'][0]
                ))

                # Set id, according to 'bpeCreateIdsDelegate'.
                try:
                    is_permanent_id_correct = is_it_uuid(
                        actual_pi_release['releases'][0]['tender']['electronicAuctions']['details'][q_0]['id']
                    )
                    if is_permanent_id_correct is True:

                        expected_details_array[q_0]['id'] = \
                            actual_pi_release['releases'][0]['tender']['electronicAuctions']['details'][q_0]['id']
                    else:
                        expected_details_array[q_0]['id'] = \
                            f"'bpeCreateIdsDelegate': the 'releases[0].tender.electronicAuctions.details[{q_0}].id' " \
                            f"must be uuid."
                except KeyError:
                    raise KeyError(f"Mismatch key into path 'releases[0].tender.electronicAuctions.details[{q_0}].id'")

                # Set relatedLot.
                # What kind of lot we need?
                for p_0 in range(len(self.payload['tender']['lots'])):
                    if self.payload['tender']['lots'][p_0]['id'] == \
                            self.payload['tender']['electronicAuctions']['details'][q_0]['relatedLot']:
                        expected_details_array[q_0]['relatedLot'] = \
                            actual_pi_release['releases'][0]['tender']['lots'][p_0]['id']

                # Set eligibleMinimumDifference.
                expected_details_array[q_0]['electronicAuctionModalities'][0]['eligibleMinimumDifference']['amount'] \
                    = \
                    self.payload['tender']['electronicAuctions']['details'][q_0]['electronicAuctionModalities'][0][
                        'eligibleMinimumDifference']['amount']

                expected_details_array[q_0]['electronicAuctionModalities'][0]['eligibleMinimumDifference']['currency'] \
                    = \
                    self.payload['tender']['electronicAuctions']['details'][q_0]['electronicAuctionModalities'][0][
                        'eligibleMinimumDifference']['currency']

            self.expected_pi_release['releases'][0]['tender']['electronicAuctions']['details'] = expected_details_array
        else:
            del self.expected_pi_release['releases'][0]['tender']['electronicAuctions']

        # FR.COM-1.62.14: Set awardCriteria.
        self.expected_pi_release['releases'][0]['tender']['awardCriteria'] = self.payload['tender']['awardCriteria']

        # FR.COM-1.62.15: Set awardCriteriaDetails.
        self.expected_pi_release['releases'][0]['tender']['awardCriteriaDetails'] = \
            self.payload['tender']['awardCriteriaDetails']

        # FR.COM-1.62.16: Set tenderPeriod.
        self.expected_pi_release['releases'][0]['tender']['tenderPeriod']['startDate'] = \
            self.payload['tender']['tenderPeriod']['startDate']

        # FR.COM-1.62.19: Set procurementMethodModalities.
        if "procurementMethodModalities" in self.payload['tender']:
            self.expected_pi_release['releases'][0]['tender']['procurementMethodModalities'] = \
                self.payload['tender']['procurementMethodModalities']
        else:
            del self.expected_pi_release['releases'][0]['tender']['procurementMethodModalities']

        # FR.COM-3.4.3: Set some value.
        # Set enquiryPeriod.
        if "enquiryPeriod" in self.payload['tender']:
            self.expected_pi_release['releases'][0]['tender']['enquiryPeriod']['startDate'] = \
                self.message_for_platform['data']['operationDate']

            self.expected_pi_release['releases'][0]['tender']['enquiryPeriod']['endDate'] = \
                self.payload['tender']['enquiryPeriod']['endDate']
        else:
            del self.expected_pi_release['releases'][0]['tender']['enquiryPeriod']

        # FR.COM-1.62.37: Set submissionMethod.
        self.expected_pi_release['releases'][0]['tender']['submissionMethod'] = ["electronicSubmission"]

        # Set submissionMethodDetails.
        submission_method_details = get_value_from_code_translation_csv(
            parameter="submissionMethodDetails",
            country=self.country,
            language=self.language
        )
        self.expected_pi_release['releases'][0]['tender']['submissionMethodDetails'] = submission_method_details

        # Set tender.submissionMethodRationale.
        submission_method_rationale = get_value_from_code_translation_csv(
            parameter="submissionMethodRationale",
            country=self.country,
            language=self.language
        )
        self.expected_pi_release['releases'][0]['tender']['submissionMethodRationale'] = [submission_method_rationale]

        """"Enrich 'relatedProcesses' object for expected PI release: releases[0].relatedProcesses"""
        # FR.COM-1.62.76: Set id.
        try:
            is_permanent_id_correct = is_it_uuid(
                actual_pi_release['releases'][0]['relatedProcesses'][0]['id']
            )
            if is_permanent_id_correct is True:

                self.expected_pi_release['releases'][0]['relatedProcesses'][0]['id'] = \
                    actual_pi_release['releases'][0]['relatedProcesses'][0]['id']
            else:
                self.expected_pi_release['releases'][0]['relatedProcesses'][0]['id'] = \
                    f"FR.COM-1.62.76: the 'releases[0].relatedProcesses[{0}].id' must be uuid."
        except KeyError:
            raise KeyError(f"Mismatch key into path 'releases[0].relatedProcesses[{0}].id'")

        # FR.COM-1.62.77: Set relationship.
        self.expected_pi_release['releases'][0]['relatedProcesses'][0]['relationship'] = ["parent"]

        # FR.COM-1.62.78: Set ocid.
        self.expected_pi_release['releases'][0]['relatedProcesses'][0]['scheme'] = "ocid"

        # FR.COM-1.62.79: Set identifier.
        self.expected_pi_release['releases'][0]['relatedProcesses'][0]['identifier'] = \
            self.message_for_platform['data']['ocid'][:28]

        # FR.COM-1.62.80: Set uri.
        self.expected_pi_release['releases'][0]['relatedProcesses'][0]['uri'] = \
            f"{self.metadata_tender_url}/{self.message_for_platform['data']['ocid'][:28]}/" \
            f"{self.message_for_platform['data']['ocid'][:28]}"
        return self.expected_pi_release

    def build_expected_ms_release(self, actual_ms_release, pmd, need_fs: bool):
        """Build MS release."""

        """Enrich general attribute for expected MS release"""
        self.expected_ms_release['uri'] = \
            f"{self.metadata_tender_url}/{self.message_for_platform['data']['ocid'][:28]}/" \
            f"{self.message_for_platform['data']['ocid'][:28]}"

        self.expected_ms_release['version'] = "1.1"
        self.expected_ms_release['extensions'] = self.extensions
        self.expected_ms_release['publisher']['name'] = self.publisher_name
        self.expected_ms_release['publisher']['uri'] = self.publisher_uri
        self.expected_ms_release['license'] = "http://opendefinition.org/licenses/"
        self.expected_ms_release['publicationPolicy'] = "http://opendefinition.org/licenses/"

        # FR.COM-3.4.6 Set created date for release.
        self.expected_ms_release['publishedDate'] = self.message_for_platform['data']['operationDate']

        """Enrich general attribute for expected MS release: releases[0]"""
        # FR.COM-3.4.2: Set ocid.
        self.expected_ms_release['releases'][0]['ocid'] = self.message_for_platform['data']['ocid'][:28]

        # FR.COM-3.4.4: Set id.
        self.expected_ms_release['releases'][0]['id'] = \
            f"{self.message_for_platform['data']['ocid'][:28]}-{actual_ms_release['releases'][0]['id'][29:42]}"

        # FR.COM-1.62.6: Set date.
        self.expected_ms_release['releases'][0]['date'] = self.message_for_platform['data']['operationDate']

        # FR.COM-3.4.7: Set tag.
        self.expected_ms_release['releases'][0]['tag'] = ["compiled"]

        # FR.COM-3.4.8: Set initiationType.
        self.expected_ms_release['releases'][0]['initiationType'] = "tender"

        # FR.COM-3.4.11: Set language.
        self.expected_ms_release['releases'][0]['language'] = self.language

        """Enrich 'planning' object for expected MS release: releases[0].planning"""
        # Set rationale.
        if "rationale" in self.payload['planning']:
            self.expected_ms_release['releases'][0]['planning']['rationale'] = self.payload['planning']['rationale']
        else:
            del self.expected_ms_release['releases'][0]['planning']['rationale']

        # Set budget.description.
        if "description" in self.payload['planning']['budget']:
            self.expected_ms_release['releases'][0]['planning']['budget']['description'] = \
                self.payload['planning']['budget']['description']
        else:
            del self.expected_ms_release['releases'][0]['planning']['budget']['description']

        # Set budget.budgetBreakdown
        expected_budget_breakdown_array = list()
        for q_0 in range(len(self.payload['planning']['budget']['budgetBreakdown'])):
            expected_budget_breakdown_array.append(copy.deepcopy(
                self.expected_ms_release['releases'][0]['planning']['budget']['budgetBreakdown'][0]
            ))

            # Set id.
            try:
                is_permanent_id_correct = is_it_uuid(
                    actual_ms_release['releases'][0]['planning']['budget']['budgetBreakdown'][q_0]['id']
                )
                if is_permanent_id_correct is True:

                    expected_budget_breakdown_array[q_0]['id'] = \
                        actual_ms_release['releases'][0]['planning']['budget']['budgetBreakdown'][q_0]['id']
                else:
                    expected_budget_breakdown_array[q_0]['id'] = \
                        f"The 'releases[0].planning.budget.budgetBreakdown[{q_0}].id' must be uuid."
            except KeyError:
                raise KeyError(f"Mismatch key into path 'releases[0].planning.budget.budgetBreakdown[{q_0}].id'")

            # Set amount.
            expected_budget_breakdown_array[q_0]['amount']['amount'] = \
                self.payload['planning']['budget']['budgetBreakdown'][q_0]['amount']['amount']

            expected_budget_breakdown_array[q_0]['amount']['currency'] = \
                self.payload['planning']['budget']['budgetBreakdown'][q_0]['amount']['currency']

            # Set classifications.
            expected_budget_breakdown_array[q_0]['classifications']['ei'] = \
                self.payload['planning']['budget']['budgetBreakdown'][q_0]['classifications']['ei']

            if "fs" in self.payload['planning']['budget']['budgetBreakdown'][q_0]['classifications']:
                expected_budget_breakdown_array[q_0]['classifications']['fs'] = \
                    self.payload['planning']['budget']['budgetBreakdown'][q_0]['classifications']['fs']

                fs_url = \
                    f"{self.metadata_budget_url}/" \
                    f"{self.payload['planning']['budget']['budgetBreakdown'][q_0]['classifications']['ei']}/" \
                    f"{self.payload['planning']['budget']['budgetBreakdown'][q_0]['classifications']['fs']}"

                actual_fs_release = requests.get(fs_url).json()

                # FR.COM-14.5.8: Set description.
                if "description" in actual_fs_release['releases'][0]['planning']['budget']:
                    expected_budget_breakdown_array[q_0]['description'] = \
                        actual_fs_release['releases'][0]['planning']['budget']['description']
                else:
                    del expected_budget_breakdown_array[q_0]['description']

                # FR.COM-14.5.7: Set period.
                expected_budget_breakdown_array[q_0]['period']['startDate'] = \
                    actual_fs_release['releases'][0]['planning']['budget']['period']['startDate']

                expected_budget_breakdown_array[q_0]['period']['endDate'] = \
                    actual_fs_release['releases'][0]['planning']['budget']['period']['endDate']

                # FR.COM-14.5.9: Set europeanUnionFunding.
                if "europeanUnionFunding" in actual_fs_release['releases'][0]['planning']['budget']:

                    expected_budget_breakdown_array[q_0]['europeanUnionFunding']['projectIdentifier'] = \
                        actual_fs_release['releases'][0]['planning']['budget']['europeanUnionFunding'][
                            'projectIdentifier']

                    expected_budget_breakdown_array[q_0]['europeanUnionFunding']['projectName'] \
                        = actual_fs_release['releases'][0]['planning']['budget']['europeanUnionFunding']['projectName']

                    if "uri" in actual_fs_release['releases'][0]['planning']['budget']['europeanUnionFunding']:

                        expected_budget_breakdown_array[q_0]['europeanUnionFunding']['uri'] = \
                            actual_fs_release['releases'][0]['planning']['budget']['europeanUnionFunding']['uri']

                    else:
                        del expected_budget_breakdown_array[q_0]['europeanUnionFunding']['uri']
                else:
                    del expected_budget_breakdown_array[q_0]['europeanUnionFunding']

                # FR.COM-14.5.6: Set sourceParty.
                expected_budget_breakdown_array[q_0]['sourceParty']['id'] = \
                    actual_fs_release['releases'][0]['planning']['budget']['sourceEntity']['id']

                expected_budget_breakdown_array[q_0]['sourceParty']['name'] = \
                    actual_fs_release['releases'][0]['planning']['budget']['sourceEntity']['name']
            else:
                del expected_budget_breakdown_array[q_0]['classifications']['fs']
                del expected_budget_breakdown_array[q_0]['description']
                del expected_budget_breakdown_array[q_0]['europeanUnionFunding']
                del expected_budget_breakdown_array[q_0]['sourceParty']
                del expected_budget_breakdown_array[q_0]['period']

        self.expected_ms_release['releases'][0]['planning']['budget']['budgetBreakdown'] = \
            expected_budget_breakdown_array

        """Enrich 'parties' object for expected MS release: releases[0].parties"""
        # Prepare party with 'procuringEntity' role.
        procuringentity_role_array = list()

        procuringentity_role_array.append(copy.deepcopy(self.expected_ms_release['releases'][0]['parties'][0]))
        del procuringentity_role_array[0]['details']

        # Set id.
        procuringentity_role_array[0]['id'] = \
            f"{self.payload['tender']['procuringEntity']['identifier']['scheme']}-" \
            f"{self.payload['tender']['procuringEntity']['identifier']['id']}"

        # Set name.
        procuringentity_role_array[0]['name'] = self.payload['tender']['procuringEntity']['name']

        # Set identifier.
        procuringentity_role_array[0]['identifier']['scheme'] = \
            self.payload['tender']['procuringEntity']['identifier']['scheme']

        procuringentity_role_array[0]['identifier']['id'] = \
            self.payload['tender']['procuringEntity']['identifier']['id']

        procuringentity_role_array[0]['identifier']['legalName'] = \
            self.payload['tender']['procuringEntity']['identifier']['legalName']

        if "uri" in self.payload['tender']['procuringEntity']['identifier']:
            procuringentity_role_array[0]['identifier']['uri'] = \
                self.payload['tender']['procuringEntity']['identifier']['uri']
        else:
            del procuringentity_role_array[0]['identifier']['uri']

        # Set address.streetAddress.
        procuringentity_role_array[0]['address']['streetAddress'] = \
            self.payload['tender']['procuringEntity']['address']['streetAddress']

        # Set address.postalCode.
        if "postalCode" in self.payload['tender']['procuringEntity']['address']:
            procuringentity_role_array[0]['address']['postalCode'] = \
                self.payload['tender']['procuringEntity']['address']['postalCode']
        else:
            del procuringentity_role_array[0]['address']['postalCode']

        # Set address.addressDetails,
        procuringentity_country_data = get_value_from_country_csv(
            country=self.payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
            language=self.language
        )
        expected_procuringentity_country_object = [{
            "scheme": procuringentity_country_data[2].upper(),
            "id": self.payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
            "description": procuringentity_country_data[1],
            "uri": procuringentity_country_data[3]
        }]

        procuringentity_region_data = get_value_from_region_csv(
            region=self.payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
            country=self.payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
            language=self.language
        )
        expected_procuringentity_region_object = [{
            "scheme": procuringentity_region_data[2],
            "id": self.payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
            "description": procuringentity_region_data[1],
            "uri": procuringentity_region_data[3]
        }]

        if self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['scheme'] != "other":

            procuringentity_locality_data = get_value_from_locality_csv(
                locality=self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],
                region=self.payload['tender']['procuringEntity']['address']['addressDetails']['region']['id'],
                country=self.payload['tender']['procuringEntity']['address']['addressDetails']['country']['id'],
                language=self.language
            )
            expected_procuringentity_locality_object = [{
                "scheme": procuringentity_locality_data[2],
                "id": self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],
                "description": procuringentity_locality_data[1],
                "uri": procuringentity_locality_data[3]
            }]
        else:
            expected_procuringentity_locality_object = [{
                "scheme": self.payload['tender']['procuringEntity']['address']['addressDetails']['locality'][
                    'scheme'],
                "id": self.payload['tender']['procuringEntity']['address']['addressDetails']['locality']['id'],

                "description": self.payload['tender']['procuringEntity']['address']['addressDetails'][
                    'locality']['description']
            }]

        procuringentity_role_array[0]['address']['addressDetails']['country'] = \
            expected_procuringentity_country_object[0]

        procuringentity_role_array[0]['address']['addressDetails']['region'] = \
            expected_procuringentity_region_object[0]

        procuringentity_role_array[0]['address']['addressDetails']['locality'] = \
            expected_procuringentity_locality_object[0]

        # Set additionalIdentifiers.
        if "additionalIdentifiers" in self.payload['tender']['procuringEntity']:
            del procuringentity_role_array[0]['additionalIdentifiers'][0]
            additional_identifiers = list()
            for q_1 in range(len(self.payload['tender']['procuringEntity']['additionalIdentifiers'])):
                additional_identifiers.append(copy.deepcopy(
                    self.expected_ms_release['releases'][0]['parties'][0]['additionalIdentifiers'][0]
                ))

                additional_identifiers[q_1]['scheme'] = \
                    self.payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['scheme']

                additional_identifiers[q_1]['id'] = \
                    self.payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['id']

                additional_identifiers[q_1]['legalName'] = \
                    self.payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['legalName']

                if "uri" in self.payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]:
                    additional_identifiers[q_1]['uri'] = \
                        self.payload['tender']['procuringEntity']['additionalIdentifiers'][q_1]['uri']
                else:
                    del additional_identifiers[q_1]['uri']

                procuringentity_role_array[0]['additionalIdentifiers'] = additional_identifiers
        else:
            del procuringentity_role_array[0]['additionalIdentifiers']

        # Set contactPoint.
        if "faxNumber" in self.payload['tender']['procuringEntity']['contactPoint']:

            procuringentity_role_array[0]['contactPoint']['faxNumber'] = \
                self.payload['tender']['procuringEntity']['contactPoint']['faxNumber']
        else:
            del procuringentity_role_array[0]['contactPoint']['faxNumber']

        if "url" in self.payload['tender']['procuringEntity']['contactPoint']:

            procuringentity_role_array[0]['contactPoint']['url'] = \
                self.payload['tender']['procuringEntity']['contactPoint']['url']
        else:
            del procuringentity_role_array[0]['contactPoint']['url']

        procuringentity_role_array[0]['contactPoint']['name'] = \
            self.payload['tender']['procuringEntity']['contactPoint']['name']

        procuringentity_role_array[0]['contactPoint']['email'] = \
            self.payload['tender']['procuringEntity']['contactPoint']['email']

        procuringentity_role_array[0]['contactPoint']['telephone'] = \
            self.payload['tender']['procuringEntity']['contactPoint']['telephone']

        # FR.COM-1.62.72: Set persones.
        if "persones" in self.payload['tender']['procuringEntity']:
            expected_persones = list()
            for q_1 in range(len(self.payload['tender']['procuringEntity']['persones'])):
                expected_persones.append(copy.deepcopy(
                    self.expected_ms_release['releases'][0]['parties'][0]['persones'][0]
                ))

                # Set id.
                expected_persones[q_1]['id'] = \
                    f"{self.payload['tender']['procuringEntity']['persones'][q_1]['identifier']['scheme']}-" \
                    f"{self.payload['tender']['procuringEntity']['persones'][q_1]['identifier']['id']}"

                # Set title.
                expected_persones[q_1]['title'] = self.payload['tender']['procuringEntity']['persones'][q_1]['title']

                # Set name.
                expected_persones[q_1]['name'] = self.payload['tender']['procuringEntity']['persones'][q_1]['name']

                # Set identifier.
                expected_persones[q_1]['identifier']['scheme'] = \
                    self.payload['tender']['procuringEntity']['persones'][q_1]['identifier']['scheme']

                expected_persones[q_1]['identifier']['id'] = \
                    self.payload['tender']['procuringEntity']['persones'][q_1]['identifier']['id']

                if "uri" in self.payload['tender']['procuringEntity']['persones'][q_1]['identifier']:
                    expected_persones[q_1]['identifier']['uri'] = \
                        self.payload['tender']['procuringEntity']['persones'][q_1]['identifier']['uri']
                else:
                    del expected_persones[q_1]['identifier']['uri']

                # Set businessFunctions.
                # Get actual businessFunctions array.
                actual_bf_array = list()
                for a_0 in range(len(actual_ms_release['releases'][0]['parties'])):

                    if "procuringEntity" in actual_ms_release['releases'][0]['parties'][a_0]['roles']:

                        for a_1 in range(len(actual_ms_release['releases'][0]['parties'][a_0]['persones'])):
                            if actual_ms_release['releases'][0]['parties'][a_0]['persones'][a_1]['id'] == \
                                    expected_persones[q_1]['id']:

                                for a_2 in range(len(
                                        actual_ms_release['releases'][0]['parties'][a_0]['persones'][a_1][
                                            'businessFunctions']
                                )):
                                    actual_bf_array.append(
                                        actual_ms_release['releases'][0]['parties'][a_0][
                                            'persones'][a_1]['businessFunctions'][a_2]
                                    )

                expected_bf_array = list()
                for q_2 in range(len(self.payload['tender']['procuringEntity']['persones'][q_1]['businessFunctions'])):

                    expected_bf_array.append(copy.deepcopy(
                        self.expected_ms_release['releases'][0]['parties'][0]['persones'][0]['businessFunctions'][0]
                    ))

                    # FR.COM-1.62.38: Set id.
                    try:
                        is_permanent_id_correct = is_it_uuid(actual_bf_array[q_2]['id'])
                        if is_permanent_id_correct is True:

                            expected_bf_array[q_2]['id'] = actual_bf_array[q_2]['id']
                        else:
                            expected_bf_array[q_2]['id'] = \
                                f"FR.COM-1.62.38: the 'releases[0].parties[*].persones[{q_1}]." \
                                f"businessFunctions[{q_2}].id' must be uuid."
                    except KeyError:
                        raise KeyError(f"Mismatch key into path 'releases[0].parties[*].persones[{q_1}]."
                                       f"businessFunctions[{q_2}].id'")

                    # Set type.
                    expected_bf_array[q_2]['type'] = \
                        self.payload['tender']['procuringEntity']['persones'][q_1]['businessFunctions'][q_2]['type']

                    # Set jobTitle.
                    expected_bf_array[q_2]['jobTitle'] = \
                        self.payload['tender']['procuringEntity']['persones'][q_1]['businessFunctions'][q_2][
                            'jobTitle']

                    # Set period.
                    expected_bf_array[q_2]['period']['startDate'] = \
                        self.payload['tender']['procuringEntity']['persones'][q_1]['businessFunctions'][q_2][
                            'period']['startDate']

                    # Set documents.
                    if "documents" in self.payload['tender']['procuringEntity']['persones'][q_1][
                            'businessFunctions'][q_2]:

                        expected_bf_documents_array = list()
                        for q_3 in range(len(
                                self.payload['tender']['procuringEntity']['persones'][q_1][
                                    'businessFunctions'][q_2]['documents']
                        )):
                            expected_bf_documents_array.append(copy.deepcopy(
                                self.expected_ms_release['releases'][0]['parties'][0]['persones'][0][
                                    'businessFunctions'][0]['documents'][0]
                            ))

                            # Set id.
                            expected_bf_documents_array[q_3]['id'] = \
                                self.payload['tender']['procuringEntity']['persones'][q_1][
                                    'businessFunctions'][q_2]['documents'][q_3]['id']

                            # Set title.
                            expected_bf_documents_array[q_3]['title'] = \
                                self.payload['tender']['procuringEntity']['persones'][q_1][
                                    'businessFunctions'][q_2]['documents'][q_3]['title']

                            # Set documentType.
                            expected_bf_documents_array[q_3]['documentType'] = \
                                self.payload['tender']['procuringEntity']['persones'][q_1][
                                    'businessFunctions'][q_2]['documents'][q_3]['documentType']

                            # Set description.
                            if "description" in self.payload['tender']['procuringEntity']['persones'][q_1][
                                    'businessFunctions'][q_2]['documents'][q_3]:

                                expected_bf_documents_array[q_3]['description'] = \
                                    self.payload['tender']['procuringEntity']['persones'][q_1][
                                        'businessFunctions'][q_2]['documents'][q_3]['description']
                            else:
                                del expected_bf_documents_array[q_3]['description']

                            # Set url.
                            expected_bf_documents_array[q_3]['url'] = \
                                f"{self.metadata_document_url}/{expected_bf_documents_array[q_3]['id']}"

                            # Set datePublished.
                            expected_bf_documents_array[q_3]['datePublished'] = \
                                self.message_for_platform['data']['operationDate']

                        expected_bf_array[q_2]['documents'] = expected_bf_documents_array
                    else:
                        del expected_bf_array[q_2]['documents']

                expected_persones[q_1]['businessFunctions'] = expected_bf_array
            procuringentity_role_array[0]['persones'] = expected_persones
        else:
            del procuringentity_role_array[0]['persones']

        # Set role.
        procuringentity_role_array[0]['roles'] = ["procuringEntity"]

        # Prepare unique party with procuringEntity role.
        unique_pe_role_array = get_unique_party_from_list_by_id(procuringentity_role_array)

        # Get id from unique party with procuringEntity role.
        unique_pe_id_array = list()
        for pe in range(len(unique_pe_role_array)):
            unique_pe_id_array.append(unique_pe_role_array[pe]['id'])

        # ------------------------------------------
        # Prepare party with 'buyer' role.
        buyer_role_array = list()
        for q_0 in range(len(self.payload['planning']['budget']['budgetBreakdown'])):

            ei_url = \
                f"{self.metadata_budget_url}/" \
                f"{self.payload['planning']['budget']['budgetBreakdown'][q_0]['classifications']['ei']}/" \
                f"{self.payload['planning']['budget']['budgetBreakdown'][q_0]['classifications']['ei']}"

            actual_ei_release = requests.get(ei_url).json()
            for a_0 in range(len(
                    actual_ei_release['releases'][0]['parties']
            )):
                if actual_ei_release['releases'][0]['parties'][a_0]['roles'] == ["buyer"]:
                    buyer_role_array.append(copy.deepcopy(
                        actual_ei_release['releases'][0]['parties'][a_0]
                    ))

        # Prepare unique party with buyer role.
        unique_buyer_role_array = get_unique_party_from_list_by_id(buyer_role_array)

        # Get id from unique party with buyer role.
        unique_buyer_id_array = list()
        for buyer in range(len(unique_buyer_role_array)):
            unique_buyer_id_array.append(unique_buyer_role_array[buyer]['id'])

        # Prepare party with 'payer' role and party with 'funder' role.
        funder_role_array = list()
        payer_role_array = list()

        parties_array = list()
        if need_fs is True:
            for q_0 in range(len(self.payload['planning']['budget']['budgetBreakdown'])):

                fs_url = \
                    f"{self.metadata_budget_url}/" \
                    f"{self.payload['planning']['budget']['budgetBreakdown'][q_0]['classifications']['ei']}/" \
                    f"{self.payload['planning']['budget']['budgetBreakdown'][q_0]['classifications']['fs']}"

                actual_fs_release = requests.get(fs_url).json()
                for a_0 in range(len(
                        actual_fs_release['releases'][0]['parties']
                )):

                    # Prepare party with 'funder' role.
                    if actual_fs_release['releases'][0]['parties'][a_0]['roles'] == ["funder"]:
                        funder_role_array.append(copy.deepcopy(
                            actual_fs_release['releases'][0]['parties'][a_0]
                        ))

                    # Prepare party with 'payer' role.
                    if "payer" in actual_fs_release['releases'][0]['parties'][a_0]['roles']:
                        payer_role_array.append(copy.deepcopy(
                            actual_fs_release['releases'][0]['parties'][a_0]
                        ))

            # Prepare unique party with payer role.
            unique_payer_role_array = get_unique_party_from_list_by_id(payer_role_array)

            # Prepare unique party with funder role.
            unique_funder_role_array = get_unique_party_from_list_by_id(funder_role_array)

            # Get id from unique party with payer role.
            unique_payer_id_array = list()
            for payer in range(len(unique_payer_role_array)):
                unique_payer_id_array.append(unique_payer_role_array[payer]['id'])

            # Get id from unique party with funder role.
            unique_funder_id_array = list()
            for funder in range(len(unique_funder_role_array)):
                unique_funder_id_array.append(unique_funder_role_array[funder]['id'])

            # Check the same id into party with payer role and party with funder role.
            same_id_into_payer_and_funder = list(set(unique_payer_id_array) & set(unique_funder_id_array))

            # Prepare temporary array with payer and funder roles or prepare temporary array with payer role.
            # Prepare temporary array with funder role.
            temp_parties_with_payer_role_array = list()
            temp_parties_with_funder_role_array = list()
            if len(same_id_into_payer_and_funder) > 0:
                for payer in range(len(unique_payer_role_array)):
                    for i_1 in range(len(same_id_into_payer_and_funder)):
                        for funder in range(len(unique_funder_role_array)):
                            if unique_payer_role_array[payer]['id'] == same_id_into_payer_and_funder[i_1] == \
                                    unique_funder_role_array[funder]['id']:
                                unique_payer_role_array[payer]['roles'] = \
                                    unique_payer_role_array[payer]['roles'] + unique_funder_role_array[funder][
                                        'roles']

                                temp_parties_with_payer_role_array.append(unique_payer_role_array[payer])

                        for funder in range(len(unique_funder_role_array)):
                            if unique_payer_role_array[payer]['id'] != same_id_into_payer_and_funder[i_1]:
                                temp_parties_with_payer_role_array.append(unique_payer_role_array[payer])

                            if unique_funder_role_array[funder]['id'] != same_id_into_payer_and_funder[i_1]:
                                temp_parties_with_funder_role_array.append(unique_payer_role_array[funder])
            else:
                temp_parties_with_payer_role_array = unique_payer_role_array
                temp_parties_with_funder_role_array = unique_funder_role_array

            # Get id from temporary parties array with payer role.
            unique_parties_id_array = list()
            for payer in range(len(temp_parties_with_payer_role_array)):
                unique_parties_id_array.append(temp_parties_with_payer_role_array[payer]['id'])

            # Check the same id into party with buyer role and party with payer role.
            same_id_into_buyer_and_payer = list(set(unique_buyer_id_array) & set(unique_parties_id_array))

            # Prepare temporary array with buyer and payer roles or prepare temporary array with buyer role.
            # Prepare permanent array with payer role.
            temp_parties_with_buyer_role_array = list()
            permanent_parties_with_payer_role_array = list()
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

                                permanent_parties_with_payer_role_array.append(
                                    temp_parties_with_payer_role_array[payer]
                                )
            else:
                temp_parties_with_buyer_role_array = unique_buyer_role_array
                permanent_parties_with_payer_role_array = temp_parties_with_payer_role_array

            # Get id from temporary parties array with funder role.
            unique_parties_id_array = list()
            for funder in range(len(temp_parties_with_funder_role_array)):
                unique_parties_id_array.append(temp_parties_with_funder_role_array[funder]['id'])

            # Get id from temporary parties array with buyer role.
            unique_buyer_id_array = list()
            for buyer in range(len(temp_parties_with_buyer_role_array)):
                unique_buyer_id_array.append(temp_parties_with_buyer_role_array[buyer]['id'])

            # Check the same id into party with buyer role and party with funder role.
            same_id_into_buyer_and_funder = list(set(unique_buyer_id_array) & set(unique_parties_id_array))

            # Prepare temporary array with buyer and funder roles or prepare permanent array with buyer role.
            # Prepare permanent array with funder role.
            permanent_parties_with_buyer_role_array = list()
            permanent_parties_with_funder_role_array = list()
            if len(same_id_into_buyer_and_funder) > 0:
                for buyer in range(len(temp_parties_with_buyer_role_array)):
                    for i_1 in range(len(same_id_into_buyer_and_funder)):
                        for funder in range(len(temp_parties_with_funder_role_array)):

                            if temp_parties_with_buyer_role_array[buyer]['id'] == \
                                    same_id_into_buyer_and_funder[i_1] == \
                                    temp_parties_with_funder_role_array[funder]['id']:

                                temp_parties_with_buyer_role_array[buyer]['roles'] = \
                                    temp_parties_with_buyer_role_array[buyer]['roles'] + \
                                    temp_parties_with_funder_role_array[funder]['roles']

                                permanent_parties_with_buyer_role_array.append(
                                    temp_parties_with_buyer_role_array[buyer]
                                )

                        for funder in range(len(temp_parties_with_funder_role_array)):
                            if temp_parties_with_funder_role_array[funder]['id'] != same_id_into_buyer_and_funder[i_1]:
                                permanent_parties_with_funder_role_array.append(
                                    temp_parties_with_funder_role_array[funder]
                                )
            else:
                permanent_parties_with_buyer_role_array = temp_parties_with_buyer_role_array
                permanent_parties_with_funder_role_array = temp_parties_with_funder_role_array

            # Get id from permanent parties array with funder role.
            unique_funder_id_array = list()
            for funder in range(len(permanent_parties_with_funder_role_array)):
                unique_funder_id_array.append(permanent_parties_with_funder_role_array[funder]['id'])

            # Check the same id into party with funder role and party with procuringEntity role.
            same_id_into_funder_and_pe = list(set(unique_funder_id_array) & set(unique_pe_id_array))

            # Get id from permanent parties array with payer role.
            unique_payer_id_array = list()
            for payer in range(len(permanent_parties_with_payer_role_array)):
                unique_payer_id_array.append(permanent_parties_with_payer_role_array[payer]['id'])

            # Check the same id into party with payer role and party with procuringEntity role.
            same_id_into_payer_and_pe = list(set(unique_payer_id_array) & set(unique_pe_id_array))

            # Get id from permanent parties array with buyer role.
            unique_buyer_id_array = list()
            for buyer in range(len(permanent_parties_with_buyer_role_array)):
                unique_buyer_id_array.append(permanent_parties_with_buyer_role_array[buyer]['id'])

            # Check the same id into party with buyer role and party with procuringEntity role.
            same_id_into_buyer_and_pe = list(set(unique_buyer_id_array) & set(unique_pe_id_array))

            # Add procuringEntity role to permanent parties with funder role array or
            # add procuringEntity role to permanent parties with payer role array or
            # add procuringEntity role to permanent parties with buyer role array or
            # prepare permanent parties with procuringEntity role array.
            permanent_parties_with_pe_role_array = list()
            if len(same_id_into_funder_and_pe) > 0:
                for funder in range(len(permanent_parties_with_funder_role_array)):
                    for i_1 in range(len(same_id_into_funder_and_pe)):
                        for pe in range(len(unique_pe_role_array)):
                            if permanent_parties_with_funder_role_array[funder]['id'] == \
                                    same_id_into_funder_and_pe[i_1] == unique_pe_role_array[pe]['id']:

                                if "persones" in unique_pe_role_array[pe]:
                                    # The party with funder role never has businessFunctions array.
                                    permanent_parties_with_funder_role_array[funder]['persones'] = \
                                        unique_pe_role_array[pe]['persones']

                                permanent_parties_with_funder_role_array[funder]['roles'] = \
                                    permanent_parties_with_funder_role_array[funder]['roles'] + \
                                    unique_pe_role_array[pe]['roles']

            elif len(same_id_into_payer_and_pe) > 0:
                for payer in range(len(permanent_parties_with_payer_role_array)):
                    for i_1 in range(len(same_id_into_payer_and_pe)):
                        for pe in range(len(unique_pe_role_array)):
                            if permanent_parties_with_payer_role_array[payer]['id'] == same_id_into_payer_and_pe[i_1] \
                                    == unique_pe_role_array[pe]['id']:

                                if "persones" in unique_pe_role_array[pe]:
                                    # The party with payer role never has businessFunctions array.
                                    permanent_parties_with_payer_role_array[payer]['persones'] = \
                                        unique_pe_role_array[pe]['persones']

                                permanent_parties_with_payer_role_array[payer]['roles'] = \
                                    permanent_parties_with_payer_role_array[payer]['roles'] + \
                                    unique_pe_role_array[pe]['roles']

            elif len(same_id_into_buyer_and_pe) > 0:
                for buyer in range(len(permanent_parties_with_buyer_role_array)):
                    for i_1 in range(len(same_id_into_buyer_and_pe)):
                        for pe in range(len(unique_pe_role_array)):
                            if permanent_parties_with_buyer_role_array[buyer]['id'] == same_id_into_buyer_and_pe[i_1] \
                                    == unique_pe_role_array[pe]['id']:

                                if "persones" in unique_pe_role_array[pe]:
                                    # The party with buyer role never has businessFunctions array.
                                    permanent_parties_with_buyer_role_array[buyer]['persones'] = \
                                        unique_pe_role_array[pe]['persones']

                                permanent_parties_with_buyer_role_array[buyer]['roles'] = \
                                    permanent_parties_with_buyer_role_array[buyer]['roles'] + \
                                    unique_pe_role_array[pe]['roles']
            else:
                permanent_parties_with_pe_role_array = unique_pe_role_array

            parties_array = \
                permanent_parties_with_buyer_role_array + permanent_parties_with_payer_role_array + \
                permanent_parties_with_funder_role_array + permanent_parties_with_pe_role_array

        elif need_fs is False:
            # Check the same id into party with buyer role and party with procuringEntity role.
            same_id_into_buyer_and_pe = list(set(unique_buyer_id_array) & set(unique_pe_id_array))

            # Add procuringEntity role to permanent parties with buyer role array or
            # prepare permanent parties with procuringEntity role array.
            permanent_parties_with_buyer_role_array = list()
            permanent_parties_with_pe_role_array = list()

            if len(same_id_into_buyer_and_pe) > 0:
                for buyer in range(len(unique_buyer_role_array)):
                    for i_1 in range(len(same_id_into_buyer_and_pe)):
                        for pe in range(len(unique_pe_role_array)):

                            if unique_buyer_role_array[buyer]['id'] == same_id_into_buyer_and_pe[i_1] \
                                    == unique_pe_role_array[pe]['id']:

                                if "persones" in unique_pe_role_array[pe]:
                                    # The party with buyer role never has businessFunctions array.
                                    unique_buyer_role_array[buyer]['persones'] = unique_pe_role_array[pe]['persones']

                                unique_buyer_role_array[buyer]['roles'] = \
                                    unique_buyer_role_array[buyer]['roles'] + unique_pe_role_array[pe]['roles']

                                permanent_parties_with_buyer_role_array.append(unique_buyer_role_array[buyer])

                        for pe in range(len(unique_pe_role_array)):
                            if unique_buyer_role_array[buyer]['id'] != same_id_into_buyer_and_pe[i_1]:
                                permanent_parties_with_buyer_role_array.append(unique_buyer_role_array[buyer])

                            if unique_pe_role_array[pe]['id'] != same_id_into_buyer_and_pe[i_1]:
                                permanent_parties_with_pe_role_array.append(unique_pe_role_array[pe])
            else:
                permanent_parties_with_buyer_role_array = unique_pe_role_array
                permanent_parties_with_pe_role_array = unique_buyer_role_array

            parties_array = permanent_parties_with_buyer_role_array + permanent_parties_with_pe_role_array

        # Sort parties array.
        expected_parties_array = list()
        if len(actual_ms_release['releases'][0]['parties']) == len(parties_array):
            for act in range(len(actual_ms_release['releases'][0]['parties'])):
                for exp in range(len(parties_array)):
                    if parties_array[exp]['id'] == actual_ms_release['releases'][0]['parties'][act]['id']:
                        expected_parties_array.append(parties_array[exp])
        else:
            raise ValueError("Quantity of objects into actual ms release doesn't equal "
                             "quantity of objects into prepared parties array")

        self.expected_ms_release['releases'][0]['parties'] = expected_parties_array

        """"Enrich 'tender' object for expected MS release: releases[0].tender"""
        # FR.COM-1.62.4: Set id.
        try:
            is_permanent_id_correct = is_it_uuid(
                actual_ms_release['releases'][0]['tender']['id']
            )
            if is_permanent_id_correct is True:

                self.expected_ms_release['releases'][0]['tender']['id'] = \
                    actual_ms_release['releases'][0]['tender']['id']
            else:
                self.expected_ms_release['releases'][0]['tender']['id'] = \
                    f"FR.COM-1.62.4: the 'releases[0].tender.id' must be uuid."
        except KeyError:
            raise KeyError(f"Mismatch key into path 'releases[0].tender.id'")

        # FR.COM-1.62.7: Set title.
        self.expected_ms_release['releases'][0]['tender']['title'] = \
            self.payload['tender']['title']

        # FR.COM-1.62.8: Set description.
        self.expected_ms_release['releases'][0]['tender']['description'] = \
            self.payload['tender']['description']

        # FR.COM-1.62.5: Set status.
        self.expected_ms_release['releases'][0]['tender']['status'] = "planning"

        # FR.COM-1.62.25: Set value.
        budget_breakdown_amount_list = list()
        for q_0 in range(len(self.payload['planning']['budget']['budgetBreakdown'])):
            budget_breakdown_amount_list.append(
                self.payload['planning']['budget']['budgetBreakdown'][q_0]['amount']['amount']
            )

        self.expected_ms_release['releases'][0]['tender']['value']['amount'] = \
            round(sum(budget_breakdown_amount_list), 2)

        self.expected_ms_release['releases'][0]['tender']['value']['currency'] = \
            self.payload['tender']['lots'][0]['value']['currency']

        # FR.COM-1.62.24: Set procurementMethod.
        self.expected_ms_release['releases'][0]['tender']['procurementMethod'] = "open"

        # FR.COM-1.62.20: Set procurementMethodDetails.
        expected_procurement_method_details = None
        try:
            """
            Enrich procurementMethodDetails, depends on pmd.
            """
            if pmd == "TEST_OT":
                expected_procurement_method_details = "test_openTender"
            elif pmd == "OT":
                expected_procurement_method_details = "openTender"
            elif pmd == "TEST_SV":
                expected_procurement_method_details = "test_smallTender"
            elif pmd == "SV":
                expected_procurement_method_details = "smallTender"
            elif pmd == "TEST_MV":
                expected_procurement_method_details = "test_microValue"
            elif pmd == "MV":
                expected_procurement_method_details = "microValue"
            else:
                ValueError("Check your pmd: You must use "
                           "'TEST_OT', 'OT', 'TEST_SV', 'SV', 'TEST_MV', 'MV' in pytest command")

            self.expected_ms_release['releases'][0]['tender']['procurementMethodDetails'] = \
                expected_procurement_method_details
        except KeyError:
            raise KeyError("Could not parse a pmd into pytest command.")

        # FR.COM-1.62.13: Set procurementMethodRationale.
        if "procurementMethodRationale" in self.payload['tender']:
            self.expected_ms_release['releases'][0]['tender']['procurementMethodRationale'] = \
                self.payload['tender']['procurementMethodRationale']
        else:
            del self.expected_ms_release['releases'][0]['tender']['procurementMethodRationale']

        # FR.COM-1.62.17: Set mainProcurementCategory.
        expected_main_procurement_category = None
        try:
            """
           Enrich mainProcurementCategory, depends on tender.classification.id.
           """
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

            self.expected_ms_release['releases'][0]['tender']['mainProcurementCategory'] = \
                expected_main_procurement_category

        except KeyError:
            raise KeyError("Could not parse tender.classification.id.")

        # FR.COM-1.62.23: Set eligibilityCriteria.
        eligibility_criteria = get_value_from_code_translation_csv(
            parameter="eligibilityCriteria",
            country=self.country,
            language=self.language
        )
        self.expected_ms_release['releases'][0]['tender']['eligibilityCriteria'] = eligibility_criteria

        # FR.COM-1.62.26: Set contractPeriod.
        expected_contract_period = get_contract_period_for_ms_release(lots_array=self.payload['tender']['lots'])
        self.expected_ms_release['releases'][0]['tender']['contractPeriod']['startDate'] = expected_contract_period[0]
        self.expected_ms_release['releases'][0]['tender']['contractPeriod']['endDate'] = expected_contract_period[1]

        # FR.COM-1.62.27:  Set procuringEntity.
        self.expected_ms_release['releases'][0]['tender']['procuringEntity']['id'] = \
            f"{self.payload['tender']['procuringEntity']['identifier']['scheme']}-" \
            f"{self.payload['tender']['procuringEntity']['identifier']['id']}"

        self.expected_ms_release['releases'][0]['tender']['procuringEntity']['name'] = \
            self.payload['tender']['procuringEntity']['name']

        # FR.COM-1.62.36: Set acceleratedProcedure.
        self.expected_ms_release['releases'][0]['tender']['acceleratedProcedure']['isAcceleratedProcedure'] = False

        # FR.COM-1.62.11: Set classification.
        try:
            """
            Enrich releases.tender.classification object, depends on items into pn_payload.
            """
            if "items" in self.payload['tender']:

                expected_cpv_data = get_value_from_cpv_dictionary_xls(
                    cpv=generate_tender_classification_id(self.payload['tender']['items']),
                    language=self.language
                )
            else:
                expected_cpv_data = get_value_from_cpv_dictionary_xls(
                    cpv=self.tender_classification_id,
                    language=self.language
                )

            self.expected_ms_release['releases'][0]['tender']['classification']['id'] = expected_cpv_data[0]
            self.expected_ms_release['releases'][0]['tender']['classification']['description'] = expected_cpv_data[1]
            self.expected_ms_release['releases'][0]['tender']['classification']['scheme'] = "CPV"
        except ValueError:
            ValueError("Impossible to enrich releases.tender.classification object.")

        # FR.COM-1.62.28: Set designContest.
        self.expected_ms_release['releases'][0]['tender']['designContest']['serviceContractAward'] = False

        # FR.COM-1.62.29: Set electronicWorkflows.useOrdering.
        self.expected_ms_release['releases'][0]['tender']['electronicWorkflows']['useOrdering'] = False

        # FR.COM-1.62.29: Set electronicWorkflows.usePayment.
        self.expected_ms_release['releases'][0]['tender']['electronicWorkflows']['usePayment'] = False

        # FR.COM-1.62.31: Set electronicWorkflows.acceptInvoicing.
        self.expected_ms_release['releases'][0]['tender']['electronicWorkflows']['acceptInvoicing'] = False

        # FR.COM-1.62.32: Set jointProcurement.isJointProcurement.
        self.expected_ms_release['releases'][0]['tender']['jointProcurement']['isJointProcurement'] = False

        # FR.COM-1.62.33: Set procedureOutsourcing.procedureOutsourced.
        self.expected_ms_release['releases'][0]['tender']['procedureOutsourcing']['procedureOutsourced'] = False

        # FR.COM-1.62.34: Set framework.isAFramework.
        self.expected_ms_release['releases'][0]['tender']['framework']['isAFramework'] = False

        # FR.COM-1.62.35: Set dynamicPurchasingSystem.hasDynamicPurchasingSystem.
        self.expected_ms_release['releases'][0]['tender']['dynamicPurchasingSystem']['hasDynamicPurchasingSystem'] = \
            False

        # FR.COM-1.62.12: Set legalBasis.
        self.expected_ms_release['releases'][0]['tender']['legalBasis'] = self.payload['tender']['legalBasis']

        """"Enrich 'relatedProcesses' object for expected MS release: releases[0].relatedProcesses"""
        # FR.COM-1.62.76: Set id.
        try:
            is_permanent_id_correct = is_it_uuid(
                actual_ms_release['releases'][0]['relatedProcesses'][0]['id']
            )
            if is_permanent_id_correct is True:

                self.expected_ms_release['releases'][0]['relatedProcesses'][0]['id'] = \
                    actual_ms_release['releases'][0]['relatedProcesses'][0]['id']
            else:
                self.expected_ms_release['releases'][0]['relatedProcesses'][0]['id'] = \
                    f"FR.COM-1.62.76: the 'releases[0].relatedProcesses[{0}].id' must be uuid."
        except KeyError:
            raise KeyError(f"Mismatch key into path 'releases[0].relatedProcesses[{0}].id'")

        # FR.COM-1.62.77: Set relationship.
        self.expected_ms_release['releases'][0]['relatedProcesses'][0]['relationship'] = ['prior']

        # FR.COM-1.62.78: Set ocid.
        self.expected_ms_release['releases'][0]['relatedProcesses'][0]['scheme'] = "ocid"

        # FR.COM-1.62.79: Set identifier.
        self.expected_ms_release['releases'][0]['relatedProcesses'][0]['identifier'] = \
            self.message_for_platform['data']['outcomes']['pin'][0]['id']

        # FR.COM-1.62.80: Set uri.
        self.expected_ms_release['releases'][0]['relatedProcesses'][0]['uri'] = \
            f"{self.metadata_tender_url}/{self.message_for_platform['data']['ocid'][:28]}/" \
            f"{self.message_for_platform['data']['outcomes']['pin'][0]['id']}"
        return self.expected_ms_release

    def build_expected_fs_release(self, actual_fs_release):
        """Build MS release."""

        expected_fs_release = copy.deepcopy(actual_fs_release)

        """"Enrich 'relatedProcesses' object for expected MS release: releases[0].relatedProcesses"""
        expected_related_processes_object = copy.deepcopy(
            self.expected_pi_release['releases'][0]['relatedProcesses'][0]
        )

        # Get actual object of relatedProcesses.
        actual_related_processes_object = dict()
        for q_0 in range(len(actual_fs_release['releases'][0]['relatedProcesses'])):
            if actual_fs_release['releases'][0]['relatedProcesses'][q_0]['relationship'] == ['prior']:
                actual_related_processes_object.update(actual_fs_release['releases'][0]['relatedProcesses'][q_0])

        # Set id.
        try:
            is_permanent_id_correct = is_it_uuid(actual_related_processes_object['id'])
            if is_permanent_id_correct is True:
                expected_related_processes_object['id'] = actual_related_processes_object['id']
            else:
                expected_related_processes_object['id'] = f"The 'releases[0].relatedProcesses[*].id' must be uuid."
        except KeyError:
            raise KeyError(f"Mismatch key into path 'releases[0].relatedProcesses[*].id'")

        # Set relationship.
        expected_related_processes_object['relationship'] = ['prior']

        # Set ocid.
        expected_related_processes_object['scheme'] = "ocid"

        # Set identifier.
        expected_related_processes_object['identifier'] = self.message_for_platform['data']['outcomes']['pin'][0]['id']

        # Set uri.
        self.expected_ms_release['releases'][0]['relatedProcesses'][0]['uri'] = \
            f"{self.metadata_tender_url}/{self.message_for_platform['data']['ocid'][:28]}/" \
            f"{self.message_for_platform['data']['outcomes']['pin'][0]['id']}"

        expected_fs_release['releases'][0]['relatedProcesses'].append(expected_related_processes_object)
        return expected_fs_release

    def build_expected_ei_release(self, actual_ei_release):
        """Build MS release."""

        expected_ei_release = copy.deepcopy(actual_ei_release)

        """"Enrich 'relatedProcesses' object for expected MS release: releases[0].relatedProcesses"""
        expected_related_processes_object = copy.deepcopy(
            self.expected_pi_release['releases'][0]['relatedProcesses'][0]
        )

        # Get actual object of relatedProcesses.
        actual_related_processes_object = dict()
        for q_0 in range(len(actual_ei_release['releases'][0]['relatedProcesses'])):
            if actual_ei_release['releases'][0]['relatedProcesses'][q_0]['relationship'] == ['prior']:
                actual_related_processes_object.update(actual_ei_release['releases'][0]['relatedProcesses'][q_0])

        # Set id.
        try:
            is_permanent_id_correct = is_it_uuid(actual_related_processes_object['id'])
            if is_permanent_id_correct is True:

                expected_related_processes_object['id'] = actual_related_processes_object['id']
            else:
                expected_related_processes_object['id'] = f"The 'releases[0].relatedProcesses[*].id' must be uuid."
        except KeyError:
            raise KeyError(f"Mismatch key into path 'releases[0].relatedProcesses[*].id'")

        # Set relationship.
        expected_related_processes_object['relationship'] = ['prior']

        # Set ocid.
        expected_related_processes_object['scheme'] = "ocid"

        # Set identifier.
        expected_related_processes_object['identifier'] = self.message_for_platform['data']['outcomes']['pin'][0]['id']

        # Set uri.
        self.expected_ms_release['releases'][0]['relatedProcesses'][0]['uri'] = \
            f"{self.metadata_tender_url}/{self.message_for_platform['data']['ocid'][:28]}/" \
            f"{self.message_for_platform['data']['outcomes']['pin'][0]['id']}"

        expected_ei_release['releases'][0]['relatedProcesses'].append(expected_related_processes_object)
        return expected_ei_release
