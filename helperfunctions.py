from pickle import FALSE
import shutil
import sys
import yaml
import time
import requests
import platform
import os
from config.extra_config import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import urllib.request
import zipfile

def open_config_file(filename):
    with open(filename, 'r', encoding='ISO-8859-1') as f:
        try:
            dict = yaml.safe_load(f)
        except IOError as err:
            print ("error while reading file" + filename + 'Details:' + str(err.args))
        except yaml.YAMLError as exc:
            print ("error while reading file" + filename + 'Details:' + str(exc.args))
    return dict


def get_district_position(distrit_name):
    return dict_distritos_maputo.index(distrit_name)

def get_province_position(province_name):
    return unidades_sanitarias.index(province_name)

def expand_province_tree(province_name, browser_webdriver):
    if province_name == 'Cidade De Maputo':
        wait = WebDriverWait(browser_webdriver, 10)
        xpath="//li[@id='orgUnitebcn8hWYrg3']/span/img"
        #expand_prov_tree = browser_webdriver.find_element_by_xpath("//li[@id='orgUnitebcn8hWYrg3']/span/img")
        expand_prov_tree =wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        expand_prov_tree.click()
    elif province_name == 'Inhambane':
        expand_prov_tree = browser_webdriver.find_element_by_xpath("//li[@id='orgUnitebcn8hWYrg3']/span/img")
        expand_prov_tree.click()
    else:
        print('No province provided')


def expand_district_tree(district_name,browser_webdriver):
   
    dictionary = open_config_file('config/org_units.yaml')
    index = get_district_position(district_name)
    print(index)
    xpath = dictionary['distritos'][index][district_name]['xpath']
    print(xpath)
    wait = WebDriverWait(browser_webdriver, 10)
    #expand_prov_tree = browser_webdriver.find_element_by_xpath("//li[@id='orgUnitebcn8hWYrg3']/span/img")
    district_element =wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    #district_element= browser_webdriver.find_element_by_xpath(xpath)
    district_element.click()
  

def select_province(province_name,browser_webdriver):
    
    dictionary = open_config_file('config/org_units.yaml')
    index = get_province_position(province_name)
    xpath = dictionary['unidades_sanitarias'][index][province_name]['xpath']
    #name = dictionary['unidades_sanitarias'][index][province_name]['name']
    #province = dictionary['unidades_sanitarias'][index][province_name]['province']
    #district = dictionary['unidades_sanitarias'][index][province_name]['district']
    wait = WebDriverWait(browser_webdriver, 10)
    #expand_prov_tree = browser_webdriver.find_element_by_xpath("//li[@id='orgUnitebcn8hWYrg3']/span/img")
    province_element =wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))  
    #province_element= browser_webdriver.find_element_by_xpath(xpath)
    province_element.click()

def check_us_in_district(us_name,district_name):
    dictionary = open_config_file('config/org_units.yaml')
    org_units = dictionary['unidades_sanitarias']
    found = False
    for  i  in range(len(org_units)):
        
        value = str(org_units[i])
        f_index = value.find("{'")
        s_index = value.find("': {")
        nome_us_no_dhis = value[f_index+2:s_index]
        if us_name == nome_us_no_dhis:
            distrito = str(org_units[i][us_name]['district'])
            if distrito == district_name:
                 print("found!")
                 return(True)
            else: 
                return(False)
    return(found)       

 
def select_form(form_name, browser_webdriver ):
     #select_form_box_element = browser_webdriver.find_element_by_xpath("//*[@id='selectedDataSetId']")
     #select_form_box_element.click()
     #form_name ='C&T_Resumo de Cuidados e Tratamento'
     xpath = "//select[@name='selectedDataSetId']/option[text()=" + "'" + form_name + "' ]"
     #print(xpath)
     wait = WebDriverWait(browser_webdriver, 10)
     #expand_prov_tree = browser_webdriver.find_element_by_xpath("//li[@id='orgUnitebcn8hWYrg3']/span/img")
     form_element =wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))  
     #form_element = browser_webdriver.find_element_by_xpath(xpath).click()
     form_element.click()

def exccutar_validacao(browser_webdriver):
    time.sleep(2) 
    btn_validate =  browser_webdriver.find_element_by_xpath('//input[@id="validateButton"][@value="Executar validação"][@style="width:120px margin-bottom: 3px"][@style=""]')
    btn_validate.click()


def select_period(periodo,browser_webdriver):
    xpath = "//select[@name='selectedPeriodId']/option[text()=" + "'" + periodo + "' ]"
    #print(xpath)
    wait = WebDriverWait(browser_webdriver, 10)
    periodo_element=wait.until(EC.element_to_be_clickable((By.XPATH, xpath))) 
    #periodo_element = browser_webdriver.find_element_by_xpath(xpath)
    periodo_element.click()

def fill_indicator_elements(indicator_name,indicator_map_file,active_sheet,log_file,browser_webdriver,tipo_entrada):
    
    indicator_yaml = open_config_file(indicator_map_file)

    if tipo_entrada=='Nao': # tipo_entrada refers to  the program behaviour beforre  entering the data ie override (tipo_entrada=='Sim')or normal entry-> tipo_entrada=='Nao'
        for k in range(len(indicator_yaml[indicator_name])):
            key = str(indicator_yaml[indicator_name][k].keys())
            f_index = key.find("['")
            s_index = key.find("']")
            indicator = key[f_index+2:s_index]
            #print(indicator)
            xpath = indicator_yaml[indicator_name][k][indicator]['xpath']
            cell_ref = indicator_yaml[indicator_name][k][indicator]['cell']
            
            try:
                cell_value = active_sheet[cell_ref].value
                if cell_value is None:
                    #skip 
                    print (cell_ref + " esta vazia no ficheiro excell.")
                    log_file.write(cell_ref + " esta vazia no ficheiro excell." + '\n' ) 
                else:
                    print(cell_ref +" : " + str(cell_value))
                    input_element = browser_webdriver.find_element_by_xpath(xpath)
                    input_element.send_keys(int(cell_value))

            except Exception as e:
                print("Algum erro ocorreu no campo : %s" % indicator )
                print(str(e) )        
                log_file.write("Algum erro ocorreu no campo  : %s" % indicator + '\n')
                print("Algum erro ocorreu no campo  : %s" % indicator + '\n')
                #log_file.close()
    elif tipo_entrada=='Sim':
        for k in range(len(indicator_yaml[indicator_name])):
            key = str(indicator_yaml[indicator_name][k].keys())
            f_index = key.find("['")
            s_index = key.find("']")
            indicator = key[f_index+2:s_index]
            #print(indicator)
            xpath = indicator_yaml[indicator_name][k][indicator]['xpath']
            cell_ref = indicator_yaml[indicator_name][k][indicator]['cell']
            
            try:
                cell_value = active_sheet[cell_ref].value
                if cell_value is None:
                    #skip 
                    print (cell_ref + " esta vazia no ficheiro excell.")
                    log_file.write(cell_ref + " esta vazia no ficheiro excell." + '\n' ) 
                else:
                    print(cell_ref +" : " + str(cell_value))
                    input_element = browser_webdriver.find_element_by_xpath(xpath)
                    input_element.clear()
                    input_element.send_keys(int(cell_value))

            except Exception as e:
                print("Algum erro ocorreu no campo : %s" % indicator )
                print(str(e) )        
                log_file.write("Algum erro ocorreu no campo  : %s" % indicator + '\n')
                print("Algum erro ocorreu no campo  : %s" % indicator + '\n')
             

def check_ct_template_integrity(active_sheet, log_file ):
       cell_ref_trimestral = active_sheet['K2'].value  # must be Trimestral
       cell_ref_semestral  = active_sheet['N2'].value  # must be Semestral
       cell_ref_tx_new     = active_sheet['A16'].value  # must be TX_NEW
       cell_ref_tx_curr  = active_sheet['A26'].value  # must be TX_CURR
       cell_ref_tx_curr_less_3m = active_sheet['J35'].value  # must be <3 months of ARVs (not MMD) 
       cell_ref_tx_pvls_brestfeeding = active_sheet['A135'].value  # must be Breastfeeding
       cell_ref_add_data_geral = active_sheet['M143'].value  # must be GERAL
       cell_ref_tx_rtt_people_prison = active_sheet['L47'].value # must be People in prison and other closed settings

       if cell_ref_trimestral!='Trimestral':
           print(cell_ref_trimestral)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula K2 deve ter o valor: Trimestral\n'  )
           print('Ha um erro no template excell.\n' )
           print('A celula K2 deve ter o valor: Trimestral\n'  )
           return(False)
       elif cell_ref_semestral!='Semestral':
           print(cell_ref_semestral)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula N2 deve ter o valor: Semestral\n'  )
           print('Ha um erro no template excell.\n'  )
           print('A celula N2 deve ter o valor: Semestral\n'  )
           return(False) 
    
       elif cell_ref_tx_new!='TX_NEW' :
           print(cell_ref_tx_new)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula A16 deve ter o valor: TX_NEW\n'  )
           print('Ha um erro no template excell.\n'  )
           print('A celula A16 deve ter o valor: TX_NEW\n'  )
           return(False) 
       elif cell_ref_tx_curr!='TX_CURR':
           print(cell_ref_tx_curr)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula A26 deve ter o valor: TX_CURR\n'  )
           print('Ha um erro no template excell.\n'  )
           print('A celula A26 deve ter o valor: TX_CURR\n'  )
           return(False) 
       elif cell_ref_tx_curr_less_3m!='6 or more months of ARVs':
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula J35 deve ter o valor: 6 or more months of ARVs\n'  )
           print(cell_ref_tx_curr_less_3m)
           print('Ha um erro no template excell.\n'  )
           print('A celula J35 deve ter o valor: 6 or more months of ARVs\n'  )
           return(False) 
       elif cell_ref_tx_pvls_brestfeeding!='Breastfeeding':
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula A135 deve ter o valor: Breastfeeding\n'  )
           print(cell_ref_tx_pvls_brestfeeding)
           print('Ha um erro no template excell.\n'  )
           print('A celula A135 deve ter o valor: Breastfeeding\n'  )
           return(False) 
       elif cell_ref_add_data_geral!='GERAL':
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula M143 deve ter o valor: GERAL\n'  )
           print(cell_ref_add_data_geral)
           print('Ha um erro no template excell.\n'  )
           print('A celula M143 deve ter o valor: GERAL\n'  )
           return(False) 
       elif cell_ref_tx_rtt_people_prison!='People in prison and other closed settings':
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula L47 deve ter o valor: People in prison and other closed settings\n'  )
           print(cell_ref_tx_rtt_people_prison)
           print('Ha um erro no template excell.\n'  )
           print('A celula L47 deve ter o valor: People in prison and other closed settings\n'  )
           return(False) 
       else:
           return(True)

def check_ptv_template_integrity(active_sheet, log_file ):
       cell_ref_main_title = active_sheet['C3'].value  # must be PMTCT Form for CCS DHIS2
       cell_ref_cpn_title  = active_sheet['B5'].value  # must be  CPN
       cell_ref_ccr_title  = active_sheet['B31'].value  # must be CCR
       cell_ref_maternidade_title = active_sheet['B43'].value  # must be Maternidade
      

       if cell_ref_main_title !='PMTCT Form for CCS DHIS2':
           print(cell_ref_main_title)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula C3 deve ter o valor: PMTCT Form for CCS DHIS2\n'  )
           print('Ha um erro no template excell.\n' )
           print('A celula C3 deve ter o valor: PMTCT Form for CCS DHIS2\n'  )
           return(False)
       elif cell_ref_cpn_title!='CPN':
           print(cell_ref_cpn_title)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula B5 deve ter o valor: CPN\n'  )
           print('Ha um erro no template excell.\n'  )
           print('A celula B5 deve ter o valor: CPN\n'  )
           return(False) 
    
       elif cell_ref_ccr_title!='CCR' :
           print(cell_ref_ccr_title)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula B31 deve ter o valor: CCR\n'  )
           print('Ha um erro no template excell.\n'  )
           print('A celula B31 deve ter o valor: CCR\n'  )
           return(False) 
       elif cell_ref_maternidade_title!='Maternidade':
           print(cell_ref_maternidade_title)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula B43 deve ter o valor: Maternidade\n'  )
           print('Ha um erro no template excell.\n'  )
           print('A celula B43 deve ter o valor: Maternidade\n'  )
           return(False) 
       else:
           return(True)
    
def check_retencao_dsd_template_integrity(active_sheet, log_file ):
       cell_ref_cohort= active_sheet['A4'].value  # must have the value 'Cohort'
       cell_ref_dsd_model = active_sheet['A13'].value  # must have the value 'DSD Model'
       cell_ref_total_under_10  = active_sheet['Q47'].value  # must have the 'Total Under 10'
 
      

       if cell_ref_cohort != 'Cohort':
           print(cell_ref_cohort)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula A4 deve ter o valor: Cohort\n'  )
           print('Ha um erro no template excell.\n' )
           print('A celula C3 deve ter o valor: Cohort\n'  )
           return(False)
       elif cell_ref_dsd_model!='DSD Model':
           print(cell_ref_dsd_model)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula B5 deve ter o valor: DSD Model\n'  )
           print('Ha um erro no template excell.\n'  )
           print('A celula B5 deve ter o valor: DSD Model\n'  )
           return(False) 
    
       elif cell_ref_total_under_10 !='Total Under 10' :
           print(cell_ref_total_under_10)
           log_file.write('Ha um erro no template excell.\n'  )
           log_file.write('A celula B31 deve ter o valor: Total Under 10\n'  )
           print('Ha um erro no template excell.\n'  )
           print('A celula B31 deve ter o valor: Total Under 10\n'  )
           return(False) 
       else:
           return(True)

def check_ats_template_integrity(sheet1,sheet2, log_file ):
       cell_ref_vct_linkage = sheet1['A78'].value  # must be Linkege
       cell_ref_vct_sub_total  = sheet1['AA64'].value  # must be  Subtotal   
       cell_ref_pediatric_services_20_24  = sheet1['N22'].value  # must be 20-24
       cell_ref_parte_b_elicited  = sheet2['B25'].value  # must be Number of contacts elicited by age/sex

       if(cell_ref_vct_linkage is None or cell_ref_vct_sub_total is None or cell_ref_pediatric_services_20_24 is None  or cell_ref_parte_b_elicited is None ):
            print('Ha um erro no template excell.\n' )
            print('A celula A78 (Sheet1) deve ter o valor:Linkege\n' )
            print('A celula AA64 (Sheet1) deve ter o valor: Subtotal\n'  )
            print('A celula N22  (Sheet1)deve ter o valor: 20-24\n'  )
            print('A celula B25  (Sheet2)deve ter o valor: Number of contacts elicited by age/sex\n'  )
            return(False) 
       else: 
            if cell_ref_vct_linkage.strip() !='Linkege':
                print(cell_ref_vct_linkage)
                log_file.write('Ha um erro no template excell.\n'  )
                log_file.write('A celula A78 (Sheet1) deve ter o valor:Linkege\n'  )
                print('Ha um erro no template excell.\n' )
                print('A celula A78 (Sheet1) deve ter o valor:Linkege\n' )
                return(False)
            elif cell_ref_vct_sub_total.strip() !='Subtotal':
                print(cell_ref_vct_sub_total)
                log_file.write('Ha um erro no template excell.\n'  )
                log_file.write('A celula AA64 (Sheet1) deve ter o valor: Subtotal\n'  )
                print('Ha um erro no template excell.\n'  )
                print('A celula AA64 (Sheet1) deve ter o valor: Subtotal\n'  )
                return(False) 
    
            elif cell_ref_pediatric_services_20_24.strip() !='20-24' :
                print(cell_ref_pediatric_services_20_24)
                log_file.write('Ha um erro no template excell.\n'  )
                log_file.write('A celula N22 (Sheet1) deve ter o valor: 20-24\n'  )
                print('Ha um erro no template excell.\n'  )
                print('A celula N22  (Sheet1)deve ter o valor: 20-24\n'  )
                return(False) 

            elif cell_ref_parte_b_elicited.strip() !='Number of contacts elicited by age/sex' :
                print(cell_ref_parte_b_elicited)
                log_file.write('Ha um erro no template excell.\n'  )
                log_file.write('A celula B25 (Sheet2) deve ter o valor: Number of contacts elicited by age/sex\n'  )
                print('Ha um erro no template excell.\n'  )
                print('A celula B25  (Sheet2)deve ter o valor: Number of contacts elicited by age/sex\n'  )
                return(False) 

            else:
                return(True)

def chrome_version():

    osname = platform.system()
    if osname == 'Windows':
        installpath1 = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        installpath2 = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        if os.path.exists(installpath1):
            installpath=installpath1
        elif os.path.exists(installpath2):
            installpath=installpath2
        else:
             return 'unknown'    
    elif osname == 'Linux':
        installpath = "/usr/bin/google-chrome"
    else:
        raise NotImplemented(f"Unknown OS '{osname}'")

    verstr = os.popen(f"{installpath} --version").read().strip('Google Chrome ').strip()
    print(verstr)
    return(verstr)


def check_driver_compactibilty(web_driver):
    
    str1 = web_driver.capabilities['browserVersion']
    str2 = web_driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    print("BrowserVersion: " +str1[0:3])
    print("DriverVersion: "  +str2[0:3])
    if str1[0:3] == str2[0:3]: 
       print("Chrome driver compactivel")
       return (True) 
    else:
        print("Chrome driver incopactivel- deve descarregar o chromedriver mais recente.")
        return(False)

def unzip_driver(zip_file,directory_to_extract_to):
  with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(directory_to_extract_to)

def dowload_appropritate_driver(web_driver, chrome_version):

    osname = platform.system()
    # Making a get request
    print('Baixando a versao compactivel do driver chrome...')
    response = requests.get( 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'+chrome_version )
    # 200 ok 
    if response.status_code==200:
        if osname == 'Windows':
            # print response
            print(response.text)
            print('Ok. Iniciando o download...')
            download_url = 'https://chromedriver.storage.googleapis.com/'+ response.text + '/chromedriver_win32.zip'
            download_default_directory=r'C:/py-dhis-data-entry/downloads'
            os.chdir(download_default_directory)
            os.remove('chromedriver_win32.zip')
            # Download the file from `url` and save it locally under `file_name`:
            with urllib.request.urlopen(download_url) as response, open('chromedriver_win32.zip', 'wb') as out_file:
                data = response.read() # a `bytes` object
                out_file.write(data)
            if os.path.exists('chromedriver_win32.zip'):
                unzip_driver('chromedriver_win32.zip',chrome_driver_directory)
                print('Download finished: chromedriver_win32.zip')
            else:
                sys.exit('Download falhou!!! deve baixar manualmente o driver do Chrome em : https://chromedriver.chromium.org/downloads ')
        elif osname == 'Linux':
            # print response
            print(response.text)
            print('Ok. Iniciando o download...')
            download_url = 'https://chromedriver.storage.googleapis.com/'+ response.text + '/chromedriver_linux64.zip'
            download_default_directory='/home/agnaldo/Git/py-dhis-data-entry/downloads'
            chrome_driver_directory='/home/agnaldo/Git/py-dhis-data-entry/drivers'
            os.chdir(download_default_directory)
            os.remove('chromedriver_linux64.zip')
            # Download the file from `url` and save it locally under `file_name`:
            with urllib.request.urlopen(download_url) as response, open('chromedriver_linux64.zip', 'wb') as out_file:
                data = response.read() # a `bytes` object
                out_file.write(data)
            if os.path.exists('chromedriver_linux64.zip'):
                unzip_driver('chromedriver_linux64.zip',chrome_driver_directory)
                print('Download finished: chromedriver_linux64.zip')
            else:
                sys.exit('Download falhou!!! deve baixar manualmente o driver do Chrome em : https://chromedriver.chromium.org/downloads ') 

        else:
            raise NotImplemented(f"Unknown OS '{osname}'")
    elif response.status_code == 404:
        sys.exit('Not Found! Nao foi possivel encontrar o driver compactivel.. deve baixar manualmente em https://chromedriver.chromium.org/downloads')    
    else:
        sys.exit('Nao foi possivel encontrar o driver compactivel.. deve baixar manualmente em https://chromedriver.chromium.org/downloads')
    
