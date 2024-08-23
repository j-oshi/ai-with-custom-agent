import sqlite3

# def count_software_companies():
#     """
#     Counts the number of software companies stored in the software_company table.

#     This function queries the software_company table in the connected SQLite database
#     and returns the total number of rows, representing the number of software companies.

#     Returns:
#         int: The total number of software companies in the database.
#     """
#     # Connect or create the database file
#     # Define database file path
#     db_file = "data/software_companies.db"
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#     cursor.execute("SELECT COUNT(*) FROM software_company")
#     count = cursor.fetchone()[0]
#     return count


def query_database(sql_command):
    """
    Executes an SQL command against a SQLite database containing two related tables:
    * **software_company** (name, postcode)
    * **software_location** (postcode, latitude, longitude)

    Args:
        sql_command (str or dict): The SQL command to execute. If a dictionary is provided, it must contain
            a key named "sql_command" with the SQL command as its value.

    Returns:
        list: A list of rows containing the results of the query.

    Raises:
        sqlite3.Error: If an error occurs while executing the SQL command.
    """

    connection = None

    try:
        if isinstance(sql_command, dict):
            sql_command = sql_command["sql_command"]

        connection = sqlite3.connect("./data/software_companies.db")
        cursor = connection.cursor()
        cursor.execute(sql_command)
        results = cursor.fetchall()
        return results

    except sqlite3.Error as error:
        print("Error:", error)
        raise  # Re-raise the exception for proper error handling

    finally:
        if connection:
            connection.close()
