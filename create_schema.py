import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error


def create_table(conn, table_name, create_sql):
    """Helper function to create a table"""
    cur = conn.cursor()
    try:
        cur.execute(create_sql)
        conn.commit()
        print(f"[OK] Created/checked table: {table_name}")
    except Error as e:
        print(f"[ERROR] Error creating table {table_name}: {e}")
    finally:
        cur.close()


def create_players_table(conn):
    """Create players table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS players (
        player_id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(255),
        name VARCHAR(255),
        country VARCHAR(100),
        playing_role VARCHAR(100),
        batting_style VARCHAR(100),
        bowling_style VARCHAR(100),
        total_runs INT DEFAULT 0,
        total_wickets INT DEFAULT 0,
        team_id INT
    );
    """
    create_table(conn, "players", create_sql)


def create_recent_matches_table(conn):
    """Create recent_matches table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS recent_matches (
        match_id INT AUTO_INCREMENT PRIMARY KEY,
        match_desc VARCHAR(500),
        team1 VARCHAR(100),
        team2 VARCHAR(100),
        venue VARCHAR(200),
        venue_city VARCHAR(100),
        start_date DATE,
        status VARCHAR(500),
        state VARCHAR(50),
        UNIQUE KEY unique_match (team1, team2, start_date)
    );
    """
    create_table(conn, "recent_matches", create_sql)


def create_top_odi_runs_table(conn):
    """Create top_odi_runs table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS top_odi_runs (
        player_id INT AUTO_INCREMENT PRIMARY KEY,
        player_name VARCHAR(255),
        runs INT,
        average DECIMAL(10, 2),
        centuries INT DEFAULT 0
    );
    """
    create_table(conn, "top_odi_runs", create_sql)


def create_venues_table(conn):
    """Create venues table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS venues (
        venue_id INT AUTO_INCREMENT PRIMARY KEY,
        venue_name VARCHAR(255),
        city VARCHAR(100),
        country VARCHAR(100),
        capacity VARCHAR(100)
    );
    """
    create_table(conn, "venues", create_sql)


def create_combined_matches_table(conn):
    """Create combined_matches table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS combined_matches (
        match_id INT AUTO_INCREMENT PRIMARY KEY,
        team1 VARCHAR(100),
        team2 VARCHAR(100),
        match_winner VARCHAR(100),
        win_margin VARCHAR(100),
        format VARCHAR(50),
        venue VARCHAR(200),
        match_date DATE,
        toss_winner VARCHAR(100),
        toss_decision VARCHAR(50),
        UNIQUE KEY unique_match (team1, team2, match_date)
    );
    """
    create_table(conn, "combined_matches", create_sql)


def create_batting_data_table(conn):
    """Create batting_data table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS batting_data (
        batting_id INT AUTO_INCREMENT PRIMARY KEY,
        match_id INT,
        player_id INT,
        player_name VARCHAR(255),
        runs INT,
        balls INT,
        strike_rate DECIMAL(10, 2),
        dismissal VARCHAR(100),
        team VARCHAR(100),
        innings_no INT,
        UNIQUE KEY unique_batting (match_id, player_id, innings_no),
        FOREIGN KEY (match_id) REFERENCES combined_matches(match_id) ON DELETE CASCADE,
        FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE SET NULL
    );
    """
    create_table(conn, "batting_data", create_sql)


def create_series_matches_table(conn):
    """Create series_matches table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS series_matches (
        series_match_id INT AUTO_INCREMENT PRIMARY KEY,
        series_name VARCHAR(255),
        team1 VARCHAR(100),
        team2 VARCHAR(100),
        venue VARCHAR(200),
        match_format VARCHAR(50),
        start_date DATE,
        status VARCHAR(500)
    );
    """
    create_table(conn, "series_matches", create_sql)


def create_players_stats_table(conn):
    """Create players_stats table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS players_stats (
        stat_id INT AUTO_INCREMENT PRIMARY KEY,
        player_name VARCHAR(255),
        player_id INT,
        test_runs INT DEFAULT 0,
        odi_runs INT DEFAULT 0,
        t20_runs INT DEFAULT 0,
        FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE
    );
    """
    create_table(conn, "players_stats", create_sql)


def create_players_partnerships_data_table(conn):
    """Create players_partnerships_data table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS players_partnerships_data (
        partnership_id INT AUTO_INCREMENT PRIMARY KEY,
        match_id INT,
        innings_no INT,
        batter1_name VARCHAR(255),
        batter2_name VARCHAR(255),
        runs_partnership INT,
        wicket_fallen INT,
        FOREIGN KEY (match_id) REFERENCES combined_matches(match_id) ON DELETE CASCADE
    );
    """
    create_table(conn, "players_partnerships_data", create_sql)


def create_bowlers_bowling_venue_data_table(conn):
    """Create bowlers_bowling_venue_data table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS bowlers_bowling_venue_data (
        bowling_id INT AUTO_INCREMENT PRIMARY KEY,
        match_id INT,
        player_id INT,
        player_name VARCHAR(255),
        venue VARCHAR(200),
        overs DECIMAL(10, 1),
        runs_conceded INT,
        wickets INT,
        economy_rate DECIMAL(10, 2),
        FOREIGN KEY (match_id) REFERENCES combined_matches(match_id) ON DELETE CASCADE,
        FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE SET NULL
    );
    """
    create_table(conn, "bowlers_bowling_venue_data", create_sql)


def create_batters_batting_data_table(conn):
    """Create batters_batting_data table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS batters_batting_data (
        batter_id INT AUTO_INCREMENT PRIMARY KEY,
        match_id INT,
        player_id INT,
        player_name VARCHAR(255),
        runs INT,
        balls_faced INT,
        strike_rate DECIMAL(10, 2),
        date DATE,
        FOREIGN KEY (match_id) REFERENCES combined_matches(match_id) ON DELETE CASCADE,
        FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE SET NULL
    );
    """
    create_table(conn, "batters_batting_data", create_sql)


def create_bowling_data_table(conn):
    """Create bowling_data table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS bowling_data (
        bowling_id INT AUTO_INCREMENT PRIMARY KEY,
        match_id INT,
        player_id INT,
        player_name VARCHAR(255),
        overs DECIMAL(10, 1),
        runs_conceded INT,
        wickets INT,
        economy_rate DECIMAL(10, 2),
        format VARCHAR(50),
        UNIQUE KEY unique_bowling (match_id, player_id),
        FOREIGN KEY (match_id) REFERENCES combined_matches(match_id) ON DELETE CASCADE,
        FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE SET NULL
    );
    """
    create_table(conn, "bowling_data", create_sql)


def create_fielding_data_table(conn):
    """Create fielding_data table"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS fielding_data (
        fielding_id INT AUTO_INCREMENT PRIMARY KEY,
        match_id INT,
        player_id INT,
        catches INT DEFAULT 0,
        stumpings INT DEFAULT 0,
        run_outs INT DEFAULT 0,
        format VARCHAR(50),
        FOREIGN KEY (match_id) REFERENCES combined_matches(match_id) ON DELETE CASCADE,
        FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE SET NULL
    );
    """
    create_table(conn, "fielding_data", create_sql)


def main():
    load_dotenv()
    host = os.getenv("DB_HOST") or "localhost"
    user = os.getenv("DB_USER") or "root"
    password = os.getenv("DB_PASSWORD") or ""
    database = os.getenv("DB_NAME") or None

    if not database:
        print("DB_NAME not set in environment. Please set DB_NAME in your .env file.")
        return

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            autocommit=True,
        )
        if conn.is_connected():
            print(f"[OK] Connected to database '{database}'. Creating tables...")
            print("=" * 60)
            
            # Create all tables
            create_players_table(conn)
            create_recent_matches_table(conn)
            create_top_odi_runs_table(conn)
            create_venues_table(conn)
            create_combined_matches_table(conn)
            create_batting_data_table(conn)
            create_series_matches_table(conn)
            create_players_stats_table(conn)
            create_players_partnerships_data_table(conn)
            create_bowlers_bowling_venue_data_table(conn)
            create_batters_batting_data_table(conn)
            create_bowling_data_table(conn)
            create_fielding_data_table(conn)
            
            print("=" * 60)
            print("[OK] All tables created successfully!")
            print("\nNext steps:")
            print("   1. Run seed_data.py to populate sample data")
            print("   2. Start using the SQL Analytics page to run queries")
            
        conn.close()
    except Error as e:
        print(f"[ERROR] Error connecting or creating tables: {e}")


if __name__ == '__main__':
    main()
