# use flask to control the web.

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import main.db

app = Flask(__name__)

app.config.from_object(__name__)
app.config.update(dict(
    SECRET_KEY='developmentkey'
))
app.config.from_envvar('PYTESTDATA_SETTINGS', silent=True)

# start work select a sql server
@app.route('/')
def home():
    return render_template('home.html')

# login the server and save the session
@app.route('/<sql>', methods=['GET', 'POST'])
def login(sql):
    if request.method == 'POST' and request.form['host'] and request.form['port'] and request.form['user'] and request.form['password']:
        host = request.form['host']
        port = request.form['port']
        user = request.form['user']
        password = request.form['password']
        params = {'host': host, 'port': port, 'user': user, 'password': password}
        check_result = main.db.connect_check(sql, params)
        if check_result == True:
            session['sql'] = params
            return redirect(url_for('db', sql=sql))
        elif isinstance(check_result, str):
            flash(check_result)
        else:
            flash('wrong user or password!')
    return render_template('login.html')

# select a database for work
@app.route('/<sql>/db')
def db(sql):
    databases = main.db.show_databases(sql, session['sql'])
    return render_template('db.html', sql=sql, databases=databases)

# show all the table in the database
@app.route('/<sql>/<database>')
def index(sql, database):
    tables = main.db.show_tables(sql, session['sql'], database)
    print(tables)
    return render_template('index.html', sql=sql, database=database, tables=tables)

@app.route('/table/index/show')
def table_index():
    return render_template('table_index.html')

# select a table for work show the table automatic analysis
@app.route('/<sql>/<database>/<name>', methods=['GET', 'POST'])
def table(sql, database, name):
    if request.method == 'POST':
        fields = flask_format_form(request.form)
        success_number, failure_number = main.db.insert(sql, session['sql'], database, name, fields)
        flash('successed ' + str(success_number) + ', failured ' + str(failure_number))
        return redirect(url_for('table_show', sql=sql, database=database, table=name))
    fields = main.db.analyze_table(sql, session['sql'], database, name)
    return render_template('table.html', sql=sql, database=database, table=name, fields=enumerate(fields))

# show the flash about change, action result, table infomation
@app.route('/<sql>/<database>/<table>/show')
def table_show(sql, database, table):
    number = main.db.count_table(sql, session['sql'], database, table)
    return render_template('table_show.html', sql=sql, database=database, table=table, number=number)

# delete the all rows
@app.route('/<sql>/<database>/<table>/delete')
def delete(sql, database, table):
    main.db.delete(sql, session['sql'], database, table)
    flash('you have delete all rows!')
    return redirect(url_for('table_show', sql=sql, database=database, table=table))

def flask_format_form(form_fields):
    fields = {}
    for field in form_fields.items():
        name = field[0]
        value = field[1]
        names = name.split('.', 1)
        if names[0] in fields:
            fields[names[0]][names[1]] = value
        else:
            fields[names[0]] = {names[1]: value}
    return fields

if __name__ == '__main__':
    app.run()
