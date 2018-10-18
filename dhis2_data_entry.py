# Author: Agnaldo Samuel
# Contact: agnaldosamuel3@gmail.com
from encodings.utf_8 import encode

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import yaml
import time
from selenium.webdriver.common.by import By
# def get_report_names(web_browser):
#     # Go to data export page
#     report_link = chrome_browser.find_element_by_link_text('Reporting')
#     report_link.click()
#     # Button to navigate through the reports . Can raise NoSuchElementException
#     div_paginate_next = web_browser.find_element_by_class_name('paginate_enabled_next')
#     report_names = []
#     # there are 4 pages in the report table list
#     for cont in range(1, 5):
#         if cont == 1:
#             # Go to first page
#             report_table = web_browser.find_element_by_class_name('reporting-data-table')
#             report_links = report_table.find_elements_by_xpath(".//td")
#             for i in report_links:
#                 report_names.append(i.text.encode('utf-8'))
#         if cont == 2:
#             # Go to second page
#             div_paginate_next.click()
#             report_table = web_browser.find_element_by_class_name('reporting-data-table')
#             report_links = report_table.find_elements_by_xpath(".//td")
#             for i in report_links:
#                 report_names.append(i.text.encode('utf-8'))
#         if cont == 3:  # Go to last page
#             div_paginate_next.click()
#             report_table = web_browser.find_element_by_class_name('reporting-data-table')
#             report_links = report_table.find_elements_by_xpath(".//td")
#             for i in report_links:
#                 report_names.append(i.text.encode('utf-8'))
#         if cont == 4:  # Go to  last  page
#             div_paginate_next.click()
#             report_table = web_browser.find_element_by_class_name('reporting-data-table')
#             report_links = report_table.find_elements_by_xpath(".//td")
#             for i in report_links:
#                 report_names.append(i.text.encode('utf-8'))
#     # Return to 1st pag on report table. Can raise NoSuchElementException
#     div_nav_pag_enabled_prev = web_browser.find_element_by_class_name('paginate_enabled_previous')
#     div_nav_pag_enabled_prev.click()
#     div_nav_pag_enabled_prev.click()
#     div_nav_pag_enabled_prev.click()
#     return report_names


# def select_report(report_name, web_browser):
#     report_names = get_report_names(web_browser)
#     # Navigating buttons. can raise NoSuchElementException
#     div_paginate_next = web_browser.find_element_by_class_name('paginate_enabled_next')
#
#     for report in report_names:
#         if report == report_name:
#             report_index = report_names.index(report_name)
#             if report_index <= 14:
#                 report_table = web_browser.find_element_by_class_name('reporting-data-table')
#                 report_lnk = report_table.find_element_by_link_text(report_name)
#                 report_lnk.click()
#                 break
#             if 14 < report_index <= 29:
#                 # Go to second page
#                 div_paginate_next.click()
#                 report_table = web_browser.find_element_by_class_name('reporting-data-table')
#                 report_lnk = report_table.find_element_by_link_text(report_name)
#                 report_lnk.click()
#                 break
#             if 29 < report_index <= 44:
#                 # Go to third page
#                 div_paginate_next.click()
#                 div_paginate_next.click()
#                 report_table = web_browser.find_element_by_class_name('reporting-data-table')
#                 report_lnk = report_table.find_element_by_link_text(report_name)
#                 report_lnk.click()
#             if report_index > 44:
#                 # Go to last page
#                 div_paginate_next.click()
#                 div_paginate_next.click()
#                 div_paginate_next.click()
#                 report_table = web_browser.find_element_by_class_name('reporting-data-table')
#                 report_lnk = report_table.find_element_by_link_text(report_name)
#                 report_lnk.click()
#                 break
#
#     return


# Read dhis2 credentials

with open("config.yaml", 'r') as stream:
    try:
        credentials = yaml.load(stream)
    except yaml.YAMLError as exc:
        print('Error reading credentials file' + exc.message)

username = credentials['dhis2_username']
password = credentials['dhis2_password']

# TODO: We must add implicit waits here, because loading dhis2 can take a while

# Login to dhis2

# Open chrome browser - Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    "download.default_directory=/home/asamuel/PycharmProjects/py-dhis-data-entry/data")
chrome_browser = webdriver.Chrome(chrome_options=chrome_options)
chrome_browser.get('http://197.249.5.100:8585/dhis/')
chrome_browser.find_element_by_id("j_username").send_keys(username)
chrome_browser.find_element_by_id("j_password").send_keys(password)
chrome_browser.find_element_by_id("submit").submit()

chrome_browser.implicitly_wait(10) #wait 10  seconds

chrome_browser.get('http://197.249.5.100:8585/dhis/dhis-web-dataentry/index.action')


def selectprovince(province_name,browser_webdriver):
    if province_name=='Cidade De Maputo':
        expand_prov_tree=browser_webdriver.find_element_by_xpath("//*[@id='orgUnitebcn8hWYrg3']/span/img")
        expand_prov_tree.click()
    elif province_name=='Inhambane':
        expand_prov_tree = browser_webdriver.find_element_by_xpath("//*[@id='orgUnitebcn8hWYrg3']/span/img")
        expand_prov_tree.click()
    else:
        print('No province provided')


selectprovince('Cidade De Maputo',chrome_browser)
# Look for data entry
#chrome_browser.find_element(By.XPATH, '//button[text()="Some text"]')
#data_entry = chrome_browser.find_element_by_xpath("//input[@type='text' or @id='undefined-Searchapps-undefined-63680']")
#data_entry.send_keys("data entry")

# start_date_element.send_keys('01-11-2016')
# end_date_element = chrome_browser.find_element_by_id('userEnteredParamendDate')
# end_date_element.send_keys('01-03-2017')
# us_element = Select(chrome_browser.find_element_by_id('userEnteredParams[location]'))
# # CS 1 Maio
# us_element.select_by_value('208')
# # output to
# output_element = Select(chrome_browser.find_element_by_name('selectedRenderer'))
# output_element.select_by_index(1)
# # run the report
# btn_request_report = chrome_browser.find_element_by_xpath("//input[@type='submit' and @value='Request Report']")
# btn_request_report.click()

# report_table = chrome_browser.find_element_by_class_name('reporting-data-table')
# report_links = report_table.find_elements_by_xpath(".//td")
# td = report_table.find_elements_by_xpath(".//a")
# for i in report_links:
# print i.text  # rel = get_report_names(chrome_browser)
# print len(rel)
# print rel

# select the report in reporting table;
# report_table = chrome_browser.find_element_by_class_name('reporting-data-table')
# selected_report = chrome_browser.find_element_by_link_text(report_table.text[0])
# reports = get_report_names(chrome_browser)
# td = report_table.find_elements_by_xpath(".//a")
# t = unicode(s, 'utf-8')
# for rep in reports:
#    # print encode(rep, 'utf-8')
#    print rep
#   #print rep[2:]

#   print i.text
#    print len(i)
# driver.find_element_by_link_text("showExportFormatDialog(&#039;ALL&#039;);")
# driver.execute_script("showExportFormatDialog(&#039;ALL&#039;)")
# driver.execute_script("document.getElementsByClassName('ui-button-text')[1].click()")
