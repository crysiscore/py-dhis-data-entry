import yaml

dict_distritos_maputo = {'kamaxakeni': 0, 'Kampfumu': 1, 'Kamubukwana': 2, 'Kanyaka': 3, 'Katembe': 4, 'Nlhamankulu': 5}


def open_config_file(filename):
    with open(filename + '.yaml', 'r') as f:
        try:
            dict = yaml.load(f)
        except IOError as err:
            print 'error while reading fild' + filename + 'Details:' + str(err.message)
    return dict


def get_district_position(prov_dist, distrit_name):
    return prov_dist.get(distrit_name)


def expand_province_tree(province_name, browser_webdriver):
    if province_name == 'Cidade De Maputo':
        expand_prov_tree = browser_webdriver.find_element_by_xpath("//*[@id='orgUnitebcn8hWYrg3']/span/img")
        expand_prov_tree.click()
    elif province_name == 'Inhambane':
        expand_prov_tree = browser_webdriver.find_element_by_xpath("//*[@id='orgUnitebcn8hWYrg3']/span/img")
        expand_prov_tree.click()
    else:
        print('No province provided')


def expand_district_tree(dict_distritos,district_name):
    dict = open_config_file('configbkp')
    list = dict["distritos"]
    dist_index= get_district_position(dict_distritos,district_name)
    a= list[dist_index]
    #b= list[dist_index][district_name]
    print dist_index
    print  district_name
    print list[dist_index]
    print list[dist_index]
    #print b

    #xpath = list[dist_index][district_name]['xpath']
    #print dist_index
    #print list[dist_index]
    #print list[dist_index]['Kamaxakeni']
    #xpath = list[dist_index]['xpath']
    #expand_dist_tree = browser_webdriver.find_element_by_xpath()
    #expand_dist_tree.click()
    #print xpath


#with open('configbkp.yaml', 'r') as f:
#    dict = yaml.load(f)


#expand_district_tree(dict_distritos_maputo,"Kamaxakeni")

expand_district_tree(dict_distritos_maputo,'kamaxakeni')
# print list['albasine_cs']['province']
# distrito = dict["distritos"]
# print list['albasine_cs']['province']
# xpath = distrito['Kamaxakeni']
# print dict.get(2)
# print dict["distritos"]
# print list['albasine_cs']
# print list['albasine_cs']['province']
# print list['albasine_cs']['district']
# print list['albasine_cs']['xpath']
# print list['albasine_cs']['name']
# print xpathKamaxakeni
# print xpath['xpath']
# print distrito['Kamaxakeni']
