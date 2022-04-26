from flask import Flask, request, make_response
from flask_httpauth import HTTPBasicAuth
import re
import requests
import socket
from authenticate import Authenticator
import canvas
import json
from zeroconf import ServiceBrowser, ServiceListener, Zeroconf


class MyListener(ServiceListener):
    ipad = ""
    port = ""
    color= ""

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print(f"Service {name} added, service info: {info}")
        if name == "LEDrpi._http._tcp.local.":
            print("hello")
            print(socket.inet_ntoa(info.addresses[0]))
            self.ipad = str(socket.inet_ntoa(info.addresses[0]))
            print(self.ipad)
            self.port = str(info.port)
            v=info.properties[b'colors']
            self.color=v.decode()

    def get_ip(self):
        print(self.ipad)
        return self.ipad

    def get_port(self):
        return self.port
    def get_col(self):
        return self.color


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)


app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    authenticate = Authenticator()

    ret = authenticate.authenticate_record(username, password)

    if ret:
        return True

@auth.error_handler
def unauthorized():
    return make_response("Error (401 Unauthorized): Wrong username/password Combination",401)



@app.route('/Canvas', methods=['GET', 'POST'])
@auth.login_required
def Canvas():
    file_name = request.args.get("file", None)
    operation = request.args.get("operation", None)
    if not file_name or not operation or operation not in ["upload", "download"]:
        return "Missing parameters\n"
    if request.method == 'POST':
        if operation == "upload":
            return canvas.upload_canvas_file(file_name)
    elif request.method == 'GET':
        if operation == "download":
            return canvas.get_canvas_file(file_name)
    return "Invalid operation\n"


@app.route('/LED', methods=['GET', 'POST'])
@auth.login_required
def led():
    global listener
    if request.method =='GET':


            ipad=listener.get_ip()
            port=listener.get_port()
            print(listener.ipad)
            try:
                r = requests.get(f"http://{ipad}:{port}/LED")
                return r.text
            except requests.exceptions.InvalidURL:
                return make_response("Error! LED RPI and its services are not avaialble",400)


    elif request.method == 'POST':
        command = request.args.get("command", None)
        col=listener.get_col()
        pattern = rf"(on|off)-{col}-([0-9]+)"
        res = re.match(pattern, command)
        if col == "":
            return ("Error! LED RPI and its services are not avaialble", 400)
        if not res:
            return "Error"
        else:
            match = re.search(pattern, command)
            groups = match.groups()
            if len(groups) != 3:
                return "Error"

            ipad = listener.ipad
            port = listener.port


            try:
                r = requests.post(
                    f"http://{ipad}:{port}/LED?status={groups[0]}&color={groups[1]}&intensity={groups[2]}")
                return r.text
            except requests.exceptions.InvalidURL:
                return make_response("Error! LED RPI and its services are not avaialble",400)



@app.route('/Create', methods=['POST'])
def create():
    if request.method == 'POST':
        username = request.args.get("username", None)
        password = request.args.get("password", None)
        if not username or not password:
            return "Missing parameters\n"
        authenticate = Authenticator()
        ret = authenticate.insert_record(username, password)
        if ret:
            return "Success\n"
        else:
            return "Failed\n"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
