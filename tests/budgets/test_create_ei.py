import copy
import allure

from class_collection.platform_authorization import PlatformAuthorization
from functions_collection.get_message_for_platform import get_message_for_platform
from functions_collection.requests_collection import create_ei_process
from payloads_collection.budget.ei_payload import ExpenditureItemPayload


@allure.parent_suite("Budget")
@allure.suite("Expenditure item")
@allure.severity("Critical")
@allure.testcase(url="")
class TestCreateEi:
    @allure.title("Check records: based on required data model.")
    def test_case_1(self, get_credits):

        bpe_host = get_credits[1]
        country = get_credits[3]
        language = get_credits[4]
        tender_classification_id = get_credits[8]

        step_number = 1
        with allure.step(f"# {step_number}. Authorization platform one: Create EI process."):
            """
            Tender platform authorization for Create EI process.
            As result, get tender platform's access token and process operation-id.
            """
            platform_one = PlatformAuthorization(bpe_host)
            access_token = platform_one.get_access_token_for_platform_one()
            ei_operation_id = platform_one.get_x_operation_id(access_token)

        step_number += 1
        with allure.step(f"# {step_number}. Send a request to create a Create EI process."):
            """
            Send api request to BPE host to create a CreateEi process.
            And save in variable ei_ocid.
            """
            try:
                """
                Build payload for CreateEi process.
                """
                ei_payload = copy.deepcopy(ExpenditureItemPayload(
                    buyer_id=0,
                    tender_classification_id=tender_classification_id)
                )

                ei_payload.delete_optional_fields(
                    "tender.description",
                    "tender.items",
                    "planning.rationale",
                    "buyer.identifier.uri",
                    "buyer.address.postalCode",
                    "buyer.additionalIdentifiers",
                    "buyer.contactPoint.faxNumber",
                    "buyer.contactPoint.url",
                    "buyer.details"
                )

                ei_payload = ei_payload.build_expenditure_item_payload()
            except ValueError:
                raise ValueError("Impossible to build payload for CreateEi process.")

            synchronous_result = create_ei_process(
                host=bpe_host,
                access_token=access_token,
                x_operation_id=ei_operation_id,
                country=country,
                language=language,
                payload=ei_payload,
                test_mode=True
            )
            message = get_message_for_platform(ei_operation_id)
            cpid = message['data']['ocid']
            allure.attach(str(message), "Message for platform.")

        step_number += 1
        with allure.step(f"# {step_number}. See result"):
            """
            Check the results of TestCase.
            """

            with allure.step(f"# {step_number}.1. Check status code"):
                """
                Check the status code of sending the request.
                """
                with allure.step('Compare actual status code and expected status code of sending request.'):
                    allure.attach(str(synchronous_result.status_code), "Actual status code.")
                    allure.attach(str(202), "Expected status code.")
                    assert synchronous_result.status_code == 202

        return ei_operation_id, cpid
