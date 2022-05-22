"""Prepare the expected payloads of the amend framework establishment process, framework agreement procedures."""
import copy
import random

from class_collection.document_registration import Document
from data_collection.data_constant import person_title_tuple, business_function_type_2_tuple, documentType_tuple
from functions_collection.prepare_date import old_period, pre_qualification_period_end_date


class AmendFrameworkEstablishmentPayload:
    """This class creates instance of payload."""

    def __init__(self, ap_payload, create_fe_payload, previous_fe_release, host_to_service, country, language,
                 environment, person_title=None, business_functions_type=None, tender_documents_type=None,
                 pre_qualification_sec=960):

        __document_one = Document(host=host_to_service)
        self.__document_one_was_uploaded = __document_one.uploading_document()
        self.__document_two_was_uploaded = __document_one.uploading_document()
        self.__host = host_to_service

        self.__businessFunctions_period_startDate = old_period()[0]
        self.__requirements_period = old_period()

        self.__country = country
        self.__language = language
        self.__environment = environment

        self.__ap_payload = copy.deepcopy(ap_payload)
        self.__create_fe_payload = copy.deepcopy(create_fe_payload)
        self.__previous_fe_release = copy.deepcopy(previous_fe_release)

        for q_0 in range(len(self.__previous_fe_release['releases'][0]['parties'])):
            if "procuringEntity" in self.__create_fe_payload['tender']:
                if self.__create_fe_payload['tender']['procuringEntity']['id'] == \
                        self.__previous_fe_release['releases'][0]['parties'][q_0]['id']:

                    for q_1 in range(len(self.__previous_fe_release['releases'][0]['parties'][q_0]['persones'])):

                        del self.__previous_fe_release['releases'][0]['parties'][q_0]['persones'][q_1]['id']

                        for q_2 in range(len(
                                self.__previous_fe_release['releases'][0]['parties'][q_0]['persones'][q_1][
                                    'businessFunctions']
                        )):
                            for q_3 in range(len(
                                    self.__previous_fe_release['releases'][0]['parties'][q_0]['persones'][q_1][
                                        'businessFunctions'][q_2]['documents']
                            )):
                                del self.__previous_fe_release['releases'][0]['parties'][q_0]['persones'][q_1][
                                    'businessFunctions'][q_2]['documents'][q_3]['url']

                                del self.__previous_fe_release['releases'][0]['parties'][q_0]['persones'][q_1][
                                    'businessFunctions'][q_2]['documents'][q_3]['datePublished']

                    self.__old_persones_array = self.__previous_fe_release['releases'][0]['parties'][q_0]['persones']

        if person_title is None:
            self.__person_title = f"{random.choice(person_title_tuple)}"
        else:
            self.__person_title = person_title

        if business_functions_type is None:
            self.__businessFunctions_type = f"{random.choice(business_function_type_2_tuple)}"
        else:
            self.__businessFunctions_type = business_functions_type

        if tender_documents_type is None:
            self.__tender_documents_type = f"{random.choice(documentType_tuple)}"
        else:
            self.__tender_documents_type = tender_documents_type

        self.__payload = {
            "preQualification": {
                "period": {
                    "endDate": pre_qualification_period_end_date(pre_qualification_sec)
                }
            },
            "tender": {
                "procuringEntity": {
                    "id": f"{ap_payload['tender']['procuringEntity']['identifier']['scheme']}-"
                          f"{ap_payload['tender']['procuringEntity']['identifier']['id']}",
                    "persones": [{
                        "title": self.__person_title,
                        "name": "amend fe: tender.procuringEntity.persones[0].name",
                        "identifier": {
                            "scheme": "MD-IDNO",
                            "id": "amend fe: tender.procuringEntity.persones[0].identifier.id",
                            "uri": "amend fe: tender.procuringEntity.persones[0].identifier.uri"
                        },
                        "businessFunctions": [{
                            "id": "0",
                            "type": self.__businessFunctions_type,
                            "jobTitle": "amend fe: tender.procuringEntity.persones[0].businessFunctions[0].jobTitle",
                            "period": {
                                "startDate": self.__businessFunctions_period_startDate
                            },
                            "documents": [{
                                "id": self.__document_one_was_uploaded[0]["data"]["id"],
                                "documentType": "regulatoryDocument",

                                "title": "amend fe: tender.procuringEntity.persones[0].businessFunctions[0]."
                                         "documents[0].title",

                                "description": "amend fe: tender.procuringEntity.persones[0].businessFunctions[0]."
                                               "documents[0].description"
                            }]
                        }]
                    }]

                },
                "documents":  [{
                    "documentType": self.__tender_documents_type,
                    "id": self.__document_one_was_uploaded[0]['data']['id'],
                    "title": "amend fe: tender.document[0].title",
                    "description": "amend fe: tender.document[0].description"
                }],
                "procurementMethodRationale": "amend fe: tender.procurementMethodRationale"
            }
        }

    def build_payload(self):
        """Build payload."""
        return self.__payload

    def delete_optional_fields(
            self, *args, person_position=0,
            business_functions_position=0,
            bf_documents_position=0,
            tender_documents_position=0):
        """Delete optional fields from payload."""

        for a in args:
            if a == "tender.procuringEntity":
                del self.__payload['tender']['procuringEntity']

            elif a == "tender.procuringEntity.persones.identifier.uri":
                del self.__payload['tender']['procuringEntity'][
                    'persones'][person_position]['identifier']['uri']

            elif a == "tender.procuringEntity.persones.businessFunctions.documents":
                del self.__payload['tender']['procuringEntity'][
                    'persones'][person_position]['businessFunctions'][business_functions_position]['documents']

            elif a == "tender.procuringEntity.persones.businessFunctions.documents.description":
                del self.__payload['tender']['procuringEntity'][
                    'persones'][person_position]['businessFunctions'][business_functions_position][
                    'documents'][bf_documents_position]['description']

            elif a == "tender.documents":
                del self.__payload['tender']['documents']

            elif a == "tender.documents.description":
                del self.__payload['tender']['documents'][tender_documents_position]['description']

            elif a == "tender.procurementMethodRationale":
                del self.__payload['tender']['procurementMethodRationale']

            else:
                raise KeyError(f"Impossible to delete attribute by path {a}.")

    def customize_old_persones(
            self, *list_of_person_id_to_change,
            need_to_add_new_bf, quantity_of_new_bf_objects, need_to_add_new_document,
            quantity_of_new_documents_objects):
        """Customize old persones. Call this method before 'add_new_persones'."""

        for a in list_of_person_id_to_change:
            for p in range(len(self.__old_persones_array)):

                if a == f"{self.__old_persones_array[p]['identifier']['scheme']}-" \
                        f"{self.__old_persones_array[p]['identifier']['id']}":

                    persones_object = copy.deepcopy(self.__payload['tender']['procuringEntity']['persones'][0])

                    persones_object['title'] = self.__person_title
                    persones_object['name'] = f"amend fe: new value for old person, " \
                                              f"tender.procuringEntity.persones[{p}].name"

                    persones_object['identifier']['scheme'] = self.__old_persones_array[p]['identifier']['scheme']
                    persones_object['identifier']['id'] = self.__old_persones_array[p]['identifier']['id']

                    persones_object['identifier']['uri'] = \
                        f"amend fe: new value for old person, tender.procuringEntity.persones[{p}].identifier.uri"

                    business_functions_array = list()
                    for q_0 in range(len(self.__old_persones_array[p]['businessFunctions'])):

                        business_functions_array.append(copy.deepcopy(
                            self.__payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0]
                        ))

                        business_functions_array[q_0]['id'] = \
                            self.__old_persones_array[p]['businessFunctions'][q_0]['id']

                        business_functions_array[q_0]['type'] = self.__businessFunctions_type

                        business_functions_array[q_0]['jobTitle'] = \
                            f"amend fe: new value for old person, tender.procuringEntity.persones[{p}]." \
                            f"businessFunctions[{q_0}].jobTitle"

                        business_functions_array[q_0]['period']['startDate'] = old_period()[0]

                        documents_array = list()
                        if "documents" in self.__old_persones_array[p]['businessFunctions'][q_0]:
                            for q_1 in range(len(self.__old_persones_array[p]['businessFunctions'][q_0]['documents'])):
                                documents_array.append(copy.deepcopy(
                                    self.__payload['tender']['procuringEntity']['persones'][0][
                                        'businessFunctions'][0]['documents'][0]
                                ))
                                documents_array[q_1]['id'] = \
                                    self.__old_persones_array[p]['businessFunctions'][q_0]['documents'][q_1]['id']

                                documents_array[q_1]['documentType'] = "regulatoryDocument"

                                documents_array[q_1]['title'] = \
                                    f"amend fe: new value for old person, tender.procuringEntity.persones[{p}]." \
                                    f"businessFunctions[{q_0}].documents[{q_1}].title"

                                documents_array[q_1]['description'] = \
                                    f"amend fe: new value for old person, tender.procuringEntity.persones[{p}]." \
                                    f"businessFunctions[{q_0}].documents[{q_1}].description"

                        if need_to_add_new_document is True:
                            new_documents_array = list()
                            for n_1 in range(quantity_of_new_documents_objects):

                                new_documents_array.append(copy.deepcopy(
                                    self.__payload['tender']['procuringEntity']['persones'][0][
                                        'businessFunctions'][0]['documents'][0]
                                ))

                                document_two = Document(host=self.__host)
                                document_two_was_uploaded = document_two.uploading_document()

                                new_documents_array[n_1]['id'] = document_two_was_uploaded[0]["data"]["id"]

                                new_documents_array[n_1]['documentType'] = "regulatoryDocument"

                                new_documents_array[n_1]['title'] = \
                                    f"amend fe: new object, tender.procuringEntity.persones[{p}]." \
                                    f"['businessFunctions'][{q_0}].documents[{n_1}.title"

                                new_documents_array[n_1]['description'] = \
                                    f"amend fe: new object, tender.procuringEntity.persones[{p}]." \
                                    f"['businessFunctions'][{q_0}].documents[{n_1}.description"

                            documents_array += new_documents_array

                        business_functions_array[q_0]['documents'] = documents_array

                    if need_to_add_new_bf is True:
                        new_business_functions_array = list()
                        for n_0 in range(quantity_of_new_bf_objects):

                            new_business_functions_array.append(copy.deepcopy(
                                self.__payload['tender']['procuringEntity']['persones'][0][
                                    'businessFunctions'][0]
                            ))

                            new_business_functions_array[n_0]['id'] = f"{len(business_functions_array)+ n_0}"

                            new_business_functions_array[n_0]['type'] = self.__businessFunctions_type

                            new_business_functions_array[n_0]['jobTitle'] = \
                                f"amend fe: new object, tender.procuringEntity.persones[{p}]." \
                                f"['businessFunctions'][{n_0}].jobTitle"

                            new_business_functions_array[n_0]['period']['startDate'] = \
                                self.__businessFunctions_period_startDate

                            new_business_functions_array[n_0]['documents'] = list()
                            for d in range(quantity_of_new_documents_objects):
                                new_business_functions_array[n_0]['documents'].append(copy.deepcopy(
                                    self.__payload['tender']['procuringEntity']['persones'][0][
                                        'businessFunctions'][0]['documents'][0]
                                ))

                                document_three = Document(host=self.__host)
                                document_three_was_uploaded = document_three.uploading_document()

                                new_business_functions_array[n_0]['documents'][d]['id'] = \
                                    document_three_was_uploaded[0]["data"]["id"]

                                new_business_functions_array[n_0]['documents'][d]['documentType'] = "regulatoryDocument"

                                new_business_functions_array[n_0]['documents'][d]['title'] = \
                                    f"amend fe: new object, tender.procuringEntity.persones[{p}]." \
                                    f"['businessFunctions'][{n_0}].documents[{d}.title"

                                new_business_functions_array[n_0]['documents'][d]['description'] = \
                                    f"amend fe: new object, tender.procuringEntity.persones[{p}]." \
                                    f"['businessFunctions'][{n_0}].documents[{d}.description"

                        business_functions_array += new_business_functions_array

                    persones_object['businessFunctions'] = business_functions_array

                    self.__old_persones_array[p] = persones_object

            self.__payload['tender']['procuringEntity']['persones'] = self.__old_persones_array

    def add_new_persones(
            self, quantity_of_persones_objects, quantity_of_bf_objects, quantity_of_documents_objects):
        """Add new oblects to tender.procuringEntity.persones array."""

        new_persones_array = list()
        for q_0 in range(quantity_of_persones_objects):
            new_persones_array.append(copy.deepcopy(
                self.__payload['tender']['procuringEntity']['persones'][0]
            ))

            new_persones_array[q_0]['title'] = self.__person_title
            new_persones_array[q_0]['name'] = f"amend fe: tender.procuringEntity.persones[{q_0}].name"
            new_persones_array[q_0]['identifier']['scheme'] = "MD-IDNO"
            new_persones_array[q_0]['identifier']['id'] = f"amend fe: tender.procuringEntity.persones[{q_0}].id"
            new_persones_array[q_0]['identifier']['uri'] = f"amend fe: tender.procuringEntity.persones[{q_0}].uri"

            new_persones_array[q_0]['businessFunctions'] = list()
            for q_1 in range(quantity_of_bf_objects):

                new_persones_array[q_0]['businessFunctions'].append(copy.deepcopy(
                    self.__payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0])
                )

                new_persones_array[q_0]['businessFunctions'][q_1]['id'] = f"{q_1}"

                new_persones_array[q_0]['businessFunctions'][q_1]['type'] = self.__businessFunctions_type

                new_persones_array[q_0]['businessFunctions'][q_1]['jobTitle'] = \
                    f"amend fe: tender.procuringEntity.persones[{q_0}].['businessFunctions'][{q_1}].jobTitle"

                new_persones_array[q_0]['businessFunctions'][q_1]['period']['startDate'] = \
                    self.__businessFunctions_period_startDate

                new_persones_array[q_0]['businessFunctions'][q_1]['documents'] = list()
                for q_2 in range(quantity_of_documents_objects):
                    new_persones_array[q_0]['businessFunctions'][q_1]['documents'].append(copy.deepcopy(
                        self.__payload['tender']['procuringEntity']['persones'][0]['businessFunctions'][0][
                            'documents'][0])
                    )

                    document_three = Document(host=self.__host)
                    document_three_was_uploaded = document_three.uploading_document()

                    new_persones_array[q_0]['businessFunctions'][q_1]['documents'][q_2]['id'] = \
                        document_three_was_uploaded[0]["data"]["id"]

                    new_persones_array[q_0]['businessFunctions'][q_1]['documents'][q_2]['documentType'] = \
                        "regulatoryDocument"

                    new_persones_array[q_0]['businessFunctions'][q_1]['documents'][q_2]['title'] = \
                        f"amend fe: tender.procuringEntity.persones[{q_0}].['businessFunctions'][{q_1}]." \
                        f"documents[{q_2}.title"

                    new_persones_array[q_0]['businessFunctions'][q_1]['documents'][q_2]['description'] = \
                        f"amend fe: tender.procuringEntity.persones[{q_0}].['businessFunctions'][{q_1}]." \
                        f"documents[{q_2}.description"

        self.__payload['tender']['procuringEntity']['persones'] += new_persones_array

    def customize_old_tender_documents(self, *list_of_documents_id_to_change):
        """Customize old documents. Call this method before 'add_new_documents'."""
        documents_array = list()
        for a in list_of_documents_id_to_change:
            for d in range(len(self.__previous_fe_release['releases'][0]['tender']['documents'])):
                if a == self.__previous_fe_release['releases'][0]['tender']['documents'][d]['id']:
                    documents_object = copy.deepcopy(self.__payload['tender']['documents'][0])

                    documents_object['id'] = self.__previous_fe_release['releases'][0]['tender']['documents'][d]['id']
                    documents_object['documentType'] = self.__tender_documents_type
                    documents_object['title'] = f"amend fe: new value for old object, tender.documents[{d}].title"

                    documents_object['description'] = \
                        f"amend fe: new value for old object, tender.documents[{d}].description"

                    documents_array.append(documents_object)
        self.__payload['tender']['documents'] = documents_array

    def add_new_tender_documents(self, quantity_of_new_documents):
        """Add new documents to the 'tender' object."""

        new_documents_array = list()
        for q_0 in range(quantity_of_new_documents):
            new_documents_array.append(copy.deepcopy(self.__payload['tender']['documents'][0]))

            document_four = Document(host=self.__host)
            document_four_was_uploaded = document_four.uploading_document()

            new_documents_array[q_0]['id'] = document_four_was_uploaded[0]["data"]["id"]
            new_documents_array[q_0]['documentType'] = self.__tender_documents_type
            new_documents_array[q_0]['title'] = f"amend fe: new object, tender.documents{q_0}.title"
            new_documents_array[q_0]['description'] = f"amend fe: new object, tender.documents{q_0}.description"

        self.__payload['tender']['documents'] += new_documents_array

    def __del__(self):
        print(f"The instance of AmendFrameworkEstablishmentPayload class: {__name__} was deleted.")
