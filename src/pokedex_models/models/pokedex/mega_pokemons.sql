--dbt run --select pokedex.mega_pokemons

{{ config(materialized='table') }}

SELECT id
	, name
	, type_1
	, type_2
	, total
	, hp
	, attack
	, defense
	, sp_attack
	, sp_defense
	, speed
	, generation
	, legendary
FROM pokedex.raw_pokedex
WHERE name LIKE 'Mega%'
ORDER BY hp DESC

