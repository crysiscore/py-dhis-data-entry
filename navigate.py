from encodings.utf_8 import encode
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import yaml
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helperfunctions import *
from openpyxl import load_workbook

indicators_files =['tb_prev.yaml','tx_tb_numerator.yaml','tx_tb_denominator.yaml','tx_rtt.yaml','tx_new.yaml','tx_ml.yaml','tx_curr.yaml',
                    'tv_pvls_numerator.yaml','tv_pvls_denominator.yaml','transferred_out.yaml','refused_treat.yaml',
                    'lftu_more_3_months.yaml','lftu_less_3_months.yaml','additional_data.yaml']

# Read dhis2 dhis_config
dhis_config = open_config_file("dhis_config.yaml")

username = dhis_config['dhis2_username']
password = dhis_config['dhis2_password']

district = dhis_config['distrito']
us_name = dhis_config['unidade_sanitaria']
period = dhis_config['periodo']
form_name = dhis_config['formulario']

#TODO (here) funcao para verificar a integridade dos parametros


# ficheiro de logs
# (same directory) in append mode and 
log_file = open("logs.txt","a+") 

# ler o ficheiro com dados
workbook = load_workbook(filename="data/albazine_ct.xlsx")
# grab the active worksheet
active_sheet =workbook['Sheet1']

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

time.sleep(5)
expand_province_tree('Cidade De Maputo',chrome_browser)
time.sleep(1)
expand_district_tree(district,chrome_browser)
time.sleep(2)
select_province(us_name, chrome_browser)
time.sleep(1)
select_form(form_name,chrome_browser)
time.sleep(1)
select_period(period,chrome_browser)
time.sleep(2)

tb_prev_file_full_path = "mapping/" + indicators_files[0]
tx_new_file_full_path  =  "mapping/" + indicators_files[4]
tx_curr_file_full_path =  "mapping/" + indicators_files[6]

#indicator_map_file,active_sheet,log_file,browser_webdriver)
#fill_indicator_elements('TB_PREV_NUMERATOR', tb_prev_file_full_path,active_sheet,log_file,chrome_browser)

#fill_indicator_elements('TX_NEW', tx_new_file_full_path,active_sheet,log_file,chrome_browser)

fill_indicator_elements('TX_CURR', tx_curr_file_full_path,active_sheet,log_file,chrome_browser)
time.sleep(20)

#chrome_browser.quit()
