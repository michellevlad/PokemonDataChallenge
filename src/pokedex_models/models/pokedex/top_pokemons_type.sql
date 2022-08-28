--dbt run --select pokedex.top_pokemons_type

{{ config(materialized='table') }}

with order_pokemons_type_total as (
    SELECT name
        , type_1
        , total
        , ROW_NUMBER() OVER(PARTITION BY type_1 ORDER BY total desc) AS r
    FROM pokedex.raw_pokedex
)

SELECT t1.name
	, t1.type_1 AS type
	, t1.total
	, t1.attack
	, t1.defense
FROM pokedex.raw_pokedex AS t1
INNER JOIN order_pokemons_type_total AS t2
    ON t1.name=t2.name
       AND t1.type_1=t2.type_1
       AND t1.total=t2.total
WHERE t2.r <= 10

