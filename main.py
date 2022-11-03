from configparser import ConfigParser
import tempfile
import werobot
from werobot.replies import SuccessReply
import requests
from threading import Thread
from paddleocr import PaddleOCR

config = ConfigParser()
config.read("config.ini")

token = config["werobot"]["token"]


robot = werobot.WeRoBot(token)


def ocr_image(image_url, session):
    image = requests.get(image_url).content
    ocr = PaddleOCR(lang="ch", show_log=False)

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

    print('operation success')


@robot.image
def img_handler(message, session):
    Thread(target=ocr_image, args=(message.img, session)).start()
    return SuccessReply()


@robot.text
def text_handler(_, session):
    if "content" not in session or len(session["content"]) == 0:
        return "图片还没有处理完成哦"
    else:
        return "\n\n".join(session["content"])


robot.config["HOST"] = config["werobot"]["host"]
robot.config["PORT"] = config["werobot"]["port"]
robot.run()
