# 🏏 Cricbuzz LiveStats - Complete Setup Guide

This guide will help you set up the complete Cricbuzz LiveStats project from scratch.

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- RapidAPI account with Cricbuzz API access
- Git (optional, for cloning)

## Step-by-Step Setup

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - Web framework
- `pandas` - Data manipulation
- `requests` - API calls
- `python-dotenv` - Environment variable management
- `mysql-connector-python` - MySQL database connector
- `SQLAlchemy` - SQL toolkit
- `PyMySQL` - MySQL driver

### Step 2: Setup MySQL Database

1. **Start MySQL Server**
   ```bash
   # On Windows (if installed as service, it should be running)
   # On Linux/Mac
   sudo systemctl start mysql
   # or
   brew services start mysql
   ```

2. **Create Database**
   ```sql
   mysql -u root -p
   ```
   Then in MySQL:
   ```sql
   CREATE DATABASE cricket_db;
   SHOW DATABASES;
   EXIT;
   ```

### Step 3: Configure Environment Variables

Create a `.env` file in the project root directory:

```env
RAPIDAPI_KEY=your_rapidapi_key_here
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=cricket_db
```

**Important**: 
- Replace `your_rapidapi_key_here` with your actual RapidAPI key
- Replace `your_mysql_password` with your MySQL root password
- Keep the `.env` file secure and never commit it to version control

### Step 4: Create Database Schema

Run the schema creation script to create all required tables:

```bash
python create_schema.py
```

Expected output:
```
[OK] Connected to database 'cricket_db'. Creating tables...
============================================================
[OK] Created/checked table: players
[OK] Created/checked table: recent_matches
[OK] Created/checked table: top_odi_runs
[OK] Created/checked table: venues
[OK] Created/checked table: combined_matches
[OK] Created/checked table: batting_data
[OK] Created/checked table: series_matches
[OK] Created/checked table: players_stats
[OK] Created/checked table: players_partnerships_data
[OK] Created/checked table: bowlers_bowling_venue_data
[OK] Created/checked table: batters_batting_data
[OK] Created/checked table: bowling_data
[OK] Created/checked table: fielding_data
============================================================
[OK] All tables created successfully!
```

### Step 5: Fetch Real Data from Cricbuzz API (Recommended)

**This is the proper way to populate your database with real cricket data:**

```bash
python fetch_api_data.py
```

This script will:
- ✅ Fetch live and recent matches from Cricbuzz API
- ✅ Extract player information (name, country, role, batting/bowling style)
- ✅ Get detailed match scorecards with batting and bowling statistics
- ✅ Store all data in MySQL database for SQL query analysis
- ✅ Handle rate limiting to avoid API quota issues

**Expected output:**
```
============================================================
Cricbuzz API Data Fetcher
============================================================

[INFO] Fetching live matches from API...
[OK] Inserted match: India vs Australia
[OK] Inserted match: England vs New Zealand
[OK] Total matches inserted: 5

[INFO] Fetching recent matches from API...
[OK] Total recent matches inserted: 10

[INFO] Fetching player data from API...
[OK] Inserted/Updated player: Virat Kohli
[OK] Inserted/Updated player: Rohit Sharma
[OK] Total players inserted/updated: 12

[INFO] Fetching scorecard data from API...
[OK] Inserted 45 batting records
[OK] Inserted 30 bowling records
```

**Note**: Make sure your `RAPIDAPI_KEY` is valid and has remaining quota.

### Step 5b: Seed Sample Data (Optional - Testing Only)

If you want to quickly test with sample data (not recommended for actual project):

```bash
python seed_data.py
```

**Important**: For the actual project submission, use `fetch_api_data.py` to demonstrate API integration.

### Step 6: Verify Database Setup

Test the database connection and verify data was inserted:

```bash
mysql -u root -p cricket_db -e "SELECT COUNT(*) as player_count FROM players;"
mysql -u root -p cricket_db -e "SELECT COUNT(*) as match_count FROM combined_matches;"
```

You should see:
- Player count (12+ if you ran fetch_api_data.py, or 10 if you ran seed_data.py)
- Match count (5+ if you ran fetch_api_data.py, or 4 if you ran seed_data.py)

### Step 7: Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Project Structure

```
Cricbuzz_livestats/
├── app.py                      # Main Streamlit application
├── create_schema.py            # Database schema creation
├── seed_data.py                # Sample data insertion
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── README.md                   # Project documentation
├── SETUP_GUIDE.md             # This file
├── pages/
│   ├── live_matches.py        # Live matches dashboard
│   ├── top_stats.py           # Player statistics
│   ├── sql_queries.py         # SQL analytics (25 queries)
│   └── crud_operations.py     # CRUD operations
└── utils/
    └── db_connection.py       # Database utilities
```

## Database Schema Overview

### Core Tables

1. **players** - Player information (name, country, role, styles)
2. **venues** - Stadium information (name, city, country, capacity)
3. **combined_matches** - Unified match data across formats
4. **recent_matches** - Recent match details and results

### Statistics Tables

5. **batting_data** - Detailed batting performance per match
6. **bowling_data** - Comprehensive bowling performance
7. **fielding_data** - Fielding statistics
8. **batters_batting_data** - Time-series batting data
9. **bowlers_bowling_venue_data** - Bowling stats by venue

### Analytics Tables

10. **top_odi_runs** - Top ODI run scorers
11. **players_stats** - Player stats across formats
12. **series_matches** - Series and tournament data
13. **players_partnerships_data** - Batting partnership records

## Testing the Application

### 1. Test Live Matches Page
- Navigate to "⚡ Live Matches"
- Should display live cricket matches from Cricbuzz API
- Click "View Scorecard" to see detailed match information

### 2. Test Top Stats Page
- Navigate to "📊 Top Stats"
- Search for a player (e.g., "Kohli", "Dhoni")
- View player profile, batting stats, and bowling stats

### 3. Test SQL Analytics Page
- Navigate to "🔍 SQL Analytics"
- Select a query from the dropdown (Q1-Q25)
- Click "Run Query" to execute
- Try Q1: "List all Indian players" - should return results

### 4. Test CRUD Operations Page
- Navigate to "🛠️ CRUD Operations"
- Enter database credentials
- Click "Connect & Discover Databases"
- Select `cricket_db` and `players` table
- Click "Load Data" to view players
- Try adding a new player using the form

## Common Issues & Solutions

### Issue: "Table 'cricket_db.players' doesn't exist"
**Solution**: Run `python create_schema.py` to create all tables

### Issue: "Access denied for user"
**Solution**: Check your `.env` file has correct DB_USER and DB_PASSWORD

### Issue: "RAPIDAPI_KEY not found"
**Solution**: Add `RAPIDAPI_KEY=your_key` to your `.env` file

### Issue: "No module named 'streamlit'"
**Solution**: Run `pip install -r requirements.txt`

### Issue: Foreign key constraint errors
**Solution**: Make sure to insert data in order:
1. Players first
2. Venues
3. Matches
4. Then dependent tables (batting_data, bowling_data, etc.)

### Issue: Empty query results
**Solution**: 
- Run `python fetch_api_data.py` to fetch real data from API (recommended)
- Or run `python seed_data.py` for sample data (testing only)

### Issue: API rate limit exceeded
**Solution**: 
- The script includes rate limiting (sleep delays)
- Wait a few minutes and run again
- Consider upgrading your RapidAPI plan if needed

## SQL Queries Included

The project includes 25 SQL queries organized by difficulty:

### Beginner (Q1-Q8)
- Basic SELECT, WHERE, GROUP BY, ORDER BY
- Simple aggregations
- Format filtering

### Intermediate (Q9-Q16)
- JOINs between tables
- Subqueries
- Complex aggregations
- Time-based filtering

### Advanced (Q17-Q25)
- Window functions (RANK, ROW_NUMBER)
- Common Table Expressions (CTEs)
- Complex analytical calculations
- Time-series analysis
- Composite scoring systems

## Next Steps

1. **Customize Data**: Replace sample data with real cricket data
2. **Add More Queries**: Create your own SQL queries in `sql_queries.py`
3. **Enhance UI**: Customize Streamlit pages with additional features
4. **Deploy**: Deploy to Streamlit Cloud or your own server

## Getting Help

- Check the README.md for feature documentation
- Review SQL queries in `pages/sql_queries.py`
- Examine database schema in `create_schema.py`
- Test individual components using the CRUD Operations page

## Security Notes

- Never commit `.env` file to version control
- Use strong MySQL passwords
- Keep API keys secure
- Consider using environment-specific configurations for production

---

**Happy Coding! 🏏📊**

