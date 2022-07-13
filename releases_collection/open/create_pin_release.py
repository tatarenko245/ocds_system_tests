""""Prepare the expected release of the create pin process, open procedure."""
import copy

from data_collection.OpenProcedure.for_test_createPIN_process.release_full_model import release_model
from data_collection.data_constant import affordable_shemes
from functions_collection.some_functions import is_it_uuid, get_value_from_cpv_dictionary_csv


class CreatePriorInformationNoticeRelease:
    """This class creates instance of release."""

    def __init__(self, environment, country, language, tender_classification_id):

        self.environment = environment
        self.language = language
        self.tender_classification_id = tender_classification_id
        self.expected_pin_release = copy.deepcopy(release_model)

        for c in range(len(affordable_shemes['data'])):
            if affordable_shemes['data'][c]['country'] == country:
                self.__items_additionalclassifications_scheme = affordable_shemes['data'][c][
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

    def build_expected_pin_release(self, payload, message_for_platform, actual_pin_release):
        """Build EI release."""

        """Enrich general attribute for expected PIN release"""
        self.expected_pin_release['uri'] = f"{self.metadata_tender_url}/{message_for_platform['data']['ocid']}/" \
                                           f"{message_for_platform['data']['outcomes']['pin'][0]['id']}"

        self.expected_pin_release['version'] = "1.1"
        self.expected_pin_release['extensions'] = self.extensions
        self.expected_pin_release['publisher']['name'] = self.publisher_name
        self.expected_pin_release['publisher']['uri'] = self.publisher_uri
        self.expected_pin_release['license'] = "http://opendefinition.org/licenses/"
        self.expected_pin_release['publicationPolicy'] = "http://opendefinition.org/licenses/"

        # FR.COM-3.4.6 Set created date for release.
        self.expected_pin_release['publishedDate'] = message_for_platform['data']['operationDate']

        """Enrich general attribute for expected PIN release: releases[0]"""
        # FR.COM-3.4.2: Set ocid.
        self.expected_pin_release['releases'][0]['ocid'] = message_for_platform['data']['outcomes']['pin'][0]['id']

        # FR.COM-3.4.4: Set id.
        self.expected_pin_release['releases'][0]['id'] = \
            f"{message_for_platform['data']['outcomes']['pin'][0]['id']}-" \
            f"{actual_pin_release['releases'][0]['id'][29:42]}"

        # FR.COM-3.4.6: Set date.
        self.expected_pin_release['releases'][0]['date'] = message_for_platform['data']['operationDate']

        # FR.COM-3.4.7: Set tag.
        self.expected_pin_release['releases'][0]['tag'] = ["planning"]

        # FR.COM-3.4.8: Set initiationType.
        self.expected_pin_release['releases'][0]['initiationType'] = "tender"

        # FR.COM-3.4.11: Set language.
        self.expected_pin_release['releases'][0]['language'] = self.language

        """Enrich attribute for expected PIN release: releases[0].tender"""
        # FR.COM-1.62.4: Set id.
        try:
            is_permanent_id_correct = is_it_uuid(
                actual_pin_release['releases'][0]['tender']['id']
            )
            if is_permanent_id_correct is True:

                self.expected_pin_release['releases'][0]['tender']['id']  = \
                    actual_pin_release['releases'][0]['tender']['id']
            else:
                self.expected_pin_release['releases'][0]['tender']['id'] = \
                    f"FR.COM-1.62.4: the 'releases[0].tender.id' must be uuid."
        except KeyError:
            KeyError(f"Mismatch key into path 'releases[0].tender.id'")

        # FR.COM-1.62.5: Set status.
        self.expected_pin_release['releases'][0]['tender']['status'] = "planning"

        # FR.COM-1.62.6: Set date.
        self.expected_pin_release['releases'][0]['tender']['date'] = message_for_platform['data']['operationDate']

        # FR.COM-1.62.9: Set secondStage.
        if "secondStage" in payload['tender']:
            if "minimumCandidates" in payload['tender']['seconStage']:
                self.expected_pin_release['releases'][0]['tender']['secondStage']['minimumCandidates'] = \
                    payload['tender']['secondStage']['minimumCandidates']
            else:
                del self.expected_pin_release['releases'][0]['tender']['secondStage']['minimumCandidates']

            if "maximumCandidates" in payload['tender']['seconStage']:
                self.expected_pin_release['releases'][0]['tender']['secondStage']['maximumCandidates'] = \
                    payload['tender']['secondStage']['maximumCandidates']
            else:
                del self.expected_pin_release['releases'][0]['tender']['secondStage']['maximumCandidates']
        else:
            del self.expected_pin_release['releases'][0]['tender']['secondStage']

        # FR.COM-1.62.10: Set otherCriteria.
        if "otherCriteria" in payload['tender']:
            self.expected_pin_release['releases'][0]['tender']['otherCriteria']['reductionCriteria'] = \
                payload['tender']['otherCriteria']['reductionCriteria']

            self.expected_pin_release['releases'][0]['tender']['otherCriteria']['qualificationSystemMethods'] = \
                payload['tender']['otherCriteria']['qualificationSystemMethods']
        else:
            del self.expected_pin_release['releases'][0]['tender']['otherCriteria']

        # FR.COM-1.62.11: Set classification.
        try:
            expected_cpv_data = get_value_from_cpv_dictionary_csv(
                cpv=self.tender_classification_id,
                language=self.language
            )

            self.expected_pin_release['releases'][0]['tender']['classification']['id'] = expected_cpv_data[0]
            self.expected_pin_release['releases'][0]['tender']['classification']['description'] = expected_cpv_data[1]
            self.expected_pin_release['releases'][0]['tender']['classification']['scheme'] = "CPV"
        except ValueError:
            ValueError("FR.COM-1.62.11: impossible to set tender.classification object.")

        # FR.COM-1.62.14: Set awardCriteria.
        self.expected_pin_release['releases'][0]['tender']['awardCriteria'] = payload['tender']['awardCriteria']

        # FR.COM-1.62.15: Set awardCriteriaDetails.
        self.expected_pin_release['releases'][0]['tender']['awardCriteriaDetails'] = \
            payload['tender']['awardCriteriaDetails']

        # FR.COM-1.62.16: Set tenderPeriod.
        self.expected_pin_release['releases'][0]['tender']['tenderPeriod']['startDate'] = \
            payload['tender']['tenderPeriod']['startDate']

        # FR.COM-1.62.19: Set procurementMethodModalities.
        if "procurementMethodModalities" in payload['tender']:
            self.expected_pin_release['releases'][0]['tender']['procurementMethodModalities'] = \
                payload['tender']['procurementMethodModalities']
        else:
            del self.expected_pin_release['releases'][0]['tender']['procurementMethodModalities']

        # FR.COM-3.4.3: Set some value.
        # Set enquiryPeriod.
        if "enquiryPeriod" in payload['tender']:
            self.expected_pin_release['releases'][0]['tender']['enquiryPeriod']['startDate'] = \
                message_for_platform['data']['operationDate']

            self.expected_pin_release['releases'][0]['tender']['enquiryPeriod']['endDate'] = \
                payload['tender']['enquiryPeriod']['endDate']
        else:
            del self.expected_pin_release['releases'][0]['tender']['enquiryPeriod']


        return self.expected_pin_release
