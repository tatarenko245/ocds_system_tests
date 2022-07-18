""""Prepare the expected release of the create pin process, open procedure."""
import copy

from data_collection.OpenProcedure.for_test_createPIN_process.release_full_model import pi_release_model, \
    ms_release_model
from data_collection.data_constant import affordable_shemes
from functions_collection.some_functions import is_it_uuid, get_value_from_cpv_dictionary_csv, \
    get_value_from_classification_unit_dictionary_csv, get_value_from_cpvs_dictionary_csv, get_value_from_country_csv, \
    get_value_from_region_csv, get_value_from_locality_csv, get_value_from_code_translation_csv


class CreatePriorInformationNoticeRelease:
    """This class creates instance of release."""

    def __init__(self, environment, country, language, tender_classification_id):

        self.environment = environment
        self.country = country
        self.language = language
        self.tender_classification_id = tender_classification_id
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

    def build_expected_pi_release(self, payload, message_for_platform, actual_pi_release):
        """Build PI release."""

        """Enrich general attribute for expected PI release"""
        self.expected_pi_release['uri'] = f"{self.metadata_tender_url}/{message_for_platform['data']['ocid'][:28]}/" \
                                          f"{message_for_platform['data']['outcomes']['pin'][0]['id']}"

        self.expected_pi_release['version'] = "1.1"
        self.expected_pi_release['extensions'] = self.extensions
        self.expected_pi_release['publisher']['name'] = self.publisher_name
        self.expected_pi_release['publisher']['uri'] = self.publisher_uri
        self.expected_pi_release['license'] = "http://opendefinition.org/licenses/"
        self.expected_pi_release['publicationPolicy'] = "http://opendefinition.org/licenses/"

        # FR.COM-3.4.6 Set created date for release.
        self.expected_pi_release['publishedDate'] = message_for_platform['data']['operationDate']

        """Enrich general attribute for expected PIN release: releases[0]"""
        # FR.COM-3.4.2: Set ocid.
        self.expected_pi_release['releases'][0]['ocid'] = message_for_platform['data']['outcomes']['pin'][0]['id']

        # FR.COM-3.4.4: Set id.
        self.expected_pi_release['releases'][0]['id'] = \
            f"{message_for_platform['data']['outcomes']['pin'][0]['id']}-" \
            f"{actual_pi_release['releases'][0]['id'][46:59]}"

        # FR.COM-1.62.6: Set date.
        self.expected_pi_release['releases'][0]['date'] = message_for_platform['data']['operationDate']

        # FR.COM-3.4.7: Set tag.
        self.expected_pi_release['releases'][0]['tag'] = ["planning"]

        # FR.COM-3.4.8: Set initiationType.
        self.expected_pi_release['releases'][0]['initiationType'] = "tender"

        # FR.COM-3.4.11: Set language.
        self.expected_pi_release['releases'][0]['language'] = self.language

        """Enrich attribute for expected PIN release: releases[0].tender"""
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
            KeyError(f"Mismatch key into path 'releases[0].tender.id'")

        # FR.COM-1.62.5: Set status.
        self.expected_pi_release['releases'][0]['tender']['status'] = "planning"

        # FR.COM-1.62.49: Set criteria.
        if "criteria" in payload['tender']:
            expected_criteria_array = list()
            for q_0 in range(len(payload['tender']['criteria'])):
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
                    KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}].id'")

                # Set title.
                expected_criteria_array[q_0]['title'] = payload['tender']['criteria'][q_0]['title']

                # Set source.
                expected_criteria_array[q_0]['source'] = "tenderer"

                # Set description.
                if "description" in payload['tender']['criteria'][q_0]:
                    expected_criteria_array[q_0]['description'] = payload['tender']['criteria'][q_0]['description']
                else:
                    del expected_criteria_array[q_0]['description']

                # Set relatesTo.
                expected_criteria_array[q_0]['relatesTo'] = payload['tender']['criteria'][q_0]['relatesTo']

                # FR.COM-1.62.59: Set relatedItem.
                if "relatedItem" in payload['tender']['criteria'][q_0]:
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
                        KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}].relatedItem'")
                else:
                    del expected_criteria_array[q_0]['relatedItem']

                # FR.COM-1.62.51: Set classification.
                if "classification" in payload['tender']['criteria'][q_0]:
                    expected_criteria_array[q_0]['classification']['scheme'] = \
                        payload['tender']['criteria'][q_0]['classification']['scheme']

                    expected_criteria_array[q_0]['classification']['id'] = \
                        payload['tender']['criteria'][q_0]['classification']['id']
                else:
                    del expected_criteria_array[q_0]['classification']

                # Set requirementGroups.
                expected_requirementgroups_array = list()
                for q_1 in range(len(payload['tender']['criteria'][q_0]['requirementGroups'])):
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
                        KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}]."
                                 f"requirementGroups[{q_1}].id'")

                    # Set description.
                    if "description" in payload['tender']['criteria'][q_0]['requirementGroups'][q_1]:
                        expected_requirementgroups_array[q_1]['description'] = \
                            payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['description']
                    else:
                        del expected_requirementgroups_array[q_1]['description']

                    # Set requirements.
                    expected_requirements_array = list()
                    for q_2 in range(len(payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'])):
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
                            KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}]."
                                     f"requirementGroups[{q_1}].requirements[{q_2}].id'")

                        # Set title.
                        expected_requirements_array[q_2]['title'] = \
                            payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2]['title']

                        # Set dataType.
                        expected_requirements_array[q_2]['dataType'] = \
                            payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2][
                                'dataType']

                        # Set description.
                        if "description" in payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                'requirements'][q_2]:
                            expected_requirements_array[q_2]['description'] = \
                                payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2][
                                    'description']
                        else:
                            del expected_requirements_array[q_2]['description']

                        # Set period.
                        if "period" in payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                'requirements'][q_2]:
                            expected_requirements_array[q_2]['period']['startDate'] = \
                                payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2][
                                    'period']['startDate']

                            expected_requirements_array[q_2]['period']['endDate'] = \
                                payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2][
                                    'period']['endDate']
                        else:
                            del expected_requirements_array[q_2]['period']

                        # Set expectedValue, minValue, maxValue and dataType.
                        if "expectedValue" not in payload['tender']['criteria'][q_0][
                                'requirementGroups'][q_1]['requirements'][q_2]:

                            del expected_requirements_array[q_2]['expectedValue']
                        else:
                            expected_requirements_array[q_2]['expectedValue'] = \
                                payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['expectedValue']

                            expected_requirements_array[q_2]['dataType'] = \
                                payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['dataType']

                        if "minValue" not in payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                'requirements'][q_2]:

                            del expected_requirements_array[q_2]['minValue']
                        else:
                            expected_requirements_array[q_2]['minValue'] = \
                                payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['minValue']

                            expected_requirements_array[q_2]['dataType'] = \
                                payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['dataType']

                        if "maxValue" not in payload['tender']['criteria'][q_0][
                                'requirementGroups'][q_1]['requirements'][q_2]:

                            del expected_requirements_array[q_2]['maxValue']
                        else:
                            expected_requirements_array[q_2]['maxValue'] = \
                                payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['maxValue']

                            expected_requirements_array[q_2]['dataType'] = \
                                payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                    'requirements'][q_2]['dataType']

                        # FR.COM-1.62.55: Set status.
                        expected_requirements_array[q_2]['status'] = "active"

                        # FR.COM-1.62.56: Set datePublished.
                        expected_requirements_array[q_2]['datePublished'] = \
                            message_for_platform['data']['operationDate']

                        # FR.COM-1.62.57: Set eligibleEvidences.
                        if "eligibleEvidences" in payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                'requirements'][q_2]:

                            expected_eligibleevidences_array = list()
                            for q_3 in range(len(
                                    payload['tender']['criteria'][q_0]['requirementGroups'][q_1]['requirements'][q_2][
                                        'eligibleEvidences']
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
                                    KeyError(f"Mismatch key into path 'releases[0].tender.criteria[{q_0}]."
                                             f"requirementGroups[{q_1}].requirements[{q_2}].eligibleEvidences[{q_3}]."
                                             f"id'")

                                # Set title.
                                expected_eligibleevidences_array[q_3]['title'] = \
                                    payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['eligibleEvidences'][q_3]['title']

                                # Set description.
                                if "description" in payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['eligibleEvidences'][q_3]:

                                    expected_eligibleevidences_array[q_3]['description'] = \
                                        payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                            'requirements'][q_2]['eligibleEvidences'][q_3]['description']
                                else:
                                    del expected_eligibleevidences_array[q_3]['description']

                                # Set type.
                                expected_eligibleevidences_array[q_3]['type'] = \
                                    payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['eligibleEvidences'][q_3]['type']

                                # Set relatedDocument.
                                if "relatedDocument" in payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
                                        'requirements'][q_2]['eligibleEvidences'][q_3]:

                                    expected_eligibleevidences_array[q_3]['relatedDocument']['id'] = \
                                        payload['tender']['criteria'][q_0]['requirementGroups'][q_1][
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
        if "conversions" in payload['tender']:
            expected_conversion_array = list()
            for q_0 in range(len(payload['tender']['conversions'])):
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
                    KeyError(f"Mismatch key into path 'releases[0].tender.conversions[{q_0}].id'")

                # What a requirement we need?
                actual_requirement = None
                for p_0 in range(len(payload['tender']['criteria'])):
                    for p_1 in range(len(payload['tender']['criteria'][p_0]['requirementGroups'])):
                        for p_2 in range(len(
                                payload['tender']['criteria'][p_0]['requirementGroups'][p_1]['requirements']
                        )):
                            if payload['tender']['criteria'][p_0]['requirementGroups'][p_1][
                                    'requirements'][p_2]['id'] == payload['tender']['conversions'][q_0]['relatedItem']:
                                # Get the requirement from actual release.
                                actual_requirement = actual_pi_release['releases'][0]['tender']['criteria'][p_0][
                                    'requirementGroups'][p_1]['requirements'][p_2]

                # Set relatedItem.
                expected_conversion_array[q_0]['relatedItem'] = actual_requirement['id']

                # Set relatesTo.
                expected_conversion_array[q_0]['relatesTo'] = "requirement"

                # Set description.
                if "description" in payload['tender']['conversions'][q_0]:
                    expected_conversion_array[q_0]['description'] = \
                        payload['tender']['conversions'][q_0]['description']
                else:
                    del self.expected_pi_release['releases'][0]['tender']['conversions']

                # Set rationale.
                expected_conversion_array[q_0]['rationale'] = payload['tender']['conversions'][q_0]['rationale']

                # Set coefficients.
                expected_coefficients_array = list()
                for q_1 in range(len(payload['tender']['conversions'][q_0]['coefficients'])):
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
                        KeyError(f"Mismatch key into path 'releases[0].tender.conversions[{q_0}]."
                                 f"coefficients[{q_1}].id'")

                    # Set value.
                    expected_coefficients_array[q_1]['value'] = \
                        payload['tender']['conversions'][q_0]['coefficients'][q_1]['value']

                    # Set coefficient.
                    expected_coefficients_array[q_1]['coefficient'] = \
                        payload['tender']['conversions'][q_0]['coefficients'][q_1]['coefficient']

                expected_conversion_array[q_0]['coefficients'] = expected_coefficients_array
            self.expected_pi_release['releases'][0]['tender']['conversions'] = expected_conversion_array
        else:
            del self.expected_pi_release['releases'][0]['tender']['conversions']

        # FR.COM-1.62.39: Set lots.
        expected_lots_array = list()
        for q_0 in range(len(payload['tender']['lots'])):
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
                KeyError(f"Mismatch key into path 'releases[0].tender.lots[{q_0}].id'")

            # Set internalId.
            if "internalId" in payload['tender']['lots'][q_0]:
                expected_lots_array[q_0]['internalId'] = payload['tender']['lots'][q_0]['internalId']
            else:
                del expected_lots_array[q_0]['internalId']

            # Set title.
            expected_lots_array[q_0]['title'] = payload['tender']['lots'][q_0]['title']

            # Set description
            expected_lots_array[q_0]['description'] = payload['tender']['lots'][q_0]['description']

            # FR.COM-1.62.41: Set status.
            expected_lots_array[q_0]['status'] = "planning"

            # Set value.
            expected_lots_array[q_0]['value']['amount'] = payload['tender']['lots'][q_0]['value']['amount']
            expected_lots_array[q_0]['value']['currency'] = payload['tender']['lots'][q_0]['value']['currency']

            # Set contactPeriod.
            expected_lots_array[q_0]['contractPeriod']['startDate'] = \
                payload['tender']['lots'][q_0]['contractPeriod']['startDate']

            expected_lots_array[q_0]['contractPeriod']['endDate'] = \
                payload['tender']['lots'][q_0]['contractPeriod']['endDate']

            # Set placeOfPerformance.

            # Set streetAddress.
            expected_lots_array[q_0]['placeOfPerformance']['address']['streetAddress'] = \
                payload['tender']['lots'][q_0]['placeOfPerformance']['address']['streetAddress']

            # Set postalCode.
            if "postalCode" in payload['tender']['lots'][q_0]['placeOfPerformance']['address']:

                expected_lots_array[q_0]['placeOfPerformance']['address']['postalCode'] = \
                    payload['tender']['lots'][q_0]['placeOfPerformance']['address']['postalCode']
            else:
                del expected_lots_array[q_0]['placeOfPerformance']['address']['postalCode']

            # Set addressDetails object for items array.
            try:
                lot_country_data = get_value_from_country_csv(

                    country=payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'country']['id'],
                    language=self.language
                )
                expected_lot_country_object = [{
                    "scheme": lot_country_data[2],
                    "id": payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'country']['id'],
                    "description": lot_country_data[1],
                    "uri": lot_country_data[3]
                }]

                lot_region_data = get_value_from_region_csv(

                    region=payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'region']['id'],
                    country=payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'country']['id'],
                    language=self.language
                )
                expected_lot_region_object = [{
                    "scheme": lot_region_data[2],
                    "id": payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'region']['id'],
                    "description": lot_region_data[1],
                    "uri": lot_region_data[3]
                }]

                if payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                        'locality']['scheme'] != "other":

                    lot_locality_data = get_value_from_locality_csv(

                        locality=payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'locality']['id'],
                        region=payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'region']['id'],
                        country=payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'country']['id'],
                        language=self.language
                    )
                    expected_lot_locality_object = [{
                        "scheme": lot_locality_data[2],

                        "id": payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'locality']['id'],
                        "description": lot_locality_data[1],
                        "uri": lot_locality_data[3]
                    }]
                else:
                    expected_lot_locality_object = [{

                        "scheme": payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'locality']['scheme'],

                        "id": payload['tender']['lots'][q_0]['placeOfPerformance']['address']['addressDetails'][
                            'locality']['id'],

                        "description": payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
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
            expected_lots_array[q_0]['placeOfPerformance']['description'] = \
                payload['tender']['lots'][q_0]['placeOfPerformance']['description']

            # Set hasOptions
            if "hasOptions" in payload['tender']['lots'][q_0]:
                expected_lots_array[q_0]['hasOptions'] = payload['tender']['lots'][q_0]['hasOptions']
            else:
                del expected_lots_array[q_0]['hasOptions']

            # Set options.
            if "options" in payload['tender']['lots'][q_0]:
                expected_options_array = list()
                for q_1 in range(len(payload['tender']['lots'][q_0]['options'])):
                    expected_options_array.append(copy.deepcopy(
                        self.expected_pi_release['releases'][0]['tender']['lots'][0]['options'][0]
                    ))

                    if "description" in payload['tender']['lots'][q_0]['options'][q_1]:
                        expected_options_array[q_1]['description'] = \
                            payload['tender']['lots'][q_0]['options'][q_1]['description']
                    else:
                        del expected_options_array[q_1]['description']

                    if "period" in payload['tender']['lots'][q_0]['options'][q_1]:
                        if "durationInDays" in payload['tender']['lots'][q_0]['options'][q_1]['period']:

                            expected_options_array[q_1]['period']['durationInDays'] = \
                                int(payload['tender']['lots'][q_0]['options'][q_1]['period']['durationInDays'])
                        else:
                            del expected_options_array[q_1]['period']['durationInDays']

                        if "startDate" in payload['tender']['lots'][q_0]['options'][q_1]['period']:

                            expected_options_array[q_1]['period']['startDate'] = \
                                payload['tender']['lots'][q_0]['options'][q_1]['period']['startDate']
                        else:
                            del expected_options_array[q_1]['period']['startDate']

                        if "endDate" in payload['tender']['lots'][q_0]['options'][q_1]['period']:

                            expected_options_array[q_1]['period']['endDate'] = \
                                payload['tender']['lots'][q_0]['options'][q_1]['period']['endDate']
                        else:
                            del expected_options_array[q_1]['endDate']

                        if "maxExtentDate" in payload['tender']['lots'][q_0]['options'][q_1]['period']:

                            expected_options_array[q_1]['period']['maxExtentDate'] = \
                                payload['tender']['lots'][q_0]['options'][q_1]['period']['maxExtentDate']
                        else:
                            del expected_options_array[q_1]['period']['maxExtentDate']
                    else:
                        del expected_options_array[q_1]['period']

                expected_lots_array[q_0]['options'] = expected_options_array
            else:
                del expected_lots_array[q_0]['options']

            # Set hasRecurrence
            if "hasRecurrence" in payload['tender']['lots'][q_0]:
                expected_lots_array[q_0]['hasRecurrence'] = payload['tender']['lots'][q_0]['hasRecurrence']
            else:
                del expected_lots_array[q_0]['hasRecurrence']

            # Set recurrence.
            if "recurrence" in payload['tender']['lots'][q_0]:
                if "dates" in payload['tender']['lots'][q_0]['recurrence']:
                    expected_dates_array = list()
                    for q_1 in range(len(payload['tender']['lots'][q_0]['recurrence']['dates'])):
                        expected_dates_array.append(copy.deepcopy(
                            self.expected_pi_release['releases'][0]['tender']['lots'][0]['recurrence']['dates'][0]
                        ))

                        expected_dates_array[q_1]['startDate'] = \
                            payload['tender']['lots'][q_0]['recurrence']['dates'][q_1]['startDate']

                    expected_lots_array[q_0]['recurrence']['dates'] = expected_dates_array
                else:
                    del expected_lots_array[q_0]['recurrence']['dates']

                if "description" in payload['tender']['lots'][q_0]['recurrence']:
                    expected_lots_array[q_0]['recurrence']['description'] = \
                        payload['tender']['lots'][q_0]['recurrence']['description']
                else:
                    del expected_lots_array[q_0]['recurrence']['description']
            else:
                del expected_lots_array[q_0]['recurrence']

            # Set hasRenewal.
            if "hasRenewal" in payload['tender']['lots'][q_0]:
                expected_lots_array[q_0]['hasRenewal'] = payload['tender']['lots'][q_0]['hasRenewal']
            else:
                del expected_lots_array[q_0]['hasRenewal']

            # Set renewal.
            if "renewal" in payload['tender']['lots'][q_0]:
                if "description" in payload['tender']['lots'][q_0]['renewal']:
                    expected_lots_array[q_0]['renewal']['description'] = \
                        payload['tender']['lots'][q_0]['renewal']['description']
                else:
                    del expected_lots_array[q_0]['renewal']['description']

                if "minimumRenewals" in payload['tender']['lots'][q_0]['renewal']:
                    expected_lots_array[q_0]['renewal']['minimumRenewals'] = \
                        int(payload['tender']['lots'][q_0]['renewal']['minimumRenewals'])
                else:
                    del expected_lots_array[q_0]['renewal']['minimumRenewals']

                if "maximumRenewals" in payload['tender']['lots'][q_0]['renewal']:
                    expected_lots_array[q_0]['renewal']['maximumRenewals'] = \
                        int(payload['tender']['lots'][q_0]['renewal']['maximumRenewals'])
                else:
                    del expected_lots_array[q_0]['renewal']['maximumRenewals']

                if "period" in payload['tender']['lots'][q_0]['renewal']:
                    if "durationInDays" in payload['tender']['lots'][q_0]['renewal']['period']:

                        expected_lots_array[q_0]['renewal']['period']['durationInDays'] = \
                            int(payload['tender']['lots'][q_0]['renewal']['period']['durationInDays'])
                    else:
                        del expected_lots_array[q_0]['renewal']['period']['durationInDays']

                    if "startDate" in payload['tender']['lots'][q_0]['renewal']['period']:

                        expected_lots_array[q_0]['renewal']['period']['startDate'] = \
                            payload['tender']['lots'][q_0]['renewal']['period']['startDate']
                    else:
                        del expected_lots_array[q_0]['renewal']['period']['startDate']

                    if "endDate" in payload['tender']['lots'][q_0]['renewal']['period']:

                        expected_lots_array[q_0]['renewal']['period']['endDate'] = \
                            payload['tender']['lots'][q_0]['renewal']['period']['endDate']
                    else:
                        del expected_lots_array[q_0]['renewal']['period']['endDate']

                    if "maxExtentDate" in payload['tender']['lots'][q_0]['renewal']['period']:

                        expected_lots_array[q_0]['renewal']['period']['maxExtentDate'] = \
                            payload['tender']['lots'][q_0]['renewal']['period']['maxExtentDate']
                    else:
                        del expected_lots_array[q_0]['renewal']['period']['maxExtentDate']
                else:
                    del expected_lots_array[q_0]['renewal']['period']
            else:
                del expected_lots_array[q_0]['renewal']

        self.expected_pi_release['releases'][0]['tender']['lots'] = expected_lots_array

        # FR.COM-1.62.45: Set items.
        expected_items_array = list()

        for q_0 in range(len(payload['tender']['items'])):
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
                KeyError(f"Mismatch key into path 'releases[0].tender.items[{q_0}].id'")

            # Set internalId.
            if "internalId" in payload['tender']['items'][q_0]:
                expected_items_array[q_0]['internalId'] = payload['tender']['items'][q_0]['internalId']
            else:
                del self.expected_pi_release['releases'][0]['tender']['items'][q_0]['internalId']

            # Set classification.
            expected_cpv_data = get_value_from_cpv_dictionary_csv(
                cpv=payload['tender']['items'][q_0]['classification']['id'],
                language=self.language
            )
            expected_items_array[q_0]['classification']['scheme'] = "CPV"
            expected_items_array[q_0]['classification']['id'] = expected_cpv_data[0]
            expected_items_array[q_0]['classification']['description'] = expected_cpv_data[1]

            # Set additionalClassifications.
            if "additionalClassifications" in payload['tender']['items'][q_0]:
                additional_classifications = list()
                for q_1 in range(len(payload['tender']['items'][q_0]['additionalClassifications'])):
                    additional_classifications.append(copy.deepcopy(
                        self.expected_pi_release['releases'][0]['tender']['items'][0]['additionalClassifications'][0]
                    ))

                    expected_cpvs_data = get_value_from_cpvs_dictionary_csv(
                        cpvs=payload['tender']['items'][q_0]['additionalClassifications'][q_1]['id'],
                        language=self.language
                    )

                    additional_classifications[q_1]['scheme'] = "CPVS"
                    additional_classifications[q_1]['id'] = expected_cpvs_data[0]
                    additional_classifications[q_1]['description'] = expected_cpvs_data[2]

                expected_items_array[q_0]['additionalClassifications'] = additional_classifications
            else:
                del expected_items_array[q_0]['additionalClassifications']

            # Set quantity.
            expected_items_array[q_0]['quantity'] = int(float(payload['tender']['items'][q_0]['quantity']))

            # Set unit.
            expected_unit_data = get_value_from_classification_unit_dictionary_csv(
                unit_id=payload['tender']['items'][q_0]['unit']['id'],
                language=self.language
            )
            expected_items_array[q_0]['unit']['id'] = expected_unit_data[0]
            expected_items_array[q_0]['unit']['name'] = expected_unit_data[1]

            # Set description.
            expected_items_array[q_0]['description'] = payload['tender']['items'][q_0]['description']

            # Set relatedLot.
            expected_items_array[q_0]['relatedLot'] = \
                self.expected_pi_release['releases'][0]['tender']['lots'][q_0]['id']

        self.expected_pi_release['releases'][0]['tender']['items'] = expected_items_array

        # FR.COM-1.62.69: Set documents.
        if "documents" in payload['tender']:
            expected_documents_array = list()
            for q_0 in range(len(payload['tender']['documents'])):
                expected_documents_array.append(copy.deepcopy(
                    self.expected_pi_release['releases'][0]['tender']['documents'][0]
                ))

                # Set id.
                expected_documents_array[q_0]['id'] = payload['tender']['documents'][q_0]['id']

                # Set title.
                expected_documents_array[q_0]['title'] = payload['tender']['documents'][q_0]['title']

                # Set documentType.
                expected_documents_array[q_0]['documentType'] = payload['tender']['documents'][q_0]['documentType']

                # Set description
                if "description" in payload['tender']['documents'][q_0]:
                    expected_documents_array[q_0]['description'] = payload['tender']['documents'][q_0]['description']
                else:
                    del expected_documents_array[q_0]['description']

                # Set url.
                expected_documents_array[q_0]['url'] = \
                    f"{self.metadata_document_url}/{expected_documents_array[q_0]['id']}"

                # Set datePublished.
                expected_documents_array[q_0]['datePublished'] = message_for_platform['data']['operationDate']

                # FR.COM-1.62.70: Set relatedLots.
                if "relatedLots" in payload['tender']['documents'][q_0]:
                    expected_documents_array[q_0]['relatedLots'] = \
                        self.expected_pi_release['releases'][0]['tender']['lots'][0]['id']
                else:
                    del expected_documents_array[q_0]['relatedLots']

            self.expected_pi_release['releases'][0]['tender']['documents'] = expected_documents_array
        else:
            del self.expected_pi_release['releases'][0]['tender']['documents']

        # FR.COM-1.62.60: Set targets.
        if "targets" in payload['tender']:
            expected_targets_array = list()
            for q_0 in range(len(payload['tender']['targets'])):
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
                    KeyError(f"Mismatch key into path 'releases[0].tender.targets[{q_0}].id'")

                # Set title.
                expected_targets_array[q_0]['title'] = payload['tender']['targets'][q_0]['title']

                # Set relatesTo.
                expected_targets_array[q_0]['relatesTo'] = payload['tender']['targets'][q_0]['relatesTo']

                # FR.COM-1.62.63: Set relatedItem.
                if "relatedItem" in payload['tender']['targets'][q_0]:
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
                for q_1 in range(len(payload['tender']['targets'][q_0]['observations'])):
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
                        KeyError(f"Mismatch key into path 'releases[0].tender.targets[{q_0}].observations[{q_1}].id'")

                    # Set period.
                    if "period" in payload['tender']['targets'][q_0]['observations'][q_1]:

                        # Set startDate.
                        if "startDate" in payload['tender']['targets'][q_0]['observations'][q_1]['period']:
                            expected_observations_array[q_1]['period']['startDate'] = \
                                payload['tender']['targets'][q_0]['observations'][q_1]['period']['startDate']
                        else:
                            del expected_observations_array[q_1]['period']['startDate']

                        # Set endDate.
                        if "startDate" in payload['tender']['targets'][q_0]['observations'][q_1]['period']:
                            expected_observations_array[q_1]['period']['endDate'] = \
                                payload['tender']['targets'][q_0]['observations'][q_1]['period']['endDate']
                        else:
                            del expected_observations_array[q_1]['period']['endDate']
                    else:
                        del expected_observations_array[q_1]['period']

                    # Set measure.
                    expected_observations_array[q_1]['measure'] = \
                        payload['tender']['targets'][q_0]['observations'][q_1]['measure']

                    # Set unit.
                    expected_unit_data = get_value_from_classification_unit_dictionary_csv(
                        unit_id=payload['tender']['targets'][q_0]['observations'][q_1]['unit']['id'],
                        language=self.language
                    )
                    expected_observations_array[q_1]['unit']['id'] = expected_unit_data[0]
                    expected_observations_array[q_1]['unit']['name'] = expected_unit_data[1]

                    # Set dimensions.
                    if "dimensions" in payload['tender']['targets'][q_0]['observations'][q_1]:
                        expected_observations_array[q_1]['dimensions'] = \
                            payload['tender']['targets'][q_0]['observations'][q_1]['dimensions']
                    else:
                        del expected_observations_array[q_1]['dimensions']

                    # Set notes.
                    expected_observations_array[q_1]['notes'] = \
                        payload['tender']['targets'][q_0]['observations'][q_1]['notes']

                    # FR.COM-1.62.64: Set relatedRequirementId.
                    if "relatedRequirementId" in payload['tender']['targets'][q_0]['observations'][q_1]:

                        # What a requirement we need?
                        for p_0 in range(len(payload['tender']['criteria'])):
                            for p_1 in range(len(payload['tender']['criteria'][p_0]['requirementGroups'])):
                                for p_2 in range(len(
                                        payload['tender']['criteria'][p_0]['requirementGroups'][p_1]['requirements']
                                )):
                                    if payload['tender']['criteria'][p_0]['requirementGroups'][p_1][
                                            'requirements'][p_2]['id'] == payload['tender']['targets'][q_0][
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
        if "electronicAuctions" in payload['tender']:
            expected_details_array = list()
            for q_0 in range(len(payload['tender']['electronicAuctions']['details'])):
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
                    KeyError(f"Mismatch key into path 'releases[0].tender.electronicAuctions.details[{q_0}].id'")

                # Set relatedLot.
                # What kind of lot we need?
                for p_0 in range(len(payload['tender']['lots'])):
                    if payload['tender']['lots'][p_0]['id'] == \
                            payload['tender']['electronicAuctions']['details'][q_0]['relatedLot']:

                        expected_details_array[q_0]['relatedLot'] = \
                            actual_pi_release['releases'][0]['tender']['lots'][p_0]['id']

                # Set eligibleMinimumDifference.
                expected_details_array[q_0]['electronicAuctionModalities'][0]['eligibleMinimumDifference']['amount'] \
                    = \
                    payload['tender']['electronicAuctions']['details'][q_0]['electronicAuctionModalities'][0][
                        'eligibleMinimumDifference']['amount']

                expected_details_array[q_0]['electronicAuctionModalities'][0]['eligibleMinimumDifference']['currency'] \
                    = \
                    payload['tender']['electronicAuctions']['details'][q_0]['electronicAuctionModalities'][0][
                        'eligibleMinimumDifference']['currency']

            self.expected_pi_release['releases'][0]['tender']['electronicAuctions']['details'] = expected_details_array
        else:
            del self.expected_pi_release['releases'][0]['tender']['electronicAuctions']

        # FR.COM-1.62.14: Set awardCriteria.
        self.expected_pi_release['releases'][0]['tender']['awardCriteria'] = payload['tender']['awardCriteria']

        # FR.COM-1.62.15: Set awardCriteriaDetails.
        self.expected_pi_release['releases'][0]['tender']['awardCriteriaDetails'] = \
            payload['tender']['awardCriteriaDetails']

        # FR.COM-1.62.16: Set tenderPeriod.
        self.expected_pi_release['releases'][0]['tender']['tenderPeriod']['startDate'] = \
            payload['tender']['tenderPeriod']['startDate']

        # FR.COM-1.62.19: Set procurementMethodModalities.
        if "procurementMethodModalities" in payload['tender']:
            self.expected_pi_release['releases'][0]['tender']['procurementMethodModalities'] = \
                payload['tender']['procurementMethodModalities']
        else:
            del self.expected_pi_release['releases'][0]['tender']['procurementMethodModalities']

        # FR.COM-3.4.3: Set some value.
        # Set enquiryPeriod.
        if "enquiryPeriod" in payload['tender']:
            self.expected_pi_release['releases'][0]['tender']['enquiryPeriod']['startDate'] = \
                message_for_platform['data']['operationDate']

            self.expected_pi_release['releases'][0]['tender']['enquiryPeriod']['endDate'] = \
                payload['tender']['enquiryPeriod']['endDate']
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
        self.expected_pi_release['releases'][0]['tender']['submissionMethodRationale'] = submission_method_rationale

        # Set relatedProcesses.
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
            KeyError(f"Mismatch key into path 'releases[0].relatedProcesses[{0}].id'")

        # Set ocid.
        self.expected_pi_release['releases'][0]['relatedProcesses'][0]['scheme'] = "ocid"

        # Set identifier.
        self.expected_pi_release['releases'][0]['relatedProcesses'][0]['identifier'] = \
            message_for_platform['data']['ocid'][:28]

        # Set uri.
        self.expected_pi_release['releases'][0]['relatedProcesses'][0]['uri'] = \
            f"{self.metadata_tender_url}/{message_for_platform['data']['ocid'][:28]}/" \
            f"{message_for_platform['data']['ocid'][:28]}"
        return self.expected_pi_release

    def build_expected_ms_release(self, payload, message_for_platform, actual_ms_release):
        """Build MS release."""

        """Enrich general attribute for expected MS release"""
        self.expected_pi_release['uri'] = f"{self.metadata_tender_url}/{message_for_platform['data']['ocid'][:28]}/" \
                                          f"{message_for_platform['data']['ocid'][:28]}"

        self.expected_pi_release['version'] = "1.1"
        self.expected_pi_release['extensions'] = self.extensions
        self.expected_pi_release['publisher']['name'] = self.publisher_name
        self.expected_pi_release['publisher']['uri'] = self.publisher_uri
        self.expected_pi_release['license'] = "http://opendefinition.org/licenses/"
        self.expected_pi_release['publicationPolicy'] = "http://opendefinition.org/licenses/"

        # FR.COM-3.4.6 Set created date for release.
        self.expected_pi_release['publishedDate'] = message_for_platform['data']['operationDate']

        """Enrich general attribute for expected PIN release: releases[0]"""
        # FR.COM-3.4.2: Set ocid.
        self.expected_pi_release['releases'][0]['ocid'] = message_for_platform['data']['ocid'][:28]

        # FR.COM-3.4.4: Set id.
        self.expected_pi_release['releases'][0]['id'] = \
            f"{message_for_platform['data']['outcomes']['pin'][0]['id']}-" \
            f"{actual_ms_release['releases'][0]['id'][46:59]}"

        # FR.COM-1.62.6: Set date.
        self.expected_pi_release['releases'][0]['date'] = message_for_platform['data']['operationDate']

        # FR.COM-3.4.7: Set tag.
        self.expected_pi_release['releases'][0]['tag'] = ["planning"]

        # FR.COM-3.4.8: Set initiationType.
        self.expected_pi_release['releases'][0]['initiationType'] = "tender"

        # FR.COM-3.4.11: Set language.
        self.expected_pi_release['releases'][0]['language'] = self.language