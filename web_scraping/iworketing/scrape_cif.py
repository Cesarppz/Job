import requests
import pandas as pd
import pickle
import pdb
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor



def loadbar(iteration,total,prefix='',suffix='',decimals=1,length=100,fill='>'):
   percent = ('{0:.' +str(decimals) + 'f}').format(100*(iteration/float(total)))
   filledLength = int(length * iteration // total)
   bar = fill * filledLength + '-' * (length - filledLength)
   print(f'\r{prefix} | {bar} | {percent}% {suffix}',end='\r')
   if iteration == total:
       print()

def get_data(url,idx):
    # REQUESTS
    r = requests.get(url)
    s = BeautifulSoup(r.text, 'lxml')
    if r.status_code == 200:
        razon_social = s.find(text="Razón Social ").parent.parent.find('span', attrs={'itemprop':'legalname'}).text
        cif = s.find(text="CIF ").parent.parent.find('span', attrs={'itemprop':'taxID'}).text

        info = {
            'Url':url,
            'Razon Social': razon_social,
            'Cif': cif
        }

        info = pd.DataFrame([info])
        if idx % 100 == 0:
            loadbar(idx, len_images) 

        data.append(info)

    


def read_urls():
    with open('listfile', 'rb') as file:
        list_urls = pickle.load(file)
    return list_urls


def main():
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        global data
        data = []
        urls = read_urls()
        global len_images
        len_images = len(urls)
        idx = range(0,len_images)

        executor.map(get_data, urls, idx)
    


    # for i in df:
    #     data.append(i)


    dataframe = pd.concat(data)
    dataframe.to_csv('cif_datoscif.csv')

if __name__ == '__main__':
    main()