""" Prepare expected message for platform, the create prior information notice process of budget."""
import copy
import re

from functions_collection.some_functions import is_it_uuid


class CreatePriorInformationNoticeMessage:
    """ Class creates instance of message for platform."""

    def __init__(self, environment, country, actual_message, expected_quantity_of_outcomes_pin=1, test_mode=False):
        self.environment = environment
        self.country = country
        self.actual_message = actual_message
        self.test_mode = test_mode
        self.expected_quantity_of_outcomes_pin = expected_quantity_of_outcomes_pin

        if environment == "dev":
            self.tender_url = "http://dev.public.eprocurement.systems/tenders"
        elif environment == "sandbox":
            self.tender_url = "http://public.eprocurement.systems/tenders"

        self.success_message = {
            "X-OPERATION-ID": "",
            "X-RESPONSE-ID": "",
            "initiator": "",
            "data": {
                "ocid": "",
                "url": "",
                "operationDate": "",
                "outcomes": {
                    "pin": [
                        {
                            "id": "",
                            "X-TOKEN": ""
                        }
                    ]
                }
            }
        }

        self.failure_message = {
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
                self.success_message['X-OPERATION-ID'] = self.actual_message['X-OPERATION-ID']
            else:
                ValueError("The message is not correct: 'X-OPERATION-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-OPERATION-ID'.")

        if "X-RESPONSE-ID" in self.actual_message:
            is_process_id_correct = is_it_uuid(self.actual_message['X-RESPONSE-ID'])

            if is_process_id_correct is True:
                self.success_message['X-RESPONSE-ID'] = self.actual_message['X-RESPONSE-ID']
            else:
                ValueError("The message is not correct: 'X-RESPONSE-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-RESPONSE-ID'.")

        if "initiator" in self.actual_message:
            self.success_message['initiator'] = "platform"
        else:
            KeyError("The message is not correct: mismatch key 'initiator'.")

        if "ocid" in self.actual_message['data']:
            if self.test_mode is False:
                pattern = f"ocds-t1s2t3-{self.country}-.............-PI-............."
            else:
                pattern = f"test-t1s2t3-{self.country}-.............-PI-............."

            is_ocid_correct = re.fullmatch(
                pattern, self.actual_message["data"]["ocid"]
            )

            if is_ocid_correct:
                self.success_message['data']['ocid'] = self.actual_message['data']['ocid']
            else:
                self.success_message['data']['ocid'] = f"The ocid is not correct: 'data.ocid."
        else:
            KeyError("The message is not correct: mismatch key 'data.ocid'.")

        if "url" in self.actual_message['data']:
            self.success_message['data']['url'] = f"{self.tender_url}/{self.success_message['data']['ocid'][:28]}"
        else:
            KeyError("The message is not correct: mismatch key 'data.url'.")

        if "operationDate" in self.actual_message['data']:
            pattern = "202.-..-..T..:..:..Z"
            is_date_correct = re.fullmatch(
                pattern, self.actual_message["data"]["operationDate"]
            )
            if is_date_correct:
                self.success_message['data']['operationDate'] = self.actual_message['data']['operationDate']

            else:
                self.success_message['data']['operationDate'] = f"The operationDate is not correct: " \
                                                                f"'data.operationDate."
        else:
            KeyError("The message is not correct: mismatch key 'data.operationDate'.")

        outcomes_pin_array = list()
        for obj in range(self.expected_quantity_of_outcomes_pin):
            outcomes_pin_array.append(copy.deepcopy(self.success_message['data']['outcomes']['pin'][0]))

            if self.test_mode is False:
                pattern = f"ocds-t1s2t3-{self.country}-.............-PI-............."
            else:
                pattern = f"test-t1s2t3-{self.country}-.............-PI-............."

            is_pin_id_correct = re.fullmatch(
                pattern, self.actual_message["data"]["outcomes"]["pin"][obj]["id"]
            )

            if is_pin_id_correct:
                outcomes_pin_array[obj]['id'] = self.actual_message["data"]["outcomes"]["pin"][obj]["id"]
            else:
                outcomes_pin_array[obj]['id'] = f"The message is not correct: 'data.outcomes.pin[{obj}].id'."

            is_pin_token_correct = is_it_uuid(self.actual_message["data"]["outcomes"]["pin"][obj]["X-TOKEN"])

            if is_pin_token_correct is True:
                outcomes_pin_array[obj]['X-TOKEN'] = self.actual_message["data"]["outcomes"]["pin"][obj]["X-TOKEN"]
            else:
                ValueError(f"The message is not correct: 'data.outcomes.pin[{obj}].X-TOKEN'.")

        self.success_message['data']['outcomes']['pin'] = outcomes_pin_array
        return self.success_message

    def build_expected_failure_message(self, error_code, error_description=None):
        """Build the message."""

        if "X-OPERATION-ID" in self.actual_message:
            is_operation_id_correct = is_it_uuid(self.actual_message['X-OPERATION-ID'])

            if is_operation_id_correct is True:
                self.failure_message['X-OPERATION-ID'] = self.actual_message['X-OPERATION-ID']
            else:
                ValueError("The message is not correct: 'X-OPERATION-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-OPERATION-ID'.")

        if "X-RESPONSE-ID" in self.actual_message:
            is_process_id_correct = is_it_uuid(self.actual_message['X-RESPONSE-ID'])

            if is_process_id_correct is True:
                self.failure_message['X-RESPONSE-ID'] = self.actual_message['X-RESPONSE-ID']
            else:
                ValueError("The message is not correct: 'X-RESPONSE-ID' must be uuid.")
        else:
            KeyError("The message is not correct: mismatch key 'X-RESPONSE-ID'.")

        if "initiator" in self.actual_message:
            self.failure_message['initiator'] = "platform"
        else:
            KeyError("The message is not correct: mismatch key 'initiator'.")

        # Prepare errors.
        self.failure_message['errors'][0]['code'] = error_code

        if error_description is None:
            del self.failure_message['errors'][0]['description']
        else:
            self.failure_message['errors'][0]['description'] = error_description

        return self.failure_message
