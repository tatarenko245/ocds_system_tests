import copy
import requests


def get_standard_criteria(environment, country, language):
    url = None
    if environment == "dev":
        url = "http://dev.public.eprocurement.systems/mdm/standardCriteria"
    elif environment == "sandbox":
        url = "http://public.eprocurement.systems/mdm/standardCriteria"
    data = requests.get(
        url=url,
        params={
            "lang": language,
            "country": country
        }
    )

    exclusion_ground_criteria_list = list()
    for criteria in copy.deepcopy(data.json()['data']):
        for i in criteria['classification']:
            if i == "id":
                if criteria['classification']['id'][0:20] == "CRITERION.EXCLUSION.":
                    exclusion_ground_criteria_list.append(criteria['classification'])

    selection_criteria_list = list()
    for criteria in copy.deepcopy(data.json()['data']):
        for i in criteria['classification']:
            if i == "id":
                if criteria['classification']['id'][0:20] == "CRITERION.SELECTION.":
                    selection_criteria_list.append(criteria['classification'])

    other_criteria_list = list()
    for criteria in copy.deepcopy(data.json()['data']):
        for i in criteria['classification']:
            if i == "id":
                if criteria['classification']['id'][0:16] == "CRITERION.OTHER.":
                    other_criteria_list.append(criteria['classification'])
    return data.json(), exclusion_ground_criteria_list, selection_criteria_list, other_criteria_list


def get_country(host, country, language):
    data = requests.get(url=f"{host}:9161/addresses/countries/{country}",
                        params={
                            'lang': language
                        }).json()

    return data


def get_region(host, country, region, language):
    data = requests.get(url=f"{host}:9161/addresses/countries/{country}/regions/{region}",
                        params={
                            'lang': language
                        }).json()
    return data


def get_locality(host, country, region, locality, language):
    data = requests.get(url=f"{host}:9161/addresses/countries/{country}/regions/{region}/"
                            f"localities/{locality}",
                        params={
                            'lang': language
                        }).json()
    return data


def get_criteria(host, language, country, pmd, phase):
    data = requests.get(
        url=f"{host}:9161/criteria",
        params={
            'lang': language,
            'country': country,
            'pmd': pmd,
            'phase': phase
        }).json()
    return data


def get_requirement_groups(host, language, country, pmd, phase, criterion_id):
    data = requests.get(
        url=f"{host}:9161/requirementGroups",
        params={
            'lang': language,
            'country': country,
            'pmd': pmd,
            'phase': phase,
            'criterionId': criterion_id
        }).json()
    return data


def get_requirements(host, language, country, pmd, phase, requirement_group_id):
    data = requests.get(
        url=f"{host}:9161/requirements",
        params={
            'lang': language,
            'country': country,
            'pmd': pmd,
            'phase': phase,
            'requirementGroupId': requirement_group_id
        }).json()
    return data
