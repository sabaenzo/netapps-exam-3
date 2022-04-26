from flask import Flask
from flask_httpauth import HTTPBasicAuth

from authenticate import Authenticator

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    auth = Authenticator()
    ret = auth.authenticate_record(username, password)
    if ret:
        return username


@app.route('/')
@auth.login_required
def index():
    return "Hello, {}!".format(auth.current_user())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=555)
