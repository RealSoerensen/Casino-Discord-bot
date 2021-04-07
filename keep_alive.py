from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Use this link to add the bot to your server: https://discord.com/api/oauth2/authorize?client_id=720669013402976318&permissions=0&scope=bot"


def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()

  