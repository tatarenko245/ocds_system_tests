"""Prepare the expected release of the withdraw expenditure item process, budget."""
import copy

from data_collection.Budget.for_test_withdrawEI_process.release_full_model import release_model


class WithdrawExpenditureItemRelease:
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

    def build_expected_ei_release(self, message_for_platform, actual_ei_release, previous_ei_release):
        """Build EI release."""

        """Enrich general attribute for expected EI release"""
        # Get value from previous release.

        self.expected_ei_release['uri'] = previous_ei_release['uri']
        self.expected_ei_release['version'] = previous_ei_release['version']
        self.expected_ei_release['extensions'] = previous_ei_release['extensions']
        self.expected_ei_release['publisher']['name'] = previous_ei_release['publisher']['name']
        self.expected_ei_release['publisher']['uri'] = previous_ei_release['publisher']['uri']
        self.expected_ei_release['license'] = previous_ei_release['license']
        self.expected_ei_release['publicationPolicy'] = previous_ei_release['publicationPolicy']
        self.expected_ei_release['publishedDate'] = previous_ei_release['publishedDate']

        """Enrich general attribute for expected EI release: releases[0]"""
        # Get value from previous release.

        self.expected_ei_release['releases'][0]['ocid'] = previous_ei_release['releases'][0]['ocid']

        self.expected_ei_release['releases'][0]['id'] = f"{previous_ei_release['releases'][0]['id'][:28]}-" \
                                                        f"{actual_ei_release['releases'][0]['id'][29:42]}"

        self.expected_ei_release['releases'][0]['tag'] = previous_ei_release['releases'][0]['tag']
        self.expected_ei_release['releases'][0]['initiationType'] = previous_ei_release['releases'][0]['initiationType']
        self.expected_ei_release['releases'][0]['language'] = previous_ei_release['releases'][0]['language']

        # FR.COM-3.6.1: Set date.
        self.expected_ei_release['releases'][0]['date'] = message_for_platform['data']['operationDate']

        """Enrich attribute for expected EI release: releases[0].planning"""
        # Get value from previous release.

        self.expected_ei_release['releases'][0]['planning']['budget']['id'] = \
            previous_ei_release['releases'][0]['planning']['budget']['id']

        self.expected_ei_release['releases'][0]['planning']['budget']['period']['startDate'] = \
            previous_ei_release['releases'][0]['planning']['budget']['period']['startDate']

        self.expected_ei_release['releases'][0]['planning']['budget']['period']['endDate'] = \
            previous_ei_release['releases'][0]['planning']['budget']['period']['endDate']

        if "rationale" in previous_ei_release['releases'][0]['planning']:

            self.expected_ei_release['releases'][0]['planning']['rationale'] = \
                previous_ei_release['releases'][0]['planning']['rationale']

        else:
            del self.expected_ei_release['releases'][0]['planning']['rationale']

        if "amount" in self.expected_ei_release['releases'][0]['planning']['budget']:

            self.expected_ei_release['releases'][0]['planning']['budget']['amount']['amount'] = \
                previous_ei_release['releases'][0]['planning']['budget']['amount']['amount']

            self.expected_ei_release['releases'][0]['planning']['budget']['amount']['currency'] = \
                previous_ei_release['releases'][0]['planning']['budget']['amount']['currency']
        else:
            del self.expected_ei_release['releases'][0]['planning']['budget']['amount']

        """Enrich attribute for expected EI release: releases[0].parties"""
        # Get value from previous release.

        self.expected_ei_release['releases'][0]['parties'] = previous_ei_release['releases'][0]['parties']

        """Enrich attribute for expected EI release: releases[0].tender"""
        # Get value from previous release.

        self.expected_ei_release['releases'][0]['tender']['id'] = previous_ei_release['releases'][0]['tender']['id']

        self.expected_ei_release['releases'][0]['tender']['mainProcurementCategory'] = \
            previous_ei_release['releases'][0]['tender']['mainProcurementCategory']

        self.expected_ei_release['releases'][0]['tender']['classification']['id'] = \
            previous_ei_release['releases'][0]['tender']['classification']['id']

        self.expected_ei_release['releases'][0]['tender']['classification']['description'] = \
            previous_ei_release['releases'][0]['tender']['classification']['description']

        self.expected_ei_release['releases'][0]['tender']['classification']['scheme'] = \
            previous_ei_release['releases'][0]['tender']['classification']['scheme']

        if "title" in previous_ei_release['releases'][0]['tender']:

            self.expected_ei_release['releases'][0]['tender']['title'] = \
                previous_ei_release['releases'][0]['tender']['title']
        else:
            del self.expected_ei_release['releases'][0]['tender']['title']

        if "description" in previous_ei_release['releases'][0]['tender']:

            self.expected_ei_release['releases'][0]['tender']['description'] = \
                previous_ei_release['releases'][0]['tender']['description']
        else:
            del self.expected_ei_release['releases'][0]['tender']['description']

        if "items" in previous_ei_release['releases'][0]['tender']:

            self.expected_ei_release['releases'][0]['tender']['items'] = \
                previous_ei_release['releases'][0]['tender']['items']
        else:
            del self.expected_ei_release['releases'][0]['tender']['items']

        # FR.COM-14.13.1: Set status.
        self.expected_ei_release['releases'][0]['tender']['status'] = "planning"

        """Enrich attribute for expected EI release: releases[0].buyer"""
        # Get value from previous release.

        self.expected_ei_release['releases'][0]['buyer']['id'] = previous_ei_release['releases'][0]['buyer']['id']
        self.expected_ei_release['releases'][0]['buyer']['name'] = previous_ei_release['releases'][0]['buyer']['name']

        return self.expected_ei_release
