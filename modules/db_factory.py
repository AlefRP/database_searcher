import psycopg2
import mysql.connector
import pyodbc


class DBConnectionFactory:
    """
    A factory class for creating database connections.

    This class is responsible for providing a connection object
    based on the type of database specified in the configuration.
    """

    def __init__(self, db_config):
        """
        Initializes the DBConnectionFactory with the given database configuration.

        Args:
            db_config (dict): A dictionary containing the database configuration.
                              Expected keys are:
                              - 'type' (str): Type of the database ('postgresql', 'mysql', 'sqlserver').
                              - 'host' (str): Hostname of the database server.
                              - 'port' (int): Port number of the database server.
                              - 'dbname' (str): Name of the database.
                              - 'user' (str): Username for the database.
                              - 'password' (str): Password for the database.
        """
        self.db_config = db_config

    def create_connection(self):
        """
        Creates and returns a database connection based on the stored configuration.

        Returns:
            Connection: A database connection object.

        Raises:
            ValueError: If the specified database type is not supported.
        """
        db_type = self.db_config["type"]
        if db_type == "postgresql":
            return psycopg2.connect(
                host=self.db_config["host"],
                port=self.db_config["port"],
                dbname=self.db_config["dbname"],
                user=self.db_config["user"],
                password=self.db_config["password"],
            )
        elif db_type == "mysql":
            return mysql.connector.connect(
                host=self.db_config["host"],
                port=self.db_config["port"],
                database=self.db_config["dbname"],
                user=self.db_config["user"],
                password=self.db_config["password"],
            )
        elif db_type == "sqlserver":
            return pyodbc.connect(
                f'DRIVER={{SQL Server}};SERVER={self.db_config["host"]};DATABASE={self.db_config["dbname"]};UID={self.db_config["user"]};PWD={self.db_config["password"]}'
            )
        else:
            raise ValueError("Unsupported database type")
