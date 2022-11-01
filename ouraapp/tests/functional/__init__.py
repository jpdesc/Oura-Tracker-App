from decorator import decorator
from flask.testing import FlaskClient


def login_user(sess, id):
    sess['_user_id'] = id


@decorator
def force_login(func, cb=None, *args, **kwargs):
    for arg in args:
        if isinstance(arg, FlaskClient):
            with arg:
                with arg.session_transaction() as sess:
                    cb(sess)
            return func(*args, **kwargs)
    return func(*args, **kwargs)
