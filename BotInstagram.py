import json
import os.path
import time
from pickle import dump, load
from random import randint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utilities import waitLoading


class BotInstagram:
    # XPaths
    xPathSeguidores = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a'

    # Cookies Path
    cookiesPath = "cookies.pkl"

    def __init__(self, user, pw, target):
        # Setup variables
        self.user = user
        self.pw = pw
        self.target = target if target != None else user

        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=.chrome-data")
        mobile_emulation = {
            "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}

        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.get(f'https://instagram.com/{self.target}/')
        print(f"Bot instanciado para {target}.")

    def exit(self):
        self.driver.close()
        del (self)

    def auth(self):

        tErrorXPath = '//*[@id="slfErrorAler..t"]'

        xPathLogin = '//*[@id="react-root"]/section/nav/div/div/div[2]/div/div/div/a[1]'
        xPathUser = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input'
        xPathPw = '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input'

        time.sleep(2)
        if self.isSessionSaved():
            self.load_session()
            self.driver.get(f'https://instagram.com/{self.target}/')
        time.sleep(2)

        isAuthenticated = True if len(self.driver.find_elements_by_xpath(xPathLogin)) == 1 else False

        if (isAuthenticated):
            print(f"Iniciando sesion en {self.user}.")
            bEntrar = self.driver.find_element_by_xpath(xPathLogin)
            bEntrar.click()
            time.sleep(3)
            self.driver.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/article/div/div/div/div/div[1]/button/span').click()
            time.sleep(20)
            """
            user_box = self.driver.find_element_by_xpath(xPathUser)
            user_box.send_keys(self.user)

            pw_box = self.driver.find_element_by_xpath(xPathPw)
            pw_box.send_keys(self.pw)

            time.sleep(randint(1, 4))

            user_box.submit()
            self.driver.implicitly_wait(3)
            tError = self.driver.find_elements_by_xpath(tErrorXPath)
            if (len(tError) != 0):
                raise Exception(tError[0].get_attribute("innerHTML").splitlines()[0])
            """
            self.save_session()

        else:
            pass
            # ........bPerfil = self.driver.find_element_by_xpath(bPerfilXPath)
            # userInited = bPerfil.get_attribute('href').replace('/', '').replace('https:www.instagram.com', '')
            # print(f"Sesion ya iniciada en {userInited}")

    def save_session(self):
        with open(self.cookiesPath, 'wb') as filehandler:
            dump(self.driver.get_cookies(), filehandler)

    def load_session(self):
        with open(self.cookiesPath, 'rb') as cookiesfile:
            cookies = load(cookiesfile)
            for cookie in cookies:
                if "expiry" in cookie:
                    cookie['expiry'] = int(cookie['expiry'])
                self.driver.add_cookie(cookie)

    def isSessionSaved(self):
        with open(self.cookiesPath, 'rb') as cookiesfile:
            cookies = cookiesfile.readlines()
            if (len(cookies) != 0):
                return True
            else:
                return False
    def getFollowsFile(self, user):
        def scrollAllPage1():
            scheight = 3.5
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:

                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight /% s);" % scheight)
                scheight += .1111

                time.sleep(0.1)

                # if (len(self.driver.find_elements_by_class_name('QN7kB')) == 1):
                #    error = True
                #    break

                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

        def scrollAllPage2():
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                waitLoading(10)
                # if (len(self.driver.find_elements_by_class_name('QN7kB')) == 1):
                #    error = True
                #    break
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

        def saveFollowersFile(user, list):
            username = lambda userElement: userElement.find_element_by_css_selector(
                'div>div.t2ksc>div.enpQJ>div.d7ByH>a').text

            print('Guardando nuevo archivo...')

            followsFile = open(f"Follows/{user}.txt", "w")
            for _user in usersLoaded:
                if (len(_user.find_elements_by_class_name('coreSpriteVerifiedBadge')) == 0):
                    print(username(_user), file=followsFile)
            followsFile.close()

            print(f'Seguidos de {user} finalizado.')

        user = user.replace('\n', '')
        tFollowsXPath = '//*[@id="react-root"]/section/main/div/ul/li[3]/a/span'
        usersXPath = '//*[@id="react-root"]/section/main/div[2]/ul/div/li'
        tFollowersXPath = '//*[@id="react-root"]/section/main/div/ul/li[3]/a/span'

        bFollowsLen = len(self.driver.find_elements_by_xpath(tFollowsXPath))

        isFamous = False

        try:
            int(self.driver.find_element_by_xpath(tFollowersXPath).text.replace('.', ''))
        except:
            isFamous = True

        while not existFollowsFile(user) and bFollowsLen != 0 and not isFamous:
            time.sleep(2)
            bFollows = self.driver.find_element_by_xpath(tFollowsXPath)
            try:
                if int(bFollows.text.replace('.', '')) > 1500:
                    break
            except:
                break
            print(f'Seguidos de {user} comenzando. [{bFollows.text} seguidos]')

            bFollows.click()
            waitLoading(3)

            scrollAllPage2()

            if len(self.driver.find_elements_by_css_selector(
                    '#react-root>section>main>div:nth-child(3)>ul>div>li.wo9IH.QN7kB>div')) == 1:
                seg = randint(1300,2000)
                print(f"NOS DETECTARON. ESPERANDO {seg} SEGUNDOS.")
                waitLoading( 3)
                time.sleep(seg)
                self.driver.execute_script("location.reload();")
                waitLoading(10)
                continue

            usersLoaded = self.driver.find_elements_by_xpath(usersXPath)

            try:
                saveFollowersFile(user, usersLoaded)
                break
            except:
                Exception('Ha ocurrido un error al guardar.')

        else:
            if bFollowsLen == 0:
                print(f"[PRIVADA] No se han podido obtener los seguidores de: {user}")
                followsFile = open(f"Follows/{user}.txt", "w+")
                time.sleep(1)
                followsFile.close()


            elif isFamous:
                print(f"[FAMOSA] No se han podido obtener los seguidores de: {user}")
                followsFile = open(f"Follows/{user}.txt", "w+")

                time.sleep(1)
                followsFile.close()



    def getInformationFile(self, user):
        user = user.replace("\n", "")

        x = '//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/h2'
        if len(self.driver.find_elements_by_xpath(x)) == 0:
            followersXPath = '//*[@id="react-root"]/section/main/div/ul/li[2]/a/span'
            followsXPath = '//*[@id="react-root"]/section/main/div/ul/li[3]/a/span'
        else:
            followersXPath = '//*[@id="react-root"]/section/main/div/ul/li[2]/span/span'
            followsXPath = '//*[@id="react-root"]/section/main/div/ul/li[3]/span/span'

        userXPath = '//*[@id="react-root"]/section/main/div/header/section/div[1]/h1'
        nameXPath = '//*[@id="react-root"]/section/main/div/div[1]/h1'
        descXPath = '//*[@id="react-root"]/section/main/div/div[1]/span'
        pubsXPath = '//*[@id="react-root"]/section/main/div/ul/li[1]/span/span'

        gET = lambda xpath: self.driver.find_element_by_xpath(xpath).text
        info = dict()

        info['username'] = gET(userXPath)

        if len(self.driver.find_elements_by_xpath(nameXPath)) == 1:
            info['name'] = gET(nameXPath).encode("utf-8", "replace").decode()

        if len(self.driver.find_elements_by_xpath(descXPath)) == 1:
            info['description'] = gET(descXPath).encode("utf-8", "replace").decode()

        if len(self.driver.find_elements_by_xpath(pubsXPath)) == 1:
            info['nPubs'] = gET(pubsXPath)

        if len(self.driver.find_elements_by_xpath(followsXPath)) == 1:
            info['nFollows'] = gET(followsXPath)

        if len(self.driver.find_elements_by_xpath(followersXPath)) == 1:
            info['nFollowers'] = gET(followersXPath)

        infoFile = open(f'Info/{user}.txt', "w")
        json.dump(info, infoFile)
        infoFile.close()


def existFollowsFile(user):
    if os.path.exists(f'Follows/{user}.txt'):
        return True
    else:
        return False


def existInfoFile(user):
    if os.path.exists(f'Follows/{user}.txt'):
        return True
    else:
        return False
