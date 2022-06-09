"""Prepare the expected payload of the create confirmation response, framework agreement procedures."""
import copy
import random

from class_collection.document_registration import Document
from data_collection.data_constant import confirmationResponse_type, business_function_type_3_tuple
from functions_collection.prepare_date import old_period


class CreateConfirmationResponsePayload:
    """This class creates instance of payload."""

    def __init__(self, environment, host_to_service, request_id):
        metadata_document_url = None
        self.__document_one = Document(host=host_to_service)
        document_one_was_uploaded = self.__document_one.uploading_document()
        try:
            if environment == "dev":
                metadata_document_url = "https://dev.bpe.eprocurement.systems/api/v1/storage/get"

            elif environment == "sandbox":
                metadata_document_url = "http://storage.eprocurement.systems/get"
        except ValueError:
            ValueError("Check your environment: You must use 'dev' or 'sandbox' environment in pytest command")

        confirmationresponse_type = f"{random.choice(confirmationResponse_type)}"
        confirmationresponse_value = None
        if confirmationresponse_type == "document":
            confirmationresponse_value = f"{metadata_document_url}/{document_one_was_uploaded[0]['data']['id']}"
        elif confirmationresponse_type == "hash":
            confirmationresponse_value = document_one_was_uploaded[2]

        self.__payload = {
            "confirmationResponse": {
                "requestId": request_id,
                "type": confirmationresponse_type,
                "value": confirmationresponse_value,
                "relatedPerson": {
                    "title": "create confirmation response: confirmationResponse.relatedPerson.title",
                    "name": "create confirmation response: confirmationResponse.relatedPerson.name",
                    "identifier": {
                        "scheme": "create confirmation response: confirmationResponse.relatedPerson.identifier.scheme",
                        "id": "create confirmation response: confirmationResponse.relatedPerson.identifier.id",
                        "uri": "create confirmation response: confirmationResponse.relatedPerson.identifier.uri",
                    },
                    "businessFunctions": [
                        {
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
                            ],
                            "id": ""
                        }
                    ]
                }
            }
        }

    def build_payload(self):
        """Build payload."""
        return self.__payload

    def delete_optional_fields(self, *args, bf_position, bf_doc_position):
        """Delete optional fields from payload."""
        for a in args:
            if a == "confirmationResponse.relatedPerson.identifier.uri":
                del self.__payload['confirmationResponse']['relatedPerson']['identifier']['uri']
            elif a == "confirmationResponse.relatedPerson.businessFunctions.documents":
                del self.__payload['confirmationResponse']['relatedPerson'][
                    'businessFunctions'][bf_position]['documents']
            elif a == "confirmationResponse.relatedPerson.businessFunctions.documents.description":
                del self.__payload['confirmationResponse']['relatedPerson'][
                    'businessFunctions'][bf_position]['documents'][bf_doc_position]['description']
            else:
                KeyError(f"Impossible to delete attribute by path {a}.")

    def customize_business_functions(self, quantity_of_bf, quantity_of_bf_documents):
        business_functions = list()
        for q_0 in range(quantity_of_bf):
            business_functions.append(copy.deepcopy(
                self.__payload['confirmationResponse']['relatedPerson']['businessFunctions'][0]
            ))
            business_functions[q_0]['id'] = f"{q_0}"
            business_functions[q_0]['type'] = f"{random.choice(business_function_type_3_tuple)}"
            business_functions[q_0]['jobTitle'] = \
                f"create confirmation response: confirmationResponse.relatedPerson.businessFunctions[{0}].jobTitle"
            business_functions[q_0]['period']['startDate'] = old_period()[0]
            del business_functions[q_0]['documents'][0]
            bf_documents = list()
            for q_1 in range(quantity_of_bf_documents):
                bf_documents.append(copy.deepcopy(
                    self.__payload['confirmationResponse']['relatedPerson']['businessFunctions'][0]['documents'][0]
                ))

                some_document_was_uploaded = self.__document_one.uploading_document()
                bf_documents[q_1]['id'] = some_document_was_uploaded[0]["data"]["id"]
                bf_documents[q_1]['documentType'] = "regulatoryDocument"

                bf_documents[q_1]['title'] = f"create confirmation response: confirmationResponse.relatedPerson." \
                                             f"businessFunctions[{0}].documents[{q_1}.title"

                bf_documents[q_1]['description'] = f"create confirmation response: confirmationResponse." \
                                                   f"relatedPerson.businessFunctions[{0}].documents[{q_1}.description"

            business_functions[q_0]['documents'] = bf_documents
        self.__payload['confirmationResponse']['relatedPerson']['businessFunctions'] = business_functions

    def __del__(self):
        print(f"The instance of IssuingFrameworkPayload class: {__name__} was deleted.")
