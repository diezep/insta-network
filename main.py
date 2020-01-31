import time

from BotInstagramNetwork import BotInstaNetwork as Bot

# _____
password = ""
with open('pw.txt', 'r') as pw:
  password = pw.read()
bot = Bot("simplecomment", password, "diegozeped.a")
bot.iniciar()
