-- SQL to create table gender_pokemons

CREATE TABLE pokedex.gender_pokemons
(
    id integer NOT NULL,
    name varchar(30) NOT NULL,
    gender varchar(10) NOT NULL,
    PRIMARY KEY (id, name, gender)
);

ALTER TABLE pokedex.gender_pokemons
    OWNER to username;
COMMENT ON TABLE pokedex.gender_pokemons
    IS 'Contains information about pokemons gender';