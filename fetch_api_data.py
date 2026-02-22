"""
Fetch real cricket data from Cricbuzz API and populate MySQL database.
This script fetches live data from the API and stores it in the database.
"""
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import requests
from datetime import datetime
import time


class CricbuzzAPIClient:
    """Client for Cricbuzz API"""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("RAPIDAPI_KEY")
        self.base_url = "https://cricbuzz-cricket.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
        }
    
    def get_live_matches(self):
        """Fetch live matches"""
        try:
            url = f"{self.base_url}/matches/v1/live"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[ERROR] API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"[ERROR] Error fetching live matches: {e}")
            return None
    
    def get_recent_matches(self):
        """Fetch recent matches"""
        try:
            url = f"{self.base_url}/matches/v1/recent"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"[ERROR] API Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"[ERROR] Error fetching recent matches: {e}")
            return None
    
    def get_scorecard(self, match_id):
        """Fetch detailed scorecard for a match"""
        try:
            url = f"{self.base_url}/mcenter/v1/{match_id}/scard"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"[ERROR] Error fetching scorecard for {match_id}: {e}")
            return None
    
    def search_players(self, query):
        """Search for players"""
        try:
            url = f"{self.base_url}/stats/v1/player/search"
            params = {"plrN": query}
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"[ERROR] Error searching players: {e}")
            return None
    
    def get_player_details(self, player_id):
        """Get player details"""
        try:
            url = f"{self.base_url}/stats/v1/player/{player_id}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"[ERROR] Error fetching player {player_id}: {e}")
            return None


class DatabaseManager:
    """Manages database operations"""
    
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("DB_HOST") or "localhost"
        self.user = os.getenv("DB_USER") or "root"
        self.password = os.getenv("DB_PASSWORD") or ""
        self.database = os.getenv("DB_NAME") or "cricket_db"
        self.conn = None
    
    def connect(self):
        """Connect to database"""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=True
            )
            return True
        except Error as e:
            print(f"[ERROR] Database connection failed: {e}")
            return False
    
    def close(self):
        """Close database connection"""
        if self.conn and self.conn.is_connected():
            self.conn.close()
    
    def insert_or_update_player(self, player_data):
        """Insert or update player in database"""
        cur = self.conn.cursor()
        try:
            # Check if player exists
            check_sql = "SELECT player_id FROM players WHERE name = %s OR full_name = %s"
            cur.execute(check_sql, (player_data.get('name', ''), player_data.get('full_name', '')))
            existing = cur.fetchone()
            
            if existing:
                # Update existing player
                update_sql = """
                UPDATE players SET 
                    full_name = %s, name = %s, country = %s, playing_role = %s,
                    batting_style = %s, bowling_style = %s
                WHERE player_id = %s
                """
                cur.execute(update_sql, (
                    player_data.get('full_name', ''),
                    player_data.get('name', ''),
                    player_data.get('country', ''),
                    player_data.get('playing_role', ''),
                    player_data.get('batting_style', ''),
                    player_data.get('bowling_style', ''),
                    existing[0]
                ))
                return existing[0]
            else:
                # Insert new player
                insert_sql = """
                INSERT INTO players (full_name, name, country, playing_role, batting_style, bowling_style, total_runs, total_wickets)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(insert_sql, (
                    player_data.get('full_name', ''),
                    player_data.get('name', ''),
                    player_data.get('country', ''),
                    player_data.get('playing_role', ''),
                    player_data.get('batting_style', ''),
                    player_data.get('bowling_style', ''),
                    player_data.get('total_runs', 0),
                    player_data.get('total_wickets', 0)
                ))
                return cur.lastrowid
        except Error as e:
            print(f"[ERROR] Error inserting player: {e}")
            return None
        finally:
            cur.close()
    
    def insert_match(self, match_data):
        """Insert match into recent_matches and combined_matches"""
        cur = self.conn.cursor()
        try:
            # Check if match already exists in recent_matches
            check_sql = """
            SELECT match_id FROM recent_matches 
            WHERE team1 = %s AND team2 = %s AND start_date = %s
            """
            cur.execute(check_sql, (
                match_data.get('team1', ''),
                match_data.get('team2', ''),
                match_data.get('start_date')
            ))
            existing = cur.fetchone()
            
            if existing:
                match_id = existing[0]
                # Update existing match
                update_sql = """
                UPDATE recent_matches SET 
                    status = %s, state = %s, venue = %s, venue_city = %s
                WHERE match_id = %s
                """
                cur.execute(update_sql, (
                    match_data.get('status', ''),
                    match_data.get('state', ''),
                    match_data.get('venue', ''),
                    match_data.get('venue_city', ''),
                    match_id
                ))
            else:
                # Insert new match
                match_sql = """
                INSERT INTO recent_matches (match_desc, team1, team2, venue, venue_city, start_date, status, state)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(match_sql, (
                    match_data.get('match_desc', ''),
                    match_data.get('team1', ''),
                    match_data.get('team2', ''),
                    match_data.get('venue', ''),
                    match_data.get('venue_city', ''),
                    match_data.get('start_date'),
                    match_data.get('status', ''),
                    match_data.get('state', '')
                ))
                match_id = cur.lastrowid
            
            # Insert or update in combined_matches
            check_combined_sql = """
            SELECT match_id FROM combined_matches 
            WHERE team1 = %s AND team2 = %s AND match_date = %s
            """
            cur.execute(check_combined_sql, (
                match_data.get('team1', ''),
                match_data.get('team2', ''),
                match_data.get('start_date')
            ))
            existing_combined = cur.fetchone()
            
            if existing_combined:
                update_combined_sql = """
                UPDATE combined_matches SET 
                    match_winner = %s, win_margin = %s, format = %s, venue = %s,
                    toss_winner = %s, toss_decision = %s
                WHERE match_id = %s
                """
                cur.execute(update_combined_sql, (
                    match_data.get('match_winner', ''),
                    match_data.get('win_margin', ''),
                    match_data.get('format', ''),
                    match_data.get('venue', ''),
                    match_data.get('toss_winner', ''),
                    match_data.get('toss_decision', ''),
                    existing_combined[0]
                ))
            else:
                combined_sql = """
                INSERT INTO combined_matches (team1, team2, match_winner, win_margin, format, venue, match_date, toss_winner, toss_decision)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(combined_sql, (
                    match_data.get('team1', ''),
                    match_data.get('team2', ''),
                    match_data.get('match_winner', ''),
                    match_data.get('win_margin', ''),
                    match_data.get('format', ''),
                    match_data.get('venue', ''),
                    match_data.get('start_date'),
                    match_data.get('toss_winner', ''),
                    match_data.get('toss_decision', '')
                ))
            
            return match_id
        except Error as e:
            print(f"[ERROR] Error inserting match: {e}")
            return None
        finally:
            cur.close()
    
    def insert_batting_data(self, batting_records):
        """Insert batting data"""
        if not batting_records:
            return 0
        
        cur = self.conn.cursor()
        inserted = 0
        try:
            for record in batting_records:
                # Check if record exists
                check_sql = """
                SELECT batting_id FROM batting_data 
                WHERE match_id = %s AND player_id = %s AND innings_no = %s
                """
                cur.execute(check_sql, (record[0], record[1], record[8]))
                existing = cur.fetchone()
                
                if existing:
                    # Update existing
                    update_sql = """
                    UPDATE batting_data SET 
                        runs = %s, balls = %s, strike_rate = %s, dismissal = %s, team = %s
                    WHERE batting_id = %s
                    """
                    cur.execute(update_sql, (record[3], record[4], record[5], record[6], record[7], existing[0]))
                else:
                    # Insert new
                    insert_sql = """
                    INSERT INTO batting_data (match_id, player_id, player_name, runs, balls, strike_rate, dismissal, team, innings_no)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(insert_sql, record)
                    inserted += 1
            return inserted
        except Error as e:
            print(f"[ERROR] Error inserting batting data: {e}")
            return 0
        finally:
            cur.close()
    
    def insert_bowling_data(self, bowling_records):
        """Insert bowling data"""
        if not bowling_records:
            return 0
        
        cur = self.conn.cursor()
        inserted = 0
        try:
            for record in bowling_records:
                # Check if record exists
                check_sql = """
                SELECT bowling_id FROM bowling_data 
                WHERE match_id = %s AND player_id = %s
                """
                cur.execute(check_sql, (record[0], record[1]))
                existing = cur.fetchone()
                
                if existing:
                    # Update existing
                    update_sql = """
                    UPDATE bowling_data SET 
                        overs = %s, runs_conceded = %s, wickets = %s, economy_rate = %s, format = %s
                    WHERE bowling_id = %s
                    """
                    cur.execute(update_sql, (record[3], record[4], record[5], record[6], record[7], existing[0]))
                else:
                    # Insert new
                    insert_sql = """
                    INSERT INTO bowling_data (match_id, player_id, player_name, overs, runs_conceded, wickets, economy_rate, format)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(insert_sql, record)
                    inserted += 1
            return inserted
        except Error as e:
            print(f"[ERROR] Error inserting bowling data: {e}")
            return 0
        finally:
            cur.close()


def parse_match_data(api_match):
    """Parse match data from API response"""
    match_info = api_match.get('matchInfo', {})
    match_score = api_match.get('matchScore', {})
    
    team1 = match_info.get('team1', {})
    team2 = match_info.get('team2', {})
    venue_info = match_info.get('venueInfo', {})
    
    # Parse start date
    start_date = None
    if match_info.get('startDate'):
        try:
            start_date = datetime.fromtimestamp(int(match_info['startDate']) / 1000).date()
        except:
            start_date = datetime.now().date()
    
    # Determine match winner and margin
    status = match_info.get('status', '')
    match_winner = ''
    win_margin = ''
    
    if 'won by' in status.lower():
        parts = status.split(' won by ')
        if len(parts) == 2:
            match_winner = parts[0].strip()
            win_margin = parts[1].strip()
    
    return {
        'match_desc': match_info.get('matchDesc', ''),
        'team1': team1.get('teamName', ''),
        'team2': team2.get('teamName', ''),
        'venue': venue_info.get('ground', ''),
        'venue_city': venue_info.get('city', ''),
        'start_date': start_date,
        'status': status,
        'state': match_info.get('stateTitle', ''),
        'match_winner': match_winner,
        'win_margin': win_margin,
        'format': match_info.get('matchFormat', ''),
        'toss_winner': match_info.get('tossResults', {}).get('tossWinnerName', ''),
        'toss_decision': match_info.get('tossResults', {}).get('decision', '')
    }


def fetch_and_store_matches(api_client, db_manager):
    """Fetch matches from API and store in database"""
    print("\n[INFO] Fetching live matches from API...")
    live_data = api_client.get_live_matches()
    
    if not live_data:
        print("[WARNING] No live matches data received")
        return
    
    matches_count = 0
    for type_match in live_data.get('typeMatches', []):
        for series in type_match.get('seriesMatches', []):
            series_info = series.get('seriesAdWrapper', {})
            matches = series_info.get('matches', [])
            
            for match in matches:
                match_data = parse_match_data(match)
                match_id = db_manager.insert_match(match_data)
                if match_id:
                    matches_count += 1
                    print(f"[OK] Inserted match: {match_data['team1']} vs {match_data['team2']}")
    
    print(f"[OK] Total matches inserted: {matches_count}")
    
    # Also fetch recent matches
    print("\n[INFO] Fetching recent matches from API...")
    recent_data = api_client.get_recent_matches()
    
    if recent_data:
        recent_count = 0
        for type_match in recent_data.get('typeMatches', []):
            for series in type_match.get('seriesMatches', []):
                series_info = series.get('seriesAdWrapper', {})
                matches = series_info.get('matches', [])
                
                for match in matches:
                    match_data = parse_match_data(match)
                    match_id = db_manager.insert_match(match_data)
                    if match_id:
                        recent_count += 1
        
        print(f"[OK] Total recent matches inserted: {recent_count}")


def fetch_and_store_players(api_client, db_manager):
    """Fetch popular players and store in database"""
    print("\n[INFO] Fetching player data from API...")
    
    # List of popular players to fetch
    popular_players = [
        "Virat Kohli", "Rohit Sharma", "MS Dhoni", "Jasprit Bumrah",
        "Ravindra Jadeja", "Steve Smith", "Pat Cummins", "Ben Stokes",
        "Kane Williamson", "Babar Azam", "Joe Root", "David Warner"
    ]
    
    players_inserted = 0
    for player_name in popular_players:
        try:
            search_results = api_client.search_players(player_name)
            if search_results and 'player' in search_results:
                for player in search_results['player'][:1]:  # Take first result
                    player_id = player.get('id')
                    if player_id:
                        # Get full player details
                        player_details = api_client.get_player_details(player_id)
                        if player_details:
                            player_data = {
                                'name': player.get('name', ''),
                                'full_name': player_details.get('name', player.get('name', '')),
                                'country': player.get('teamName', ''),
                                'playing_role': player_details.get('role', ''),
                                'batting_style': player_details.get('bat', ''),
                                'bowling_style': player_details.get('bowl', ''),
                                'total_runs': 0,  # Will be updated from stats
                                'total_wickets': 0
                            }
                            
                            db_id = db_manager.insert_or_update_player(player_data)
                            if db_id:
                                players_inserted += 1
                                print(f"[OK] Inserted/Updated player: {player_data['name']}")
                        
                        # Rate limiting
                        time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Error fetching player {player_name}: {e}")
            continue
    
    print(f"[OK] Total players inserted/updated: {players_inserted}")


def fetch_and_store_scorecards(api_client, db_manager):
    """Fetch scorecards for matches and store batting/bowling data"""
    print("\n[INFO] Fetching scorecard data from API...")
    
    # Get match IDs from database
    cur = db_manager.conn.cursor()
    cur.execute("SELECT match_id FROM combined_matches LIMIT 10")
    match_ids = [row[0] for row in cur.fetchall()]
    cur.close()
    
    if not match_ids:
        print("[WARNING] No matches found in database to fetch scorecards")
        return
    
    batting_records = []
    bowling_records = []
    
    for match_id in match_ids[:5]:  # Limit to 5 to avoid rate limits
        try:
            scorecard = api_client.get_scorecard(str(match_id))
            if not scorecard or 'scorecard' not in scorecard:
                continue
            
            for innings in scorecard.get('scorecard', []):
                innings_no = innings.get('inningsId', 1)
                team_name = innings.get('batteamname', '')
                
                # Process batting data
                for batsman in innings.get('batsman', []):
                    # Find player in database
                    cur = db_manager.conn.cursor()
                    cur.execute("SELECT player_id FROM players WHERE name LIKE %s LIMIT 1", 
                              (f"%{batsman.get('name', '')}%",))
                    player_row = cur.fetchone()
                    player_id = player_row[0] if player_row else None
                    cur.close()
                    
                    if player_id:
                        batting_records.append((
                            match_id,
                            player_id,
                            batsman.get('name', ''),
                            batsman.get('runs', 0),
                            batsman.get('balls', 0),
                            batsman.get('strkrate', 0.0),
                            batsman.get('outdec', ''),
                            team_name,
                            innings_no
                        ))
                
                # Process bowling data
                for bowler in innings.get('bowler', []):
                    cur = db_manager.conn.cursor()
                    cur.execute("SELECT player_id FROM players WHERE name LIKE %s LIMIT 1",
                              (f"%{bowler.get('name', '')}%",))
                    player_row = cur.fetchone()
                    player_id = player_row[0] if player_row else None
                    cur.close()
                    
                    if player_id:
                        bowling_records.append((
                            match_id,
                            player_id,
                            bowler.get('name', ''),
                            float(bowler.get('overs', 0)),
                            bowler.get('runs', 0),
                            bowler.get('wickets', 0),
                            float(bowler.get('economy', 0.0)),
                            'ODI'  # Default format
                        ))
            
            time.sleep(1)  # Rate limiting
            
        except Exception as e:
            print(f"[ERROR] Error fetching scorecard for match {match_id}: {e}")
            continue
    
    # Bulk insert batting and bowling data
    if batting_records:
        count = db_manager.insert_batting_data(batting_records)
        print(f"[OK] Inserted {count} batting records")
    
    if bowling_records:
        count = db_manager.insert_bowling_data(bowling_records)
        print(f"[OK] Inserted {count} bowling records")


def main():
    """Main function to fetch and store API data"""
    print("=" * 60)
    print("Cricbuzz API Data Fetcher")
    print("=" * 60)
    
    # Initialize clients
    api_client = CricbuzzAPIClient()
    db_manager = DatabaseManager()
    
    if not db_manager.connect():
        print("[ERROR] Failed to connect to database. Exiting.")
        return
    
    try:
        # Fetch and store matches
        fetch_and_store_matches(api_client, db_manager)
        
        # Fetch and store players
        fetch_and_store_players(api_client, db_manager)
        
        # Fetch and store scorecards (batting/bowling data)
        fetch_and_store_scorecards(api_client, db_manager)
        
        print("\n" + "=" * 60)
        print("[OK] Data fetching completed!")
        print("=" * 60)
        print("\nYou can now:")
        print("  1. Run SQL queries in the SQL Analytics page")
        print("  2. View data in the CRUD Operations page")
        print("  3. Test all 25 SQL queries with real data")
        
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    finally:
        db_manager.close()


if __name__ == '__main__':
    main()

