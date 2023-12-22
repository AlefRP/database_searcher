import sys
from modules.db_searcher import DatabaseSearcher


def main():
    """
    Main function to execute the DatabaseSearcher from the command line.

    The script expects command-line arguments for database configuration and search parameters.
    Usage: python script.py db_type host port dbname user password search_value expected_type comparison_type
    """
    if len(sys.argv) != 10:
        print(
            "Incorrect usage. Expected 9 arguments but got {}.".format(
                len(sys.argv) - 1
            )
        )
        print(
            "Usage: python script.py db_type host port dbname user password search_value expected_type comparison_type"
        )
        sys.exit(1)

    db_config = {
        "type": sys.argv[1],
        "host": sys.argv[2],
        "port": sys.argv[3],
        "dbname": sys.argv[4],
        "user": sys.argv[5],
        "password": sys.argv[6],
    }
    search_value = sys.argv[7]
    expected_type = sys.argv[8]
    comparison_type = sys.argv[9]

    searcher = DatabaseSearcher(db_config)
    try:
        searcher.search_value(search_value, expected_type, comparison_type)
    finally:
        searcher.close()


if __name__ == "__main__":
    main()
