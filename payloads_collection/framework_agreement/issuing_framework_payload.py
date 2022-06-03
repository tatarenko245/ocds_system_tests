"""Prepare the expected payload of the issuing framework, framework agreement procedures."""
from functions_collection.prepare_date import get_actual_datetime


class IssuingFrameworkPayload:
    """This class creates instance of payload."""

    def __init__(self):

        self.__payload = {
            "contract": {
                "internalId": "",
                "dateSigned": ""
            }
        }

    def build_payload(self):
        """Build payload."""
        self.__payload['contract']['internalId'] = "issuing framework: contract.internalId"
        self.__payload['contract']['dateSigned'] = get_actual_datetime()
        return self.__payload

    def delete_optional_fields(self, *args):
        """Call this method LAST! Delete optional fields from payload."""
        for a in args:
            if a == "contract":
                del self.__payload['contract']
            elif a == "contract.internalId":
                del self.__payload['contract']['internalId']
            elif a == "contract.dateSigned":
                del self.__payload['contract']['dateSigned']
            else:
                KeyError(f"Impossible to delete attribute by path {a}.")

    def __del__(self):
        print(f"The instance of IssuingFrameworkPayload class: {__name__} was deleted.")
