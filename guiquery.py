import requests
import base64
import io
from PIL import Image

status_url = "http://127.0.0.1:5000/status"
latest_url = "http://127.0.0.1:5000/get_latest"
idx_new_url = "http://127.0.0.1:5000/idx_new"

def get_status ():
    x = requests.get(status_url)
    print(x.text)
    return x.text

def get_img_idx ():
    i = requests.get(idx_new_url)
    #print(i.text)
    return i.text

def get_latest ():
    if get_status() == "1":
        img = requests.get(latest_url, params={'img_idx': get_img_idx()})
        img = base64.b64decode(img.content)
        img = Image.open(io.BytesIO(img))
        img.show()
    print("STOP")


if __name__ == "__main__":
    print("DEBUG")
    get_latest()
