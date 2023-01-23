import pandas as pd
import json
import re
import argparse


def change_types(field):
    """Cambia los datos de numpy64 a int

    Args:
        field : data

    Returns:
        data
    """

    if type(field) == list:
        for idx, f in enumerate(field):
            if type(f) != str:
                field[idx] = f.item()
    else:
        if type(field) != str:
            field = field.item()
    
    return field


def extract_repited_values(data:dict) -> list:
    """Organiza en el diccionario los datos repatidos en los headears de tipo listas

    Args:
        data (dict): datos

    Returns:
        list
    """
    
    field_list =  list(data.keys())
    box = []
    for i in range(len(data[field_list[0]])):
        pivot_box = []
        for name in field_list:
            pivot_box.append({name:data[name][i]})

        dict_transicion = {}
        for i in pivot_box:
            dict_transicion.update(i)
        box.append(dict_transicion)
    
    return box


def create_dict(organized_columns:dict, df) -> dict : 
    """Crea el diccionario de datos

    Args:
        organized_columns (dict): Contiene las columans organizadas por jerarquia
        df (pd.DataFrame: df

    Returns:
        dict
    """
    value_dict = {}
    last_value = None
            
    for value, key in organized_columns.items():
        key_dict = {}
        for i in key:
            field = list(dict.fromkeys(df[i].values))
            column_name = i.split('_')[-1]
            if len(field) == 1: 
                key_dict[column_name] = change_types(field[0])
            elif len(field) > 1:
                key_dict[column_name] = change_types(field)
        
        
            
        if 'list' in value.lower():
            if type(key_dict[column_name]) == list:
                dict_values = extract_repited_values(key_dict)
                value_dict[last_value].update({value:dict_values})
            else:
                value_dict[last_value].update({value:[key_dict]})

        else:
            value_dict[value] = key_dict
            last_value = value
    
    return value_dict


def extract_unique_df(df, compare_columns:list) -> list:
    """Crea un sub set de df dependiendo de los datos por los que se vaya a discriminar

    Args:
        df (pd.DataFrame): df
        compare_columns (list): Lista de las columnas para usar como discriminante

    Returns:
        list
    """
    pivot_table = pd.DataFrame(df[compare_columns].value_counts()).reset_index()
    unique_values = pivot_table[compare_columns].values
    box_df = []
    
    for unique_value in unique_values:
        sub_df = df.query(f'{compare_columns[0]} == "{unique_value[0]}" and {compare_columns[1]} == "{unique_value[1]}" and {compare_columns[2]} == "{unique_value[2]}" ')
        box_df.append(sub_df)
        
    return box_df


def extract_main_info(df, columns:list) -> list:
    """Extrae los datos y los arganiza segun su jerarqui 

    Args:
        df (pd.DataFrame): df
        columns (list): lista de datos

    Returns:
        list
    """
    data = []
    open_nesting, data_columns = extract_data_columns(columns, df)
    organized_columns = organize_sub_headers(open_nesting, data_columns)
    # compare_columns = ['Market_depAirport' ,'Market_arrAirport', 'EffectiveInterval_begin', 'EffectiveInterval_end']
    dfs = extract_unique_df(df, compare_columns)
    
    
    for df in dfs:
        info = create_dict(organized_columns, df)
        data.append(info)
    
    return data


def organize_sub_headers(open_nesting:list, data_columns:list) -> dict:
    """Organiza la corralecion de los sub-headers

    Args:
        open_nesting (list): Columnas que son header
        data_columns (list): Columnas de datos

    Returns:
        dict
    """
    organization = {}
    for idx, header in enumerate(open_nesting):
        header = header.split('_')[-1]
        pattern = re.compile(r'{}_(\w+)'.format(header))
        
        header_data = []
        for column in data_columns:
            if re.match(pattern, column):
                header_data.append(column)

        organization[header] = header_data
                

    return organization


def extract_data_columns(columns:list,  df) -> tuple:
    """Extrae los diferentes tipos de columnas, discriminando por si están vacías o no

    Args:
        columns (list): _description_
        df (pd.DataFrame): df

    Returns:
        Tuple: Listas de las columnas separadas
    """

    open_nesting = []
    data_columns = []
    
    for column in columns:
        if pd.isnull(df[column].unique()[0]) and len(df[column].unique()) == 1:
            open_nesting.append(column)
        else:
            data_columns.append(column)
            
    return open_nesting, data_columns


def extract_columns_types(columns:list) -> tuple:
    """Extrae los diferentes tipos de columnas, discriminando por si tienen o no _

    Args:
        columns (list): columna del df

    Returns:
        tuple: Tupla de listas
    """
    has_underscore      = []
    has_not_underscore  = []


    for i in columns:
        if '_' in i:
            has_underscore.append(i)
        else:
            has_not_underscore.append(i)
            
    return has_underscore, has_not_underscore


def build_dictionary(df, has_underscore:list, has_not_underscore:list) -> dict:
    """Funcion que crea los diferentes encabezados del diccionario y su contenido

    Args:
        df (pd.DataFrame): df
        has_underscore (list): lista de las columnas que tienen "_"
        has_not_underscore (list): lista de las columnas que no tienen "_"

    Returns:
        dict: dict con la informacion final, estructurada
    """
    final_json = {}    
    
    for header in has_not_underscore:
        if 'list' in header.lower():
            final_json[header] = extract_main_info(df, has_underscore)
        else:
            assert (len(df[header].unique()) == 1), 'Hay mas de un valor en los encabezados unicos'
            final_json[header] = df[header].unique()[0]
                
    return final_json

def save_json(data: dict) -> None:
    """Guarda el dic en un archivo JSON

    Args:
        data (dict): Dic con la infomacion
    """
    with open('data.json', 'w') as file:
        json.dump(data,  file)


def create_json(df) -> json:
    """
    Funcion Madre

    Args:
        df (pd.DataFrame): df

    Returns:
        None
    """


    columns = df.columns
    has_underscore, has_not_underscore = extract_columns_types(columns)
    final_json = build_dictionary(df, has_underscore, has_not_underscore)
    save_json(final_json)
    
    return 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file','-file',type=str,help='Introduzca el path hacie el archivo csv',default='20191115031051-market-average-fares.csv' , nargs='?')
    parser.add_argument('--delimiter', '-d', type=str, default='|', help='csv delimiter')
    parser.add_argument('--compare_columns', '-c', type=list, default=['Market_depAirport' ,'Market_arrAirport', 'EffectiveInterval_begin', 'EffectiveInterval_end'] , help='csv delimiter')
    args = parser.parse_args()
    if args.file:
        global compare_columns
        compare_columns = args.compare_columns

        df = pd.read_csv(args.file, delimiter=args.delimiter)

    
    create_json(df)

