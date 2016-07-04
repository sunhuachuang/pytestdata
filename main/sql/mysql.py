import pymysql
#import pymysql.cursors

def connect_check(params):
    # Connect to the database
    try:
        pymysql.connect(host=params['host'],
                        port=int(params['port']),
                        user=params['user'],
                        password=params['password'],
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
        return True
    except pymysql.err.OperationalError:
        return False

def show_databases(params):
    connect =  __connect(params)
    try:
        with connect.cursor() as cursor:
            cursor.execute("show databases")
            results = cursor.fetchall()
            results = [k['Database'] for k in results]
    finally:
        connect.close()
    return results

def show_tables(params, database):
    connect =  __connect(params, database)
    try:
        with connect.cursor() as cursor:
            cursor.execute("show tables")
            results = cursor.fetchall()
            results = [k['Tables_in_'+database] for k in results]
    finally:
        connect.close()
    return results

def desc_table(params, database, table):
    connect =  __connect(params, database)
    try:
        with connect.cursor() as cursor:
            cursor.execute("SHOW COLUMNS FROM "+table)
            results = __desc_fields(cursor.fetchall())
    finally:
        connect.close()
    return results

def count_table(params, database, table):
    connect =  __connect(params, database)
    try:
        with connect.cursor() as cursor:
            cursor.execute("select count(*) FROM "+table)
            results = cursor.fetchone()
    finally:
        connect.close()
    return results['count(*)']

def insert_data(params, database, table, data):
    field_names, field_values = data
    connect =  __connect(params, database)
    try:
        with connect.cursor() as cursor:
            query = 'insert into ' + table + ' (' + ','.join(field_names) + ') values ({});';
            query_sql = ''
            for field_value in field_values:
                query_sql += query.format(','.join(map(lambda x: "'" + str(x) + "'", field_value)))
            print(query_sql)
            cursor.execute(query_sql)
            connect.commit()
    finally:
        connect.close()
    return count_table(params, database, table)

def __connect(params, database=None):
    return pymysql.connect(host=params['host'],
                           port=int(params['port']),
                           user=params['user'],
                           password=params['password'],
                           database=database,
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

def __desc_fields(fields):
    results = []
    for field in fields:
        analyzed_field = {}
        analyzed_field['name'] = field['Field']
        if field['Key'] == 'PRI':
            analyzed_field['key'] = 'pri'
        else:
            analyzed_field['key'] = field['Key']

        field_type = field['Type'].lower()
        if 'int' in field_type:
            analyzed_field['type'] = ('int', field_type.split('(')[1].split(')')[0])
        elif 'char' in field_type:
            analyzed_field['type'] = ('str', field_type.split('(')[1].split(')')[0])
        elif 'float' in field_type or 'double' in field_type or 'deciaml' in field_type:
            numbers = field_type.split('(')[1].split(')')[0].split(',')
            analyzed_field['type'] = ('float', numbers[0], numbers[1])
        elif 'time' in field_type:
            analyzed_field['type'] = ('datetime',)
        elif 'date' in field_type:
            analyzed_field['type'] = ('date',)
        elif 'bool' in field_type:
            analyzed_field['type'] = ('bool',)
        elif 'blob' in field_type or 'text' in field_type:
            analyzed_field['type'] = ('text',)
        elif 'enum':
            analyzed_field['type'] = ('enum',)
        else:
            analyzed_field['type'] = (field_type,)

        analyzed_field['default'] = field['Default']
        analyzed_field['nullable'] = field['Null'] == 'Yes'
        analyzed_field['extra'] = field['Extra']
        results.append(analyzed_field)
    return results
