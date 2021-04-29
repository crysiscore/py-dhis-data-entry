import yaml
import time
from config.extra_config import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


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
                #log_file.close() 

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
      