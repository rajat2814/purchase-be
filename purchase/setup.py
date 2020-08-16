import random

from datetime import datetime, timedelta

from purchase.models import PurchaseModel, PurchaseStatusModel


def random_date(start, end, used=[]):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    list_of_seconds = [i for i in range(1, int_delta, int(int_delta / 5000))]
    list_of_seconds = list(set(list_of_seconds) - set(used))
    random_second = random.choice(list_of_seconds)
    return start + timedelta(seconds=random_second)


def setup_data():

    status_mapper = {
        1: 'open',
        2: 'verified',
        3: 'dispatched',
        4: 'delivered'
    }

    user_mapper = {
        1: {
            'purchaser_name': 'Tom',
            'quantity': 1
        },
        2: {
            'purchaser_name': 'Jerry',
            'quantity': 2
        },
        3: {
            'purchaser_name': 'Jarvis',
            'quantity': 3
        },
        4: {
            'purchaser_name': 'Jack',
            'quantity': 4
        },
        5: {
            'purchaser_name': 'Jill',
            'quantity': 5
        },
        6: {
            'purchaser_name': 'Ravi',
            'quantity': 6
        },
        7: {
            'purchaser_name': 'Kishan',
            'quantity': 7
        },
        8: {
            'purchaser_name': 'Kyle',
            'quantity': 8
        },
        9: {
            'purchaser_name': 'Jackson',
            'quantity': 9
        },
        10: {
            'purchaser_name': 'Vayu',
            'quantity': 10
        }
    }

    total_quantity = 35000
    number_of_entries = 5000

    zeros_array = list()
    zeros_array = [0] * (total_quantity - number_of_entries)
    ones_array = list()
    ones_array = [1] * (number_of_entries - 1)
    zeros_array.extend(ones_array)
    random.shuffle(zeros_array)
    elements = list()
    counter = 0
    for curri in range(len(zeros_array)):
        curr = zeros_array[curri]
        if curr == 1:
            elements.append(counter + 1)
            counter = 0
        else:
            counter += 1
    if counter > 0:
        elements.append(counter + 1)
    extras = 0
    for i, num in enumerate(elements):
        if num > 10:
            extras += (num - 10)
            elements[i] = 10
    for i, num in enumerate(elements):
        if num < 10:
            how_much = 10 - num
            if (extras - how_much) < 0:
                elements[i] += extras
                break
            else:
                elements[i] += how_much
                extras -= how_much

    purchase_model_insert_list = []
    purchase_status_model_insert_list = []

    for quantity in elements:
        purchase_model_insert_list.\
            append(PurchaseModel(**user_mapper.get(quantity)))

    PurchaseModel.objects.bulk_create(purchase_model_insert_list)

    min_date = datetime.strptime('1/1/2019 11:30 PM', '%m/%d/%Y %I:%M %p')
    max_date = datetime.strptime('3/31/2020 4:30 AM', '%m/%d/%Y %I:%M %p')

    used = []

    for purchase in PurchaseModel.objects.all():

        created_at = random_date(min_date, (max_date - timedelta(days=1)), used=used)

        used.append(int((created_at - min_date).total_seconds()))

        for i in range(1, random.randint(1, 4) + 1):

            if not i == 1:
                created_at = created_at + timedelta(seconds=1000)

            data = {
                'status': status_mapper[i],
                'purchase': purchase,
                'created_at': created_at
            }
            purchase_status_model_insert_list.\
                append(PurchaseStatusModel(**data))

    PurchaseStatusModel.objects.bulk_create(purchase_status_model_insert_list)
