import time

from BotInstagram import BotInstagram, existFollowsFile
from NetworkGraphs import NetworkGraph
from utilities import waitLoading

with open('pw.txt', 'r') as pw:
  password = pw.read()
user = "simplecomment"
target = "diegozeped.a"

bot = BotInstagram(user , password, target)

print("Iniciando bot Insta-Network.")
bot.auth()

bot.getFollowsFile(target)

print(f'Comenzando escaneo en red de amigos de {target}.')
time.sleep(3)

with open(f'Follows/{target}.txt', 'r') as targetFollows:
  usersFollow = list(targetFollows.readlines())
targetFollows.close()


for user in usersFollow:
  user = user.replace("\n", '')
  if not existFollowsFile(user):
    bot.driver.get(f"https://instagram.com/{user}/")
    waitLoading(4)
    bot.getInformationFile(user)
    waitLoading(3)
    bot.getFollowsFile(user)

bot.exit()

print("Red de escaneo de amigos completada.\n"
      "------------------------------------\n"
      "  Iniciado relaciones en gráficas.")

NetworkGraph("diegozeped.a")
