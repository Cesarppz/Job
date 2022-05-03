import re
from agenda_tools import months
from datetime import datetime
import datetime as dt

mes = datetime.now().month
dia = datetime.now().day
year = datetime.now().year

def clean_schedule(schedule, pattern_schedule, split_pattern = 'al'):
    if schedule:
        schedule = schedule.lower()
        string = re.search(pattern_schedule, schedule).group(1)
        string = re.split(split_pattern,string)
        fp = string[0].strip()
        try:
            lp = string[1].strip()
            return fp, lp
        except:
            return fp

def schedule_in_list(schedule, pattern_schedule):
    schedule_list = []
    for i in schedule:
        if i:
            result = re.findall(pattern_schedule,i)
            if result:
                result[0].strip()
                schedule_list.extend(result)
    return schedule_list

def eliminar_de(schedule_list,replace_pattern='de',replace_item=' '):
    for idx , i in enumerate(schedule_list):
        i = i.replace(replace_pattern,replace_item)
        schedule_list[idx] = ' '.join(i.split())
    return schedule_list


def eliminar_de_not_list(schedule,replace_pattern='de',replace_item=' '):
    schedule = schedule.replace(replace_pattern,replace_item)
    schedule = ' '.join(schedule.split())
    return schedule

def eliminar_spacios_list(schedule_list):
    for _ in schedule_list:
        try:
            schedule_list.remove('\n')
        except ValueError:
            break
    return schedule_list

def get_datetime(date, adv=False):
    if adv == False:
        dict_adv = months.dict_of_months_adv_spanish_to_spanish
        dict_trans = months.dict_of_months_adv_spanish_to_english
        date = date.replace('  ',' ').strip()
        date = date.split()
        mes = dict_adv[date[1].capitalize()]
        date[1] = dict_trans[mes]
        return ' '.join(date)

def transform_to_adv(date):
    dict_adv = months.dict_of_months_adv_spanish_to_spanish
    date = date.replace('  ',' ').strip()
    date = date.split()
    date[1] = dict_adv[date[1].capitalize()]
    return ' '.join(date)

def transform_to_adv_spa_eng(date):
    dict_adv = months.dict_of_months_adv_spanish_to_english
    date = date.replace('  ',' ').strip()
    date = date.split()
    date[1] = dict_adv[date[1].capitalize()]
    return ' '.join(date)

def transform_to_adv_eng_spa(date):
    dict_adv = months.dict_of_months_adv_english_to_spanish
    date = date.replace('  ',' ').strip()
    date = date.split()
    date[1] = dict_adv[date[1].capitalize()]
    return ' '.join(date)

def remove_blank_spaces(text):
    return text.replace('\xa0',' ').replace('\n',' ').replace('\t',' ').replace('  ',' ').replace('\n',' ').replace(',','').replace('.','').strip()


def desde_hasta_in_schedule(df, desde_field = 'Desde', hasta_field = 'Hasta'):
    df[desde_field] = df[desde_field].apply(lambda x : f'Desde {x}')
    df[hasta_field] = df[hasta_field].apply(lambda x : f'Hasta {x}')
    return df

def horario_format(horario):
    horario = re.split('[A-Za-zñ\.]+',horario.lower())   
    for i in horario:
        if i == '':
            horario.remove('')
        elif i == ' ':
            horario.remove(' ')
    return horario


def get_schedule(schedule):
    schedule = schedule.lower()
    schedule = schedule.replace('días','').replace('día','').replace('del','').replace('del','').replace('desde','').replace('de','').replace('el','').replace('hasta','').replace('sábado','').replace('lunes','').replace('martes','').replace('miércoles','').replace('jueves','').replace('viernes','').replace('domingo','').replace('aplazado al','')
    schedule = remove_blank_spaces(schedule)
    switch = False
    if 'Hasta' in schedule:
        schedule.replace('Hasta','')
        switch = True
    
    schedule_split = schedule.split('al')
    if len(schedule_split) == 1:
        schedule_split = schedule_split[0].split('-')
    if len(schedule_split) == 1:
        schedule_split = schedule_split[0].split('–')
    if len(schedule_split) == 1:
        schedule_split = schedule_split[0].split(' y ')
    
    fp , lp = schedule_split[0], schedule_split[-1]
    chanced_year = False
    #Separados por coma
    if ',' in fp:
        fp = fp.split(',')[0]
    if ',' in lp:
        lp = lp.split(',')[-1]
    fp, lp = remove_blank_spaces(fp), remove_blank_spaces(lp)
    #Solo numero 
    if len(fp.split()) == 1:
        fp = '{} {} {}'.format(fp,lp.split()[1], year)
    #Missing year
    elif len(fp.split()) == 2:
        fp = '{} {}'.format(fp,year)
        chanced_year = True
    #lp missing year
    if len(lp.split()) == 2:
        lp = '{} {}'.format(lp,year)
        chanced_year = True
    
    # print(fp)
    # print(lp)
    try:
        fp = transform_to_adv(fp)
        lp = transform_to_adv(lp)
    except Exception:
        pass
    
    # print(fp)
    # print(lp)
    from_date = datetime.strptime(transform_to_adv_spa_eng(fp),'%d %b %Y')
    to_date = datetime.strptime(transform_to_adv_spa_eng(lp),'%d %b %Y')
    if chanced_year:
        if from_date.month < mes and to_date.month < mes and from_date.month - mes > 6:
            from_date = from_date + dt.timedelta(days=365)
            to_date = to_date + dt.timedelta(days=365)
        elif from_date.month < mes and to_date.month >= mes and from_date.month - mes > 6:
            from_date = from_date + dt.timedelta(days=365)
        elif to_date.month < mes and from_date.month >= mes and to_date.month - mes > 6:
            to_date = to_date + dt.timedelta(days=365)
    if switch:
        fp, from_date = None, None
    from_date = from_date.strftime('%d/%m/%Y')
    to_date = to_date.strftime('%d/%m/%Y')
    fp = transform_to_adv_eng_spa(transform_to_adv_spa_eng(fp))
    lp = transform_to_adv_eng_spa(transform_to_adv_spa_eng(lp))
    fp = ' '.join(fp.split()[:2])
    lp = ' '.join(lp.split()[:2])

    return fp, lp, from_date, to_date
    