import re
from selenium.webdriver.common.by import By
def Connect_To_Lichess(driver):
    """
    """
    driver.get("https://lichess.org/login")
    # Connect to lichess.org
    Username = driver.find_element(by=By.ID, value="form3-username")
    Password = driver.find_element(by=By.ID, value="form3-password")

    Username.send_keys("mathematical_gambler")
    Password.send_keys("24989127aZ")# Privacy violation

    Log_in_button = driver.find_element(By.CSS_SELECTOR, "#main-wrap > main > form > div.one-factor > button")
    Log_in_button.click()


# Keyboard_commands
def Keyboard_commands(driver, command):
    """
    command: keyboard notations to be played
    """
    Keyboard = driver.find_element(By.CSS_SELECTOR, "#main-wrap > main > div.round__app.variant-standard > div.keyboard-move > input") # 
    Keyboard.clear()
    Keyboard.send_keys(command)
