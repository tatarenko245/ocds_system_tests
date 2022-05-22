"""Prepare the expected payloads of the create qualification declare non conflict of interest,
framework agreement procedures."""
import copy
import random
import uuid

from class_collection.document_registration import Document
from data_collection.data_constant import business_function_type_2_tuple, person_title_tuple
from functions_collection.prepare_date import old_period


class QualificationDeclareNonConflictOfInterestPayload:
    """This class creates instance of payload."""

    def __init__(self, service_host, requirement_id, tenderer_id, value):

        self.__host = service_host
        self.__document = Document(self.__host)

        self.__payload = {
            "requirementResponse": {
                "id": str(uuid.uuid4()),
                "value": value,
                "relatedTenderer": {
                    "id": tenderer_id
                },
                "responder": {
                    "title": "",
                    "name": "qualification declare: requirementResponse.responder.name",
                    "identifier": {
                        "scheme": "qualification declare: requirementResponse.responder.identifier.scheme",
                        "id": "qualification declare: requirementResponse.responder.identifier.id",
                        "uri": "qualification declare: requirementResponse.responder.identifier.uri"
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
                                    "description": ""
                                }
                            ]
                        }
                    ]
                },
                "requirement": {
                    "id": requirement_id
                }
            }
        }

    def build_payload(self):
        """Build payload."""
        self.__payload['requirementResponse']['responder']['title'] = f"{random.choice(person_title_tuple)}"
        return self.__payload

    def delete_optional_fields(
            self, *args, bf_position=0, bf_doc_position=0):
        """Call this method LAST! Delete optional fields from payload."""
        for a in args:
            if a == "requirementResponse":
                del self.__payload['requirementResponse']
            elif a == "requirementResponse.responder.identifier.uri":
                del self.__payload['requirementResponse']['responder']['identifier']['uri']
            elif a == "requirementResponse.responder.businessFunctions.documents":
                del self.__payload['requirementResponse']['responder']['businessFunctions'][bf_position]['documents']
            elif a == "requirementResponse.responder.businessFunctions.documents.description":
                del self.__payload['requirementResponse']['responder']['businessFunctions'][bf_position][
                    'documents'][bf_doc_position]['description']
            else:
                KeyError(f"Impossible to delete attribute by path {a}.")

    def customize_business_functions(self, quantity_of_bf, quantity_of_bf_documents):
        business_functions = list()
        for q_0 in range(quantity_of_bf):
            business_functions.append(copy.deepcopy(
                self.__payload['requirementResponse']['responder']['businessFunctions'][0]
            ))
            business_functions[q_0]['id'] = f"{q_0}"
            business_functions[q_0]['type'] = f"{random.choice(business_function_type_2_tuple)}"
            business_functions[q_0]['jobTitle'] = \
                f"qualification declare: requirementResponse.responder.businessFunctions[{q_0}]['jobTitle']"
            business_functions[q_0]['period']['startDate'] = old_period()[0]
            del business_functions[q_0]['documents'][0]
            bf_documents = list()
            for q_1 in range(quantity_of_bf_documents):
                bf_documents.append(copy.deepcopy(
                    self.__payload['requirementResponse']['responder']['businessFunctions'][0]['documents'][0]
                ))

                some_document_was_uploaded = self.__document.uploading_document()
                bf_documents[q_1]['id'] = some_document_was_uploaded[0]["data"]["id"]
                bf_documents[q_1]['documentType'] = "regulatoryDocument"
                bf_documents[q_1]['title'] = f"qualification declare: requirementResponse.responder." \
                                             f"businessFunctions[{q_0}].documents[{q_1}.title"
                bf_documents[q_1]['description'] = f"qualification declare: requirementResponse.responder." \
                                                   f"businessFunctions[{q_0}].documents[{q_1}.description"

            business_functions[q_0]['documents'] = bf_documents
        self.__payload['requirementResponse']['responder']['businessFunctions'] = business_functions

    def __del__(self):
        print(f"The instance of QualificationDeclareNonConflictOfInterestPayload class: {__name__} was deleted.")
