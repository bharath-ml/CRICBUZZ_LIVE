# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics


[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cricbuzzlivestats-app.streamlit.app/)

A **Python + Streamlit** project that delivers real-time cricket updates, live scorecards, and player insights using the Cricbuzz API. This project also integrates with a **MySQL** to store and manage cricket data, such as players, squads, and key statistics.

## 🚀 Features
* **📊 Live Cricket Updates** – Fetches real-time match details, including scores, status, and venues.
* **📝 Scorecards & Player Insights** – View batting, bowling, and player statistics at a glance.
* **🎯 Interactive Streamlit Dashboard** – A clean, responsive UI with filtering options.
* **🗄️ Database Support** – A MySQL backend for data persistence.
* **🔎 SQL Query Playground** – Write and execute custom SQL queries directly inside the app.
* **🛠 CRUD Operations** – Add, update, delete, and view cricket data in real time.

## ⚙️ Installation & Setup
### 1️⃣ Clone the Repository

```
git clone <repository-url>
cd cricbuzz_livestats
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables
Create a `.env` file in the project's root directory and add your database and API credentials. This helps keep your sensitive information secure.

```
RAPIDAPI_KEY="your_api_key_here"
DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="your_password"
DB_NAME="cricket_db"
```

### 4️⃣ Setup Database Schema
Create the MySQL database and all required tables:

```bash
# First, create the database in MySQL
mysql -u root -p
CREATE DATABASE cricket_db;
EXIT;

# Then run the schema creation script
python create_schema.py
```

This will create all 13 tables needed for the project:
- `players` - Player information
- `recent_matches` - Recent match data
- `top_odi_runs` - Top ODI run scorers
- `venues` - Stadium and venue information
- `combined_matches` - Unified match data
- `batting_data` - Detailed batting statistics
- `series_matches` - Series match information
- `players_stats` - Player statistics across formats
- `players_partnerships_data` - Batting partnership data
- `bowlers_bowling_venue_data` - Bowling statistics by venue
- `batters_batting_data` - Detailed batter statistics
- `bowling_data` - Bowling performance data
- `fielding_data` - Fielding statistics

### 5️⃣ Fetch Real Data from API (Recommended)
Populate the database with real cricket data from Cricbuzz API:

```bash
python fetch_api_data.py
```

This script will:
- Fetch live and recent matches from Cricbuzz API
- Extract player information and store in database
- Get match scorecards with batting and bowling statistics
- Store all data in MySQL for SQL query analysis

**Note**: This requires a valid `RAPIDAPI_KEY` in your `.env` file.

### 6️⃣ Seed Sample Data (Optional - for testing only)
If you want to test with sample data instead of API data:

```bash
python seed_data.py
```

**Note**: For the actual project, use `fetch_api_data.py` to get real data from the API.

### 7️⃣ Run the App

```bash
streamlit run app.py
```

## 🎯 Key Features Walkthrough
### 1️⃣ Live Matches Dashboard
* **Auto-Refresh**: The dashboard updates every 30 seconds for live scores.
* **Filters**: You can filter matches by format, status, and venue.
* **Match Details**: Click on a match to view ball-by-ball information.
* **Visuals**: See real-time match statistics and data visualizations.

### 2️⃣ Top Stats & Analytics
* **Batting Leaders**: View leaderboards for runs, averages, strike rates, and boundaries.
* **Bowling Leaders**: See top bowlers by wickets, economy rates, and maidens.
* **Team Trends**: Compare teams across different cricket formats.
* **Data Management**: Quickly refresh, clear, or regenerate data.

### 3️⃣ SQL Query Playground
* **25 Pre-Built Queries**: Complete set of SQL queries covering beginner to advanced levels:
  - **Beginner (Q1-Q8)**: Basic SELECT, WHERE, GROUP BY, ORDER BY operations
  - **Intermediate (Q9-Q16)**: JOINs, subqueries, aggregate functions
  - **Advanced (Q17-Q25)**: Window functions, CTEs, complex analytical calculations
* **Custom Query Builder**: Write and execute your own SQL queries.
* **Schema Explorer**: An interactive browser to view your database structure.

### 4️⃣ CRUD Operations
* **Player Management**: Add, update, and remove player information.
* **Match Management**: Manage match schedules and results.
* **Performance Data**: Insert or clean up batting and bowling statistics.

## 📦 requirements.txt

```
streamlit
pandas
requests
python-dotenv
mysql-connector-python
SQLAlchemy
PyMySQL
```

## 🗄️ Database Schema

The project uses a comprehensive MySQL database schema with 13 tables:

1. **players** - Core player information (name, country, role, batting/bowling style)
2. **recent_matches** - Recent match details and results
3. **top_odi_runs** - Top ODI run scorers with statistics
4. **venues** - Stadium information with capacity
5. **combined_matches** - Unified match data across formats
6. **batting_data** - Detailed batting performance per match
7. **series_matches** - Series and tournament match information
8. **players_stats** - Player statistics across Test, ODI, and T20 formats
9. **players_partnerships_data** - Batting partnership records
10. **bowlers_bowling_venue_data** - Bowling statistics by venue
11. **batters_batting_data** - Detailed batter statistics over time
12. **bowling_data** - Comprehensive bowling performance data
13. **fielding_data** - Fielding statistics (catches, stumpings, run-outs)

## 🔍 SQL Queries Included

The project includes 25 SQL queries covering:

- **Basic Queries**: Player listings, match summaries, venue information
- **Aggregate Functions**: Team wins, player counts, format-wise statistics
- **JOINs**: Cross-table analysis, player-match relationships
- **Window Functions**: Rankings, trends, performance evolution
- **CTEs (Common Table Expressions)**: Complex analytical queries
- **Time-Series Analysis**: Performance trends over time
- **Advanced Analytics**: Composite scoring, head-to-head analysis, form tracking

## 🛠️ Project Structure

```
Cricbuzz_livestats/
├── app.py                 # Main Streamlit application
├── create_schema.py       # Database schema creation script
├── seed_data.py          # Sample data insertion script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── README.md             # Project documentation
├── pages/
│   ├── live_matches.py   # Live matches dashboard
│   ├── top_stats.py      # Player statistics page
│   ├── sql_queries.py    # SQL analytics page (25 queries)
│   └── crud_operations.py # CRUD operations interface
└── utils/
    └── db_connection.py   # Database connection utilities
```

## 🚨 Troubleshooting

### Database Connection Issues
- Ensure MySQL is running: `mysql -u root -p`
- Verify database exists: `SHOW DATABASES;`
- Check `.env` file has correct credentials

### Table Not Found Errors
- Run `python create_schema.py` to create all tables
- Verify tables exist: `USE cricket_db; SHOW TABLES;`

### Empty Query Results
- Run `python seed_data.py` to populate sample data
- Check data exists: `SELECT COUNT(*) FROM players;`

### API Errors
- Verify `RAPIDAPI_KEY` is set in `.env`
- Check API key is valid and has remaining quota

## 🙏 Acknowledgments
* **Cricbuzz API** – For rich, real-time cricket data.
* **Streamlit** – For the easy-to-use web app framework.
* **MySQL** – For reliable data storage and queries.

## ❤️ Built For
This project is built for cricket fans, analysts, and developers who want to explore data-driven insights in real time.
