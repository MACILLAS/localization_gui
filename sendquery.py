import requests
import json
import base64
from io import BytesIO
from PIL import Image

url = "http://127.0.0.1:5000/visualize"

Q = Image.open("./test_imgs/cell_t.jpg")
R = Image.open("./test_imgs/cell_t.jpg")
q = Image.open("./test_imgs/g_plate.jpg")
r = Image.open('./test_imgs/g_plate.jpg')

Q_bytes = BytesIO()
R_bytes = BytesIO()
q_bytes = BytesIO()
r_bytes = BytesIO()
Q.save(Q_bytes, format="JPEG")
R.save(R_bytes, format="JPEG")
q.save(q_bytes, format="JPEG")
r.save(r_bytes, format="JPEG")

# Send loaded PIL Images
data = [
    ('Q', ('Q', base64.b64encode(Q_bytes.getvalue()))),
    ('R', ('R', base64.b64encode(R_bytes.getvalue()))),
    ('q', ('q', base64.b64encode(q_bytes.getvalue()))),
    ('r', ('r', base64.b64encode(r_bytes.getvalue()))),
    ('idx', ('idx', json.dumps({'idx': 1}))),
]

r = requests.post(url, files=data)

# Loading from File
#files = [
#    ('Q', ('Q', open("./test_imgs/cell_t.jpg", 'rb'))),
#    ('R', ('R', open("./test_imgs/cell_t.jpg", 'rb'))),
#    ('q', ('q', open("./test_imgs/g_plate.jpg", 'rb'))),
#    ('r', ('r', open("./test_imgs/g_plate.jpg", 'rb'))),
#    ('idx', ('idx', json.dumps({'idx': 1}))),
#]

#r = requests.post(url, files=files)

print(r)

