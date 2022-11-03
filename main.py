from configparser import ConfigParser
import tempfile
import werobot
from werobot.replies import SuccessReply
from werobot.utils import to_binary
import requests
from threading import Thread
from paddleocr import PaddleOCR

config = ConfigParser()
config.read("config.ini")

token = config["werobot"]["token"]


robot = werobot.WeRoBot(token)


def ocr_image(image_url, id):
    image = requests.get(image_url).content
    ocr = PaddleOCR(lang="ch", show_log=False)

    session = robot.session_storage[id]

    text_content = ""

    with tempfile.NamedTemporaryFile(mode="wb") as f:
        f.write(image)
        result = ocr.ocr(f.name, cls=False)[0]

        for line in result:
            text_content += line[-1][0] + "\n"

    if "content" not in session or len(session["content"]) == 0:
        session["content"] = [text_content]
    else:
        session["content"].append(text_content)

    robot.session_storage[id] = session

    print("operation success")


@robot.image
def img_handler(message, session):
    id = to_binary(message.source)
    Thread(target=ocr_image, args=(message.img, id)).start()
    return SuccessReply()


@robot.text
def text_handler(_, session):
    if "content" not in session or len(session["content"]) == 0:
        return "图片还没有处理完成哦"
    else:
        result = []
        for _ in len(session["content"]):
            result.append(session["content"].pop(0))

        return "\n\n".join(result)


robot.config["HOST"] = config["werobot"]["host"]
robot.config["PORT"] = config["werobot"]["port"]
robot.run()
