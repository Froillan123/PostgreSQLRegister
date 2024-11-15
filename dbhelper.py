import psycopg2
from psycopg2 import sql
import os

# PostgreSQL connection URL
DATABASE_URL = "postgresql://kimperor:IpqD0dsN2w8XC50R68dWMSETpigqoEkK@dpg-csrcg4jtq21c73d1c270-a:5432/registration_kcg0"

# Function to establish database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to execute a SQL statement (insert, update, delete)
def postprocess(sql: str, params=None) -> bool:
    conn = get_db_connection()
    if conn is None:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        conn.commit()
        print("SQL executed and committed successfully.")  # Debugging line
        return True
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


# Function to execute a SELECT SQL query and return results
def getprocess(sql: str, params=None) -> list:
    conn = get_db_connection()
    if conn is None:
        return []
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params)
        data = cursor.fetchall()
        return data
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

# Function to retrieve all records from a table
def getall_records(table: str) -> list:
    sql = f'SELECT * FROM {table}'
    return getprocess(sql)

# Function to retrieve a single record from a table based on conditions
def getone_record(table: str, **kwargs) -> list:
    keys = list(kwargs.keys())
    values = list(kwargs.values())
    query = sql.SQL("SELECT * FROM {table} WHERE {key} = %s").format(
        table=sql.Identifier(table),
        key=sql.Identifier(keys[0])
    )
    conn = get_db_connection()  # Establish the connection
    if conn is None:
        return []

    try:
        # Use the connection to execute the query
        return getprocess(query.as_string(conn), (values[0],))
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return []
    finally:
        conn.close()

# Function to add a record to a table
def add_record(table: str, **kwargs) -> bool:
    keys = list(kwargs.keys())
    values = list(kwargs.values())
    fields = ", ".join(keys)
    data = "', '".join(values)
    sql = f"INSERT INTO {table} ({fields}) VALUES('{data}')"
    print(f"Executing SQL: {sql}")  # Debugging line
    return postprocess(sql)


# Function to update a record in a table
def update_record(table: str, **kwargs) -> bool:
    keys = list(kwargs.keys())
    values = list(kwargs.values())
    fields = [f"{keys[i]} = '{values[i]}'" for i in range(1, len(keys))]
    field = ', '.join(fields)
    sql = f"UPDATE {table} SET {field} WHERE {keys[0]} = '{values[0]}'"
    return postprocess(sql)

# Function to delete a record from a table
def delete_record(table: str, **kwargs) -> bool:
    keys = list(kwargs.keys())
    values = list(kwargs.values())
    sql = f"DELETE FROM {table} WHERE {keys[0]} = '{values[0]}'"
    return postprocess(sql)
