import json
import numpy as np
import os
import pandas as pd
import psycopg2
import psycopg2.extras as extras
import re
import requests


def read_raw_data():
    # Read raw data from CSVs provided
    raw_data = pd.concat([pd.read_csv('../raw_datasets/pokemon_1.csv'), pd.read_csv('../raw_datasets/pokemon_2.csv')],
                         ignore_index=True)
    return raw_data


def clean_data(df):
    # Clean the Mega Pokemon names and leave it how it's in the Bulbapedia
    df['Name'] = df['Name'].apply(lambda x: ''.join(map(str, re.findall('[A-Z][a-z]*', x)[1:])) if 'Mega' in x else x)
    # Add blank space where names are together all words and preparing to write in PSQL with {}
    df['Name'] = df['Name'].apply(lambda x: re.sub(r"(\w)([A-Z])", r"\1 \2", x))

    # Change fields Type1 and Type2 to Upper first letter
    df['Type 1'] = df['Type 1'].str.title()
    df['Type 2'] = df['Type 2'].replace(np.nan, 'None')
    df['Type 2'] = df['Type 2'].str.title()

    # Cast field "Legendary" to boolean 0: False 1: True
    df['Legendary'] = df['Legendary'].map(
        {False: False, True: True, 'False': False, 'True': True, '0': False, '1': True})

    # Replace nan values with 0
    df.replace(np.nan, 0)

    # Drop duplicates
    df = df.drop_duplicates()

    # Rename columns of dataframe for postgresql
    df.columns = ['id', 'name', 'type_1', 'type_2', 'total', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense',
                  'speed', 'generation', 'legendary']

    return df


def write_data_to_psql(df, table):
    # Prepare dataframe to be inserted
    tuples = [tuple(x) for x in df.to_numpy()]
    # Getting columns from dataframe
    columns = ','.join(list(df.columns))
    # Getting query to insert data
    psql_query = """DELETE FROM %s WHERE id IS NOT NULL; INSERT INTO %s (%s) VALUES %%s ;""" % (table, table, columns)

    try:
        # Configure connection with local database PostgreSQL
        connection = psycopg2.connect(user="username", password="1234", host="localhost", port="5432"
                                      , database="pokedex")
        cursor = connection.cursor()

        # Write data in table
        extras.execute_values(cursor, psql_query, tuples, template=None, page_size=2000)
        connection.commit()
        print("Data inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert records into table", error)

    finally:
        # Closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return None


def get_gender_data():
    df = pd.DataFrame(columns=['id', 'name', 'gender'])
    # First we get the female information
    for gender in ['female', 'male']:
        url = 'https://pokeapi.co/api/v2/gender/{}'
        response = requests.get(url.format(gender)).text
        data = json.loads(response)
        aux = pd.DataFrame.from_dict(data["pokemon_species_details"])
        aux = pd.DataFrame(aux['pokemon_species'].tolist())
        aux['name'] = aux['name'].str.title()
        aux['id'] = aux['url'].apply(
            lambda x: x.replace('https://pokeapi.co/api/v2/pokemon-species/', '').replace('/', ''))
        aux = aux.drop(columns=['url'])
        aux['gender'] = gender
        df = pd.concat([df, aux])

    df['id'] = df['id'].astype('int')

    return df


def main():
    print("Hello young trainer! Let's organize this mess.")
    raw_data = read_raw_data()

    # Clean data
    print("Alright, now let's clean this mess.")
    df = clean_data(raw_data)

    # Write data in database
    print("Let's move this data in a better place")
    write_data_to_psql(df, 'pokedex.raw_pokedex')

    print("End of part 1. Let's move to dbt")

    print("First part of dbt: execute model fast_ice_pokemon")
    os.system("cd pokedex_models && dbt run --select pokedex.fast_ice_pokemon")

    print("Second part of dbt: execute model top_pokemons_type")
    os.system("cd pokedex_models && dbt run --select pokedex.top_pokemons_type")

    print("Third part of dbt: execute model mega_pokemons")
    os.system("cd pokedex_models && dbt run --select pokedex.mega_pokemons")

    print("And for finishing, please visit the Datastudio report"
        " https://datastudio.google.com/reporting/ff1ffe8a-c821-4d76-8888-285abb19a789 .")

    print("About the extra part: let's find out about the gender relation")
    df = get_gender_data()
    print("Let's write this brand new information in our pokedex database")
    write_data_to_psql(df, 'pokedex.gender_pokemons')
    print("Extra part of dbt: execute model gender_pokemon_distribution")
    os.system("cd pokedex_models && dbt run --select pokedex.gender_pokemon_distribution")
    print("End of the extra task")


if __name__ == '__main__':
    main()
