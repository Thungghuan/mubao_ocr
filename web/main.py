from flask import Flask, send_from_directory, request
from flask_socketio import SocketIO, emit
import base64
from paddleocr import PaddleOCR
import tempfile

app = Flask("mubao_ocr")
app.config["SECRET_KEY"] = "mubao_ocr"
socketio = SocketIO(app)


def ocr(image):
    ocr = PaddleOCR(lang="ch", show_log=False)

    text_content = ""

    with tempfile.NamedTemporaryFile(mode="wb") as f:
        f.write(image)
        result = ocr.ocr(f.name, cls=False)[0]

        for line in result:
            text_content += line[-1][0] + "\n"

    return text_content


@app.route("/")
def root():
    return send_from_directory("web/mubao_ocr/dist", "index.html")


@app.route("/assets/<path:path>")
def assets(path):
    return send_from_directory("web/mubao_ocr/dist/assets", path)


@app.route("/vite.svg")
def favicon():
    return send_from_directory("web/mubao_ocr/dist", "vite.svg")


@app.route("/image/reg", methods=["POST"])
def add_reg_image():
    if request.method == "POST":
        image = base64.b64encode(request.files["image"].read())
        socketio.emit("regImage", image.decode("ascii"))
        result = ocr(image)
        socketio.emit("regReuslt", {"content": result})

    return "OK"


@app.route("/image/sim", methods=["POST"])
def add_sim_image():
    if request.method == "POST":
        image = base64.b64encode(request.files["image"].read())
        socketio.emit("simImage", image.decode("ascii"))
    return "OK"


@socketio.on("ping")
def ping_pong():
    emit("pong")
    print("pong")


socketio.run(app, host="0.0.0.0", port=8888)
