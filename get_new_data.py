from selenium import webdriver
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import copyfile
import yaml


with open("config.yaml", 'r') as stream:
    try:
        credentials = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

username = credentials['openmrs_username']
password = credentials['openmrs_password']


driver_loc = "/usr/lib/chromium-browser/chromedriver"
os.environ["webdriver.chrome.driver"] = driver_loc

options = webdriver.ChromeOptions() 
options.add_argument("download.default_directory=/home/joebrew/Documents/zambezia/data")


# Modify original mintapi code to get to work locally
username = credentials['redcap_name']
password = credentials['redcap_password']
from selenium import webdriver
driver = webdriver.Chrome(driver_loc, chrome_options = options)

driver.get("https://sap.manhica.net:4703/redcap/")
driver.implicitly_wait(10)  # seconds

driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("login_btn").submit()

time.sleep(2)

# Go to data export
driver.get("https://sap.manhica.net:4703/redcap/redcap_v6.17.2/DataExport/index.php?pid=87")

# driver.find_element_by_link_text("showExportFormatDialog(&#039;ALL&#039;);")
# driver.execute_script("showExportFormatDialog(&#039;ALL&#039;)")
driver.execute_script("document.getElementsByClassName('ui-button-text')[1].click()")

# Click on csv export
e = driver.find_element_by_id('export_choices_table')
e.click()

from selenium.webdriver.common.action_chains import ActionChains

N = 13  # number of times you want to press TAB

actions = ActionChains(driver) 
for _ in range(N):
    actions = actions.send_keys(Keys.TAB)
actions.perform()

actions = ActionChains(driver) 
actions = actions.send_keys(Keys.RETURN)
actions.perform()

time.sleep(60)

# Specify download location
N = 3  # number of times you want to press TAB

actions = ActionChains(driver) 
for _ in range(N):
    actions = actions.send_keys(Keys.TAB)
actions.perform()


actions = ActionChains(driver) 
actions = actions.send_keys(Keys.RETURN)
actions.perform()

time.sleep(30)

# Get the name of the file
os.chdir('/home/joebrew/Downloads')
max_mtime = 0
for dirname,subdirs,files in os.walk("."):
    for fname in files:
        full_path = os.path.join(dirname, fname)
        mtime = os.stat(full_path).st_mtime
        if mtime > max_mtime:
            max_mtime = mtime
            max_dir = dirname
            max_file = fname

# Move file from downloads
destination_dir = '/home/joebrew/Documents/zambezia/data'
destination_file = destination_dir + '/' + max_file
copyfile(src = max_file, dst = destination_file)

# Print a message
print 'Done. File at ' + destination_file
# time.sleep(50)
# driver.close()