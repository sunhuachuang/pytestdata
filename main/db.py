# about database connect and some actions interface.
# writed by sunhuachuang #
import main.automatic, main.action, main.custom

def connect_check(sql, params):
    if sql == 'mysql':
        try:
            import main.sql.mysql
            return main.sql.mysql.connect_check(params)
        except ImportError:
            return 'you need install pymysql (pip install PyMySQL)'

def __connect():
    pass

def __close():
    pass

def __initsql(sql):
    if sql == 'mysql':
        import main.sql.mysql
        return main.sql.mysql

# get all databases
# @params sql_name(str), params({})
# @return []
def show_databases(sql, params):
    sqlpackage = __initsql(sql)
    databases = sqlpackage.show_databases(params)
    return databases

# get all tables
# @params sql_name(str), params({}), database_name(str)
# @return []
def show_tables(sql, params, database):
    sqlpackage = __initsql(sql)
    return sqlpackage.show_tables(params, database)

# execute query
# @params sql_name(str), params({}), query(str)
# @return bool
def execute(sql, params, query):
    pass

# create format query for insert
# @params sql_name(str), params({}), table_name(str), fields([{}])
# @return tuple (success_number, failure_number)
def insert(sql, params, database, table, fields, number):
    new_fields = main.custom.custom_fields(sql, database, table, fields)
    data = main.action.create_data(new_fields, number)
    sqlpackage = __initsql(sql)
    return sqlpackage.insert_data(params, database, table, data)

# create format query for delete
# @params sql_name(str), params({}), database(str), table_name(str)
# @reutrn str
def delete(sql, params, database, table):
    pass

# auto analyze the table
# @params sql_name(str), params({}), database(str), table_name(str)
# @return []
def analyze_table(sql, params, database, table):
    sqlpackage = __initsql(sql)
    descs = sqlpackage.desc_table(params, database, table)
    return main.automatic.analyze(descs)

# count the rows in table
def count_table(sql, params, database, table):
    sqlpackage = __initsql(sql)
    return sqlpackage.count_table(params, database, table)
