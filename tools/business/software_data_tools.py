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
  This function takes an SQL command as a string and executes it against the 
  software_company table. It returns a list of rows containing the 
  results of the query.

  Args:
      sql_command (str): The SQL command to execute.

  Returns:
      list: A list of rows containing the results of the query.
  """
  connection = None
  try:
    connection = sqlite3.connect("./data/software_companies.db")
    cursor = connection.cursor()
    cursor.execute(sql_command)
    results = cursor.fetchall()
    return results
  except sqlite3.Error as error:
    print("Error:", error)
  finally:
    if connection:
      connection.close()
