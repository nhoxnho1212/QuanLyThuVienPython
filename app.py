from flask import Flask, render_template, request, session, redirect, url_for
import requests
import json
from datetime import datetime
app = Flask(__name__)
url_api = "http://0.0.0.0:8080/api/"
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
def ticks(dt):
    return (dt - datetime(1, 1, 1)).total_seconds() * 10000000
@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/index')
def index():
    if 'token' not in session or 'payload' not in session:
        return redirect(url_for('login'))
    headers = [
        {
            'text': 'id',
            'align': 'start',
            'filterable': False,
            'value': 'id',

        },
        { 'text': 'Email', 'value': 'email' },
        { 'text': 'First name', 'value': 'firstname' },
        { 'text': 'Last name', 'value': 'lastname' },
        { 'text': 'avatar', 'value': 'avatar' },
        { 'text': 'role', 'value': 'role' },
        { 'text': 'function', 'value': 'employee_functions' },
        { 'text': 'Actions', 'value': 'actions', 'sortable': 'false' },
    ]

    response = requests.get(url_api + "user",
                            headers={
                                'Content-Type':'application/json',
                                'x-access-token': session['token']
                            }
                         )
    contents = None
    ver = ticks(datetime.utcnow())

    if response.status_code == 200:
        contents = response.json()['payload']

        for content in contents:
            if content['role'] == 'USER_ROLE.NHAN_VIEN':
                content['role'] = 'NHAN_VIEN'
            elif content['role'] == 'USER_ROLE.MANAGER':
                content['role'] = 'MANAGER'

            if content['employee_functions'] == 'EMPLOYEE.NONE_FUNCTION':
                content['employee_functions'] = 'NONE_FUNCTION'
            if content['employee_functions'] == 'EMPLOYEE.THU_THU':
                content['employee_functions'] = 'THU_THU'
            if content['employee_functions'] == 'EMPLOYEE.THU_KHO':
                content['employee_functions'] = 'THU_KHO'
            if content['employee_functions'] == 'EMPLOYEE.THU_QUY':
                content['employee_functions'] = 'THU_QUY'


        return render_template('admin-usermangerment.html', headers=headers, contents=contents, user_payload = session['payload'], token = session['token'],ver = ver)
    return render_template('admin-usermangerment.html', headers=headers, user_payload = session['payload'], token = session['token'], ver = ver)

@app.route('/registry', methods=['get','post'])
def registry():
    message = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        try:
            response = requests.post(url_api + "user",
                                     data=json.dumps({
                                         'email': email,
                                         'lastname': lastname,
                                         'firstname': firstname,
                                         'password': password
                                     }),
                                     headers= {'Content-Type':'application/json'}
                                     )
            if response.status_code == 200:
                return redirect(url_for('login'))
            else:
                message = response.json()["error"]
        except Exception as e:
            message = "No Internet Connection!"

    return render_template('registry.html', message=message)

@app.route('/login',methods=['get',"post"])
def login():
    message = None
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            response = requests.post(url_api + "login",
                                     data=json.dumps({
                                         'email': email,
                                         'password': password
                                     }),
                                     headers= {'Content-Type':'application/json'}
                                     )

            if response.status_code == 200:
                session['token'] = response.json()["token"]
                session['payload'] = response.json()['payload']
                payload = session['payload']
                if payload['role'] =='USER_ROLE.admin_root' or payload['role'] == 'USER_ROLE.MANAGER':
                    return redirect(url_for('index'))
                elif  payload['employee_functions'] =='EMPLOYEE.THU_KHO' or payload['employee_functions'] =='EMPLOYEE.THU_THU':
                    return redirect(url_for('book_management'))
            else:
                message = response.json()["error"]
        except Exception as e:
            message = "No Internet Connection!"
    if request.method == "GET":
        if not ('token' in session and 'payload' in session):
            return render_template('login.html', message=message)
        else:
            payload = session['payload']
            if payload['role'] =='USER_ROLE.admin_root' or payload['role'] == 'USER_ROLE.MANAGER':
                redirect(url_for('index'))
            elif payload['employee_functions'] == 'EMPLOYEE.NONE_FUNCTION' or payload['EMPLOYEE.THU_THU']:
                redirect(url_for('book_management'))

    return render_template('login.html', message=message)
@app.route('/book-management')
def book_management():
    if 'token' not in session or 'payload' not in session:
        return redirect(url_for('login'))
    headers = [
        {
            'text': 'id',
            'align': 'start',
            'filterable': False,
            'value': 'id',

        },
        { 'text': 'Name', 'value': 'name' },
        { 'text': 'Author', 'value': 'author' },
        { 'text': 'Category', 'value': 'category' },
        { 'text': 'Image', 'value': 'image' },
        { 'text': 'STAFF ID', 'value': 'user_id' },
        { 'text': 'Actions', 'value': 'actions', 'sortable': 'false' },
    ]

    response = requests.get(url_api + "book",
                            headers={
                                'Content-Type':'application/json',
                                'x-access-token': session['token']
                            }
                            )
    contents = None

    if response.status_code == 200:
        contents = response.json()['payload']

        return render_template('book-management.html', headers=headers, contents=contents, user_payload = session['payload'], token = session['token'])
    return render_template('book-management.html', headers=headers, user_payload = session['payload'], token = session['token'])


@app.route('/logout')
def logout():
    session.pop('token', None)
    session.pop('payload', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='localhost', port='8081', debug=True)
