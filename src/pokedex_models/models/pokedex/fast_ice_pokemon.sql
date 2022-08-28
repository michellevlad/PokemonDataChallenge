--dbt run --select pokedex.fast_ice_pokemon

{{ config(materialized='table') }}

with fastest_ice_generation as (
    SELECT type_1
        , generation
        , MAX(speed) as max_speed
    FROM pokedex.raw_pokedex
    WHERE type_1 = 'Ice'
    GROUP BY type_1, generation
)

SELECT r1.name
	, r1.type_1 AS type
	, r1.generation
	, r2.max_speed
FROM pokedex.raw_pokedex AS r1
INNER JOIN fastest_ice_generation AS r2
    ON r1.type_1=r2.type_1
       AND r1.generation=r2.generation
       AND r1.speed=r2.max_speed

