import copy
import csv
import datetime
import fnmatch
import random
import time
from pathlib import Path
from uuid import UUID

import pytz
import xlrd

from data_collection.data_constant import cpv_category_tuple, cpv_goods_high_level_tuple, cpv_works_high_level_tuple, \
    cpv_services_high_level_tuple
from data_collection.data_constant import cpv_goods_low_level_03_tuple, cpv_goods_low_level_1_tuple, \
    cpv_goods_low_level_2_tuple, \
    cpv_goods_low_level_3_tuple, cpv_goods_low_level_44_tuple, cpv_goods_low_level_48_tuple, \
    cpv_works_low_level_45_tuple, cpv_services_low_level_5_tuple, cpv_services_low_level_6_tuple, \
    cpv_services_low_level_7_tuple, cpv_services_low_level_8_tuple, cpv_services_low_level_92_tuple, \
    cpv_services_low_level_98_tuple, locality_id_tuple


def generate_items_array(quantity_of_object, item_object, tender_classification_id, lots_array=None):
    copy.deepcopy(item_object)
    items_array = []
    for i in range(quantity_of_object):
        item_json = copy.deepcopy(item_object)
        item_json['id'] = str(i)
        items_array.append(item_json)

    new_array_items = []
    for i in range(quantity_of_object):
        if lots_array is not None:
            for o in items_array:
                for r in o:
                    if r == "relatedLot":
                        items_array[i]['relatedLot'] = lots_array[i]['id']
                    else:
                        pass
        else:
            pass
        item_classification_id = None
        if tender_classification_id[0:2] == "03":
            item_classification_id = f"{random.choice(cpv_goods_low_level_03_tuple)}"
        elif tender_classification_id[0] == "1":
            item_classification_id = f"{random.choice(cpv_goods_low_level_1_tuple)}"
        elif tender_classification_id[0] == "2":
            item_classification_id = f"{random.choice(cpv_goods_low_level_2_tuple)}"
        elif tender_classification_id[0] == "3":
            item_classification_id = f"{random.choice(cpv_goods_low_level_3_tuple)}"
        elif tender_classification_id[0:2] == "44":
            item_classification_id = f"{random.choice(cpv_goods_low_level_44_tuple)}"
        elif tender_classification_id[0:2] == "48":
            item_classification_id = f"{random.choice(cpv_goods_low_level_48_tuple)}"
        elif tender_classification_id[0:2] == "45":
            item_classification_id = f"{random.choice(cpv_works_low_level_45_tuple)}"
        elif tender_classification_id[0] == "5":
            item_classification_id = f"{random.choice(cpv_services_low_level_5_tuple)}"
        elif tender_classification_id[0] == "6":
            item_classification_id = f"{random.choice(cpv_services_low_level_6_tuple)}"
        elif tender_classification_id[0] == "7":
            item_classification_id = f"{random.choice(cpv_services_low_level_7_tuple)}"
        elif tender_classification_id[0] == "8":
            item_classification_id = f"{random.choice(cpv_services_low_level_8_tuple)}"
        elif tender_classification_id[0:2] == "92":
            item_classification_id = f"{random.choice(cpv_services_low_level_92_tuple)}"
        elif tender_classification_id[0:2] == "98":
            item_classification_id = f"{random.choice(cpv_services_low_level_98_tuple)}"
        else:
            Exception("Error: check your 'tender.classification.id'")
        items_array[i]['classification']['id'] = item_classification_id
        val = items_array[i]
        new_array_items.append(copy.deepcopy(val))
    return new_array_items


def get_locality_id_according_with_region_id(region_id):
    locality_id = locality_id_tuple
    for i in locality_id:
        if region_id[:3] == i[:3]:
            return i


def time_bot(expected_time):
    expected_time = datetime.datetime.strptime(expected_time, "%Y-%m-%dT%H:%M:%SZ")
    time_at_now = datetime.datetime.strptime(datetime.datetime.strftime(datetime.datetime.now(pytz.utc),
                                                                        "%Y-%m-%dT%H:%M:%SZ"), "%Y-%m-%dT%H:%M:%SZ")
    while time_at_now < expected_time:
        time_at_now = datetime.datetime.strptime(datetime.datetime.strftime(datetime.datetime.now(pytz.utc),
                                                                            "%Y-%m-%dT%H:%M:%SZ"), "%Y-%m-%dT%H:%M:%SZ")
        if time_at_now >= expected_time:
            time.sleep(3)
            break
    print("The time was expired")


def prepare_tender_classification_id():
    tender_classification_id = None
    category = random.choice(cpv_category_tuple)
    if category == "goods":
        tender_classification_id = random.choice(cpv_goods_high_level_tuple)
    elif category == "works":
        tender_classification_id = random.choice(cpv_works_high_level_tuple)
    elif category == "services":
        tender_classification_id = random.choice(cpv_services_high_level_tuple)
    return tender_classification_id


def is_it_uuid(uuid_to_test):
    try:
        uuid_obj = UUID(uuid_to_test)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


# This function returns root dir.
def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_value_from_cpvs_dictionary_csv(cpvs, language):
    path = get_project_root()
    with open(f'{path}/data_collection/CPVS_dictionary.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            cur_arr = row[0].split(';')
            if cur_arr[0] == cpvs and cur_arr[3] == f'"{language}"':
                return cur_arr[0].replace('"', ''), cur_arr[1].replace('"', ''), cur_arr[2].replace('"', ''), cur_arr[
                    3].replace('"', '')


def get_value_from_cpv_dictionary_xls(cpv, language):
    path = get_project_root()
    # Open current xlsx file.
    excel_data_file = xlrd.open_workbook(f'{path}/data_collection/CPV_dictionary.xls')
    # Take current page of the file.
    sheet = excel_data_file.sheet_by_index(0)

    # classification_description = []
    # How much rows contains into file?
    rows_number = sheet.nrows
    column_number = sheet.ncols
    requested_row = list()
    requested_column = list()
    if rows_number > 0:
        for row in range(0, rows_number):
            if cpv in sheet.row(row)[0].value:
                requested_row.append(row)

    if column_number > 0:
        for column in range(0, column_number):
            if language.upper() in sheet.col(column)[0].value:
                requested_column.append(column)
    new_cpv = sheet.cell_value(rowx=int(requested_row[0]), colx=0)
    description = sheet.cell_value(rowx=int(requested_row[0]), colx=int(requested_column[0]))
    return new_cpv, description


def get_value_from_classification_unit_dictionary_csv(unit_id, language):
    path = get_project_root()
    with open(f'{path}/data_collection/Units_dictionary.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            cur_arr = row[0].split(',')
            if cur_arr[0] == f'{unit_id}' and cur_arr[4].replace(';', '') == f'"{language}"':
                return cur_arr[0].replace("'", ""), cur_arr[2].replace('"', '')


def generate_tender_classification_id(items_array):
    list_of_keys = list()
    list_of_values = list()
    for o in items_array:
        for id_ in o['classification']:
            if id_ == "id":
                list_of_keys.append(id_)
                list_of_values.append(o['classification']['id'])
    quantity = len(list_of_keys)
    if quantity >= 2:
        classification_1 = list_of_values[0]
        classification_2 = list_of_values[1]
        s_1 = fnmatch.fnmatch(classification_1[0], classification_2[0])
        s_2 = fnmatch.fnmatch(classification_1[1], classification_2[1])
        s_3 = fnmatch.fnmatch(classification_1[2], classification_2[2])
        s_4 = fnmatch.fnmatch(classification_1[3], classification_2[3])
        s_5 = fnmatch.fnmatch(classification_1[4], classification_2[4])
        s_6 = fnmatch.fnmatch(classification_1[5], classification_2[5])
        s_7 = fnmatch.fnmatch(classification_1[6], classification_2[6])
        s_8 = fnmatch.fnmatch(classification_1[7], classification_2[7])
        s_9 = fnmatch.fnmatch(classification_1[8], classification_2[8])
        s_10 = fnmatch.fnmatch(classification_1[9], classification_2[9])
        new = list()
        if s_1 is True:
            new.append(classification_1[0])
        else:
            new.append("0")
        if s_2 is True:
            new.append(classification_1[1])
        else:
            new.append("0")
        if s_3 is True:
            new.append(classification_1[2])
        else:
            new.append("0")
        if s_4 is True:
            new.append(classification_1[3])
        else:
            new.append("0")
        if s_5 is True:
            new.append(classification_1[4])
        else:
            new.append("0")
        if s_6 is True:
            new.append(classification_1[5])
        else:
            new.append("0")
        if s_7 is True:
            new.append(classification_1[6])
        else:
            new.append("0")
        if s_8 is True:
            new.append(classification_1[7])
        else:
            new.append("0")
        if s_9 is True:
            new.append(classification_1[8])
        else:
            new.append("0")
        if s_10 is True:
            new.append(classification_1[9])
        else:
            new.append("0")
        new_classification_id = copy.deepcopy(
            str(new[0] + new[1] + new[2] + new[3] + new[4] + new[5] + new[6] + new[7]))
        tender_classification_id = f"{new_classification_id[0:3]}00000"
        iteration = quantity - 2
        index = 1
        while iteration > 0:
            index += 1
            classification_1 = new_classification_id
            classification_2 = list_of_values[index]
            s_1 = fnmatch.fnmatch(classification_1[0], classification_2[0])
            s_2 = fnmatch.fnmatch(classification_1[1], classification_2[1])
            s_3 = fnmatch.fnmatch(classification_1[2], classification_2[2])
            s_4 = fnmatch.fnmatch(classification_1[3], classification_2[3])
            s_5 = fnmatch.fnmatch(classification_1[4], classification_2[4])
            s_6 = fnmatch.fnmatch(classification_1[5], classification_2[5])
            s_7 = fnmatch.fnmatch(classification_1[6], classification_2[6])
            s_8 = fnmatch.fnmatch(classification_1[7], classification_2[7])
            new = list()
            if s_1 is True:
                new.append(classification_1[0])
            else:
                new.append("0")
            if s_2 is True:
                new.append(classification_1[1])
            else:
                new.append("0")
            if s_3 is True:
                new.append(classification_1[2])
            else:
                new.append("0")
            if s_4 is True:
                new.append(classification_1[3])
            else:
                new.append("0")
            if s_5 is True:
                new.append(classification_1[4])
            else:
                new.append("0")
            if s_6 is True:
                new.append(classification_1[5])
            else:
                new.append("0")
            if s_7 is True:
                new.append(classification_1[6])
            else:
                new.append("0")
            if s_8 is True:
                new.append(classification_1[7])
            else:
                new.append("0")
            new_classification_id = copy.deepcopy(
                str(new[0] + new[1] + new[2] + new[3] + new[4] + new[5] + new[6] + new[7]))
            iteration -= 1
            tender_classification_id = f"{new_classification_id[0:4]}0000"
    else:
        tender_classification_id = f"{items_array[0]['classification']['id'][0:4]}0000"
    return tender_classification_id


def get_value_from_country_csv(country, language):
    path = get_project_root()
    with open(f'{path}/data_collection/country.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == country and row[4] == language:
                return row


def get_value_from_region_csv(region, country, language):
    path = get_project_root()
    with open(f'{path}/data_collection/region.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == region and row[4] == country and row[5] == language:
                return row


def get_value_from_locality_csv(locality, region, country, language):
    path = get_project_root()
    with open(f'{path}/data_collection/locality.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == locality and row[4] == region and row[5] == country and row[6] == language:
                return row


def get_unique_party_from_list_by_id(parties_array):
    set_of_party_id = set()
    dictionary_of_all_parties = dict()
    for q in range(len(parties_array)):
        mapper = {
            parties_array[q]['id']: parties_array[q]
        }
        dictionary_of_all_parties.update(mapper)
        set_of_party_id.add(parties_array[q]['id'])

    unique_parties_array = list()
    for q in set_of_party_id:
        unique_parties_array.append(dictionary_of_all_parties[q])
    return unique_parties_array


def generate_lots_array(quantity_of_object, lot_object):
    copy.deepcopy(lot_object)
    lots_array = []
    for i in range(quantity_of_object):
        lot_json = copy.deepcopy(lot_object)
        lot_json['id'] = str(i)

        if "value" in lot_object:
            lot_json['value']['amount'] = round(float(lot_object['value']['amount'] / quantity_of_object), 2)

        lots_array.append(lot_json)

    new_array_lots = []
    for quantity_of_object in range(quantity_of_object):
        val = lots_array[quantity_of_object]
        new_array_lots.append(copy.deepcopy(val))
    return new_array_lots


def get_sum_of_lot(lots_array):
    """
    This function returns result of sum all lots into payload.
    """
    sum_of_lot = list()
    for lot_object in lots_array:
        if "value" in lot_object:
            if "amount" in lot_object['value']:
                sum_of_lot.append(lot_object['value']['amount'])
            else:
                KeyError("Check lot_object['value']['amount']")
        else:
            KeyError("Check lot_object['value']")
    s = float(format(sum(sum_of_lot), '.2f'))
    return s


def get_contract_period_for_ms_release(lots_array):
    start_date = list()
    end_date = list()
    for lot_object in lots_array:
        if "contractPeriod" in lot_object:
            if "startDate" in lot_object['contractPeriod']:
                date = datetime.datetime.strptime(lot_object['contractPeriod']['startDate'], "%Y-%m-%dT%H:%M:%SZ")
                start_date.append(date)
            else:
                KeyError("Check lot_object['contractPeriod']['startDate']")

            if "endDate" in lot_object['contractPeriod']:
                date = datetime.datetime.strptime(lot_object['contractPeriod']['endDate'], "%Y-%m-%dT%H:%M:%SZ")
                end_date.append(date)
            else:
                KeyError("Check lot_object['contractPeriod']['endDate']")
        else:
            KeyError("Check lot_object['contractPeriod']")
    minimum_date = min(start_date)
    start_date_for_ms_release = minimum_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    maximum_date = max(end_date)
    end_date_for_ms_release = maximum_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    return start_date_for_ms_release, end_date_for_ms_release


def make_unique_numbers(n):
    """
    This function returns set of the unique numbers.
    """
    set_of_numbers = set()
    while len(set_of_numbers) < n:
        set_of_numbers.add(random.randint(0, n))
    return set_of_numbers


def set_eligibility_evidences_unique_temporary_id(payload_criteria_array):
    """
    This function returns
    criteria[*].requirementGroups[*].requirements[*].eligibleEvidences[*].id as temporary id.
    """
    quantity_of_id_list = list()
    for i in payload_criteria_array:
        if "requirementGroups" in i:
            for i_1 in i['requirementGroups']:
                if "requirements" in i_1:
                    for i_2 in i_1['requirements']:
                        if "eligibleEvidences" in i_2:
                            for i_3 in i_2['eligibleEvidences']:
                                if "id" in i_3:
                                    quantity_of_id_list.append(i_3['id'])

    test = make_unique_numbers(len(quantity_of_id_list))
    iterator = len(test)
    if len(quantity_of_id_list) == len(test):
        for i in payload_criteria_array:
            if "requirementGroups" in i:
                for i_1 in i['requirementGroups']:
                    if "requirements" in i_1:
                        for i_2 in i_1['requirements']:
                            if "eligibleEvidences" in i_2:
                                for i_3 in i_2['eligibleEvidences']:
                                    if "id" in i_3:
                                        i_3['id'] = str(iterator)
                                        iterator -= 1

    return payload_criteria_array


def set_criteria_array_unique_temporary_id(payload_criteria_array):
    """
    This function returns criteria array with unique criteria[*].id, criteria[*].requirementGroups[*].id,
    criteria[*].requirementGroups[*].requirements[*].id as temporary id.
    """
    criteria_objects = list()
    for o in payload_criteria_array:
        if "id" in o:
            criteria_objects.append(o['id'])

    requirement_groups_objects = list()
    for o in payload_criteria_array:
        if "id" in o:
            for o_1 in o['requirementGroups']:
                if "id" in o_1:
                    requirement_groups_objects.append(o_1['id'])

    requirements_objects = list()
    for o in payload_criteria_array:
        if "id" in o:
            for o_1 in o['requirementGroups']:
                if "id" in o_1:
                    for o_2 in o_1['requirements']:
                        if "id" in o_2:
                            requirements_objects.append(o_1['id'])

    quantity_of_criteria_objects = len(criteria_objects)
    quantity_of_requirement_group_objects = len(requirement_groups_objects)
    quantity_of_requirement_objects = len(requirements_objects)

    test = make_unique_numbers(quantity_of_criteria_objects)
    iterator = len(test)
    criteria_list = []
    if quantity_of_criteria_objects == len(test):
        for o in payload_criteria_array:
            o['id'] = str(iterator).zfill(3)
            iterator -= 1
            criteria_list.append(o)

    test = make_unique_numbers(quantity_of_requirement_group_objects)
    iterator = len(test)
    requirement_groups_list = []
    if quantity_of_requirement_group_objects == len(test):
        for o in criteria_list:
            for o_1 in o['requirementGroups']:
                o_1['id'] = f"{o['id']}-{str(iterator).zfill(3)}"
                iterator -= 1
                requirement_groups_list.append(o_1)

    test = make_unique_numbers(quantity_of_requirement_objects)
    iterator = len(test)
    requirements_list = []
    if quantity_of_requirement_objects == len(test):
        for o in requirement_groups_list:
            for o_1 in o['requirements']:
                o_1['id'] = f"{o['id']}-{str(iterator).zfill(3)}"
                iterator -= 1
                requirements_list.append(o_1)

    return payload_criteria_array


def set_unique_temporary_id_for_requirement_responses_evidences(payload_requirement_responses_array):
    """
    This function returns
    'submission.requirementResponses[*].evidences[*].id' as temporary id.
    """
    quantity_of_id_list = list()
    for q_0 in payload_requirement_responses_array:
        for q_1 in q_0['evidences']:
            if "id" in q_1:
                quantity_of_id_list.append(q_1['id'])

    test = make_unique_numbers(len(quantity_of_id_list))
    iterator = len(test)
    if len(quantity_of_id_list) == len(test):
        for q_0 in payload_requirement_responses_array:
            for q_1 in q_0['evidences']:
                if "id" in q_1:
                    q_1['id'] = str(iterator)
                    iterator -= 1
    return payload_requirement_responses_array
