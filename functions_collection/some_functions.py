import copy
import datetime
import random
import time
import pytz

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
    for quantity_of_object in range(quantity_of_object):
        if lots_array is not None:
            for o in items_array:
                for r in o:
                    if r == "relatedLot":
                        items_array[quantity_of_object]['relatedLot'] = lots_array[quantity_of_object]['id']
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
        items_array[quantity_of_object]['classification']['id'] = item_classification_id
        val = items_array[quantity_of_object]
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
