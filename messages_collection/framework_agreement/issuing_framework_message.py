""" Prepare expected message for platform, the Issuing Framework process of Framework Agreement procedure."""
import copy
import fnmatch

from functions_collection.some_functions import is_it_uuid


class IssuingFrameworkMessage:
    """ Class creates instance of message for platform."""

    def __init__(self, environment, cpid, ocid, test_mode=False):

        self.__environment = environment
        self.__cpid = cpid
        self.__ocid = ocid
        self.__test_mode = test_mode

        if environment == "dev":
            self.tender_url = "http://dev.public.eprocurement.systems/tenders"
        elif environment == "sandbox":
            self.tender_url = "http://public.eprocurement.systems/tenders"

        self.__platform_message = {
            "X-OPERATION-ID": "",
            "X-RESPONSE-ID": "",
            "initiator": "",
            "data": {
                "ocid": "",
                "url": "",
                "operationDate": ""
            }
        }

        self.__bpe_message = {
            "X-OPERATION-ID": "",
            "X-RESPONSE-ID": "",
            "initiator": "",
            "data": {
                "ocid": "",
                "url": "",
                "operationDate": "",
                "outcomes": {
                    "requests": [
                        {
                            "id": "",
                            "X-TOKEN": ""
                        }
                    ]
                }
            }
        }

    def build_expected_platform_message(self, actual_message):
        """Build the message."""

        if "X-OPERATION-ID" in actual_message:
            is_operation_id_correct = is_it_uuid(actual_message['X-OPERATION-ID'])

            if is_operation_id_correct is True:
                self.__platform_message['X-OPERATION-ID'] = actual_message['X-OPERATION-ID']
            else:
                ValueError("The message is not correct: 'X-OPERATION-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-OPERATION-ID'.")

        if "X-RESPONSE-ID" in actual_message:
            is_process_id_correct = is_it_uuid(actual_message['X-RESPONSE-ID'])

            if is_process_id_correct is True:
                self.__platform_message['X-RESPONSE-ID'] = actual_message['X-RESPONSE-ID']
            else:
                ValueError("The message is not correct: 'X-RESPONSE-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-RESPONSE-ID'.")

        if "initiator" in actual_message:
            self.__platform_message['initiator'] = "platform"
        else:
            KeyError("The message is not correct: mismatch key 'initiator'.")

        if "ocid" in actual_message['data']:
            self.__platform_message['data']['ocid'] = self.__ocid
        else:
            KeyError("The message is not correct: mismatch key 'data.ocid'.")

        if "url" in actual_message['data']:
            self.__platform_message['data']['url'] = f"{self.tender_url}/{self.__cpid}/{self.__ocid}"
        else:
            KeyError("The message is not correct: mismatch key 'data.url'.")

        if "operationDate" in actual_message['data']:
            is_date_correct = fnmatch.fnmatch(actual_message["data"]["operationDate"], "202*-*-*T*:*:*Z")

            if is_date_correct is True:
                self.__platform_message['data']['operationDate'] = actual_message['data']['operationDate']
            else:
                ValueError("The message is not correct: 'data.operationDate'.")
        else:
            KeyError("The message is not correct: mismatch key 'data.operationDate'.")

        return self.__platform_message

    def build_expected_bpe_message(self, actual_message, expected_quantity_of_outcomes_requests):
        """Build the message."""

        if "X-OPERATION-ID" in actual_message:
            is_operation_id_correct = is_it_uuid(actual_message['X-OPERATION-ID'])

            if is_operation_id_correct is True:
                self.__bpe_message['X-OPERATION-ID'] = actual_message['X-OPERATION-ID']
            else:
                ValueError("The message is not correct: 'X-OPERATION-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-OPERATION-ID'.")

        if "X-RESPONSE-ID" in actual_message:
            is_process_id_correct = is_it_uuid(actual_message['X-RESPONSE-ID'])

            if is_process_id_correct is True:
                self.__bpe_message['X-RESPONSE-ID'] = actual_message['X-RESPONSE-ID']
            else:
                ValueError("The message is not correct: 'X-RESPONSE-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-RESPONSE-ID'.")

        if "initiator" in actual_message:
            self.__bpe_message['initiator'] = "bpe"
        else:
            KeyError("The message is not correct: mismatch key 'initiator'.")

        if "ocid" in actual_message['data']:
            self.__bpe_message['data']['ocid'] = self.__ocid
        else:
            KeyError("The message is not correct: mismatch key 'data.ocid'.")

        if "url" in actual_message['data']:
            self.__bpe_message['data']['url'] = f"{self.tender_url}/{self.__cpid}/{self.__ocid}"
        else:
            KeyError("The message is not correct: mismatch key 'data.url'.")

        if "operationDate" in actual_message['data']:
            is_date_correct = fnmatch.fnmatch(actual_message["data"]["operationDate"], "202*-*-*T*:*:*Z")

            if is_date_correct is True:
                self.__bpe_message['data']['operationDate'] = actual_message['data']['operationDate']
            else:
                ValueError("The message is not correct: 'data.operationDate'.")
        else:
            KeyError("The message is not correct: mismatch key 'data.operationDate'.")

        outcomes_requests_array = list()
        for obj in range(expected_quantity_of_outcomes_requests):
            outcomes_requests_array.append(copy.deepcopy(self.__bpe_message['data']['outcomes']['requests'][0]))

            is_requests_id_correct = is_it_uuid(actual_message["data"]["outcomes"]["requests"][obj]["id"])

            if is_requests_id_correct is True:
                outcomes_requests_array[obj]['id'] = actual_message["data"]["outcomes"]["requests"][obj]["id"]
            else:
                ValueError("The message is not correct: 'data.outcomes.requests.id'.")

            is_requests_token_correct = is_it_uuid(actual_message["data"]["outcomes"]["requests"][obj]["X-TOKEN"])

            if is_requests_token_correct is True:
                outcomes_requests_array[obj]['X-TOKEN'] = actual_message["data"]["outcomes"]["requests"][obj]["X-TOKEN"]
            else:
                ValueError("The message is not correct: 'data.outcomes.requests.X-TOKEN'.")

        self.__bpe_message['data']['outcomes']['requests'] = outcomes_requests_array
        return self.__bpe_message
