from peewee import SqliteDatabase, Model, DoesNotExist
from flask import redirect, session
import bcrypt

from models.user import buildUser

from services.cryptoService import cryptoService

from dotenv import load_dotenv
import os

load_dotenv()

db = SqliteDatabase(os.getenv('database_url'))


def authenticate(subject: str, password: str):

    if subject and password:

        if type(subject) == str and type(password) == str and '=' not in subject:

            db.connect()

            User: Model = buildUser(db)

            result: Model = User.get(User.username == subject) or None

            if result is not None:

                check = result.password

                transform = cryptoService()

                check: bytes = transform.decrypt(
                    check, os.environ.get('crypt_key', False))

                if bcrypt.checkpw(password.encode('utf8'), check):
                    return result

            db.close()

    return False


def Login(subject, password):

    subject = authenticate(subject=subject, password=password)

    if subject:
        
        transform = cryptoService()

        return transform.crypt(password, os.environ.get('crypt_key', False))

    return False           


def AuthenticateMiddleware(route):

    def inner(*args, **kargs):

        authHeader: dict = session.get('sec_key', False)

        if authHeader:
            
            subject = authHeader.get('subject', False)
            
            pwd = authHeader.get('pwd', False)
            
            transform = cryptoService()
            
            pwd = transform.decrypt(pwd, os.environ.get('crypt_key', False))

            tmp = Login(subject,
                        pwd.decode('utf8'))
            if tmp:

                return route(*args, **kargs)

        return redirect('/login')

    inner.__name__ = route.__name__

    return inner


def RegisterUser(subject: str, password: str):

    if subject and password:

        if type(subject) == str and type(password) == str and '=' not in subject:

            model: Model = buildUser(db)

            try:
                exist = model.select().where(model.username == subject)

                if not exist:

                    raise DoesNotExist

            except DoesNotExist:

                salt = bcrypt.gensalt()
                pwd = bcrypt.hashpw(password.encode('utf8'), salt)

                transform = cryptoService()

                pwd: bytes = transform.crypt(
                    pwd, os.environ.get('crypt_key', False))

                try:

                    model.create(username=subject,
                                 password=pwd.decode('utf8'))

                    return transform.crypt(password, os.environ.get('crypt_key', False))

                except Exception as err:

                    print(err)

                    return False

    return False
