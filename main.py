import psycopg2
import mysql.connector
import pyodbc

class DatabaseSearcher:
    """
    A class to search for a specific value across all tables and columns of a given database.

    Attributes:
        db_type (str): Type of the database (postgresql, mysql, sqlserver).
        connection (Connection): Database connection object.
        cursor (Cursor): Cursor for executing database operations.
    """
    def __init__(self, db_config):
        """
        Initializes the DatabaseSearcher with the given database configuration.

        Args:
            db_config (dict): A dictionary containing database configuration.
        """
        self.db_type = db_config['type']
        if self.db_type == 'postgresql':
            self.connection = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password']
            )
        elif self.db_type == 'mysql':
            self.connection = mysql.connector.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password']
            )
        elif self.db_type == 'sqlserver':
            self.connection = pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={db_config["host"]};DATABASE={db_config["dbname"]};UID={db_config["user"]};PWD={db_config["password"]}'
            )
        self.cursor = self.connection.cursor()

    def search_value(self, search_value, expected_type, comparison_type):
        """
        Searches for the given value across all tables and columns of the configured database.

        Args:
            search_value (str): The value to search for.
            expected_type (str): The expected data type of the column.
            comparison_type (str): The type of comparison to use (LIKE or EQUAL).
        """
        if self.db_type == 'postgresql':
            # PostgreSQL specific query
            query = "SELECT table_schema, table_name, column_name FROM information_schema.columns WHERE data_type = %s"
            self.cursor.execute(query, (expected_type,))
        elif self.db_type == 'mysql':
            # MySQL specific query
            query = "SELECT table_schema, table_name, column_name FROM information_schema.columns WHERE data_type = %s"
            self.cursor.execute(query, (expected_type,))
        elif self.db_type == 'sqlserver':
            # SQL Server specific query
            query = "SELECT table_schema, table_name, column_name FROM information_schema.columns WHERE data_type = ?"
            self.cursor.execute(query, (expected_type,))

        columns = self.cursor.fetchall()

        for schema, table, column in columns:
            try:
                if self.db_type in ['postgresql', 'mysql']:
                    full_query = f"SELECT * FROM `{schema}`.`{table}` WHERE `{column}` {self._get_comparison_operator(comparison_type)} %s"
                    self.cursor.execute(full_query, (search_value,))
                elif self.db_type == 'sqlserver':
                    full_query = f"SELECT * FROM [{schema}].[{table}] WHERE [{column}] {self._get_comparison_operator(comparison_type)} ?"
                    self.cursor.execute(full_query, (search_value,))

                results = self.cursor.fetchall()

                if results:
                    print(f"Found in '{table}', column '{column}'")
            except Exception as e:
                print(f"Error in '{table}', column '{column}': {e}")
                self.connection.rollback()

    def _get_comparison_operator(self, comparison_type):
        """
        Returns the SQL operator for the given comparison type.

        Args:
            comparison_type (str): The type of comparison (LIKE or EQUAL).

        Returns:
            str: SQL operator for the comparison.
        """
        if comparison_type == 'LIKE':
            return "LIKE"
        elif comparison_type == 'EQUAL':
            return "="

    def close(self):
        """
        Closes the database connection and cursor.
        """
        self.cursor.close()
        self.connection.close()

def main():
    """
    Main function to execute the DatabaseSearcher from command line.
    """
    if len(sys.argv) != 10:
        print("Usage: python script.py db_type host port dbname user password search_value expected_type comparison_type")
        sys.exit(1)

    db_config = {
        'type': sys.argv[1],
        'host': sys.argv[2],
        'port': sys.argv[3],
        'dbname': sys.argv[4],
        'user': sys.argv[5],
        'password': sys.argv[6]
    }
    search_value = sys.argv[7]
    expected_type = sys.argv[8]
    comparison_type = sys.argv[9]

    searcher = DatabaseSearcher(db_config)
    searcher.search_value(search_value, expected_type, comparison_type)
    searcher.close()

if __name__ == "__main__":
    main()