query_states = '''
    CREATE TABLE IF NOT EXISTS prueba.states(
        Name character varying(4) Primary Key,
        Complete_name varchar(100)
    )
'''

query_corona_cases = '''
    CREATE TABLE IF NOT EXISTS prueba.corona_cases
    (
    id serial,
    state character varying(4),
    stateFIPS integer,
    total_cases bigint,
    CONSTRAINT corona_pk PRIMARY KEY (id),
    CONSTRAINT state_fk FOREIGN KEY (state)
        REFERENCES prueba.states (name) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL
        NOT VALID
    );

'''

query_population = '''
    CREATE TABLE IF NOT EXISTS prueba.population
(
    id serial NOT NULL,
    state character varying(4),
    population_number integer,
    male integer,
    female integer,
    PRIMARY KEY (id),
    CONSTRAINT fk_state FOREIGN KEY (state)
        REFERENCES prueba.states (name) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL
        NOT VALID
);
    
'''

query_insured_population = '''
CREATE TABLE IF NOT EXISTS prueba.uninsured_population
(
    id serial,
    state character varying(4),
    population integer,
    uninsured_population integer,
    male_ui_population integer,
    femaile_ui_population integer,
    age_0_18 integer,
    age_19_34 integer, 
    age_35_49 integer,
    age_50_64 integer,
    PRIMARY KEY (id),
    FOREIGN KEY (state)
        REFERENCES prueba.states (name) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL
        NOT VALID
);
'''

