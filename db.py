import sqlite3
import pandas as pd
from sqlalchemy import create_engine

db = "bbfa-db.db"

engine = create_engine("sqlite:///foo.db")


def create():
    # Connect to database
    conn = sqlite3.connect(db)

    # Open the cursor
    cursor = conn.cursor()

    # Open the external sql file.
    file = open("create_table.sql", "r")

    # Read out the sql script text in the file.
    sql_script_string = file.read()

    # Close the sql file object.
    file.close()

    # Run the sql script string
    cursor.executescript(sql_script_string)

    # Commit the changes
    conn.commit()

    # Close connection
    conn.close()


def run_query(q):
    with sqlite3.connect(db) as conn:
        return pd.read_sql(q, conn)


def run_command(c):
    with sqlite3.connect(db) as conn:
        conn.isolation_level = None
        conn.execute(c)


def show_tables():
    q = """
        SELECT
            name
        FROM sqlite_master
        WHERE type IN ("table","view");
        """
    return run_query(q)


def get_table_row_count(tablename):
    q = (
        """
        SELECT
            COUNT(1)
        FROM %s;
        """
        % tablename
    )
    return run_query(q)["COUNT(1)"][0]


if __name__ == "__main__":
    create()
