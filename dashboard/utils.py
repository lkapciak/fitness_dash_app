import pandas as pd
import psycopg2

def connect_to_database(host, port, database, user, password):

    return psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port)


def fetch_query_results(cursor, query_text):
    cursor.execute(query_text)
    return pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
