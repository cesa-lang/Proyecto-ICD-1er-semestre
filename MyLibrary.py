import os
import json
import pandas as pd
import statistics as st

# Extaer datos para convertir en info_list:

def data_extraction_il(route):
    info_list = []
    for file in os.listdir(route):
        if file.endswith(".json"):
            with open(os.path.join(route,file)) as file_data:
                content = json.load(file_data)
                info_list.append(content)
    return info_list

# Extraer los datos y conversion a dataframe:

def data_extraction_df(route):
    info_list = []
    for file in os.listdir(route):
        if file.endswith(".json"):
            with open(os.path.join(route,file)) as file_data:
                content = json.load(file_data)
                info_list.append(content)
    database = pd.DataFrame(info_list)
    return database

# Calcular la mediana en un array de valores:

def median_calculus(list):
    list = sorted(list)
    if len(list) == 0:
        return 0
    elif len(list) % 2 == 1:
        return list[len(list)//2]
    else:
        medium_place1 = list[len(list)//2-1]
        medium_place2 = list[len(list)//2]
        median = (medium_place1 + medium_place2)/2
        return median
    
# Extraccion de la informacion de digitalizacion de los lugares:

def digitalization_info(database):    
    dig_dic = {} 
    dig_info = database[["Place","Accounts or website"]]
    for i,j in dig_info.iterrows():
        place = j["Place"]
        acc = j["Accounts or website"]
        dig_dic[place] = [j for j in acc.values() if j is not None]
    for x,y in dig_dic.items():
        dig_dic[x] = len(y)

    centers = [i for i in dig_dic.keys()]
    cuant_dig = [j for j in dig_dic.values()]

    dig_dic1 = {} 
    for number, center in zip(cuant_dig,centers):
        if number not in dig_dic1:
            dig_dic1[number] = []
        dig_dic1[number].append(center)

    for x,y in dig_dic1.items(): 
        dig_dic1[x] = len(y)
    centers = [i for i in dig_dic1.values()]
    cuant_dig = [j for j in dig_dic1.keys()]
    list_data = [cuant_dig,centers]
    return list_data

# Extraccion del diccionario asignado a una categoria en el menu:

def category_extraction(info_list,category):
    data_list = []
    for i in info_list:
        data_list.append(i["Menu card"][category])
    return data_list

# Extraer a un diccionario con todos los platos de una categoria asignados a su lugar:

def plates_extraction(listdir,info_list,category):
    cat_dic = {}
    plates_list = []
    for i,j in zip(listdir,info_list):
        for k in j["Menu card"][category].keys():
            plates_list.append(k)
            cat_dic[i] = plates_list
    return cat_dic

# Extraer a una lista todos los precios de opciones en una categoria:

def prices_ext_per_place(listdir,info_list,category):
    diction = {}
    category_prices = []
    for i,j in zip(listdir,info_list):
        if j["Menu card"][category] is None:
            continue
        for f in i["Menu card"][category].values():
            if f is None:
                continue
            category_prices.append(f)
        diction[i] = category_prices
    return diction

# Contar para todos los locales la cantidad de ofertas de las categorias seleccionadas y devolverlas en una lista de diccionarios:

def cuantity_extraction(route,info_list):
    dic_list = []
    ref_list = []
    counter = 0
    for x,y in zip(os.listdir(route),info_list):
        for f in y["Menu card"]:
            if f is None:
                ref_list.append(0)
            else:
                for k in f.keys():
                    counter += 1
            ref_list.append(counter)
        dic_list.append({x:ref_list})
    return dic_list

# Extraccion de los precios por categoria dada para todos los locales:

def cat_prices(info_list,category):
    category_prices = []
    for i in info_list:
        if i["Menu card"][category] is None:
            continue
        for j in i["Menu card"][category].values():
            if j is None:
                continue
            category_prices.append(j)
    return category_prices

# Extraer lista de categorias de platos vegetarianos de todos los lugares:

def veg_cat_list(info_list):
    veg_data = []
    for a in info_list: 
        if a["Menu card"]["Vegetarian options"] is None:
            continue
        for f in a["Menu card"]["Vegetarian options"].values():
            veg_data.append(f)
    return veg_data

# Extraer diccionario con los locales y su cantidad de platos vegetarianos asignada: 

def veg_cuantity(route):
    places_veg = []
    dict1 = {}
    for name in os.listdir(route):
        if name.endswith(".json"):
            file_route = os.path.join(route,name)
            with open(file_route,"r")as file:
                info = json.load(file)
        places_veg.append(info["Menu card"]["Vegetarian options"])

    for i,j in zip(os.listdir(route),places_veg):
        if j is None:
            dict1[i] = 0
        else:
            dict1[i] = len(j)
    return dict1

# Extraer las medias de capacidad por municipio:

def capacity_procesing(dataframe):
    mun_cap_list = []
    cap_list = []
    capacity = dataframe[["Location.Municipality","Capacity"]]
    capacity = capacity.dropna()
    for i,j in zip(capacity["Location.Municipality"],capacity["Capacity"]):
        mun_cap_list.append(i)
        cap_list.append(j)

    cap_mun = {}
    for municipality, capacities in zip(mun_cap_list,cap_list):
        if municipality not in cap_mun:
            cap_mun[municipality] = []
        cap_mun[municipality].append(capacities)

    medians = {}
    for mun,val in cap_mun.items():
        medians[mun] = round(st.median(val))

    mun = [i for i in medians.keys()]
    val = [j for j in medians.values()]
    data_list = [mun,val]
    return data_list

# Obtener de los pares de un diccionario el valor:

def obtein_value(item):
    return item[1]

# Organizar diccionarios de una categoria segun su cantidad de platos:

def cat_quant(info_list,category):
    cat_variety_pp = {}
    var_list = []
    for i in info_list:
        if i["Menu card"][category] is None:
            var_list.append(0)
            cat_variety_pp[i["Place"]] = var_list
        elif i["Menu card"][category] is not None:
            var_list = [x for x in i["Menu card"][category]]
            cat_variety_pp[i["Place"]] = var_list

    cat_quant = {}
    for i,j in cat_variety_pp.items():
        cat_quant[i] = len(j)
    return cat_quant