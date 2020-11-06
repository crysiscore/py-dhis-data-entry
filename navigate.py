# Author: Agnaldo Samuel
# Contact: agnaldosamuel3@gmail.com
from encodings.utf_8 import encode

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import yaml
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helperfunctions import expand_province_tree , expand_district_tree , open_config_file



# Read dhis2 credentials
credentials = open_config_file("dhis-login.yaml")

username = credentials['dhis2_username']
password = credentials['dhis2_password']

# Open chrome browser - Chrome options

driver_loc = "/usr/bin/chromedriver"
chrome_options = webdriver.ChromeOptions()
#TODO 
# default_directory  must be a configurable parameter, and thus should be written to a file
chrome_options.add_argument(
    "download.default_directory=/home/agnaldo/Git/py-dhis-data-entry/downloads")
    
chrome_browser = webdriver.Chrome(driver_loc, options=chrome_options) #Optional argument, if not specified will search path.
#TODO 
# DHIS url must be a configurable parameter, and thus should be written to a file
chrome_browser.get('http://localhost:9090/dhis/')
chrome_browser.find_element_by_id("j_username").send_keys(username)
chrome_browser.find_element_by_id("j_password").send_keys(password)
chrome_browser.find_element_by_id("submit").click()


chrome_browser.get('http://localhost:9090/dhis/dhis-web-dataentry/index.action')

time.sleep(6)
expand_province_tree('Cidade De Maputo',chrome_browser)
time.sleep(1)
expand_district_tree('Katembe',chrome_browser)




"""
#def selectprovince(province_name,browser_webdriver):
    #chrome_browser.implicitly_wait(10)
    #chrome_browser=chrome_browser.find_element_by_xpath("//li[@id='orgUnitj9Inbtfw3Wu']/span[contains(@class,'toggle')]")
    #expand_root_tree=browser_webdriver.find_element_by_xpath("//li[@id='orgUnitwafWzemVbX4']/a[contains(@class, 'selected')]")
    #expand_root_tree.click()
   if province_name=='Cidade De Maputo':
            expand_prov_tree=chrome_browser.find_element_by_xpath("//*[@id='orgUnitebcn8hWYrg3']/span[1]")
            expand_prov_tree.click()
        elif province_name=='Inhambane':
            expand_prov_tree = chrome_browser.find_element_by_xpath("//*[@id='orgUnitebcn8hWYrg3']/span/img")
            expand_prov_tree.click()
        else:
            print('No province provided') """


#selectprovince('Cidade De Maputo',chrome_browser)
