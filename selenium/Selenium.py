
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

""" Import WebDriver Manager for Python """
from webdriver_manager.chrome import ChromeDriverManager



""" setting the Extension Integration """
options = webdriver.ChromeOptions()
options.add_extension('/home/cuore-pc/Programming/Projects/ASR_Chess/extension_6_3_0_0.crx')

""" Use install() to get the location used by the manager and pass it to the driver in a service class instance:
"""
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

###
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = webdriver.ChromeOptions()
options.add_extension('/home/cuore-pc/Programming/Projects/ASR_Chess/extension_6_3_0_0.crx')
driver = webdriver.Chrome(options=options) 
driver.get('http://www.google.com')
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
