--dbt run --select pokedex.gender_pokemon_distribution

{{ config(materialized='table') }}

with gender_agg as (
    SELECT id
        , name
        , COUNT(distinct gender) AS total_genders
    FROM pokedex.gender_pokemons
    GROUP BY id
        , name
)

SELECT r.id
	, r.name
	, r.type_1 AS type
	, CASE WHEN g2.total_genders > 1 THEN 'both genders'
	    WHEN g2.total_genders = 1 THEN g1.gender
	    ELSE 'no gender specified'
	    END AS gender
FROM pokedex.raw_pokedex AS r
LEFT JOIN pokedex.gender_pokemons AS g1
    ON r.id = g1.id
LEFT JOIN gender_agg AS g2
    ON g1.id = g2.id


