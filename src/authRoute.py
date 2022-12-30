from flask import Blueprint, session, request, redirect, render_template

from services.security import Login, RegisterUser


authProvider = Blueprint('auth_blueprint', __name__)


@authProvider.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username, pwd = request.form['username'], request.form['password']

        if type(username) == str and '=' not in username and type(pwd):
            
            tmp = Login(username, pwd)

            if tmp:
                
                if session.get('sec_key', False):
                    session.pop('sec_key')
                
                session['sec_key'] = {'subject':username, 'pwd': tmp}
                
                return redirect('/')
                      

    return render_template('pages/auth/login.html', url_post='/login', url_reg='/register')

@authProvider.route('/logout', methods=['GET'])
def logout():
    
    session.clear()
    
    return redirect('/')

@authProvider.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username, pwd = request.form['username'], request.form['password']

        if type(username) == str and '=' not in username and type(pwd):

            tmp = RegisterUser(username, pwd)
            if tmp:
                
                if session.get('sec_key', False):
                    session.pop('sec_key')
                
                session['sec_key'] = {'subject':username, 'pwd': tmp}
                
                return redirect('/')

    return render_template('pages/auth/register.html', url_post='/register', url_back='/login')