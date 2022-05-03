import requests
from bs4 import BeautifulSoup
import csv
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}
url = 'https://www.thefork.es/restaurantes/madrid-c328022'
main_url = 'https://www.thefork.es'

def extract_info_pages(link):
    link = f'{main_url}{link}'
    soup = get_request(link)
    title = soup.find('h1').get_text()
    print(title)

def get_main_links(soup):
    h2 = soup.find_all('h2',attrs={'class':"css-siel6k e7dhrrp0"})
    links = [i.find('a').get('href') for i in h2]
    return links


def get_request(url, proxy, timeout = 2):
   # print(proxy)
    #r = requests.get(url, headers=headers, proxies={'http':proxy,'https':proxy}, timeout=timeout)
    requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup


def try_proxy(url):
    proxies = []

    with open('Free_Proxy_List.csv','r') as file:
        reader = csv.reader(file)
        for row in reader:
            proxies.append(row[-1])
            print(row[-1])

    for proxy in proxies:
        try :
            soup= get_request(url, proxy=proxy)
            if soup:
                print('Work')
                return soup
                break
        except:
            print('No')
            pass

def main():
    soup = get_request(url)
    if soup:
        links = get_main_links(soup)

        for link in links:
            extract_info_pages(link)

if __name__ == '__main__':
    main()