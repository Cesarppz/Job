import logging
logger = logging.getLogger()

def make_title(title, place_name, fp_schedule = None, lp_schedule = None):
    if fp_schedule == None or lp_schedule == None:
        return f'{title} / {place_name} /'
    else:
        return  f'{title} / {place_name} / {fp_schedule} al {lp_schedule}'

# Clocar cada la primera letra de cada palabra en mayuscula
def capitals_titles(df, title_field = 'title/Product_name'):
    try:
        df[title_field] = df[title_field].apply(lambda x : ' '.join([i.capitalize() for i in x.split()]))
    except:
        pass
    return df 