from decorator import decorator
from flask.testing import FlaskClient
from ouraapp.auth.routes import load_user


def login_user(sess, id):
    sess['_user_id'] = id
    sess['_fresh'] = True


@decorator
def force_login(func, cb=None, *args, **kwargs):
    for arg in args:
        if isinstance(arg, FlaskClient):
            with arg:
                with arg.session_transaction() as sess:
                    cb(sess)
            return func(*args, **kwargs)
    return func(*args, **kwargs)
