#Pokemon Data Challenge
Satoshi needs helps organising his Pokemon database. Can you help him create a clean, organised database and answer some
of his questions?

#Background

The raw data is split in two CSV files with these columns:

* "#" = Pokemon ID (https://www.pokemon.com/us/pokedex/)
* "Type 1" = Pokemon type
* "Type 2" = Pokemon type
* "Total" = Sum of pokemon's attributes
* "HP" = Hit Points, shows the stats of strength pokemon
* "Attack" = Shows the stats of attack ability pokemon in physical form
*"Defense" = Shows the stats of defence ability pokemon in physical form
* "Sp. Atk" = Special Attack, Shows the stats of attack ability pokemon in non-physical form
* "Sp. Def" = Special Defense, Shows the stats of defence ability pokemon in non-physical form
* "Speed" = Movement speed of pokemon
* "Generation" = The "n" generation of pokemon
* "Legendary" = Shows stats of pokemon

These are the questions he would like answered:
* The fastest ice Pokemon in every generation.
* An aggregate with top 10 Pokemons per “Type” based on “Total”. He also wants to see Attack and Defense average on the list.
* Satoshi introduced Mega versions of Pokemons in 2013. What are they called and which one is the strongest?

#The Assignment

You can use any language/tool/DB you want. You should be able to run the solution on your computer without needing cloud
 services or similar. We will look at your technical implementation but don’t forget, equally important to explain your
  code and thought process.

1. Data Pipeline - Create some kind of data pipeline to clean, fix, alter, skew, model and ingest the data into a
 database of your choice.
2. Query the data - Answer the questions above with a coding language like SQL, Python etc.
3. Present results - Visualize some of your findings in a chart or dashboard of your choice.
4. Plan a production environment - Present how would you prefer to setup up your pipeline in a production environment.
5. BONUS - Enrich the data with gender You will find gender data here https://pokeapi.co/docs/v2#genders.
 What is the distribution between genders?
 
#Solution
To solve this challenge, I have used separated the solution in 3 parts:
* Getting the data and cleaning it - Python script - src and raw_datasets folders
* Data modelling to solve the questions - dbt models - src/pokedex_models folder
* Representing the data in a dashboard - Datastudio - Link: https://datastudio.google.com/reporting/ff1ffe8a-c821-4d76-8888-285abb19a789 

The database of choice is PostgreSQL and it's on local domain.
Commands to star PSQL database:
    brew services restart postgresql
    pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
    psql postgres

To create database Pokedex:
    CREATE DATABASE pokedex;
    GRANT ALL PRIVILEGES ON DATABASE pokedex TO username;
    
To get all the data processed in PSQL tables, execute script src/PokemonChallenge.py

First, gets data from csv and inserts it in raw_pokedex.

After, runs dbt models to answer the questions:
* dbt run --select pokedex.fast_ice_pokemon
* dbt run --select pokedex.top_pokemons_type
* dbt run --select pokedex.mega_pokemons

For the representation of the data in the dashboard, I downloaded the tables in csv and uploaded to Datastudio 
(I used this manual solution because I couldn't connect the local psql database to Datastudio).

For the extra part, I connect to the API and recollect the data about Pokemon gender (I had to consult the api 2 times
 because it specify the gender you wanted to consult)

It followed the same schema as before, formatted the data in the python part and executed a dbt model to get the final
 table:
* dbt run --select pokedex.gender_pokemon_distribution


#Resources:

Everything about the Pokemon domain https://bulbapedia.bulbagarden.net/wiki/Main_Page
