import re
import getpass
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import getpass


def Connect_To_Lichess(driver):
    """
    """
    driver.get("https://lichess.org/login")
    # Connect to lichess.org
    Username = driver.find_element(by=By.ID, value="form3-username")
    Password = driver.find_element(by=By.ID, value="form3-password")

    Username.send_keys("mathematical_gambler")
    try:
        p = getpass.getpass()
    except Exception as error:
        print('ERROR', error)
    else:
        Password.send_keys(p)
    Selector = "#main-wrap > main > form > div.one-factor > button"
    Log_in_button = driver.find_element(By.CSS_SELECTOR, Selector)
    Log_in_button.click()


# Keyboard_commands
def Keyboard_commands(driver, command):
    """
    command: keyboard notations to be played
    """
    Selector = "#main-wrap > main > div.round__app.variant-standard > div.keyboard-move > input"
    Keyboard = driver.find_element(By.CSS_SELECTOR, Selector)
    Keyboard.clear()
    Keyboard.send_keys(command)
    Keyboard.send_keys(Keys.RETURN)
    sleep(1)


def Waiting_Myturn(driver):
    """
    Function that listen to an element indicating whether it
    is our turn to play.
    """
    print("Waiting Turn")
    wait = WebDriverWait(driver, 10000)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//title[contains(text(),'Your turn')]")))
    print("Your Turn, Speak your move")
