
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import concurrent.futures
from time import perf_counter
from agenda_tools import download_images
import logging
logger = logging.getLogger()
start = perf_counter()

import requests

def start():
    df1 = pd.read_csv('/home/cesar/Dropbox/My PC (LAPTOP-51JCM9VV)/results_outlet_25_3.csv',index_col=['Unnamed: 0'])

    df1 = df1[df1['Images'] != '/imagen/foto-piso-no-encontrada.jpg']

    df1.drop_duplicates(inplace=True)

    images_df1 = list(df1.Images)

    list_names = list(df1.loc[:,'Nombre'])

    return df1, images_df1, list_names


# "threading is for working in parallel, and async is for waiting in parallel".


#urls = range(1, 25000)

def get_data(image,idx):
    
    download_images.download_image_with_requests(image,nombre_del_lugar='Inmobiliaria_Bancaria',idx=idx,len_links=len_images)
    

def main():
    with ThreadPoolExecutor() as executor:
        df1 , urls, _ = start()
        global len_images
        len_images = len(urls)
        idx = range(0,len_images)
        names_images = executor.map(get_data, urls, idx)

if __name__ == '__main__':
    main()

# df1['images_names'] = list(names_images)
# df1.to_excel('./results_inmobiliaria_final_async.xlsx')


# time taken: 37.273589322998305





# from concurrent.futures import ThreadPoolExecutor
# import pandas as pd
# from time import perf_counter
# from agenda_tools import download_images
# import logging
# logger = logging.getLogger()
# start = perf_counter()

# import requests

# def start():
#     df1 = pd.read_csv('/home/cesar/Dropbox/My PC (LAPTOP-51JCM9VV)/results_inmobiliaria_24_3.csv',index_col=['Unnamed: 0'])

#     df1 = df1[df1['Images'] != '/imagen/foto-piso-no-encontrada.jpg']

#     df1.drop_duplicates(inplace=True)

#     images_df1 = list(df1.Images)

#     list_names = list(df1.loc[:,'Nombre'])

#     return df1, images_df1, list_names


# # "threading is for working in parallel, and async is for waiting in parallel".




