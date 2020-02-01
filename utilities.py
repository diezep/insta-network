from random import randint
from time import sleep

randFloat = lambda min, max: float(randint(min, max) + randint(1, min) / randint(min + 1, max))


def waitForClick(driver, element_xpath):
    element = driver.find_element_by_xpath(element_xpath)
    element.click()

    driver.implicitly_wait(randFloat(2, 4))

    while True:
        page_state = driver.execute_script(
            'return document.readyState;'
        )
        if page_state == 'complete': break

        sleep(randFloat(1, 2))


waitLoading = lambda max: sleep(2 + randFloat(1, max))
