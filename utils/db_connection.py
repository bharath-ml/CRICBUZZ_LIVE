import mysql.connector
from mysql.connector import Error
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from urllib.parse import quote_plus

def create_connection(host, user, passwd, database=None):
    """Create a new MySQL connection. Don't cache connections across reruns."""
    return mysql.connector.connect(
        host=host,
        user=user,
        password=passwd,
        database=database,
        autocommit=True,
    )

@st.cache_data(ttl=300)
def list_databases(host, user, passwd):
    """Returns a list of available user databases, excluding system databases."""
    conn = create_connection(host, user, passwd)
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    all_databases = [db[0] for db in cursor]
    cursor.close()
    conn.close()

    excluded_dbs = {"information_schema", "performance_schema", "mysql", "sys"}
    return sorted([db for db in all_databases if db not in excluded_dbs])

@st.cache_data(ttl=300)
def list_tables(host, user, passwd, database):
    """Returns a list of tables for a specific database."""
    try:
        conn = create_connection(host, user, passwd, database)
        cursor = conn.cursor()
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'BASE TABLE'")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return sorted(tables)
    except Error:
        return []

@st.cache_data(ttl=300)
def get_table_columns(host, user, passwd, database, table):
    """Returns a list of columns for a specific table."""
    try:
        conn = create_connection(host, user, passwd, database)
        cursor = conn.cursor()
        col_q = """
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
            ORDER BY ORDINAL_POSITION
        """
        cursor.execute(col_q, (database, table))
        cols = cursor.fetchall()
        cursor.close()
        conn.close()

        return [
            {
                "name": c[0],
                "type": c[1],
                "nullable": c[2],
                "key": c[3],
                "default": c[4],
                "extra": c[5],
            }
            for c in cols
        ]
    except Error:
        return []

def fetch_table(host, user, passwd, database, table, limit=200):
    """Return dataframe and the exact SQL used."""
    sql = f"SELECT * FROM `{table}` LIMIT {int(limit)};"
    password_encoded = quote_plus(passwd)
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password_encoded}@{host}/{database}")
    df = pd.read_sql(sql, engine)
    engine.dispose()
    return df, sql

def run_select(host, user, passwd, database, select_sql):
    """Run a user-provided SELECT (read-only)."""
    if not select_sql.strip().lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed here.")
    password_encoded = quote_plus(passwd)
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password_encoded}@{host}/{database}")
    df = pd.read_sql(select_sql, engine)
    engine.dispose()
    return df

def insert_row(host, user, passwd, database, table, data):
    """Insert a row using parameterized SQL. Returns affected rows and SQL preview."""
    cols = [f"`{c}`" for c in data.keys()]
    placeholders = ", ".join(["%s"] * len(cols))
    sql = f"INSERT INTO `{table}` ({', '.join(cols)}) VALUES ({placeholders});"
    values = list(data.values())

    conn = create_connection(host, user, passwd, database)
    cur = conn.cursor()
    cur.execute(sql, values)
    affected = cur.rowcount
    cur.close()
    conn.close()
    return affected, sql

def delete_rows(host, user, passwd, database, table, where_clause):
    """Delete rows matching a WHERE clause. (Use carefully.)"""
    where = where_clause.strip()
    if not where:
        raise ValueError("Refusing to delete without a WHERE clause.")
    sql = f"DELETE FROM `{table}` WHERE {where};"
    conn = create_connection(host, user, passwd, database)
    cur = conn.cursor()
    cur.execute(sql)
    affected = cur.rowcount
    cur.close()
    conn.close()
    return affected, sql

def execute_update(host, user, passwd, database, table, set_clause, where_clause):
    """Run an UPDATE with user-provided SET and WHERE parts."""
    set_part = set_clause.strip()
    where_part = where_clause.strip()
    if not set_part:
        raise ValueError("SET clause cannot be empty.")
    if not where_part:
        raise ValueError("Refusing to update without a WHERE clause.")
    sql = f"UPDATE `{table}` SET {set_part} WHERE {where_part};"
    conn = create_connection(host, user, passwd, database)
    cur = conn.cursor()
    cur.execute(sql)
    affected = cur.rowcount
    cur.close()
    conn.close()
    return affected, sql
