import pandas as pd
import os
import re 

pattern = re.compile(r'.*\.csv')
pattern2 = re.compile(r'(.*)\.csv')


def main():
    list_of_csv = os.listdir('//mnt/c/Users/cesar/Desktop/mi_barrio_negocios')
    list_of_csv = [re.match(pattern, i).group(0) for i in list_of_csv if re.match(pattern, i)]
    
    for i in list_of_csv:
        df = pd.read_csv('//mnt/c/Users/cesar/Desktop/mi_barrio_negocios/'+i)
        new_name = re.match(pattern2, i).group(1) + '.xlsx'
        new_path = '//mnt/c/Users/cesar/Desktop/mi_barrio_negocios/' + new_name
        df.to_excel(new_path,index=False)


if __name__ == '__main__':
    main()