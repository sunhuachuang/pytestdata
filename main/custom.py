# 1. change fileds type by custom
# 2. save the custom for next use.
# writed by sunhuachuang #
import os

def custom_fields(sql, database, table, fields):
    fields = __format(fields)
    __log(sql, database, table, fields)
    return fields


def __log(sql, database, table, fields):
    file_dir = 'cache/sql/' + sql + '/' + database + '/'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_dir + table, 'w') as f:
        f.write(str(fields))

def __format(fields):
    new_fields = []
    if isinstance(fields, dict):
        fields = list(fields.values())
    for f in fields:
        if 'nullable' in f:
            f['nullable'] = True
        else:
            f['nullable'] = False

        if 'unique' in f:
            f['unique'] = True
        else:
            f['unique'] = False

        f['max'] = int(f['max'])
        f['min'] = int(f['min'])
        new_fields.append(f)
    return new_fields
