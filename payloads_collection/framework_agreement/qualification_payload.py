"""Prepare the expected payloads of the qualification, framework agreement procedures."""
import copy
import random

from class_collection.document_registration import Document
from data_collection.data_constant import documentType_for_qualification_process


class QualificationPayload:
    """This class creates instance of payload."""

    def __init__(self, service_host):

        self.__host = service_host
        self.__document = Document(self.__host)

        self.__payload = {
            "qualification": {
                "statusDetails": "",
                "internalId": "qualification: qualification.internalId",
                "description": "qualification: qualification.description",
                "documents": [
                    {
                        "id": "",
                        "documentType": "",
                        "title": "",
                        "description": ""
                    }
                ]
            }
        }

    def build_payload(self, status):
        """Build payload."""
        self.__payload['qualification']['statusDetails'] = status
        return self.__payload

    def delete_optional_fields(
            self, *args, doc_position):
        """Call this method LAST! Delete optional fields from payload."""
        for a in args:
            if a == "qualification.internalId":
                del self.__payload['qualification']['internalId']
            elif a == "qualification.description":
                del self.__payload['qualification']['description']
            elif a == "qualification.documents":
                del self.__payload['qualification']['documents']
            elif a == f"qualification.documents[{doc_position}]":
                del self.__payload['qualification']['documents'][doc_position]
            elif a == f"qualification.documents[{doc_position}].description":
                del self.__payload['qualification']['documents'][doc_position]['description']
            else:
                KeyError(f"Impossible to delete attribute by path {a}.")

    def customize_qualification_documents(self, quantity_of_documents):
        """Customize qualification.documents array."""

        new_documents_array = list()
        for q_0 in range(quantity_of_documents):
            new_documents_array.append(copy.deepcopy(self.__payload['qualification']['documents'][0]))

            document_was_uploaded = self.__document.uploading_document()
            new_documents_array[q_0]['id'] = document_was_uploaded[0]["data"]["id"]
            new_documents_array[q_0]['documentType'] = f"{random.choice(documentType_for_qualification_process)}"
            new_documents_array[q_0]['title'] = f"qualification: qualification.documents{q_0}.title"
            new_documents_array[q_0]['description'] = f"qualification: qualification.documents{q_0}.description"

        self.__payload['qualification']['documents'] = new_documents_array

    def __del__(self):
        print(f"The instance of QualificationPayload class: {__name__} was deleted.")
