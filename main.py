import time

from BotInstagram import BotInstagram

# _____
from utilities import waitLoading

password = ""
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
  if (not bot.existFollowsList(user)):
    bot.driver.get(f"https://instagram.com/{user}/")
    waitLoading(4)
    bot.getInformationFile(user)
    waitLoading(3)
    bot.getFollowsFile(user)

print("Red de escaneo de amigos completada.\n"
      "-----------------------------------\n"
      "  Iniciado relaciones en gráficas.")


bot.exit()
