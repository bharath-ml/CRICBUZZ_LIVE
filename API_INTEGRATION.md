# 🔌 API Integration Guide

## Overview

This project integrates with the **Cricbuzz API via RapidAPI** to fetch real-time cricket data and store it in MySQL database for SQL analysis.

## Two Data Population Methods

### 1. ✅ **fetch_api_data.py** (Recommended - Real API Data)

This is the **proper method** for your project that demonstrates API integration:

```bash
python fetch_api_data.py
```

**What it does:**
- ✅ Fetches **real live matches** from Cricbuzz API
- ✅ Fetches **recent matches** from Cricbuzz API  
- ✅ Extracts **player information** (name, country, role, batting/bowling style)
- ✅ Gets **detailed scorecards** with batting and bowling statistics
- ✅ Stores all data in MySQL database
- ✅ Handles **rate limiting** to avoid API quota issues
- ✅ Prevents **duplicate data** with proper checks

**API Endpoints Used:**
- `/matches/v1/live` - Live cricket matches
- `/matches/v1/recent` - Recent completed matches
- `/mcenter/v1/{matchId}/scard` - Detailed match scorecards
- `/stats/v1/player/search` - Search for players
- `/stats/v1/player/{playerId}` - Get player details

**This demonstrates:**
- ✅ REST API integration
- ✅ JSON data parsing
- ✅ Database operations with real data
- ✅ Error handling and rate limiting
- ✅ Data transformation from API to database schema

### 2. ⚠️ **seed_data.py** (Testing Only - Sample Data)

This is for **quick testing** with hardcoded sample data:

```bash
python seed_data.py
```

**What it does:**
- Inserts hardcoded sample players, matches, and statistics
- Useful for testing SQL queries without API calls
- **Not recommended for project submission**

## Why Use API Integration?

Your project requirements emphasize:
- **🌐 API Integration** - Utilizing Cricbuzz Cricket API via REST
- **📊 Real-time Data** - Live match updates and player statistics
- **🗄️ Database Storage** - Storing API data in MySQL for analysis
- **🔍 SQL Analytics** - Running queries on real cricket data

Using `fetch_api_data.py` demonstrates all these requirements!

## How It Works

### Step 1: Fetch Matches
```python
# Fetches live and recent matches
live_matches = api_client.get_live_matches()
recent_matches = api_client.get_recent_matches()
```

### Step 2: Parse and Store
```python
# Parses match data from JSON
match_data = parse_match_data(api_match)

# Stores in database
db_manager.insert_match(match_data)
```

### Step 3: Fetch Player Data
```python
# Searches for players
players = api_client.search_players("Virat Kohli")

# Gets detailed player information
player_details = api_client.get_player_details(player_id)

# Stores in database
db_manager.insert_or_update_player(player_data)
```

### Step 4: Fetch Scorecards
```python
# Gets detailed match scorecard
scorecard = api_client.get_scorecard(match_id)

# Extracts batting and bowling data
# Stores in batting_data and bowling_data tables
```

## Data Flow

```
Cricbuzz API (RapidAPI)
    ↓
fetch_api_data.py
    ↓
Parse JSON Response
    ↓
Transform to Database Schema
    ↓
MySQL Database
    ↓
SQL Queries (25 queries)
    ↓
Streamlit Dashboard
```

## Running the API Fetcher

### Prerequisites
1. Valid `RAPIDAPI_KEY` in `.env` file
2. Database schema created (`python create_schema.py`)
3. MySQL database running

### Execution
```bash
# 1. Make sure your .env has the API key
RAPIDAPI_KEY=your_actual_api_key_here

# 2. Run the fetcher
python fetch_api_data.py
```

### Expected Output
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

[OK] Data fetching completed!
```

## Rate Limiting

The script includes rate limiting to avoid exceeding API quotas:
- 0.5 second delay between player searches
- 1 second delay between scorecard fetches
- Handles API errors gracefully

## Data Updates

The script handles duplicate data:
- **Players**: Updates if exists, inserts if new
- **Matches**: Updates status if exists, inserts if new
- **Batting/Bowling**: Updates statistics if exists, inserts if new

This allows you to run the script multiple times to update data without duplicates.

## Troubleshooting

### API Key Issues
```
[ERROR] API Error: 401
```
**Solution**: Check your `RAPIDAPI_KEY` in `.env` file

### Rate Limit Exceeded
```
[ERROR] API Error: 429
```
**Solution**: Wait a few minutes and run again, or upgrade your RapidAPI plan

### No Data Returned
```
[WARNING] No live matches data received
```
**Solution**: 
- Check if there are currently live matches
- Verify API key has access to Cricbuzz endpoints
- Check your internet connection

### Database Errors
```
[ERROR] Database connection failed
```
**Solution**: 
- Verify MySQL is running
- Check database credentials in `.env`
- Ensure database exists: `CREATE DATABASE cricket_db;`

## Best Practices

1. **Run fetch_api_data.py regularly** to keep data updated
2. **Use seed_data.py only for testing** SQL queries structure
3. **Check API quota** before running multiple times
4. **Monitor database size** as data accumulates
5. **Backup database** before major data fetches

## Project Submission

For your project submission, make sure to:
- ✅ Use `fetch_api_data.py` to demonstrate API integration
- ✅ Show real data in SQL queries (not just sample data)
- ✅ Document the API integration process
- ✅ Include screenshots of real match data
- ✅ Explain how data flows from API to database to queries

---

**Remember**: The goal is to demonstrate **real API integration**, not just hardcoded sample data! 🚀

