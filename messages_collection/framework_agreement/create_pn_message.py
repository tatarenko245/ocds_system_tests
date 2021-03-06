""" Prepare expected message for platform, the create planning notice process of budget."""
import copy
import fnmatch

from functions_collection.some_functions import is_it_uuid


class PlanningNoticeMessage:
    """ Class creates instance of message for platform."""

    def __init__(self, environment, actual_message, expected_quantity_of_outcomes_ei=1, test_mode=False):
        self.environment = environment
        self.actual_message = actual_message
        self.test_mode = test_mode
        self.expected_quantity_of_outcomes_ei = expected_quantity_of_outcomes_ei

        if environment == "dev":
            self.budget_url = "http://dev.public.eprocurement.systems/tenders"
        elif environment == "sandbox":
            self.budget_url = "http://public.eprocurement.systems/tenders"

        self.__message = {
            "X-OPERATION-ID": "",
            "X-RESPONSE-ID": "",
            "initiator": "",
            "data": {
                "ocid": "",
                "url": "",
                "operationDate": "",
                "outcomes": {
                    "pn": [
                        {
                            "id": "",
                            "X-TOKEN": ""
                        }
                    ]
                }
            }
        }

    def build_expected_message(self):
        """Build the message."""

        if "X-OPERATION-ID" in self.actual_message:
            is_operation_id_correct = is_it_uuid(self.actual_message['X-OPERATION-ID'])

            if is_operation_id_correct is True:
                self.__message['X-OPERATION-ID'] = self.actual_message['X-OPERATION-ID']
            else:
                ValueError("The message is not correct: 'X-OPERATION-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-OPERATION-ID'.")

        if "X-RESPONSE-ID" in self.actual_message:
            is_process_id_correct = is_it_uuid(self.actual_message['X-RESPONSE-ID'])

            if is_process_id_correct is True:
                self.__message['X-RESPONSE-ID'] = self.actual_message['X-RESPONSE-ID']
            else:
                ValueError("The message is not correct: 'X-RESPONSE-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-RESPONSE-ID'.")

        if "initiator" in self.actual_message:
            self.__message['initiator'] = "platform"
        else:
            KeyError("The message is not correct: mismatch key 'initiator'.")

        if "ocid" in self.actual_message['data']:
            if self.test_mode is False:
                is_ocid_correct = fnmatch.fnmatch(self.actual_message["data"]["ocid"], "ocds-t1s2t3-MD-*")
            else:
                is_ocid_correct = fnmatch.fnmatch(self.actual_message["data"]["ocid"], "test-t1s2t3-MD-*")

            if is_ocid_correct is True:
                self.__message['data']['ocid'] = self.actual_message['data']['ocid']
            else:
                ValueError("The message is not correct: 'data.ocid'.")
        else:
            KeyError("The message is not correct: mismatch key 'data.ocid'.")

        if "url" in self.actual_message['data']:
            self.__message['data']['url'] = f"{self.budget_url}/{self.__message['data']['ocid']}"
        else:
            KeyError("The message is not correct: mismatch key 'data.url'.")

        if "operationDate" in self.actual_message['data']:
            is_date_correct = fnmatch.fnmatch(self.actual_message["data"]["operationDate"], "202*-*-*T*:*:*Z")

            if is_date_correct is True:
                self.__message['data']['operationDate'] = self.actual_message['data']['operationDate']
            else:
                ValueError("The message is not correct: 'data.operationDate'.")
        else:
            KeyError("The message is not correct: mismatch key 'data.operationDate'.")

        outcomes_pn_array = list()
        for obj in range(self.expected_quantity_of_outcomes_ei):
            outcomes_pn_array.append(copy.deepcopy(self.__message['data']['outcomes']['pn'][0]))

            if self.test_mode is False:
                is_pn_id_correct = fnmatch.fnmatch(
                    self.actual_message["data"]["outcomes"]["pn"][obj]["id"], "ocds-t1s2t3-MD-*-PN-*"
                )
            else:
                is_pn_id_correct = fnmatch.fnmatch(
                    self.actual_message["data"]["outcomes"]["pn"][obj]["id"], "test-t1s2t3-MD-*-PN-*"
                )

            if is_pn_id_correct is True:
                outcomes_pn_array[obj]['id'] = self.actual_message["data"]["outcomes"]["pn"][obj]["id"]
            else:
                ValueError(f"The message is not correct: 'data.outcomes.pn[{obj}].id'.")

            is_pn_token_correct = is_it_uuid(self.actual_message["data"]["outcomes"]["pn"][obj]["X-TOKEN"])

            if is_pn_token_correct is True:
                outcomes_pn_array[obj]['X-TOKEN'] = self.actual_message["data"]["outcomes"]["pn"][obj]["X-TOKEN"]
            else:
                ValueError(f"The message is not correct: 'data.outcomes.pn[{obj}].X-TOKEN'.")

        self.__message['data']['outcomes']['pn'] = outcomes_pn_array
        return self.__message
