""" Prepare expected message for platform, the create expenditure item process of budget."""
import copy
import fnmatch

from functions_collection.some_functions import is_it_uuid


class ExpenditureItemMessage:
    """ Class creates instance of message for platform."""

    def __init__(self, environment, country, actual_message, expected_quantity_of_outcomes_ei=1, test_mode=False):
        self.environment = environment
        self.country = country
        self.actual_message = actual_message
        self.test_mode = test_mode
        self.expected_quantity_of_outcomes_ei = expected_quantity_of_outcomes_ei

        if environment == "dev":
            self.budget_url = "http://dev.public.eprocurement.systems/budgets"
        elif environment == "sandbox":
            self.budget_url = "http://public.eprocurement.systems/budgets"

        self.__success_message = {
            "X-OPERATION-ID": "",
            "X-RESPONSE-ID": "",
            "initiator": "",
            "data": {
                "ocid": "",
                "url": "",
                "operationDate": "",
                "outcomes": {
                    "ei": [
                        {
                            "id": "",
                            "X-TOKEN": ""
                        }
                    ]
                }
            }
        }

        self.__failure_message = {
            "X-OPERATION-ID": "",
            "X-RESPONSE-ID": "",
            "initiator": "",
            "errors": [
                {
                    "code": "",
                    "description": ""
                }
            ]
        }

    def build_expected_success_message(self):
        """Build the message."""

        if "X-OPERATION-ID" in self.actual_message:
            is_operation_id_correct = is_it_uuid(self.actual_message['X-OPERATION-ID'])

            if is_operation_id_correct is True:
                self.__success_message['X-OPERATION-ID'] = self.actual_message['X-OPERATION-ID']
            else:
                ValueError("The message is not correct: 'X-OPERATION-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-OPERATION-ID'.")

        if "X-RESPONSE-ID" in self.actual_message:
            is_process_id_correct = is_it_uuid(self.actual_message['X-RESPONSE-ID'])

            if is_process_id_correct is True:
                self.__success_message['X-RESPONSE-ID'] = self.actual_message['X-RESPONSE-ID']
            else:
                ValueError("The message is not correct: 'X-RESPONSE-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-RESPONSE-ID'.")

        if "initiator" in self.actual_message:
            self.__success_message['initiator'] = "platform"
        else:
            KeyError("The message is not correct: mismatch key 'initiator'.")

        if "ocid" in self.actual_message['data']:
            if self.test_mode is False:
                is_ocid_correct = fnmatch.fnmatch(self.actual_message["data"]["ocid"], f"ocds-t1s2t3-{self.country}-*")
            else:
                is_ocid_correct = fnmatch.fnmatch(self.actual_message["data"]["ocid"], f"test-t1s2t3-{self.country}-*")

            if is_ocid_correct is True:
                self.__success_message['data']['ocid'] = self.actual_message['data']['ocid']
            else:
                ValueError("The message is not correct: 'data.ocid'.")
        else:
            KeyError("The message is not correct: mismatch key 'data.ocid'.")

        if "url" in self.actual_message['data']:
            self.__success_message['data']['url'] = f"{self.budget_url}/{self.__success_message['data']['ocid']}"
        else:
            KeyError("The message is not correct: mismatch key 'data.url'.")

        if "operationDate" in self.actual_message['data']:
            is_date_correct = fnmatch.fnmatch(self.actual_message["data"]["operationDate"], "202*-*-*T*:*:*Z")

            if is_date_correct is True:
                self.__success_message['data']['operationDate'] = self.actual_message['data']['operationDate']
            else:
                ValueError("The message is not correct: 'data.operationDate'.")
        else:
            KeyError("The message is not correct: mismatch key 'data.operationDate'.")

        outcomes_ei_array = list()
        for obj in range(self.expected_quantity_of_outcomes_ei):
            outcomes_ei_array.append(copy.deepcopy(self.__success_message['data']['outcomes']['ei'][0]))

            if self.test_mode is False:
                is_ei_id_correct = fnmatch.fnmatch(
                    self.actual_message["data"]["outcomes"]["ei"][obj]["id"], f"ocds-t1s2t3-{self.country}-*"
                )
            else:
                is_ei_id_correct = fnmatch.fnmatch(
                    self.actual_message["data"]["outcomes"]["ei"][obj]["id"], f"test-t1s2t3-{self.country}-*"
                )

            if is_ei_id_correct is True:
                outcomes_ei_array[obj]['id'] = self.actual_message["data"]["outcomes"]["ei"][obj]["id"]
            else:
                ValueError(f"The message is not correct: 'data.outcomes.ei[{obj}].id'.")

            is_ei_token_correct = is_it_uuid(self.actual_message["data"]["outcomes"]["ei"][obj]["X-TOKEN"])

            if is_ei_token_correct is True:
                outcomes_ei_array[obj]['X-TOKEN'] = self.actual_message["data"]["outcomes"]["ei"][obj]["X-TOKEN"]
            else:
                ValueError(f"The message is not correct: 'data.outcomes.ei[{obj}].X-TOKEN'.")

        self.__success_message['data']['outcomes']['ei'] = outcomes_ei_array
        return self.__success_message

    def build_expected_failure_message(self, error_code, error_description=None):
        """Build the message."""

        if "X-OPERATION-ID" in self.actual_message:
            is_operation_id_correct = is_it_uuid(self.actual_message['X-OPERATION-ID'])

            if is_operation_id_correct is True:
                self.__failure_message['X-OPERATION-ID'] = self.actual_message['X-OPERATION-ID']
            else:
                ValueError("The message is not correct: 'X-OPERATION-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-OPERATION-ID'.")

        if "X-RESPONSE-ID" in self.actual_message:
            is_process_id_correct = is_it_uuid(self.actual_message['X-RESPONSE-ID'])

            if is_process_id_correct is True:
                self.__failure_message['X-RESPONSE-ID'] = self.actual_message['X-RESPONSE-ID']
            else:
                ValueError("The message is not correct: 'X-RESPONSE-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-RESPONSE-ID'.")

        if "initiator" in self.actual_message:
            self.__failure_message['initiator'] = "platform"
        else:
            KeyError("The message is not correct: mismatch key 'initiator'.")

        # Prepare errors.
        self.__failure_message['errors'][0]['code'] = error_code

        if error_description is None:
            del self.__failure_message['errors'][0]['description']
        else:
            self.__failure_message['errors'][0]['description'] = error_description

        return self.__failure_message
