"""Prepare the expected releases of the framework establishment process, framework agreement procedures."""
import copy
import json

from functions_collection.cassandra_methods import fe_enquiry_period_end_date
from functions_collection.some_functions import is_it_uuid, get_value_from_country_csv, get_value_from_region_csv, \
    get_value_from_locality_csv


class AmendFrameworkEstablishmentRelease:
    """This class creates instance of release."""

    def __init__(self, environment, country, language, pmd, cpid, ocid, payload,
                 actual_message, previous_ap_release, previous_fe_release, actual_fe_release, previous_fa_release,
                 actual_fa_release):

        self.__country = country
        self.__language = language
        self.__pmd = pmd
        self.__cpid = cpid
        self.__ocid = ocid
        self.__payload = payload
        self.__actual_message = actual_message
        self.__previous_fe_release = previous_fe_release
        self.__actual_fe_release = actual_fe_release
        self.__previous_fa_release = previous_fa_release
        self.__actual_fa_release = actual_fa_release

        try:
            if environment == "dev":
                self.__metadata_document_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get"
            elif environment == "sandbox":
                self.__metadata_document_url = "http://storage.eprocurement.systems/get"
        except ValueError:
            ValueError("Check your environment: You must use 'dev' or 'sandbox' environment in pytest command")

        self.__expected_ap_release = previous_ap_release

        self.__expected_fe_release = {
            "uri": self.__previous_fe_release['uri'],

            "version": self.__previous_fe_release['version'],
            "extensions": self.__previous_fe_release['extensions'],
            "publisher": {
                "name": self.__previous_fe_release['publisher']['name'],
                "uri": self.__previous_fe_release['publisher']['uri']
            },
            "license": self.__previous_fe_release['license'],
            "publicationPolicy": self.__previous_fe_release['publicationPolicy'],
            "publishedDate": self.__previous_fe_release['publishedDate'],
            "releases": [
                {
                    "ocid": self.__previous_fe_release['releases'][0]['ocid'],
                    "id": f"{self.__ocid}-{self.__actual_fe_release['releases'][0]['id'][46:59]}",
                    "date": self.__actual_message['data']['operationDate'],
                    "tag": [
                        "tenderAmendment"
                    ],
                    "language": self.__previous_fe_release['releases'][0]['language'],
                    "initiationType": self.__previous_fe_release['releases'][0]['initiationType'],
                    "parties": [
                        {
                            "id": "",
                            "name": "",
                            "identifier": {
                                "scheme": "",
                                "id": "",
                                "legalName": "",
                                "uri": ""
                            },
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
                            },
                            "additionalIdentifiers": [
                                {
                                    "scheme": "",
                                    "id": "",
                                    "legalName": "",
                                    "uri": ""
                                }
                            ],
                            "contactPoint": {
                                "name": "",
                                "email": "",
                                "telephone": "",
                                "faxNumber": "",
                                "url": ""
                            },
                            "persones": [
                                {
                                    "id": "",
                                    "title": "",
                                    "name": "",
                                    "identifier": {
                                        "scheme": "",
                                        "id": "",
                                        "uri": ""
                                    },
                                    "businessFunctions": [
                                        {
                                            "id": "",
                                            "type": "",
                                            "jobTitle": "",
                                            "period": {
                                                "startDate": ""
                                            },
                                            "documents": [
                                                {
                                                    "id": "",
                                                    "documentType": "",
                                                    "title": "",
                                                    "description": "",
                                                    "url": "",
                                                    "datePublished": ""
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ],
                            "roles": [
                                ""
                            ]
                        }
                    ],
                    "tender": {
                        "id": "",
                        "status": "",
                        "statusDetails": "",
                        "criteria": [
                            {
                                "id": "",
                                "title": "",
                                "source": "",
                                "description": "",
                                "requirementGroups": [
                                    {
                                        "id": "",
                                        "description": "",
                                        "requirements": [
                                            {
                                                "id": "",
                                                "title": "",
                                                "dataType": "",
                                                "status": "",
                                                "datePublished": "",
                                                "description": "",
                                                "period": {
                                                    "startDate": "",
                                                    "endDate": ""
                                                },
                                                "eligibleEvidences": [
                                                    {
                                                        "id": "",
                                                        "title": "",
                                                        "type": "",
                                                        "description": "",
                                                        "relatedDocument": {
                                                            "id": ""
                                                        }
                                                    }
                                                ],
                                                "expectedValue": "",
                                                "minValue": "",
                                                "maxValue": ""
                                            }
                                        ]
                                    }
                                ],
                                "relatesTo": "",
                                "classification": {
                                    "scheme": "",
                                    "id": ""
                                }
                            }
                        ],
                        "otherCriteria": {
                            "reductionCriteria": "",
                            "qualificationSystemMethods": ""
                        },
                        "enquiryPeriod": {
                            "startDate": "",
                            "endDate": ""
                        },
                        "hasEnquiries": False,
                        "documents": [
                            {
                                "id": "",
                                "documentType": "",
                                "title": "",
                                "description": "",
                                "url": "",
                                "datePublished": ""
                            }
                        ],
                        "submissionMethod": [
                            ""
                        ],
                        "submissionMethodDetails": "",
                        "submissionMethodRationale": [
                            ""
                        ],
                        "requiresElectronicCatalogue": False,
                        "procurementMethodModalities": [""],
                        "secondStage": {
                            "minimumCandidates": 1,
                            "maximumCandidates": 2
                        }
                    },
                    "preQualification": {
                        "period": {
                            "startDate": "",
                            "endDate": ""
                        }
                    },
                    "hasPreviousNotice": False,
                    "purposeOfNotice": {
                        "isACallForCompetition": False
                    },
                    "relatedProcesses": [
                        {
                            "id": "",
                            "relationship": [
                                ""
                            ],
                            "scheme": "",
                            "identifier": "",
                            "uri": ""
                        }
                    ]
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
                    "id": f"{self.__ocid}-{self.__actual_fa_release['releases'][0]['id'][46:59]}",
                    "date": self.__actual_message['data']['operationDate'],
                    "tag": self.__previous_fa_release['releases'][0]['tag'],
                    "language": self.__previous_fa_release['releases'][0]['language'],
                    "initiationType": self.__previous_fa_release['releases'][0]['initiationType'],
                    "tender": {
                        "id": self.__previous_fa_release['releases'][0]['tender']['id'],
                        "title": self.__previous_fa_release['releases'][0]['tender']['title'],
                        "description": self.__previous_fa_release['releases'][0]['tender']['description'],
                        "status": "active",
                        "statusDetails": "establishment",
                        "value": {
                            "amount": self.__previous_fa_release['releases'][0]['tender']['value']['amount'],
                            "currency": self.__previous_fa_release['releases'][0]['tender']['value']['currency']
                        },
                        "procurementMethod": self.__previous_fa_release['releases'][0]['tender']['procurementMethod'],
                        "procurementMethodDetails": self.__previous_fa_release['releases'][0]['tender'][
                            'procurementMethodDetails'],
                        "procurementMethodRationale": "",
                        "mainProcurementCategory": self.__previous_fa_release['releases'][0]['tender'][
                            'mainProcurementCategory'],
                        "hasEnquiries": self.__previous_fa_release['releases'][0]['tender']['hasEnquiries'],
                        "eligibilityCriteria": self.__previous_fa_release['releases'][0]['tender'][
                            'eligibilityCriteria'],
                        "contractPeriod": {
                            "startDate": self.__previous_fa_release['releases'][0]['tender']['contractPeriod'][
                                'startDate'],
                            "endDate": self.__previous_fa_release['releases'][0]['tender']['contractPeriod'][
                                'endDate']
                        },
                        "procuringEntity": {
                            "id": "",
                            "name": ""
                        },
                        "acceleratedProcedure": {
                            "isAcceleratedProcedure": self.__previous_fa_release['releases'][0]['tender'][
                                'acceleratedProcedure']['isAcceleratedProcedure']
                        },
                        "classification": {
                            "scheme": self.__previous_fa_release['releases'][0]['tender']['classification']['scheme'],
                            "id": self.__previous_fa_release['releases'][0]['tender']['classification']['id'],
                            "description": self.__previous_fa_release['releases'][0]['tender']['classification'][
                                'description']
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
                    "relatedProcesses": [
                        {
                            "id": "",
                            "relationship": [
                                ""
                            ],
                            "scheme": "",
                            "identifier": "",
                            "uri": ""
                        }
                    ]
                }
            ]
        }

    def build_expected_ap_release(self):
        """Build AP release."""
        return self.__expected_ap_release

    def build_expected_fe_release(self):
        """Build FE release."""

        # Prepare 'parties' array, based on previous FE release.
        expected_persones_list = list()
        person_list = list()
        parties = self.__previous_fe_release['releases'][0]['parties']
        for q in range(len(parties)):
            if parties[q]['roles'][0] == "procuringEntity":
                person_list = (copy.deepcopy(parties[q]['persones']))
        # If some person preset into payload, then update person.
        if "procuringEntity" in self.__payload['tender']:
            expected_old_person = list()
            for rp in range(len(person_list)):
                for pp in range(len(self.__payload['tender']['procuringEntity']['persones'])):
                    p_person_id = \
                        f"{self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['scheme']}-" \
                        f"{self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['id']}"
                    if p_person_id == person_list[rp]['id']:
                        person_list[rp]['title'] = self.__payload['tender']['procuringEntity']['persones'][pp]['title']
                        person_list[rp]['name'] = self.__payload['tender']['procuringEntity']['persones'][pp]['name']
                        person_list[rp]['identifier']['scheme'] = \
                            self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['scheme']
                        person_list[rp]['identifier']['id'] = \
                            self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['id']
                        if "uri" in self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']:
                            person_list[rp]['identifier']['uri'] = \
                                self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['uri']
                        for rbf in range(len(person_list[rp]['businessFunctions'])):
                            for pbf in range(len(self.__payload['tender']['procuringEntity']['persones'][pp][
                                                     'businessFunctions'])):
                                if person_list[rp]['businessFunctions'][rbf]['id'] == \
                                        self.__payload['tender']['procuringEntity']['persones'][pp][
                                            'businessFunctions'][pbf]['id']:
                                    person_list[rp]['businessFunctions'][rbf]['type'] = self.__payload['tender'][
                                        'procuringEntity']['persones'][pp]['businessFunctions'][pbf]['type']
                                    person_list[rp]['businessFunctions'][rbf]['jobTitle'] = self.__payload['tender'][
                                        'procuringEntity']['persones'][pp]['businessFunctions'][pbf]['jobTitle']
                                    person_list[rp]['businessFunctions'][rbf]['period']['startDate'] = \
                                        self.__payload['tender']['procuringEntity']['persones'][pp][
                                            'businessFunctions'][pbf]['period']['startDate']
                                    if "documents" in person_list[rp]['businessFunctions'][rbf] and \
                                            "documents" in self.__payload['tender']['procuringEntity']['persones'][pp][
                                                            'businessFunctions'][pbf]:
                                        release_bf_doc_id = list()
                                        payload_bf_doc_id = list()
                                        for rbfd in range(len(person_list[rp]['businessFunctions'][rbf]['documents'])):
                                            for pbfd in range(
                                                    len(self.__payload['tender']['procuringEntity']['persones'][pp][
                                                            'businessFunctions'][pbf]['documents'])):
                                                release_bf_doc_id.append(
                                                    person_list[rp]['businessFunctions'][rbf]['documents'][rbfd]['id'])
                                                payload_bf_doc_id.append(
                                                    self.__payload['tender']['procuringEntity']['persones'][pp][
                                                        'businessFunctions'][pbf]['documents'][pbfd]['id']
                                                )
                                                if person_list[rp]['businessFunctions'][rbf][
                                                        'documents'][rbfd]['id'] == \
                                                        self.__payload['tender']['procuringEntity']['persones'][pp][
                                                            'businessFunctions'][pbf]['documents'][pbfd]['id']:
                                                    person_list[rp]['businessFunctions'][rbf][
                                                        'documents'][rbfd]['documentType'] = \
                                                        self.__payload['tender']['procuringEntity']['persones'][pp][
                                                            'businessFunctions'][pbf]['documents'][pbfd]['documentType']
                                                    person_list[rp]['businessFunctions'][rbf][
                                                        'documents'][rbfd]['title'] = \
                                                        self.__payload['tender']['procuringEntity']['persones'][pp][
                                                            'businessFunctions'][pbf]['documents'][pbfd]['title']
                                                    if "description" in self.__payload['tender'][
                                                            'procuringEntity']['persones'][pp][
                                                            'businessFunctions'][pbf]['documents'][pbfd]:
                                                        person_list[rp]['businessFunctions'][rbf][
                                                            'documents'][rbfd]['description'] = \
                                                            self.__payload['tender']['procuringEntity']['persones'][pp][
                                                                'businessFunctions'][pbf]['documents'][pbfd][
                                                                'description']
                                        release_bf_doc_id = list()
                                        for rbfd in range(len(person_list[rp]['businessFunctions'][rbf]['documents'])):
                                            release_bf_doc_id.append(
                                                person_list[rp]['businessFunctions'][rbf]['documents'][rbfd]['id'])
                                        payload_bf_doc_id = list()
                                        for pbfd in range(
                                                len(self.__payload['tender']['procuringEntity']['persones'][pp][
                                                        'businessFunctions'][pbf]['documents'])):
                                            payload_bf_doc_id.append(
                                                self.__payload['tender']['procuringEntity']['persones'][pp][
                                                    'businessFunctions'][pbf]['documents'][pbfd]['id']
                                            )
                                        diff_doc_id = list(set(payload_bf_doc_id) - set(release_bf_doc_id))
                                        for i in range(len(diff_doc_id)):
                                            for pbfd in range(
                                                    len(self.__payload['tender']['procuringEntity']['persones'][pp][
                                                            'businessFunctions'][pbf]['documents'])):
                                                if diff_doc_id[i] == self.__payload['tender'][
                                                    'procuringEntity']['persones'][pp][
                                                        'businessFunctions'][pbf]['documents'][pbfd]['id']:
                                                    new_bf_doc_obj = copy.deepcopy(
                                                        self.__expected_fe_release['releases'][0]['parties'][0][
                                                            'persones'][0]['businessFunctions'][0]['documents'][0]
                                                    )
                                                    new_bf_doc_obj['id'] = self.__payload['tender'][
                                                        'procuringEntity']['persones'][pp][
                                                        'businessFunctions'][pbf]['documents'][pbfd]['id']
                                                    new_bf_doc_obj['documentType'] = self.__payload['tender'][
                                                        'procuringEntity']['persones'][pp][
                                                        'businessFunctions'][pbf]['documents'][pbfd]['documentType']
                                                    new_bf_doc_obj['title'] = self.__payload['tender'][
                                                        'procuringEntity']['persones'][pp][
                                                        'businessFunctions'][pbf]['documents'][pbfd]['title']
                                                    if "description" in self.__payload['tender'][
                                                        'procuringEntity']['persones'][pp][
                                                            'businessFunctions'][pbf]['documents'][pbfd]:
                                                        new_bf_doc_obj['description'] = self.__payload['tender'][
                                                            'procuringEntity']['persones'][pp][
                                                            'businessFunctions'][pbf]['documents'][pbfd]['description']
                                                    else:
                                                        del new_bf_doc_obj['description']
                                                    new_bf_doc_obj['url'] = f"{self.__metadata_document_url}/" \
                                                                            f"{new_bf_doc_obj['id']}"
                                                    new_bf_doc_obj['datePublished'] = self.__actual_message[
                                                        'data']['operationDate']
                                                    person_list[rp]['businessFunctions'][rbf]['documents'].append(
                                                        new_bf_doc_obj)
                        release_bf_id = list()
                        for rbf in range(len(person_list[rp]['businessFunctions'])):
                            release_bf_id.append(
                                person_list[rp]['businessFunctions'][rbf]['id'])
                        payload_bf_id = list()
                        for pbf in range(
                                len(self.__payload['tender']['procuringEntity']['persones'][pp][
                                        'businessFunctions'])):
                            payload_bf_id.append(
                                self.__payload['tender']['procuringEntity']['persones'][pp][
                                    'businessFunctions'][pbf]['id']
                            )
                        diff_bf_id = list(set(payload_bf_id) - set(release_bf_id))
                        for i in range(len(diff_bf_id)):
                            for pbf in range(
                                    len(self.__payload['tender']['procuringEntity']['persones'][pp][
                                            'businessFunctions'])):
                                if diff_bf_id[i] == self.__payload['tender'][
                                    'procuringEntity']['persones'][pp][
                                        'businessFunctions'][pbf]['id']:
                                    new_bf_obj = copy.deepcopy(
                                        self.__expected_fe_release['releases'][0]['parties'][0][
                                            'persones'][0]['businessFunctions'][0]
                                    )
                                    new_bf_obj['id'] = self.__payload['tender']['procuringEntity']['persones'][pp][
                                        'businessFunctions'][pbf]['id']
                                    new_bf_obj['type'] = self.__payload['tender']['procuringEntity']['persones'][pp][
                                                            'businessFunctions'][pbf]['type']
                                    new_bf_obj['jobTitle'] = self.__payload['tender']['procuringEntity'][
                                        'persones'][pp]['businessFunctions'][pbf]['jobTitle']
                                    new_bf_obj['period']['startDate'] = self.__payload['tender']['procuringEntity'][
                                        'persones'][pp]['businessFunctions'][pbf]['period']['startDate']
                                    del new_bf_obj['documents'][0]
                                    if "documents" in self.__payload['tender']['procuringEntity'][
                                            'persones'][pp]['businessFunctions'][pbf]:
                                        for pbfd in range(
                                                len(self.__payload['tender']['procuringEntity']['persones'][pp][
                                                        'businessFunctions'][pbf]['documents'])):
                                            new_bf_doc_obj = copy.deepcopy(
                                                self.__expected_fe_release['releases'][0]['parties'][0][
                                                    'persones'][0]['businessFunctions'][0]['documents'][0]
                                            )
                                            new_bf_doc_obj['id'] = self.__payload['tender'][
                                                'procuringEntity']['persones'][pp][
                                                'businessFunctions'][pbf]['documents'][pbfd]['id']
                                            new_bf_doc_obj['documentType'] = self.__payload['tender'][
                                                'procuringEntity']['persones'][pp][
                                                'businessFunctions'][pbf]['documents'][pbfd]['documentType']
                                            new_bf_doc_obj['title'] = self.__payload['tender'][
                                                'procuringEntity']['persones'][pp][
                                                'businessFunctions'][pbf]['documents'][pbfd]['title']
                                            if "description" in self.__payload['tender'][
                                                'procuringEntity']['persones'][pp][
                                                    'businessFunctions'][pbf]['documents'][pbfd]:
                                                new_bf_doc_obj['description'] = self.__payload['tender'][
                                                    'procuringEntity']['persones'][pp][
                                                    'businessFunctions'][pbf]['documents'][pbfd]['description']
                                            else:
                                                del new_bf_doc_obj['description']
                                            new_bf_doc_obj['url'] = f"{self.__metadata_document_url}/" \
                                                                    f"{new_bf_doc_obj['id']}"
                                            new_bf_doc_obj['datePublished'] = self.__actual_message[
                                                'data']['operationDate']
                                            new_bf_obj['documents'].append(new_bf_doc_obj)
                                    person_list[rp]['businessFunctions'].append(new_bf_obj)
            expected_persones_list += person_list
            release_person_id = list()
            for rp in range(len(person_list)):
                release_person_id.append(person_list[rp]['id'])
            payload_person_id = list()
            for pp in range(
                    len(self.__payload['tender']['procuringEntity']['persones'])):
                p_person_id = \
                    f"{self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['scheme']}-" \
                    f"{self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['id']}"
                payload_person_id.append(p_person_id)
            dif_person_id = list(set(payload_person_id) - set(release_person_id))

            for i in range(len(dif_person_id)):
                for pp in range(
                        len(self.__payload['tender']['procuringEntity']['persones'])):
                    p_person_id = \
                        f"{self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['scheme']}-" \
                        f"{self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['id']}"
                    if dif_person_id[i] == p_person_id:
                        new_person_obj = copy.deepcopy(
                            self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0]
                        )
                        new_person_obj['id'] = p_person_id
                        new_person_obj['title'] = self.__payload['tender']['procuringEntity']['persones'][pp]['title']
                        new_person_obj['name'] = self.__payload['tender']['procuringEntity']['persones'][pp]['name']
                        new_person_obj['identifier']['scheme'] = \
                            self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['scheme']
                        new_person_obj['identifier']['id'] = \
                            self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['id']
                        if "uri" in self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']:
                            new_person_obj['identifier']['uri'] = \
                                self.__payload['tender']['procuringEntity']['persones'][pp]['identifier']['uri']
                        else:
                            del new_person_obj['identifier']['uri']
                        del new_person_obj['businessFunctions'][0]
                        for pbf in range(len(
                                self.__payload['tender']['procuringEntity']['persones'][pp]['businessFunctions']
                        )):
                            new_bf_obj = copy.deepcopy(
                                self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0][
                                    'businessFunctions'][0]
                            )
                            new_bf_obj['id'] = self.__payload['tender']['procuringEntity']['persones'][pp][
                                'businessFunctions'][pbf]['id']
                            new_bf_obj['type'] = self.__payload['tender']['procuringEntity']['persones'][pp][
                                'businessFunctions'][pbf]['type']
                            new_bf_obj['jobTitle'] = self.__payload['tender']['procuringEntity']['persones'][pp][
                                'businessFunctions'][pbf]['jobTitle']
                            new_bf_obj['period']['startDate'] = self.__payload['tender']['procuringEntity'][
                                'persones'][pp]['businessFunctions'][pbf]['period']['startDate']
                            del new_bf_obj['documents'][0]
                            if "documents" in self.__payload['tender']['procuringEntity'][
                                    'persones'][pp]['businessFunctions'][pbf]:
                                for pbfd in range(len(
                                        self.__payload['tender']['procuringEntity']['persones'][pp][
                                            'businessFunctions'][pbf]['documents']
                                )):
                                    new_bf_doc_obj = copy.deepcopy(
                                        self.__expected_fe_release['releases'][0]['parties'][0]['persones'][0][
                                            'businessFunctions'][0]['documents'][0]
                                    )
                                    new_bf_doc_obj['id'] = self.__payload['tender']['procuringEntity']['persones'][pp][
                                            'businessFunctions'][pbf]['documents'][pbfd]['id']
                                    new_bf_doc_obj['documentType'] = self.__payload['tender']['procuringEntity'][
                                        'persones'][pp]['businessFunctions'][pbf]['documents'][pbfd]['documentType']
                                    new_bf_doc_obj['title'] = self.__payload['tender']['procuringEntity'][
                                        'persones'][pp]['businessFunctions'][pbf]['documents'][pbfd]['title']
                                    if "description" in range(len(self.__payload['tender']['procuringEntity'][
                                            'persones'][pp]['businessFunctions'][pbf]['documents'][pbfd])):
                                        new_bf_doc_obj['description'] = self.__payload['tender']['procuringEntity'][
                                            'persones'][pp]['businessFunctions'][pbf]['documents'][pbfd]['description']
                                    else:
                                        del new_bf_doc_obj['description']
                                    new_bf_doc_obj['url'] = f"{self.__metadata_document_url}/{new_bf_doc_obj['id']}"
                                    new_bf_doc_obj['datePublished'] = self.__actual_message['data']['operationDate']
                                    new_bf_obj['documents'].append(new_bf_doc_obj)
                            else:
                                del new_bf_obj['documents']
                            new_person_obj['businessFunctions'].append(new_bf_obj)
                        expected_persones_list.append(new_person_obj)
            self.__expected_fe_release['releases'][0]['parties'] = self.__previous_fe_release['releases'][0]['parties']
            for q in range(len(self.__expected_fe_release['releases'][0]['parties'])):
                if self.__expected_fe_release['releases'][0]['parties'][q]['roles'][0] == "procuringEntity":
                    self.__expected_fe_release['releases'][0]['parties'][q]['persones'] = expected_persones_list
            # Sort objects into persones, businessFucntions, documents:
            # Set terminal id for 'persones[*].businessFucntions[*].id':
        else:
            self.__expected_fe_release['releases'][0]['parties'] = self.__previous_fe_release['releases'][0]['parties']
        return self.__expected_fe_release
