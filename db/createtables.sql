
CREATE TYPE e_estatetype AS ENUM (
    'flat',
    'apartment',
    'penthouse'
);

CREATE TABLE t_estate (
    id SERIAL,
    object_id VARCHAR,
    title VARCHAR,
    address VARCHAR,
    floor REAL,
    area REAL,
    estatetype e_estatetype,
    
    PRIMARY KEY(id),
    UNIQUE(object_id)
);

CREATE TABLE t_metrostation (
    id SERIAL,
    title VARCHAR,
    
    PRIMARY KEY(id)
);

CREATE TABLE t_proximity (
    id SERIAL,
    estate_id INTEGER,
    metrostation_id INTEGER,
    
    PRIMARY KEY(id),
    FOREIGN KEY(estate_id) REFERENCES t_estate(id) ON DELETE CASCADE,
    FOREIGN KEY(metrostation_id) REFERENCES t_metrostation(id) ON DELETE CASCADE
);
