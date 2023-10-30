import requests
import json
import base64
from io import BytesIO
from PIL import Image
import cv2
import numpy as np

url = "http://127.0.0.1:5000/visualize"

Q = np.asarray(Image.open("./test_imgs/cell_t.jpg"))
R = np.asarray(Image.open("./test_imgs/cell_t.jpg"))
q = np.asarray(Image.open("./test_imgs/cell_t.jpg"))
r = np.asarray(Image.open('./test_imgs/g_plate.jpg'))


Q_ = cv2.imencode('.jpg',  cv2.cvtColor(Q, cv2.COLOR_BGR2RGB))[1].tobytes()
R_ = cv2.imencode('.jpg', cv2.cvtColor(R, cv2.COLOR_BGR2RGB))[1].tobytes()
q_ = cv2.imencode('.jpg', cv2.cvtColor(q, cv2.COLOR_BGR2RGB))[1].tobytes()
r_ = cv2.imencode('.jpg', cv2.cvtColor(r, cv2.COLOR_BGR2RGB))[1].tobytes()
annot_id = "1"

files = {'idx': json.dumps({'idx': annot_id}), 'Q': Q_, 'R': R_, 'q': q_, 'r': r_}

response = requests.post(url, files=files, timeout=0.1)

#Q_bytes = BytesIO()
#R_bytes = BytesIO()
#q_bytes = BytesIO()
#r_bytes = BytesIO()
#Q.save(Q_bytes, format="JPEG")
#R.save(R_bytes, format="JPEG")
#q.save(q_bytes, format="JPEG")
#r.save(r_bytes, format="JPEG")

# Send loaded PIL Images
#data = [
#    ('Q', ('Q', base64.b64encode(Q_bytes.getvalue()))),
#    ('R', ('R', base64.b64encode(R_bytes.getvalue()))),
#    ('q', ('q', base64.b64encode(q_bytes.getvalue()))),
#    ('r', ('r', base64.b64encode(r_bytes.getvalue()))),
#    ('idx', ('idx', json.dumps({'idx': 2}))),
#]

#r = requests.post(url, files=data)

# Loading from File
#files = [
#    ('Q', ('Q', open("./test_imgs/cell_t.jpg", 'rb'))),
#    ('R', ('R', open("./test_imgs/cell_t.jpg", 'rb'))),
#    ('q', ('q', open("./test_imgs/g_plate.jpg", 'rb'))),
#    ('r', ('r', open("./test_imgs/g_plate.jpg", 'rb'))),
#    ('idx', ('idx', json.dumps({'idx': 1}))),
#]

#r = requests.post(url, files=files)

print(response)

