import mysql.connector
from mysql.connector import Error


def connect_to_db(host, port, user, password, schema):
    """Establish connection to MySQL database"""
    try:
        print(f"Attempting to connect to {host}:{port} with user '{user}' to schema '{schema}'")
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=schema,
            autocommit=True,
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            print(f"Successfully connected to {schema} database")
            return connection
    except Error as e:
        error_msg = str(e)
        print(f"Connection Error: {error_msg}")
        return None
    except Exception as e:
        error_msg = str(e)
        print(f"Unexpected Error: {error_msg}")
        return None


def get_tables(connection):
    """Retrieve all table names from the connected database"""
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        return tables
    except Error as e:
        print(f"Error retrieving tables: {e}")
        return []
