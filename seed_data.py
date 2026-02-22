import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta


def get_connection():
    """Create and return database connection"""
    load_dotenv()
    host = os.getenv("DB_HOST") or "localhost"
    user = os.getenv("DB_USER") or "root"
    password = os.getenv("DB_PASSWORD") or ""
    database = os.getenv("DB_NAME") or None
    
    if not database:
        raise ValueError("DB_NAME not set in environment. Please set DB_NAME in your .env file.")
    
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        autocommit=True,
    )


def insert_sample_players(conn):
    """Insert sample player data"""
    players_data = [
        ("Virat Kohli", "Virat Kohli", "India", "Batsman", "Right-handed", "Right-arm medium", 12000, 0),
        ("Rohit Sharma", "Rohit Sharma", "India", "Batsman", "Right-handed", "Right-arm offbreak", 10000, 0),
        ("Jasprit Bumrah", "Jasprit Bumrah", "India", "Bowler", "Right-handed", "Right-arm fast", 200, 300),
        ("Ravindra Jadeja", "Ravindra Jadeja", "India", "Allrounder", "Left-handed", "Left-arm orthodox", 2500, 250),
        ("MS Dhoni", "MS Dhoni", "India", "Wicket-keeper", "Right-handed", "Right-arm medium", 10000, 0),
        ("Steve Smith", "Steve Smith", "Australia", "Batsman", "Right-handed", "Right-arm legbreak", 8000, 20),
        ("Pat Cummins", "Pat Cummins", "Australia", "Bowler", "Right-handed", "Right-arm fast", 500, 200),
        ("Ben Stokes", "Ben Stokes", "England", "Allrounder", "Left-handed", "Right-arm fast-medium", 5000, 150),
        ("Kane Williamson", "Kane Williamson", "New Zealand", "Batsman", "Right-handed", "Right-arm offbreak", 7000, 30),
        ("Babar Azam", "Babar Azam", "Pakistan", "Batsman", "Right-handed", "Right-arm legbreak", 6000, 0),
    ]
    
    cur = conn.cursor()
    insert_sql = """
    INSERT INTO players (full_name, name, country, playing_role, batting_style, bowling_style, total_runs, total_wickets)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cur.executemany(insert_sql, players_data)
        print(f"[OK] Inserted {len(players_data)} players")
    except Error as e:
        print(f"[ERROR] Error inserting players: {e}")
    finally:
        cur.close()


def insert_sample_venues(conn):
    """Insert sample venue data"""
    venues_data = [
        ("Wankhede Stadium", "Mumbai", "India", "33000"),
        ("Eden Gardens", "Kolkata", "India", "66000"),
        ("MCG", "Melbourne", "Australia", "100024"),
        ("Lord's", "London", "England", "30000"),
        ("Sydney Cricket Ground", "Sydney", "Australia", "48000"),
        ("Narendra Modi Stadium", "Ahmedabad", "India", "132000"),
    ]
    
    cur = conn.cursor()
    insert_sql = """
    INSERT INTO venues (venue_name, city, country, capacity)
    VALUES (%s, %s, %s, %s)
    """
    
    try:
        cur.executemany(insert_sql, venues_data)
        print(f"[OK] Inserted {len(venues_data)} venues")
    except Error as e:
        print(f"[ERROR] Error inserting venues: {e}")
    finally:
        cur.close()


def insert_sample_recent_matches(conn):
    """Insert sample recent matches"""
    today = datetime.now()
    matches_data = [
        ("India vs Australia - 1st ODI", "India", "Australia", "Wankhede Stadium", "Mumbai", 
         today - timedelta(days=5), "India won by 5 wickets", "Complete"),
        ("England vs New Zealand - 2nd Test", "England", "New Zealand", "Lord's", "London",
         today - timedelta(days=10), "England won by 3 wickets", "Complete"),
        ("Pakistan vs South Africa - T20", "Pakistan", "South Africa", "MCG", "Melbourne",
         today - timedelta(days=2), "Pakistan won by 20 runs", "Complete"),
        ("India vs England - 3rd ODI", "India", "England", "Eden Gardens", "Kolkata",
         today - timedelta(days=1), "Match in progress", "Live"),
    ]
    
    cur = conn.cursor()
    insert_sql = """
    INSERT INTO recent_matches (match_desc, team1, team2, venue, venue_city, start_date, status, state)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cur.executemany(insert_sql, matches_data)
        print(f"[OK] Inserted {len(matches_data)} recent matches")
    except Error as e:
        print(f"[ERROR] Error inserting recent matches: {e}")
    finally:
        cur.close()


def insert_sample_combined_matches(conn):
    """Insert sample combined matches"""
    today = datetime.now()
    matches_data = [
        ("India", "Australia", "India", "5 wickets", "ODI", "Wankhede Stadium", today - timedelta(days=5), "India", "bat"),
        ("England", "New Zealand", "England", "3 wickets", "Test", "Lord's", today - timedelta(days=10), "England", "bowl"),
        ("Pakistan", "South Africa", "Pakistan", "20 runs", "T20", "MCG", today - timedelta(days=2), "Pakistan", "bat"),
        ("India", "England", "India", "45 runs", "ODI", "Eden Gardens", today - timedelta(days=1), "India", "bowl"),
    ]
    
    cur = conn.cursor()
    insert_sql = """
    INSERT INTO combined_matches (team1, team2, match_winner, win_margin, format, venue, match_date, toss_winner, toss_decision)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cur.executemany(insert_sql, matches_data)
        print(f"[OK] Inserted {len(matches_data)} combined matches")
    except Error as e:
        print(f"[ERROR] Error inserting combined matches: {e}")
    finally:
        cur.close()


def insert_sample_top_odi_runs(conn):
    """Insert sample top ODI run scorers"""
    top_runs_data = [
        ("Virat Kohli", 12000, 59.07, 43),
        ("Rohit Sharma", 10000, 49.27, 29),
        ("MS Dhoni", 10000, 50.57, 10),
        ("Steve Smith", 8000, 44.83, 12),
        ("Kane Williamson", 7000, 47.54, 13),
        ("Babar Azam", 6000, 56.83, 18),
    ]
    
    cur = conn.cursor()
    insert_sql = """
    INSERT INTO top_odi_runs (player_name, runs, average, centuries)
    VALUES (%s, %s, %s, %s)
    """
    
    try:
        cur.executemany(insert_sql, top_runs_data)
        print(f"[OK] Inserted {len(top_runs_data)} top ODI run scorers")
    except Error as e:
        print(f"[ERROR] Error inserting top ODI runs: {e}")
    finally:
        cur.close()


def insert_sample_series_matches(conn):
    """Insert sample series matches"""
    today = datetime.now()
    series_data = [
        ("India Tour of Australia 2024", "India", "Australia", "MCG", "ODI", today - timedelta(days=30), "India won by 5 wickets"),
        ("England Tour of India 2024", "England", "India", "Wankhede Stadium", "Test", today - timedelta(days=20), "India won by 8 wickets"),
        ("T20 World Cup 2024", "Pakistan", "South Africa", "Narendra Modi Stadium", "T20", today - timedelta(days=15), "Pakistan won by 20 runs"),
    ]
    
    cur = conn.cursor()
    insert_sql = """
    INSERT INTO series_matches (series_name, team1, team2, venue, match_format, start_date, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cur.executemany(insert_sql, series_data)
        print(f"[OK] Inserted {len(series_data)} series matches")
    except Error as e:
        print(f"[ERROR] Error inserting series matches: {e}")
    finally:
        cur.close()


def insert_sample_batting_data(conn):
    """Insert sample batting data"""
    # Get match_ids and player_ids
    cur = conn.cursor()
    cur.execute("SELECT match_id FROM combined_matches LIMIT 4")
    match_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT player_id, name FROM players LIMIT 5")
    players = cur.fetchall()
    
    if not match_ids or not players:
        print("[WARNING] No matches or players found. Skipping batting data.")
        cur.close()
        return
    
    batting_data = []
    for i, match_id in enumerate(match_ids):
        for j, (player_id, name) in enumerate(players[:3]):
            batting_data.append((
                match_id, player_id, name, 
                50 + (i * 10) + (j * 5),  # runs
                40 + (i * 5) + (j * 3),   # balls
                120.0 + (i * 5),           # strike_rate
                "caught" if j % 2 == 0 else "not out",  # dismissal
                "India" if i % 2 == 0 else "Australia",  # team
                1 if i < 2 else 2  # innings_no
            ))
    
    insert_sql = """
    INSERT INTO batting_data (match_id, player_id, player_name, runs, balls, strike_rate, dismissal, team, innings_no)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cur.executemany(insert_sql, batting_data)
        print(f"[OK] Inserted {len(batting_data)} batting records")
    except Error as e:
        print(f"[ERROR] Error inserting batting data: {e}")
    finally:
        cur.close()


def insert_sample_players_stats(conn):
    """Insert sample players stats"""
    cur = conn.cursor()
    cur.execute("SELECT player_id, name FROM players LIMIT 6")
    players = cur.fetchall()
    
    if not players:
        print("[WARNING] No players found. Skipping players stats.")
        cur.close()
        return
    
    stats_data = []
    for i, (player_id, name) in enumerate(players):
        stats_data.append((
            name, player_id,
            2000 + (i * 500) if i % 2 == 0 else 0,  # test_runs
            3000 + (i * 400) if i % 3 != 0 else 0,  # odi_runs
            1000 + (i * 200) if i % 2 == 1 else 0,  # t20_runs
        ))
    
    insert_sql = """
    INSERT INTO players_stats (player_name, player_id, test_runs, odi_runs, t20_runs)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    try:
        cur.executemany(insert_sql, stats_data)
        print(f"[OK] Inserted {len(stats_data)} player stats records")
    except Error as e:
        print(f"[ERROR] Error inserting players stats: {e}")
    finally:
        cur.close()


def insert_sample_batters_batting_data(conn):
    """Insert sample batters batting data"""
    cur = conn.cursor()
    cur.execute("SELECT match_id FROM combined_matches LIMIT 4")
    match_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT player_id, name FROM players LIMIT 5")
    players = cur.fetchall()
    
    if not match_ids or not players:
        print("[WARNING] No matches or players found. Skipping batters batting data.")
        cur.close()
        return
    
    today = datetime.now()
    batters_data = []
    for i, match_id in enumerate(match_ids):
        for j, (player_id, name) in enumerate(players[:3]):
            batters_data.append((
                match_id, player_id, name,
                40 + (i * 10) + (j * 5),  # runs
                30 + (i * 5) + (j * 3),   # balls_faced
                130.0 + (i * 5),          # strike_rate
                today - timedelta(days=30-i)  # date
            ))
    
    insert_sql = """
    INSERT INTO batters_batting_data (match_id, player_id, player_name, runs, balls_faced, strike_rate, date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cur.executemany(insert_sql, batters_data)
        print(f"[OK] Inserted {len(batters_data)} batters batting records")
    except Error as e:
        print(f"[ERROR] Error inserting batters batting data: {e}")
    finally:
        cur.close()


def insert_sample_bowling_data(conn):
    """Insert sample bowling data"""
    cur = conn.cursor()
    cur.execute("SELECT match_id FROM combined_matches LIMIT 4")
    match_ids = [row[0] for row in cur.fetchall()]
    
    cur.execute("SELECT player_id, name FROM players WHERE playing_role IN ('Bowler', 'Allrounder') LIMIT 3")
    players = cur.fetchall()
    
    if not match_ids or not players:
        print("[WARNING] No matches or bowlers found. Skipping bowling data.")
        cur.close()
        return
    
    bowling_data = []
    for i, match_id in enumerate(match_ids):
        for j, (player_id, name) in enumerate(players):
            bowling_data.append((
                match_id, player_id, name,
                10.0,  # overs
                50 + (i * 10),  # runs_conceded
                2 + j,  # wickets
                5.0 + (i * 0.5),  # economy_rate
                ["ODI", "Test", "T20"][i % 3]  # format
            ))
    
    insert_sql = """
    INSERT INTO bowling_data (match_id, player_id, player_name, overs, runs_conceded, wickets, economy_rate, format)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        cur.executemany(insert_sql, bowling_data)
        print(f"[OK] Inserted {len(bowling_data)} bowling records")
    except Error as e:
        print(f"[ERROR] Error inserting bowling data: {e}")
    finally:
        cur.close()


def main():
    """Main function to seed all sample data"""
    try:
        conn = get_connection()
        if conn.is_connected():
            print("=" * 60)
            print("Seeding sample data into cricket_db...")
            print("=" * 60)
            
            # Insert data in order (respecting foreign keys)
            insert_sample_players(conn)
            insert_sample_venues(conn)
            insert_sample_recent_matches(conn)
            insert_sample_combined_matches(conn)
            insert_sample_top_odi_runs(conn)
            insert_sample_series_matches(conn)
            insert_sample_batting_data(conn)
            insert_sample_players_stats(conn)
            insert_sample_batters_batting_data(conn)
            insert_sample_bowling_data(conn)
            
            print("=" * 60)
            print("[OK] Sample data seeding completed!")
            print("\nYou can now:")
            print("   1. Run SQL queries in the SQL Analytics page")
            print("   2. View data in the CRUD Operations page")
            print("   3. Test all 25 SQL queries")
            
        conn.close()
    except Error as e:
        print(f"[ERROR] Error: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")


if __name__ == '__main__':
    main()

