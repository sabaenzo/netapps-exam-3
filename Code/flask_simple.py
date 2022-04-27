from flask import Flask, request
from flask import render_template

app = Flask(__name__)


@app.route("/")
def get_some_info():
    print("Hello world!")
    return "nothing"


# curl -d "name=enzo&last_name=saba" -X POST http://127.0.0.1:5000/send
@app.route("/send", methods=['POST', 'GET'])
def receive_info():
    if request.method == 'POST':
        print(f"Received a {request.method} request to {request.path}: {request.form}")
        return "Thank you for posting"
    else:
        return "Please only use this route for posting data"


@app.route("/file")
def show_file(name=None):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    app.run(port=5000, debug=True)

