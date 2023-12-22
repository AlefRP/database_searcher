from db_factory import DBConnectionFactory


class DatabaseSearcher:
    """
    A class to search for a specific value across all tables and columns of a given database.
    """

    def __init__(self, db_config):
        """
        Initializes the DatabaseSearcher with the given database configuration.

        Args:
            db_config (dict): A dictionary containing database configuration.
        """
        self.factory = DBConnectionFactory(db_config)
        self.connection = self.factory.create_connection()
        self.cursor = self.connection.cursor()

    def search_value(self, search_value, expected_type, comparison_type):
        """
        Searches for the given value across all tables and columns of the configured database.

        Args:
            search_value (str): The value to search for.
            expected_type (str): The expected data type of the column.
            comparison_type (str): The type of comparison to use (LIKE or EQUAL).
        """
        query = """
            SELECT table_schema, table_name, column_name
            FROM information_schema.columns
            WHERE data_type = %s
        """
        self.cursor.execute(query, (expected_type,))
        columns = self.cursor.fetchall()

        for schema, table, column in columns:
            try:
                sql = f"SELECT * FROM {schema}.{table} WHERE {column} {self._get_comparison_operator(comparison_type)} %s"
                self.cursor.execute(sql, (search_value,))
                results = self.cursor.fetchall()

                if results:
                    print(f"Found in '{table}', column '{column}': {results}")
            except Exception as e:
                print(f"Error searching in '{table}', column '{column}': {e}")
                # Optionally, you might want to log the error instead of printing it
                self.connection.rollback()

    def _get_comparison_operator(self, comparison_type):
        """
        Returns the SQL operator for the given comparison type.

        Args:
            comparison_type (str): The type of comparison (LIKE or EQUAL).

        Returns:
            str: SQL operator for the comparison.
        """
        if comparison_type == "LIKE":
            return "LIKE"
        elif comparison_type == "EQUAL":
            return "="
        else:
            raise ValueError(f"Invalid comparison type: {comparison_type}")

    def close(self):
        """
        Closes the database connection and cursor.
        """
        self.cursor.close()
        self.connection.close()
