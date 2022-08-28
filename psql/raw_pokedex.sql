-- SQL to create table raw_pokedex

CREATE TABLE pokedex.raw_pokedex
(
    id integer NOT NULL,
    name varchar(30) NOT NULL,
    type_1 varchar(10) NOT NULL,
    type_2 varchar(10),
    total integer,
    hp integer,
    attack integer,
    defense integer,
    sp_attack integer,
    sp_defense integer,
    speed integer,
    generation integer,
    legendary boolean,
    PRIMARY KEY (id, name, generation)
);

ALTER TABLE pokedex.raw_pokedex
    OWNER to username;
COMMENT ON TABLE pokedex.raw_pokedex
    IS 'Contains all Pokemon data';