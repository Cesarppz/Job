def create_schema(curs):
    query_schema = 'CREATE SCHEMA IF NOT EXISTS prueba'
    curs.execute(query_schema)

def create_tables(curs):
    curs.execute(query_states)
    curs.execute(query_corona_cases)
    curs.execute(query_insured_population)
    curs.execute(query_population)

def load_tables(curs):
    create_schema(curs)
    create_tables(curs)
    
    
    
def load_insurance(cursor, connection, df):
    for i in df.values:
        insert_query = '''INSERT INTO prueba.uninsured_population(state, population, uninsured_population, male_ui_population, femaile_ui_population, age_0_18,age_19_34, age_35_49,age_50_64) 
                        VALUES(
                            \'{state}\', {population}, {uninsured_population}, {male_ui_population}, {femaile_ui_population}, {age_0}, {age_19}, {age_35}, {age_50} 
                            );'''.format(
                            state=i[0], 
                            population=i[1],
                            uninsured_population=i[2],
                            male_ui_population=i[3],
                            femaile_ui_population=i[4],
                            age_0=i[5],
                            age_19=i[6],
                            age_35=i[7],
                            age_50=i[8]
        )
#         print(insert_query)
        cursor.execute(
            insert_query
        )
    connection.commit()

def load_corona_cases(cursor, connection, df):
    for i in df.values:
        
        insert_query = '''INSERT INTO prueba.corona_cases(state,statefips, total_cases) 
                        VALUES(
                            \'{state}\',{statefips} , {total_cases}
                            );'''.format(
                            state=i[0], 
                            statefips=i[1],
                            total_cases=i[2]
        )
#         print(insert_query)
        cursor.execute(
            insert_query
        )
    connection.commit()
    

def load_population(cursor, connection, df):
    for i in df.values:
        insert_query = '''INSERT INTO prueba.population(state, population_number, male, female) 
                        VALUES(
                            \'{state}\', {population_number}, {male}, {female}
                            );'''.format(
                            state=i[4], 
                            population_number=i[1],
                            male=i[2],
                            female=i[3]
        )
#         print(insert_query)
        cursor.execute(
            insert_query
        )
    connection.commit()
    
    
def insert_states(cursor, connection, df):
    for i in df.values:
        insert_query = '''INSERT INTO prueba.states(name, complete_name) VALUES(\'{abb}\', \'{name}\') 
                        ON CONFLICT (name) DO UPDATE SET complete_name = excluded.complete_name;'''.format(abb=i[-1], name=i[0])
        cursor.execute(
            insert_query
        )
    connection.commit()