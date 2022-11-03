from configparser import ConfigParser
import werobot

config = ConfigParser()
config.read("config.ini")

token = config["werobot"]["token"]
host = config["werobot"]["host"]
port = config["werobot"]["port"]


robot = werobot.WeRoBot(token)


@robot.handler
def hello(message):
    return "Hello World!"


robot.run()
