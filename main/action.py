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

        if field_lang == 'en':
            import main.langs.en
            lang = main.langs.en

        while len(field_store_values[field_name]) < number:
            value = create_function(field_min, field_max, lang)
            if field_unique:
                field_store_values[field_name].add(value)
            else:
                field_store_values[field_name].append(value)

    field_values = __format(field_store_values)
    return field_names, field_values

def get_create_function(field_type):
    # true name
    def __get_name(min_value, max_value, lang):
        first_name = random.choice(lang.first_name)
        second_name = random.choice(lang.second_name)
        return first_name + ' ' + second_name

    # age 1 - 100
    def __get_age(min_value, max_value, lang):
        return random.randrange(min_value, max_value+1, 2)

    if field_type == 'name':
        return __get_name
    elif field_type == 'age':
        return __get_age




def __format(field_store_values):
    field_values = []
    return field_values
