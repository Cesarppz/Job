import pandas as pd
import pickle
from agenda_tools import download_images
import traceback

def start():
    df1 = pd.read_csv('/home/cesar/Dropbox/My PC (LAPTOP-51JCM9VV)/results_inmobiliaria_24_3.csv',index_col=['Unnamed: 0'])

    df1 = df1[df1['Images'] != '/imagen/foto-piso-no-encontrada.jpg']

    df1.drop_duplicates(inplace=True)

    images_df1 = list(df1.Images)

    list_names = list(df1.loc[:,'Nombre'])

    return df1, images_df1, list_names

def process1(images_df1,list_names):
    if len(list_names) == len(images_df1):
        names_images = []
        for idx,image in enumerate(images_df1):
            try:
                name_image = download_images.download_image_with_requests_without_format(image,nombre_del_lugar='Inmobiliaria Bancaria',idx=idx,len_links=len(images_df1),title_for_image='_'.join(list_names[idx].replace('/','').split(' ')))
            except Exception as ex:
                traceback.print_exc(ex)
                name_image = None
                print('Error al descargar')

            names_images.append(name_image)
            if idx % 101 == 0:
                print(f'Descargada image {idx+1}/{len(images_df1)}')
        return names_images

def process2(images_df1):
    try:
        images_names = download_images.download_image_with_requests_async(images_df1,nombre_del_lugar='inmobiliaria_bancaria')
        return images_names
    except Exception as ex:
        print(ex)


def main(type_p='2'):
    df1, images_df1, list_names = start()

    if type_p == '1':
        names_images = process1(images_df1,list_names)
    else:
        names_images = process2(images_df1)

    with open('fork.dat','wb') as f:
        pickle.dump(names_images,f)
    df1['images'] = names_images
    df1.to_excel('/home/cesar/Dropbox/My PC (LAPTOP-51JCM9VV)/results_inmobiliaria_final.xlsx')
    df1.to_excel('./results_inmobiliaria_final.xlsx')

if __name__ == '__main__':
    res = input('Tipo de porgrama: ') 
    main(res)