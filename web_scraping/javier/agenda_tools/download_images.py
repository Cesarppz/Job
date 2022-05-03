#from os import mkdir
import os
import re 
import logging
logger = logging.getLogger()
import urllib
import subprocess
import ssl
import requests
from datetime import date, datetime
from w3lib.url import safe_url_string

mes = datetime.now().month
dia = datetime.now().day
ssl._create_default_https_context = ssl._create_unverified_context

link_image_pattern = re.compile(r'^(http).*/.+\.((jpg|jpeg|png|JPG|JPEG|svg|gif|webp))')
link_image_pattern2 = re.compile(r'^(http).*/.+')


def download(image,second_try_image = None, nombre_del_lugar = None, idx=0, len_links=0,title_for_image=None):
    
    if image or second_try_image != None:
            if image:
                image_format = re.match(link_image_pattern,image).group(2)
                image_name = f'{nombre_del_lugar}_{idx}de{len_links}_{dia}_{mes}.{image_format}'
                if title_for_image != None:
                    image_name = f'{title_for_image}.{image_format}'
                image = safe_url_string(image)  #Hacer que la url tolere los acentos y caracteres especiales
                urllib.request.urlretrieve(image,image_name)
            else:
                image_format = re.match(link_image_pattern,second_try_image).group(2)
                image_name = f'{nombre_del_lugar}_{idx}de{len_links}_{dia}_{mes}.{image_format}'
                if title_for_image != None:
                    image_name = f'{title_for_image}.{image_format}'
                second_try_image = safe_url_string(second_try_image)
                urllib.request.urlretrieve(second_try_image,image_name)

            #Mover la imagen a la carpeta de imagenes
            nombre_dir = f'data_{nombre_del_lugar}_{dia}_{mes}'
            try:
                os.makedirs(f'./{nombre_dir}')
            except FileExistsError:
                pass
            except Exception as ex:
                logger.error(ex)

            subprocess.run(['mv',image_name,'{}/{}'.format(nombre_dir,image_name)],cwd='.')

            return image_name
    else :
        print('-'*20)
        logger.warning(f'La imagen {idx} no se descrago')
        print('-'*20)
        image_name = None
        return image_name


def download_opener(image,second_try_image = None, nombre_del_lugar = None, idx=0, len_links=0,title_for_image=None):
    
    if image or second_try_image != None:
            if image:
                image_format = re.match(link_image_pattern,image).group(2)
                image_name = f'{nombre_del_lugar}_{idx}de{len_links}_{dia}_{mes}.{image_format}'
                if title_for_image != None:
                    image_name = f'{title_for_image}.{image_format}'
                image = safe_url_string(image)  #Hacer que la url tolere los acentos y caracteres especiales
                opener = urllib.request.URLopener()
                opener.addheader('User-Agent', 'whatever')
                opener.retrieve(image, image_name)
            else:
                image_format = re.match(link_image_pattern,second_try_image).group(2)
                image_name = f'{nombre_del_lugar}_{idx}de{len_links}_{dia}_{mes}.{image_format}'
                if title_for_image != None:
                    image_name = f'{title_for_image}.{image_format}'
                second_try_image = safe_url_string(second_try_image)
                opener = urllib.request.URLopener()
                opener.addheader('User-Agent', 'whatever')
                opener.retrieve(second_try_image, image_name)

            #Mover la imagen a la carpeta de imagenes
            nombre_dir = f'data_{nombre_del_lugar}_{dia}_{mes}'
            try:
                os.makedirs(f'./{nombre_dir}')
            except FileExistsError:
                pass
            except Exception as ex:
                logger.error(ex)
                
            subprocess.run(['mv',image_name,'{}/{}'.format(nombre_dir,image_name)],cwd='.')

            return image_name
    else :
        print('-'*20)
        logger.warning(f'La imagen {idx} no se descrago. Image: {image}')
        print('-'*20)
        image_name = None
        return image_name


def download_image_with_requests(image,second_try_image = None, nombre_del_lugar = None, idx=0, len_links=0,title_for_image=None):
    
    if image or second_try_image != None:
            if image:
                image_format = re.match(link_image_pattern,image).group(2)
                image_name = f'{nombre_del_lugar}_{idx}de{len_links}_{dia}_{mes}.{image_format}'
                if title_for_image != None:
                    image_name = f'{title_for_image}.{image_format}'
                image = safe_url_string(image)
                image = requests.get(image).content
            else:
                image_format = re.match(link_image_pattern,second_try_image).group(2)
                image_name = f'{nombre_del_lugar}_{idx}de{len_links}_{dia}_{mes}.{image_format}'
                if title_for_image != None:
                    image_name = f'{title_for_image}.{image_format}'
                second_try_image = safe_url_string(second_try_image)
                image = requests.get(second_try_image).content

            with open(image_name,'wb') as f:
                f.write(image)

            #Mover la imagen a la carpeta de imagenes
            nombre_dir = f'data_{nombre_del_lugar}_{dia}_{mes}'
            try:
                os.makedirs(f'./{nombre_dir}')
            except FileExistsError:
                pass
            except Exception as ex:
                logger.error(ex)

            subprocess.run(['mv',image_name,'{}/{}'.format(nombre_dir,image_name)],cwd='.')

            return image_name
    else :
        print('-'*20)
        logger.warning(f'La imagen {idx} no se descrago')
        print('-'*20)
        image_name = None
        return image_name    


def download_image_with_requests_without_format(image,second_try_image = None, nombre_del_lugar = None, idx=0, len_links=0,title_for_image=None):
    
    if image or second_try_image != None:
            if image:
                image_name = f'{nombre_del_lugar}_{idx}de{len_links}_{dia}_{mes}.jpg'
                if title_for_image != None:
                    image_name = f'{title_for_image}.jpg'
                image = safe_url_string(image)
                image = requests.get(image).content
            else:
                image_name = f'{nombre_del_lugar}_{idx}de{len_links}_{dia}_{mes}.jpg'
                if title_for_image != None:
                    image_name = f'{title_for_image}.jpg'
                second_try_image = safe_url_string(second_try_image)
                image = requests.get(second_try_image).content

            with open(image_name,'wb') as f:
                f.write(image)

            #Mover la imagen a la carpeta de imagenes
            nombre_dir = f'data_{nombre_del_lugar}_{dia}_{mes}'
            try:
                os.makedirs(f'./{nombre_dir}')
            except FileExistsError:
                pass
            except Exception as ex:
                logger.error(ex)

            subprocess.run(['mv',image_name,'{}/{}'.format(nombre_dir,image_name)],cwd='.')

            return image_name
    else :
        print('-'*20)
        logger.warning(f'La imagen {idx} no se descrago')
        print('-'*20)
        image_name = None
        return image_name    