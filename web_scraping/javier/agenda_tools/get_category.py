import logging
from sre_constants import CATEGORY
logger = logging.getLogger(__name__)

category_dict = {
    'Arte':'1',
    'Cine':'2',
    'Cine V.O.':'3',
    'Cine de Autor':'4',
    'Danza':'5',
    'Exposiciones':'6',
    'Flamenco':'7',
    'Fotografía':'8',
    'Jazz y Soul':'9',
    'Literatura y Poesía':'10',
    'Literatura':'10',
    'Magia y Circo':'11',
    #'Niños y Familia':'12',
    'Teatro para Niños':'12', 
    'Familia':'12',        
    'Ópera':'13', 
    'Clásica':'25',
    'Piano':'26',
    'Performance':'14',
    'Planes':'15',
    'Talleres':'16',
    'Teatro':'17',
    'Teatro Comedia':'18',
    'Teatro Músical':'19',
    #'Música':'20',
    'Conciertos':'20',     
    'Monologos':'21',
    'Cabaret':'22',
    'Otras Músicas':'23',
    'Impro':'24',
    'Cine para Niños':'27',
    'Cultura Urbana':'28',
    'Conferencias y Debates':'29',
    'Mentalismo':'30'
    }

def id_category(category):
    try:
        id_category = category_dict[category]
        return id_category
    except KeyError:
        logger.error(f'- Category Key Error - in key {category}')
    except Exception as ex:
        logger.error(ex)


def chance_category(category):
    category = ' '.join([i.capitalize() for i in category.split()]).replace(' Y ',' y ').replace(' Para ',' para ').replace(' De ',' de ').replace(' En ',' en ').strip()
    if category == 'Circo':
        category = 'Magia y Circo'
    elif category == 'Cine':
            category = 'Cine de Autor'
    elif category == 'Musical':
        category = 'Teatro Músical'
    elif category == 'Familiar':
        category = 'Teatro para Niños'
    elif category == 'Comedia':
        category = 'Teatro Comedia'
    elif category == 'Musical para toda la Familia':
        category = 'Familia'
    elif category == 'Danza Africana':
        category = 'Danza'
    elif category == 'Improvisación':
        category = 'Teatro'
    elif category == 'Musica':
        category = 'Conciertos'
    elif category == 'Infantil-juvenil':
        category = 'Teatro para Niños'
    elif category == 'Conciertos':
        category = 'Conciertos'
    elif category == 'Opera':
        category = 'Ópera'
    elif category == 'ópera':
        category = 'Ópera'
    elif category == 'Teatroinfantil':
        category = 'Teatro para Niños'
    elif category == 'Teatrocomediahumor':
        category = 'Teatro Comedia'
    elif category == 'Culturaurbana':
        category = 'Cultura Urbana'
    if category == 'Teatro Familiar':
        category = 'Teatro para Niños'
    elif category == 'Teatro Musical':
        category = 'Teatro Músical'
    elif category == 'Recital':
        category = 'Conciertos'
    elif category == 'Musicales':
        category = 'Teatro Músical'
    elif category == 'Comedia, Teatro':
        category = 'Teatro Comedia'
    elif category == 'Magia, Teatro':
        category = 'Magia y Circo'
    elif category == 'Comedia Musical':
        category = 'Teatro Comedia'
    elif category == 'Infantil':
        category = 'Teatro para Niños'
    elif category == 'Monologo':
        category = 'Monologos'
    elif category == 'Pequeño Teatro Gran Vía':
        category = 'Teatro'
    elif category == 'Infantil y Familiar':
        category = 'Teatro para Niños'
    elif category == 'Concierto':
        category = 'Conciertos'
    elif category == 'Comedia en Inglés':
        category = 'Teatro Comedia'
    elif category == 'Comedia Improvisación':
        category = 'Impro'
    elif category == 'Mentalismo':
        category = 'Conciertos'
    elif category == 'Infantil':
        category = 'Teatro para Niños'
    elif category == 'Comedia Improvisación Musical':
        category = 'Teatro Músical'
    elif category == 'Magia':
        category = 'Magia y Circo'
    elif category == 'Comedia ácida':
        category = 'Teatro Comedia'
    elif category == 'Comedia Monólogo':
        category = 'Teatro Comedia'
    elif category == 'Bebés':
        category = 'Teatro para Niños'
    elif category == 'Improvisación inglés':
        category = 'Impro'
    elif category == 'mucho humor':
        category = 'Teatro Comedia'
    elif category == 'Comedia Magia':
        category = 'Magia y Circo'
    elif category == 'Magia con mucho humor':
        category = 'Magia y Circo'
    elif category == 'Teatro infantil CIRCO':
        category = 'Teatro para Niños'
    elif category == 'Cortometrajes':
        category = 'Cine de Autor'
    elif category == 'Musical':
        category = 'Conciertos'
    elif category == 'Familiar':
        category = 'Teatro para Niños'
    elif category == 'Comedia':
        category = 'Teatro Comedia'
    elif category == 'Musical para toda la Familia':
        category = 'Familia'
    elif category == 'Danza Africana':
        category = 'Danza'
    elif category == 'Improvisación':
        category = 'Impro'
    elif category == 'Niños y Familia':
        category = 'Teatro para Niños'
    elif category == 'Música':
        category = 'Conciertos'
    elif category == 'Lecturas Dramatizadas':
        category = 'Literatura y Poesía'
    elif category == 'Lecturas dramatizada':
        category = 'Literatura y Poesía'
    elif category == 'Lectura dramatizada':
        category = 'Literatura y Poesía'
    elif category == 'Teatro de objetos':
        category = 'Teatro'
    elif category == 'Cartelera  Comedia  Teatro Lara':
        category = 'Teatro'
    elif category == 'Drama - Clásico':
        category = 'Teatro'
    elif category == 'Drama':
        category = 'Teatro'
    elif category == 'Poesía & Performance':
        category = 'Performance'
    elif category == 'Teatrocomediahumor':
        category = 'Teatro Comedia'
    elif category == 'Culturaurbana':
        category = 'Cultura Urbana'
    elif category == 'Literatura':
        category = 'Literatura y Poesía'
    elif category == 'Conferencia':
        category = 'Conferencias y Debates'
    elif category == 'Entrevista':
        category = 'Conferencias y Debates'
    elif category == 'Debate':
        category = 'Conferencias y Debates'
    elif category == 'Coloquio':
        category = 'Conferencias y Debates'
    elif category == 'Melodramas':
        category = 'Literatura y Poesía '
    return category


def main_category(category):
    main_category = ''
    
    if category in ['Cine','Cine V.O.','Cine de Autor','Cine para Niños']:
        main_category = 'Peliculas'
    elif category in ['Cabaret','Impro','Monologos','Magia y Circo','Teatro','Teatro Músical','Teatro Comedia','Teatro para Niños','Familia']:
        main_category = 'Teatros'
    elif category in ['Clásica','Conciertos','Ópera','Flamenco','Piano','Jazz y Soul','Otras Músicas']:
        main_category = 'Música'
    elif category in ['Arte','Fotografía','Exposiciones','Literatura','Literatura y Poesía','Conferencias y Debates','Mentalismo']:
        main_category = 'Exposiciones'
    elif category in ['Danza','Flamenco','Performance','Cultura Urbana']:
        main_category = 'Baile'
    
    else:
        logger.error(f'- Key Error - in main_category {category}')
    
    return main_category

