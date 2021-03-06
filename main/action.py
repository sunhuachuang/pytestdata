# create insert data.
# writed by sunhuachuang #

# @params fields [{}, {}]
# @return ([field_names], [[value1, value2],[]...])
import random

def create_data(fields, number):
    field_names = []

    # store the values every field has a list or set values, each get every first value become a row
    field_store_values = {}

    for field in fields:
        field_name     = field['name']
        field_min      = field['min']
        field_max      = field['max']
        field_lang     = field['language']
        field_foreign  = field['foreign_key']
        field_nullable = field['nullable']
        field_default  = field['default']
        field_unique   = field['unique']

        field_names.append(field_name)
        create_function = get_create_function(field['type'])

        if field_unique:
            field_store_values[field_name] = set()
        else:
            field_store_values[field_name] = []

        lang = getattr(__import__('main.langs', fromlist=[field_lang]), field_lang)

        while len(field_store_values[field_name]) < number:
            value = create_function(field_min, field_max, lang)
            if field_unique:
                field_store_values[field_name].add(value)
            else:
                field_store_values[field_name].append(value)

    field_values = __format(field_names, field_store_values, number)
    return field_names, field_values

def get_create_function(field_type): #TODO
    # true name
    def __get_name(min_value, max_value, lang):
        first_name = random.choice(lang.first_name)
        second_name = random.choice(lang.second_name)
        return first_name + ' ' + second_name

    # age 1 - 100
    def __get_age(min_value, max_value, lang):
        return random.randrange(min_value, max_value+1, 2)

    return eval("__get_" + field_type)

# @param [], {'': [], '': set()...}, int
# @return [[,], [,] ...]
def __format(field_names, field_store_values, number):
    field_values = []
    l = len(field_names)
    for i in range(number):
        field_value = []
        for i in range(l):
            field_value.append(field_store_values[field_names[i]].pop())
        field_values.append(field_value)
    return field_values
