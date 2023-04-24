import sys
import requests
from typing import Any, Tuple, Dict, List

create_results_route = "nitestmonitor/v2/results"
create_steps_route = "nitestmonitor/v2/steps"
update_results_route = "nitestmonitor/v2/update-results"
update_steps_route = "nitestmonitor/v2/update-steps"
delete_results_route = "nitestmonitor/v2/delete-results"
delete_result_route = "nitestmonitor/v2/results"

api_key = ""
base_url = ""

headers = { 'X-NI-API-KEY': api_key }

def update_headers() -> None:
    global headers, api_key
    headers = { 'X-NI-API-KEY': api_key }

def set_base_url_and_api_key(server_url: str, key: str) -> None:
    global api_key, base_url
    base_url = server_url
    api_key = key
    update_headers()

def create_test_result_request(results: List) -> Dict:
    """
    Creates a create test result request object.
    :param results: List of results to be created
    :return: A dictionary which is required for creating the results
    """
    return {
        "results":results
    }

def test_step_create_or_update_request_object(steps: List, update_result_total_time: bool = True) -> Dict:
    """
    Creates a create/update test step request object.
    :param results: List of steps to be created/updated
    :param update_result_total_time: A boolean to determine if result total time needs to be updated
    :return: A dictionary which is required for creating/updating the steps
    """
    return{
        "steps": steps,
        "updateResultTotalTime": update_result_total_time
    }

def update_test_results_request(results: List, determine_status_from_steps: bool = True) -> Dict:
    """
    Creates a update test result request object.
    :param results: List of results to be updated
    :param determine_status_from_steps: A boolean to determine if the result status needs to be updated 
    based on the status of the steps
    :return: A dictionary which is required for updating the results
    """
    return{
        "results": results,
        "determineStatusFromSteps": determine_status_from_steps
    }

def delete_results_request(result_ids: List, delete_steps: bool):
    """
    Creates a delete test results request object.
    :param result_ids: List of result Ids to be deleted
    :param delete_steps: A boolean to determine if the steps associated with results should be deleted or not
    :return: A dictionary which is required for deleting the results
    """
    return {
        "ids":result_ids,
        "deleteSteps":delete_steps
    }

def create_results(results: List) -> Dict:
    """
    Creates new test results from the supplied models. The server automatically generates the result ids.
    :param results: List of results to be created
    :return: json response after creating the results
    """
    if len(results) == 0 :
        raise ValueError("Number of results to be created can not be empty.")
    body = create_test_result_request(results)
    request_url = base_url + create_results_route
    request_response = raise_post_request(request_url, body)

    return request_response.json()

def update_results(results: List) -> Dict:
    """
    Updates existing test results by merging or replacing values.
    :param results: List of results to be updated
    :return: json response after updating the results
    """
    if len(results) == 0 :
        raise ValueError("Number of results to be updated can not be empty.")
    body = update_test_results_request(results, determine_status_from_steps=True)
    request_url = base_url + update_results_route
    request_response = raise_post_request(request_url, body)

    return request_response.json()

def create_steps(steps: List) -> Dict:
    """
    Creates new test steps from the supplied models. 
    The result associated with the steps must exist prior to step creation. 
    The server automatically generates step ids if not provided.
    :param steps: Steps to be created
    :return: json response after creating steps
    """
    if len(steps) == 0 :
        raise ValueError("Number of steps to be created can not be empty.")
    body = test_step_create_or_update_request_object(
            steps, update_result_total_time=True
        )
    request_url = base_url + create_steps_route
    request_response = raise_post_request(request_url, body)

    return request_response.json()

def update_steps(steps: List) -> Dict:
    """
    Updates existing steps by merging or replacing values.
    :param steps: List of steps to be updated
    :return: json response after updating steps
    """
    if len(steps) == 0 :
        raise ValueError("Number of steps to be updated can not be empty.")
    body = test_step_create_or_update_request_object(
                steps, update_result_total_time=True
            )
    request_url = base_url + update_steps_route
    request_response = raise_post_request(request_url, body)

    return request_response.json()

def delete_result(result_id: str, delete_steps: bool = True) -> None:
    """
    Deletes test result.
    :param result_id: result Id to be deleted
    """
    if result_id == None :
        raise ValueError("Missing required parameter 'result_id' in ResultsApi->DeleteResultV2 request.")
    request_url = f"{base_url}{delete_result_route}/{result_id}?deleteSteps{delete_steps}"
    raise_delete_request(request_url)

def delete_results(result_ids: List, delete_steps: bool = True) -> Dict:
    """
    Delete multiple test results.
    :param result_ids: List of result Ids to be deleted
    :return: json response after deleting the results
    """
    if result_ids == None or len(result_ids) == 0:
        raise ValueError("result_ids is a required property for ResultsApi->DeleteResultsV2 and cannot be null or empty.")
    request_url = f"{base_url}{delete_results_route}"
    body = delete_results_request(result_ids, delete_steps)   
    request_response = raise_post_request(request_url, body)
    if request_response.status_code != 204 :
        return request_response.json()
    else:
        return {}

def raise_post_request(url: str, body: Dict) -> requests.Response:
    """
    Makes the post request API call.
    :param url: request url to be called
    :param body: API call body
    :return: response of the API call
    """
    request_response =  requests.post(url, json=body, headers=headers)
    request_response.raise_for_status()

    return request_response

def raise_delete_request(url: str) -> requests.Response:
    """
    Makes the delete request API call.
    :param url: request url to be called
    :return: response of the API call
    """
    request_response = requests.delete(url, headers=headers)
    request_response.raise_for_status()

    return request_response