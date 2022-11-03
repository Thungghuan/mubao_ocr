from configparser import ConfigParser
import tempfile
import werobot
import requests
from paddleocr import PaddleOCR

config = ConfigParser()
config.read("config.ini")

token = config["werobot"]["token"]


robot = werobot.WeRoBot(token)


def ocr_image(image_url):
    image = requests.get(image_url).content
    ocr = PaddleOCR(lang="ch", show_log=False)

    text_content = ""

    with tempfile.NamedTemporaryFile(mode="wb") as f:
        f.write(image)
        result = ocr.ocr(f.name, cls=False)[0]

        for line in result:
            text_content += line[-1][0] + "\n"

    return text_content


# @robot.image 修饰的 Handler 只处理图片消息
@robot.image
def img(message):
    return ocr_image(message.img)


robot.config["HOST"] = config["werobot"]["host"]
robot.config["PORT"] = config["werobot"]["port"]
robot.run()
