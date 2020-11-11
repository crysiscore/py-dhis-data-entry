import yaml
import time

dict_distritos_maputo = ['Kamaxakeni', 'Kampfumu', 'Kamubukwana', 'Kanyaka', 'Katembe', 'Nlhamankulu','Kamavota']
unidades_sanitarias = [ '1_de_junho_cs', 'albasine_cs', 'hulene_psa', 'mavalane_cs', 'mavalane_hg', 'pescadores_ps','romao_psa', '1_de_maio_cs',
'polana_canico_cs','1_alto_mae_csurb','hospital_central_de_mapito_hc','hospital_central_pediatrico_de_maputo_hc','malhangalene_cs','maxaquene_csurb',
'Hospital_militar_de_maputo','polana_cimento_csurb','porto_csurb','bagamoio_cs','hospital_psiquiatrico_do_infulene_cs','inhagoia_ps',
'magoanine_tenda_psa','zimpeto_ps','inhaca_ps','catembe_cs','chamissava_cs','incassane_cs','mutsekwa_ps','centro_de_saude_do_chamanculo_cs',
'chamanculo_hg','jose_macamo_cs','jose_macamo_HG','xipamanine_csurb']
forms =['C&T_Resumo de Cuidados e Tratamento']
periodos = ['Novembro 2020', 'Dezembro 2020','Janeiro 2021','Fevereiro 2021','Março 2021','Abril 2021','Maio 2021','Junho 2021','Julho 2021','Agosto 2021','Setembro 2021']

def open_config_file(filename):
    with open(filename, 'r') as f:
        try:
            dict = yaml.safe_load(f)
        except IOError as err:
            print ("error while reading file" + filename + 'Details:' + str(err.args))
        except yaml.YAMLError as exc:
            print ("error while reading file" + filename + 'Details:' + str(exc.message))
    return dict


def get_district_position(distrit_name):
    return dict_distritos_maputo.index(distrit_name)

def get_province_position(province_name):
    return unidades_sanitarias.index(province_name)

def expand_province_tree(province_name, browser_webdriver):
    expand_root_tree=browser_webdriver.find_element_by_xpath("//li[@id='orgUnitj9Inbtfw3Wu']/span/img[contains(@src, '/images/colapse.png')]")
    expand_root_tree.click()
    time.sleep(3)
    if province_name == 'Cidade De Maputo':
        expand_prov_tree = browser_webdriver.find_element_by_xpath("//li[@id='orgUnitebcn8hWYrg3']/span/img")
        expand_prov_tree.click()
    elif province_name == 'Inhambane':
        expand_prov_tree = browser_webdriver.find_element_by_xpath("//li[@id='orgUnitebcn8hWYrg3']/span/img")
        expand_prov_tree.click()
    else:
        print('No province provided')


def expand_district_tree(district_name,browser_webdriver):
   
    dictionary = open_config_file('org_units.yaml')
    index = get_district_position(district_name)
    print(index)
    xpath = dictionary['distritos'][index][district_name]['xpath']
    print(xpath)
    district_element= browser_webdriver.find_element_by_xpath(xpath)
    district_element.click()
  

def select_province(province_name,browser_webdriver):
    
    dictionary = open_config_file('org_units.yaml')
    index = get_province_position(province_name)
    xpath = dictionary['unidades_sanitarias'][index][province_name]['xpath']
    #name = dictionary['unidades_sanitarias'][index][province_name]['name']
    #province = dictionary['unidades_sanitarias'][index][province_name]['province']
    #district = dictionary['unidades_sanitarias'][index][province_name]['district']
      
    province_element= browser_webdriver.find_element_by_xpath(xpath)
    province_element.click()
 

def select_form(form_name, browser_webdriver ):
     #select_form_box_element = browser_webdriver.find_element_by_xpath("//*[@id='selectedDataSetId']")
     #select_form_box_element.click()
     #form_name ='C&T_Resumo de Cuidados e Tratamento'
     xpath = "//select[@name='selectedDataSetId']/option[text()=" + "'" + form_name + "' ]"
     print(xpath)
     form_element = browser_webdriver.find_element_by_xpath(xpath).click()


def select_period(periodo,browser_webdriver):
    xpath = "//select[@name='selectedPeriodId']/option[text()=" + "'" + periodo + "' ]"
    #print(xpath)
    form_element = browser_webdriver.find_element_by_xpath(xpath).click()


def fill_indicator_elements(indicator_name,indicator_map_file,active_sheet,log_file,browser_webdriver):
    
    indicator_yaml = open_config_file(indicator_map_file)

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
              print (cell_ref + " is empty")
              log_file.write(cell_ref + " is an empty cell." + '\n' ) 
          else:
              print(cell_ref +" : " + str(cell_value))
              input_element = browser_webdriver.find_element_by_xpath(xpath)
              input_element.send_keys(cell_value)

        except Exception as e:

          print("An exception occurred in key : %s" % indicator )
          print(str(e) )        
          log_file.write("An exception occurred in key : %s" % indicator + '\n')
          #log_file.close()
    
