import requests
import os

from servicesKeys import token


def get_canvas_file(file_id: str) -> str:
    params = {"access_token": token}
    course_id = "145421"
    r = requests.get(
        f"https://vt.instructure.com/api/v1/courses/{course_id}/files/{file_id}", params=params)
    file = requests.get(r.json()["url"])
    with open(r.json()["display_name"], "wb") as f:
        f.write(file.content)
    return r.text


def upload_canvas_file(file_name: str) -> str:
    params = {"access_token": token,
              "name": file_name,
              }
    path = os.path.join(os.getcwd(), file_name)
    if not os.path.exists(path):
        return
    r = requests.post(
        f"https://vt.instructure.com/api/v1/users/self/files", params=params)
    with open(path, "rb") as f:
        out = requests.post(r.json()["upload_url"],
                            data=r.json()["upload_params"],
                            files={"file": f})
    return out.text