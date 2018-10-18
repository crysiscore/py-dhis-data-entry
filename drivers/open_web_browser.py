from selenium import webdriver
import yaml

# Read OpenMRS credentials
# with open("config.yaml", 'r') as stream:
#     try:
#         credentials = yaml.load(stream)
#     except yaml.YAMLError as exc:
#         print('Error reading credentials file' + exc.message)
#
# username = credentials['openmrs_username']
# password = credentials['openmrs_password']


# Open chrome browser - Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("download.default_directory=/home/agnaldo/PycharmProjects/py-dhis-data-entry/data")
chrome_browser = webdriver.Chrome(chrome_options=chrome_options)
chrome_browser.get('http://seleniumhq.org/')

# Login to OpenMRS
# chrome_browser.find_element_by_id("username").send_keys("")
# chrome_browser.find_element_by_id("password").send_keys(password)
btn_input = chrome_browser.find_element_by_xpath("//input[@type='input']")

print btn_input.location