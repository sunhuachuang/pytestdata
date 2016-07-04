# automatic distinguish fileds type.
# writed by sunhuachuang #

# descs
# name     => str
# key      => str (pri or other)
# type     => tuple (typename, params) int str float datetime date bool text enum
# default  => str
# nullable => bool (True or False)
# extra    => str

#results
# name        => str
# type        => str
# min         => int
# max         => int
# default     => str
# nullable    => bool
# unique      => bool
# foreign_key => str (table_name)
# language    => str
from functools import reduce

# @param descs([{}, {}])
# @return [{},]
def analyze(descs):
    results = []
    for desc in descs:
        if desc['extra'] == 'auto_increment':
            continue
        field = __analyze_field(desc)
        results.append(field)
    return results

def __analyze_field(desc):
    field_type = desc['type'][0]
    result = {}
    result['name']        = desc['name']
    result['default']     = desc['default']
    result['nullable']    = desc['nullable']
    result['unique']      = desc['extra'] == 'uni'
    if desc['key']:
        result['foreign_key'] = 'TODO'
    result['foreign_key'] = ''
    result['language']    = 'en'

    fnr = eval('__' + field_type)(desc, result)
    return fnr

def __int(desc, result):
    type_name = desc['name']
    result['min'] = 1
    result['max'] = reduce(lambda x, y: x + 9*10**y, range(int(desc['type'][1])+1))
    if 'age' in type_name:
        result['type'] = 'age'
        result['max']  = 100
    else:
        result['type'] = 'randomint'

    return result

def __str(desc, result):
    type_name = desc['name']
    result['min'] = 1
    result['max'] = desc['type'][1]

    if 'username' in type_name:
        result['type'] = 'username'

    elif 'company' in type_name and 'name' in type_name:
        result['type'] = 'companyname'

    elif 'name' in type_name:
        result['type'] = 'name'

    else:
        result['type'] = 'randomstring'

    return result

def __float(desc, result):
    result['type']        = 'name'
    result['min']         = 1
    result['max']         = 44
    return result

def __datetime(decs, result):
    result['type']        = 'name'
    result['min']         = 1
    result['max']         = 44
    return result

def __date(desc, result):
    result['type']        = 'name'
    result['min']         = 1
    result['max']         = 44
    return result

def __bool(desc, result):
    result['type']        = 'name'
    result['min']         = 1
    result['max']         = 44
    return result

def __text(desc, result):
    result['type']        = 'name'
    result['min']         = 1
    result['max']         = 44
    return result

def __enum(desc, result):
    result['type']        = 'name'
    result['min']         = 1
    result['max']         = 44
    return result
