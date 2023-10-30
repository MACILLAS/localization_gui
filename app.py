from PIL import Image
import flask
import json
import io
from io import StringIO, BytesIO
import base64

app_ = flask.Flask(__name__)

class RefReq:
    def __init__(self, v):
        self.value = v
        self.img_idx = "0"

event = RefReq("0")

class ImgStore:
    def __init__(self):
        self.index = []
        for i in range(100):
            self.index.append([])

    def get_latest(self, img_idx):
        return self.index[int(img_idx)][-1]

    def add(self, img_idx, image):
        self.index[int(img_idx)].append(image)

db = ImgStore()

@app_.route('/status', methods=['GET'])
def status():
    return event.value

@app_.route('/idx_new', methods=['GET'])
def status_idx_new():
    return event.img_idx

#def serve_pil_image(pil_img):
#    img_io = io.BytesIO() #StringIO()
#    #pil_img.save("Stuff.jpg")
#    pil_img.save(img_io, 'JPEG', quality=70)
#    img_io.seek(0)
#    return flask.send_file(img_io, mimetype='image/jpeg')

@app_.route('/get_latest', methods=['GET'])
def get_latest():
    img_idx = flask.request.args.get('img_idx')
    print(img_idx)

    if img_idx == event.img_idx:
        # Return the images and reset event flags
        event.value = "0"
        event.img_idx = "0"
        #print(type(db.get_latest(img_idx)))
        #serve_pil_image(db.get_latest(img_idx))
        buffered = BytesIO()
        db.get_latest(img_idx).save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return img_str

    return "OK"

@app_.route('/visualize', methods=['POST'])
def visualize():
    if flask.request.method == 'POST':

        ''' Extract the index. '''
        idx = json.load(flask.request.files['idx'])
        idx = idx['idx']


        '''  Extract images from File '''
        Q_img = flask.request.files["Q"]
        Q_img = Image.open(io.BytesIO(Q_img.read()))
        R_img = flask.request.files["R"]
        R_img = Image.open(io.BytesIO(R_img.read()))
        q_img = flask.request.files["q"]
        q_img = Image.open(io.BytesIO(q_img.read()))
        r_img = flask.request.files["r"]
        r_img = Image.open(io.BytesIO(r_img.read()))


        """
        Q_img = flask.request.files['Q'].read()
        Q_img = base64.b64decode(Q_img)
        Q_img = Image.open(io.BytesIO(Q_img))
        R_img = flask.request.files['R'].read()
        R_img = base64.b64decode(R_img)
        R_img = Image.open(io.BytesIO(R_img))

        q_img = flask.request.files['q'].read()
        q_img = base64.b64decode(q_img)
        q_img = Image.open(io.BytesIO(q_img))
        r_img = flask.request.files['r'].read()
        r_img = base64.b64decode(r_img)
        r_img = Image.open(io.BytesIO(r_img))
        """

        ''' Compose Images '''
        # r on Left q on Right
        r_img_size = r_img.size
        q_img_size = q_img.size
        q_img = q_img.resize(r_img_size)
        comp_image = Image.new('RGB', (2*r_img_size[0], r_img_size[1]), (250,250,250))
        comp_image.paste(r_img, (0, 0))
        comp_image.paste(q_img, (r_img_size[0], 0))

        ''' Save the Images to Memory & Set Flags '''
        event.img_idx = str(idx)
        event.value = "1"
        db.add(idx, comp_image)

    else:
        output = "POST only Plz!"
    output = "OK"
    return output

if __name__ == "__main__":
    #kwargs = {'host': '0.0.0.0', 'threaded': True, 'use_reloader': False, 'debug': True}
    #flaskThread = Thread(target=app_.run, daemon=True, kwargs=kwargs).start()
    app_.run(host="0.0.0.0", debug=True)