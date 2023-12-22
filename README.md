# DatabaseSearcher :mag_right:

> A versatile tool for searching specific values across different database types including PostgreSQL, MySQL, and SQL Server.

## :page_with_curl: Introduction

`DatabaseSearcher` is a Python tool designed to facilitate searching for specific values across all tables and columns of various types of databases. It supports PostgreSQL, MySQL, and SQL Server, making it a versatile solution for database administrators and developers.

## :gear: Installation

Before installing `DatabaseSearcher`, ensure you have Python installed on your system. Then, you can install the necessary database drivers using pip:

```bash
pip install psycopg2-binary mysql-connector-python pyodbc
```

## :rocket: Usage

To use `DatabaseSearcher`, you need to set up your database configuration. Here's an example for PostgreSQL:

```python
db_config = {
    'type': 'postgresql',
    'host': 'localhost',
    'port': 5432,
    'dbname': 'mydatabase',
    'user': 'myuser',
    'password': 'mypassword'
}
```

After configuring the database, you can initialize and use DatabaseSearcher as follows:

```python
from db_searcher import DatabaseSearcher

# Create an instance of the DatabaseSearcher
searcher = DatabaseSearcher(db_config)

# Perform the search
search_value = 'value_to_search'
expected_type = 'data_type_of_column'
comparison_type = 'LIKE'  # or 'EQUAL'

try:
    searcher.search_value(search_value, expected_type, comparison_type)
finally:
    searcher.close()
```

This section provides clear instructions on how to set up and use the `DatabaseSearcher` with a PostgreSQL database as an example. The Python code snippets illustrate how to configure the database, initialize the searcher, and perform a search operation.

## :memo: License

This project is licensed under the [MIT License](LICENSE.md) - see the LICENSE file for details.

## :email: Contact

If you have any questions, feature requests, or bug reports, please feel free to open an issue on our GitHub repository. We welcome contributions, so if you'd like to make changes or improvements, please fork the repository and submit a pull request.

- **Open an Issue**: [GitHub Issues](https://github.com/AlefRP/database_searcher/issues)
- **Submit a Pull Request**: Fork the repository and create a pull request with your changes.