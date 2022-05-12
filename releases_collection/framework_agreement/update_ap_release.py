"""Prepare the expected releases of the update aggregated plan process, framework agreement procedures."""
import copy

from functions_collection.some_functions import get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv, is_it_uuid, get_value_from_cpvs_dictionary_csv, get_value_from_cpv_dictionary_xls, \
    get_value_from_classification_unit_dictionary_csv, generate_tender_classification_id


class UpdateAggregatedPlanRelease:
    """This class creates instance of release."""

    def __init__(self, environment, language, cpid, ocid, payload, actual_message, actual_ap_release,
                 previous_ap_release, actual_ms_release, previous_fa_release):

        self.__language = language
        self.__cpid = cpid
        self.__ocid = ocid
        self.__payload = payload
        self.__actual_message = actual_message
        self.__actual_ap_release = actual_ap_release
        self.__previous_ap_release = previous_ap_release
        self.__actual_ms_release = actual_ms_release
        self.__previous_fa_release = previous_fa_release

        try:
            if environment == "dev":
                self.__metadata_tender_url = "http://dev.public.eprocurement.systems/tenders"
                self.__metadata_document_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get"
                self.__metadata_budget_url = "http://dev.public.eprocurement.systems/budgets"

            elif environment == "sandbox":
                self.__metadata_tender_url = "http://public.eprocurement.systems/tenders"
                self.__metadata_document_url = "http://storage.eprocurement.systems/get"
                self.__metadata_budget_url = "http://public.eprocurement.systems/budgets"
        except ValueError:
            ValueError("Check your environment: You must use 'dev' or 'sandbox' environment in pytest command")

        self.__expected_ap_release = {
            "uri": self.__previous_ap_release['uri'],
            "version": self.__previous_ap_release['version'],
            "extensions": self.__previous_ap_release['extensions'],
            "publisher": {
                "name": self.__previous_ap_release['publisher']['name'],
                "uri": self.__previous_ap_release['publisher']['uri']
            },
            "license": self.__previous_ap_release['license'],
            "publicationPolicy": self.__previous_ap_release['publicationPolicy'],
            "publishedDate": self.__previous_ap_release['publishedDate'],
            "releases": [
                {
                    "ocid": self.__previous_ap_release['releases'][0]['ocid'],
                    "id": f"{self.__ocid}-{self.__actual_ap_release['releases'][0]['id'][46:59]}",
                    "date": self.__actual_message['data']['operationDate'],
                    "tag": [
                        "planningUpdate"
                    ],
                    "language": self.__previous_ap_release['releases'][0]['language'],
                    "initiationType": self.__previous_ap_release['releases'][0]['initiationType'],
                    "parties": self.__previous_ap_release['releases'][0]['parties'],
                    "tender": {
                        "id": self.__previous_ap_release['releases'][0]['tender']['id'],
                        "status": self.__previous_ap_release['releases'][0]['tender']['status'],
                        "statusDetails": self.__previous_ap_release['releases'][0]['tender']['statusDetails'],
                        "items": [
                            {
                                "id": "",
                                "internalId": "",
                                "description": "",
                                "classification": {
                                    "scheme": "",
                                    "id": "",
                                    "description": ""
                                },
                                "additionalClassifications": [
                                    {
                                        "scheme": "",
                                        "id": "",
                                        "description": ""
                                    }
                                ],
                                "quantity": 0.0,
                                "unit": {
                                    "name": "",
                                    "id": ""
                                },
                                "deliveryAddress": {
                                    "streetAddress": "",
                                    "postalCode": "",
                                    "addressDetails": {
                                        "country": {
                                            "scheme": "",
                                            "id": "",
                                            "description": "",
                                            "uri": ""
                                        },
                                        "region": {
                                            "scheme": "",
                                            "id": "",
                                            "description": "",
                                            "uri": ""
                                        },
                                        "locality": {
                                            "scheme": "",
                                            "id": "",
                                            "description": "",
                                            "uri": ""
                                        }
                                    }
                                },
                                "relatedLot": ""
                            }
                        ],
                        "lots": [
                            {
                                "id": "",
                                "internalId": "",
                                "title": "",
                                "description": "",
                                "status": "",
                                "statusDetails": "",
                                "placeOfPerformance": {
                                    "address": {
                                        "streetAddress": "",
                                        "postalCode": "",
                                        "addressDetails": {
                                            "country": {
                                                "scheme": "",
                                                "id": "",
                                                "description": "",
                                                "uri": ""
                                            },
                                            "region": {
                                                "scheme": "",
                                                "id": "",
                                                "description": "",
                                                "uri": ""
                                            },
                                            "locality": {
                                                "scheme": "",
                                                "id": "",
                                                "description": "",
                                                "uri": ""
                                            }
                                        }
                                    }
                                }
                            }
                        ],
                        "tenderPeriod": {
                            "startDate": self.__payload['tender']['tenderPeriod']['startDate']
                        },
                        "hasEnquiries": self.__previous_ap_release['releases'][0]['tender']['hasEnquiries'],
                        "documents": [
                            {
                                "id": "",
                                "documentType": "",
                                "title": "",
                                "description": "",
                                "url": "",
                                "datePublished": "",
                                "relatedLots": [""]
                            }
                        ],
                        "submissionMethod": self.__previous_ap_release['releases'][0]['tender']['submissionMethod'],
                        "submissionMethodDetails": self.__previous_ap_release['releases'][0]['tender'][
                            'submissionMethodDetails'],
                        "submissionMethodRationale": self.__previous_ap_release['releases'][0]['tender'][
                            'submissionMethodRationale'],
                        "requiresElectronicCatalogue": self.__previous_ap_release['releases'][0]['tender'][
                            'requiresElectronicCatalogue']
                    },
                    "hasPreviousNotice": self.__previous_ap_release['releases'][0]['hasPreviousNotice'],
                    "purposeOfNotice": {
                        "isACallForCompetition": self.__previous_ap_release['releases'][0][
                            'purposeOfNotice']['isACallForCompetition']
                    },
                    "relatedProcesses": self.__previous_ap_release['releases'][0]['relatedProcesses']
                }
            ]
        }

        self.__expected_fa_release = {
            "uri": self.__previous_fa_release['uri'],
            "version": self.__previous_fa_release['version'],
            "extensions": self.__previous_fa_release['extensions'],
            "publisher": {
                "name": self.__previous_fa_release['publisher']['name'],
                "uri": self.__previous_fa_release['publisher']['uri']
            },
            "license": self.__previous_fa_release['license'],
            "publicationPolicy": self.__previous_fa_release['publicationPolicy'],
            "publishedDate": self.__previous_fa_release['publishedDate'],
            "releases": [
                {
                    "ocid": self.__previous_fa_release['releases'][0]['ocid'],
                    "id": f"{self.__cpid}-{self.__actual_ms_release['releases'][0]['id'][29:42]}",
                    "date": self.__actual_message['data']['operationDate'],
                    "tag": self.__previous_fa_release['releases'][0]['tag'],
                    "language": self.__previous_fa_release['releases'][0]['language'],
                    "initiationType": self.__previous_fa_release['releases'][0]['initiationType'],
                    "tender": {
                        "id": self.__previous_fa_release['releases'][0]['tender']['id'],
                        "title": "",
                        "description": "",
                        "status": self.__previous_fa_release['releases'][0]['tender']['status'],
                        "statusDetails": self.__previous_fa_release['releases'][0]['tender']['statusDetails'],
                        "value": {
                            "amount": self.__previous_fa_release['releases'][0]['tender']['value']['amount'],
                            "currency": ""
                        },
                        "procurementMethod": self.__previous_fa_release['releases'][0]['tender']['procurementMethod'],
                        "procurementMethodDetails": self.__previous_fa_release['releases'][0]['tender'][
                            'procurementMethodDetails'],
                        "procurementMethodRationale": "",
                        "mainProcurementCategory": "",
                        "hasEnquiries": self.__previous_fa_release['releases'][0]['tender']['hasEnquiries'],
                        "eligibilityCriteria": self.__previous_fa_release['releases'][0]['tender'][
                            'eligibilityCriteria'],
                        "contractPeriod": {
                            "startDate": self.__previous_fa_release['releases'][0]['tender']['contractPeriod'][
                                'startDate'],
                            "endDate": self.__previous_fa_release['releases'][0]['tender']['contractPeriod'][
                                'endDate']
                        },
                        "acceleratedProcedure": {
                            "isAcceleratedProcedure": self.__previous_fa_release['releases'][0]['tender'][
                                'acceleratedProcedure']['isAcceleratedProcedure']
                        },
                        "classification": {
                            "scheme": "",
                            "id": "",
                            "description": ""
                        },
                        "designContest": {
                            "serviceContractAward": self.__previous_fa_release['releases'][0]['tender'][
                                'designContest']['serviceContractAward']
                        },
                        "electronicWorkflows": {
                            "useOrdering": self.__previous_fa_release['releases'][0]['tender'][
                                'electronicWorkflows']['useOrdering'],
                            "usePayment": self.__previous_fa_release['releases'][0]['tender'][
                                'electronicWorkflows']['usePayment'],
                            "acceptInvoicing": self.__previous_fa_release['releases'][0]['tender'][
                                'electronicWorkflows']['acceptInvoicing']
                        },
                        "jointProcurement": {
                            "isJointProcurement": self.__previous_fa_release['releases'][0]['tender'][
                                'jointProcurement']['isJointProcurement']
                        },
                        "legalBasis": self.__previous_fa_release['releases'][0]['tender']['legalBasis'],
                        "procedureOutsourcing": {
                            "procedureOutsourced": self.__previous_fa_release['releases'][0]['tender'][
                                'procedureOutsourcing']['procedureOutsourced']
                        },
                        "dynamicPurchasingSystem": {
                            "hasDynamicPurchasingSystem": self.__previous_fa_release['releases'][0]['tender'][
                                'dynamicPurchasingSystem']['hasDynamicPurchasingSystem']
                        },
                        "framework": {
                            "isAFramework": self.__previous_fa_release['releases'][0]['tender'][
                                'framework']['isAFramework']
                        }
                    },
                    "relatedProcesses": self.__previous_fa_release['releases'][0]['relatedProcesses']
                }
            ]
        }

    def build_expected_ap_release(self):

        if "lots" in self.__payload['tender']:
            lots_array = list()
            for q_0 in range(len(self.__payload['tender']['lots'])):
                lots_array.append(copy.deepcopy(
                    self.__expected_ap_release['releases'][0]['tender']['lots'][0]
                ))

                if "internalId" in self.__payload['tender']['lots'][q_0]:
                    lots_array[q_0]['internalId'] = self.__payload['tender']['lots'][q_0]['internalId']
                else:
                    del lots_array[q_0]['internalId']

                lots_array[q_0]['title'] = self.__payload['tender']['lots'][q_0]['title']
                lots_array[q_0]['description'] = self.__payload['tender']['lots'][q_0]['description']
                lots_array[q_0]['status'] = "planning"
                lots_array[q_0]['statusDetails'] = "empty"

                if "placeOfPerformance" in self.__payload['tender']['lots'][q_0]:
                    lots_array[q_0]['placeOfPerformance']['address']['streetAddress'] = \
                        self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address']['streetAddress']

                    if "postalCode" in self.__payload['tender']['lots'][q_0]['placeOfPerformance']:
                        lots_array[q_0]['placeOfPerformance']['address']['postalCode'] = \
                            self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address']['postalCode']
                    else:
                        del lots_array[q_0]['placeOfPerformance']['address']['postalCode']

                    try:
                        f"""
                        Prepare releases[0].tender.lots[{q_0}].placeOfPerformance.address.addressDetails object".
                        """
                        lot_country_data = get_value_from_country_csv(
                            country=self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                'addressDetails']['country']['id'],

                            language=self.__language
                        )
                        expected_lot_country_object = [{
                            "scheme": lot_country_data[2],

                            "id": self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                'addressDetails']['country']['id'],

                            "description": lot_country_data[1],
                            "uri": lot_country_data[3]
                        }]

                        lot_region_data = get_value_from_region_csv(
                            region=self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                'addressDetails']['region']['id'],

                            country=self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                'addressDetails']['country']['id'],

                            language=self.__language
                        )
                        expected_lot_region_object = [{
                            "scheme": lot_region_data[2],

                            "id": self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                'addressDetails']['region']['id'],

                            "description": lot_region_data[1],
                            "uri": lot_region_data[3]
                        }]

                        if "locality" in self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                'addressDetails']:
                            if self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                    'addressDetails']['locality']['scheme'] == "CUATM":

                                lot_locality_data = get_value_from_locality_csv(

                                    locality=self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                        'addressDetails']['locality']['id'],

                                    region=self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                        'addressDetails']['region']['id'],

                                    country=self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                        'addressDetails']['country']['id'],

                                    language=self.__language
                                )
                                expected_lot_locality_object = [{
                                    "scheme": lot_locality_data[2],

                                    "id": self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                        'addressDetails']['locality']['id'],

                                    "description": lot_locality_data[1],
                                    "uri": lot_locality_data[3]
                                }]
                            else:
                                expected_lot_locality_object = [{
                                    "scheme": self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                        'addressDetails']['locality']['scheme'],

                                    "id": self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                        'addressDetails'][
                                        'locality']['id'],

                                    "description": self.__payload['tender']['lots'][q_0]['placeOfPerformance'][
                                        'address']['addressDetails']['locality']['description'],

                                    "uri": self.__payload['tender']['lots'][q_0]['placeOfPerformance']['address'][
                                        'addressDetails']['locality']['uri']
                                }]
                            lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality'] = \
                                expected_lot_locality_object[0]
                        else:
                            del lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['locality']

                        lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['country'] = \
                            expected_lot_country_object[0]

                        lots_array[q_0]['placeOfPerformance']['address']['addressDetails']['region'] = \
                            expected_lot_region_object[0]

                    except ValueError:
                        ValueError(
                            f"Impossible to prepare the 'expected releases[0].tender.lots[{q_0}]."
                            f"placeOfPerformance.address.addressDetails' object.")
                else:
                    del lots_array[q_0]['placeOfPerformance']

            # Sort 'lots' array and set id:
            expected_lots = list()
            for act in range(len(self.__actual_ap_release['releases'][0]['tender']['lots'])):
                for exp in range(len(lots_array)):
                    if lots_array[exp]['description'] == \
                            self.__actual_ap_release['releases'][0]['tender']['lots'][act]['description']:

                        try:
                            """Set permanent id."""
                            is_permanent_id_correct = is_it_uuid(
                                self.__actual_ap_release['releases'][0]['tender']['lots'][act]['id']
                            )
                            if is_permanent_id_correct is True:
                                lots_array[exp]['id'] = \
                                    self.__actual_ap_release['releases'][0]['tender']['lots'][act]['id']
                            else:
                                ValueError(f"The 'releases[0].tender.lots[{act}].id' must be uuid.")
                        except KeyError:
                            KeyError(f"Mismatch key into path 'releases[0].tender.lots[{act}].id'")

                        expected_lots.append(lots_array[exp])
            self.__expected_ap_release['releases'][0]['tender']['lots'] = expected_lots
        else:
            del self.__payload['tender']['lots']

        if "items" in self.__payload['tender']:
            items_array = list()
            for q_0 in range(len(self.__payload['tender']['items'])):
                items_array.append(copy.deepcopy(
                    self.__expected_ap_release['releases'][0]['tender']['items'][0]
                ))

                try:
                    """Set permanent id."""
                    is_permanent_id_correct = is_it_uuid(
                        self.__actual_ap_release['releases'][0]['tender']['items'][q_0]['id']
                    )
                    if is_permanent_id_correct is True:
                        items_array[q_0]['id'] = self.__actual_ap_release['releases'][0]['tender']['items'][q_0]['id']
                    else:
                        ValueError(f"The 'releases[0].tender.items[{q_0}].id' must be uuid.")
                except KeyError:
                    KeyError(f"Mismatch key into path 'releases[0].tender.items[{q_0}].id'")

                if "internalId" in self.__payload['tender']['items'][q_0]:
                    items_array[q_0]['internalId'] = self.__payload['tender']['items'][q_0]['internalId']
                else:
                    del items_array[q_0]['internalId']

                items_array[q_0]['description'] = self.__payload['tender']['items'][q_0]['description']

                expected_cpv_data = get_value_from_cpv_dictionary_xls(
                    cpv=self.__payload['tender']['items'][q_0]['classification']['id'],
                    language=self.__language
                )

                items_array[q_0]['classification']['scheme'] = "CPV"
                items_array[q_0]['classification']['id'] = expected_cpv_data[0]
                items_array[q_0]['classification']['description'] = expected_cpv_data[1]
                items_array[q_0]['quantity'] = round(float(self.__payload['tender']['items'][q_0]['quantity']), 1)

                expected_unit_data = get_value_from_classification_unit_dictionary_csv(
                    unit_id=self.__payload['tender']['items'][q_0]['unit']['id'],
                    language=self.__language
                )

                items_array[q_0]['unit']['id'] = expected_unit_data[0]
                items_array[q_0]['unit']['name'] = expected_unit_data[1]

                items_array[q_0]['relatedLot'] = self.__expected_ap_release['releases'][0]['tender']['lots'][q_0]['id']

                if "additionalClassifications" in self.__payload['tender']['items'][q_0]:
                    additional_classifications = list()
                    for q_1 in range(len(self.__payload['tender']['items'][q_0]['additionalClassifications'])):
                        additional_classifications.append(copy.deepcopy(
                            self.__expected_ap_release['releases'][0]['tender']['items'][0][
                                'additionalClassifications'][0]
                        ))

                        expected_cpvs_data = get_value_from_cpvs_dictionary_csv(
                            cpvs=self.__payload['tender']['items'][q_0]['additionalClassifications'][q_1]['id'],
                            language=self.__language
                        )

                        additional_classifications[q_1]['scheme'] = "CPVS"
                        additional_classifications[q_1]['id'] = expected_cpvs_data[0]
                        additional_classifications[q_1]['description'] = expected_cpvs_data[2]

                    items_array[q_0]['additionalClassifications'] = additional_classifications
                else:
                    del items_array[q_0]['additionalClassifications']

                if "deliveryAddress" in self.__payload['tender']['items'][q_0]:
                    if "streetAddress" in self.__payload['tender']['items'][q_0]['deliveryAddress']:

                        items_array[q_0]['deliveryAddress']['streetAddress'] = \
                            self.__payload['tender']['items'][q_0]['deliveryAddress']['streetAddress']
                    else:
                        del items_array[q_0]['deliveryAddress']['streetAddress']

                    if "postalCode" in self.__payload['tender']['items'][q_0]['deliveryAddress']:

                        items_array[q_0]['deliveryAddress']['postalCode'] = \
                            self.__payload['tender']['items'][q_0]['deliveryAddress']['postalCode']
                    else:
                        del items_array[q_0]['deliveryAddress']['postalCode']

                    try:
                        """
                        "Prepare releases[0].tender.items[*].deliveryAddress.addressDetails object".
                        """
                        item_country_data = get_value_from_country_csv(
                            country=self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                'addressDetails']['country']['id'],

                            language=self.__language
                        )
                        expected_item_country_object = [{
                            "scheme": item_country_data[2],

                            "id": self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                'addressDetails']['country']['id'],

                            "description": item_country_data[1],
                            "uri": item_country_data[3]
                        }]

                        item_region_data = get_value_from_region_csv(
                            region=self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                'addressDetails']['region']['id'],

                            country=self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                'addressDetails']['country']['id'],

                            language=self.__language
                        )
                        expected_item_region_object = [{
                            "scheme": item_region_data[2],

                            "id": self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                'addressDetails']['region']['id'],

                            "description": item_region_data[1],
                            "uri": item_region_data[3]
                        }]

                        if "locality" in self.__payload['tender']['items'][q_0]['deliveryAddress']['addressDetails']:
                            if self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                    'addressDetails']['locality']['scheme'] == "CUATM":

                                item_locality_data = get_value_from_locality_csv(

                                    locality=self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                        'addressDetails']['locality']['id'],

                                    region=self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                        'addressDetails']['region']['id'],

                                    country=self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                        'addressDetails']['country']['id'],

                                    language=self.__language
                                )
                                expected_item_locality_object = [{
                                    "scheme": item_locality_data[2],

                                    "id": self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                        'addressDetails']['locality']['id'],

                                    "description": item_locality_data[1],
                                    "uri": item_locality_data[3]
                                }]
                            else:
                                expected_item_locality_object = [{
                                    "scheme": self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                        'addressDetails']['locality']['scheme'],

                                    "id": self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                        'addressDetails']['locality']['id'],

                                    "description": self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                        'addressDetails']['locality']['description'],

                                    "uri": self.__payload['tender']['items'][q_0]['deliveryAddress'][
                                        'addressDetails']['locality']['uri']
                                }]

                            items_array[q_0]['deliveryAddress']['addressDetails']['locality'] = \
                                expected_item_locality_object[0]
                        else:
                            del items_array[q_0]['deliveryAddress']['addressDetails']['locality']

                        items_array[q_0]['deliveryAddress']['addressDetails']['country'] = \
                            expected_item_country_object[0]

                        items_array[q_0]['deliveryAddress']['addressDetails']['region'] = \
                            expected_item_region_object[0]
                    except ValueError:
                        ValueError(
                            f"Impossible to prepare the expected releases[0].tender.items[{q_0}].deliveryAddress."
                            "addressDetails object.")
                else:
                    del items_array[q_0]['deliveryAddress']

            # Sort 'items' array and set id:
            expected_items = list()
            for act in range(len(self.__actual_ap_release['releases'][0]['tender']['items'])):
                for exp in range(len(items_array)):
                    if items_array[exp]['description'] == \
                            self.__actual_ap_release['releases'][0]['tender']['items'][act]['description']:

                        try:
                            """Set permanent id."""
                            is_permanent_id_correct = is_it_uuid(
                                self.__actual_ap_release['releases'][0]['tender']['items'][act]['id']
                            )
                            if is_permanent_id_correct is True:
                                items_array[exp]['id'] = \
                                    self.__actual_ap_release['releases'][0]['tender']['items'][act]['id']
                            else:
                                ValueError(f"The 'releases[0].tender.items[{act}].id' must be uuid.")
                        except KeyError:
                            KeyError(f"Mismatch key into path 'releases[0].tender.items[{act}].id'")

                        if "additionalClassifications" in items_array[exp]:
                            expected_additional_classifications = list()
                            for act_1 in range(len(
                                    self.__actual_ap_release['releases'][0]['tender']['items'][act][
                                        'additionalClassifications']
                            )):
                                for exp_1 in range(len(items_array[exp]['additionalClassifications'])):
                                    if items_array[exp]['additionalClassifications'][exp_1]['id'] == \
                                            self.__actual_ap_release['releases'][0]['tender']['items'][act][
                                                'additionalClassifications'][act_1]['id']:
                                        expected_additional_classifications.append(
                                            items_array[exp]['additionalClassifications'][exp_1]
                                        )
                            items_array[exp]['additionalClassifications'] = expected_additional_classifications
                        expected_items.append(items_array[exp])
            self.__expected_ap_release['releases'][0]['tender']['items'] = expected_items
        else:
            del self.__payload['tender']['items']

        if "documents" in self.__payload['tender']:
            documents_array = list()
            for q_0 in range(len(self.__payload['tender']['documents'])):
                documents_array.append(copy.deepcopy(
                    self.__expected_ap_release['releases'][0]['tender']['documents'][0]
                ))

                documents_array[q_0]['id'] = self.__payload['tender']['documents'][q_0]['id']
                for q_1 in range(len(self.__previous_ap_release['releases'][0]['tender']['documents'])):

                    if documents_array[q_0]['id'] == \
                            self.__previous_ap_release['releases'][0]['tender']['documents'][q_1]['id']:

                        documents_array[q_0]['documentType'] = \
                            self.__previous_ap_release['releases'][0]['tender']['documents'][q_1]['documentType']

                        if "description" in self.__previous_ap_release['releases'][0]['tender']['documents'][q_1]:
                            documents_array[q_0]['description'] = \
                                self.__previous_ap_release['releases'][0]['tender']['documents'][q_1]['description']

                        if "datePublished" in self.__previous_ap_release['releases'][0]['tender']['documents'][q_1]:
                            documents_array[q_0]['datePublished'] = \
                                self.__previous_ap_release['releases'][0]['tender']['documents'][q_1]['datePublished']

                        if "relatedLots" in self.__previous_ap_release['releases'][0]['tender']['documents'][q_1]:
                            documents_array[q_0]['relatedLots'] = \
                                self.__previous_ap_release['releases'][0]['tender']['documents'][q_1]['relatedLots']

                documents_array[q_0]['title'] = self.__payload['tender']['documents'][q_0]['title']

                if "description" in self.__payload['tender']['documents'][q_0]:
                    documents_array[q_0]['description'] = self.__payload['tender']['documents'][q_0]['description']
                else:
                    if documents_array[q_0]['description'] == "":
                        del documents_array[q_0]['description']

                documents_array[q_0]['url'] = f"{self.__metadata_document_url}/{documents_array[q_0]['id']}"

                if documents_array[q_0]['datePublished'] == "":
                    documents_array[q_0]['datePublished'] = self.__actual_message['data']['operationDate']

                if documents_array[q_0]['documentType'] == "":
                    documents_array[q_0]['documentType'] = self.__payload['tender']['documents'][q_0]['documentType']

                if "relatedLots" in self.__payload['tender']['documents'][q_0]:

                    documents_array[q_0]['relatedLots'] = \
                        [self.__actual_ap_release['releases'][0]['tender']['lots'][q_0]['id']]
                else:
                    if documents_array[q_0]['relatedLots'] == [""]:
                        del documents_array[q_0]['relatedLots']

            # Sort 'documents' array and set id:
            expected_documents = list()
            for act in range(len(self.__actual_ap_release['releases'][0]['tender']['documents'])):
                for exp in range(len(documents_array)):
                    if documents_array[exp]['id'] == \
                            self.__actual_ap_release['releases'][0]['tender']['documents'][act]['id']:
                        expected_documents.append(documents_array[exp])
            self.__expected_ap_release['releases'][0]['tender']['documents'] = expected_documents
        else:
            del self.__payload['tender']['documents']
        return self.__expected_ap_release

    def build_expected_fa_release(self):
        # BR-2.3.1.12:
        self.__expected_fa_release['releases'][0]['tender']['title'] = self.__payload['tender']['title']
        self.__expected_fa_release['releases'][0]['tender']['description'] = self.__payload['tender']['description']

        if "items" in self.__payload['tender']:
            expected_cpv_data = get_value_from_cpv_dictionary_xls(
                cpv=generate_tender_classification_id(self.__payload['tender']['items']),
                language=self.__language
            )
            self.__expected_fa_release['releases'][0]['tender']['classification']['id'] = expected_cpv_data[0]
            self.__expected_fa_release['releases'][0]['tender']['classification']['description'] = expected_cpv_data[1]
            self.__expected_fa_release['releases'][0]['tender']['classification']['scheme'] = "CPV"

            try:
                """
               Enrich mainProcurementCategory, depends on tender.classification.id.
               """
                expected_main_procurement_category = None
                if \
                        expected_cpv_data[0][0:2] == "03" or \
                        expected_cpv_data[0][0] == "1" or \
                        expected_cpv_data[0][0] == "2" or \
                        expected_cpv_data[0][0] == "3" or \
                        expected_cpv_data[0][0:2] == "44" or \
                        expected_cpv_data[0][0:2] == "48":
                    expected_main_procurement_category = "goods"
                elif \
                        expected_cpv_data[0][0:2] == "45":
                    expected_main_procurement_category = "works"
                elif \
                        expected_cpv_data[0][0] == "5" or \
                        expected_cpv_data[0][0] == "6" or \
                        expected_cpv_data[0][0] == "7" or \
                        expected_cpv_data[0][0] == "8" or \
                        expected_cpv_data[0][0:2] == "92" or \
                        expected_cpv_data[0][0:2] == "98":
                    expected_main_procurement_category = "services"
                else:
                    ValueError("Check your tender.classification.id")

                self.__expected_fa_release['releases'][0]['tender']['mainProcurementCategory'] = \
                    expected_main_procurement_category
            except KeyError:
                KeyError("Could not parse tender.classification.id.")
        else:
            self.__expected_fa_release['releases'][0]['tender']['classification']['id'] = \
                self.__previous_fa_release['releases'][0]['tender']['classification']['id']
            self.__expected_fa_release['releases'][0]['tender']['classification']['scheme'] = \
                self.__previous_fa_release['releases'][0]['tender']['classification']['scheme']
            self.__expected_fa_release['releases'][0]['tender']['classification']['description'] = \
                self.__previous_fa_release['releases'][0]['tender']['classification']['description']

        if "value" in self.__payload['tender']:
            self.__expected_fa_release['releases'][0]['tender']['value']['currency'] = \
                self.__payload['tender']['value']['currency']
        else:
            self.__expected_fa_release['releases'][0]['tender']['value']['currency'] = \
                self.__previous_fa_release['releases'][0]['tender']['value']['currency']

        if "procurementMethodRationale" in self.__payload['tender']:
            self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale'] = \
                self.__payload['tender']['procurementMethodRationale']
        else:
            del self.__expected_fa_release['releases'][0]['tender']['procurementMethodRationale']

        return self.__expected_fa_release
