from flask import Flask, render_template, request, redirect
from flask_talisman import Talisman
from peewee import SqliteDatabase, Model

from dotenv import load_dotenv
import os

from models import item
from services.security import AuthenticateMiddleware
from authRoute import authProvider

app = Flask(__name__)

Talisman(app)

load_dotenv()

app.secret_key = os.getenv('secure_key', 'BAD SECRET KEY')

app.register_blueprint(authProvider)


db = SqliteDatabase(os.getenv('database_url'))

@app.before_request
def before():
    db.connect()


@app.after_request
def after(res):
    db.close()
    return res


@app.route('/')
@AuthenticateMiddleware
def home():

    items: Model = item.buildItem(None, db)

    return render_template('pages/home/home.html', 
                           url_link='create', 
                           itemsList=[item for item in items.select()][::-1],
                           log_out= 'logout')


@app.route('/create', methods=['GET', 'POST'])
@AuthenticateMiddleware
def create():

    if request.method == 'POST':
        items: Model = item.buildItem(None, db)

        if request.form['name_item'] and len(request.form['name_item']) > 1:
            items.create(name=request.form['name_item'])
            return redirect('/')

    return render_template('pages/create.html')


@app.route('/delete/<int:pk>')
@AuthenticateMiddleware
def delete(pk):

    items: Model = item.buildItem(None, db)

    items.delete_by_id(pk)
    return redirect('/')



if __name__ == '__main__':
    app.run()
