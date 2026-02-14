# Data Analytics Application

Ever wish you could instantly understand your customer behavior without writing complex SQL queries? **This is it.**

A universal web-based analytics platform that connects to any MySQL database and gives you real customer insights in minutes, not days.

## Features

- Works with ANY MySQL database - Just give it your credentials, it handles the rest
- 4 different analysis types - Find patterns you didn't know existed
- Smart customer segmentation - Know exactly what type of customer each person is
- Real-time search & filtering - Find the customers you're looking for in seconds
- Beautiful, simple interface - No confusing dashboards. Just clear information.
- Blazing fast - Runs locally on your machine. No waiting for the cloud.
- No setup pain - Three commands and you're running

## Quick Start

### Prerequisites
- Python 3.7 or higher (don't have it? [Get it here](https://www.python.org))
- MySQL database somewhere (with login credentials)
- Any browser

### Installation

**Step 1:** Clone or download this repo

**Step 2:** Install the dependencies (copy-paste this)
```bash
pip install mysql-connector-python pandas
```

**Step 3:** Start it up
```bash
python backend/app.py
```

**Step 4:** Open your browser
```
http://localhost:8000
```

Done. That's it. You're running.

## How to Use

### The 4-Step Process

1. **Connect** - Give it your MySQL credentials
2. **Pick a table** - Choose what data you want to analyze
3. **Choose an analysis** - Pick what you want to learn (Order Frequency? Churn Risk? Segments?)
4. **Get insights** - See your customers in a whole new way

### The 4 Analysis Types

| Analysis | Answers | Use When |
|----------|---------|----------|
| **Order Frequency** | When will they order next? | Planning inventory or marketing timing |
| **Recency** | How long since they ordered? | Finding customers who've gone quiet |
| **Churn Risk** | Are they about to leave? | Saving customers before they go |
| **Segmentation** | What type of customer are they? | Planning targeted strategies |

### Search & Filter

- **Search:** Find specific customers by name or ID
- **Filter:** Filter by segment, risk level, etc.
- **Combine both:** Superpower. Use it.

**Real example:** Filter to "At Risk" customers, then search for "John" to find all at-risk Johns.

## Project Structure

```
data-analytics-app/
├── backend/
│   ├── app.py              # HTTP server and API endpoints
│   └── analytics.py        # Analytics calculations engine
├── frontend/
│   └── index.html          # Complete web application UI
├── USER_MANUAL.md          # Detailed user guide
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

## System Requirements

- **OS:** Windows, macOS, or Linux
- **Python:** 3.7 or higher
- **Database:** MySQL 5.7+ or MariaDB 10.3+
- **Browser:** Chrome, Firefox, Safari, or Edge
- **Port:** 8000 (must be available)

## Technical Details

### Dependencies
- `mysql-connector-python` - MySQL database connection
- `pandas` - Data manipulation and analysis
- Python standard library (http.server, json, datetime, etc.)

### How It Works

1. **Frontend** (index.html) - Single-page web application built with vanilla JavaScript, HTML, CSS
2. **Backend** (app.py) - HTTP server handling requests and serving files
3. **Analytics Engine** (analytics.py) - Performs calculations on customer data
4. **Database** - Connects to user's MySQL database to analyze customer data

### Supported Column Types

The application auto-detects:
- **Date columns:** DATE, DATETIME, TIMESTAMP
- **ID columns:** INT, BIGINT, VARCHAR, UUID
- **Name columns:** VARCHAR, TEXT, CHAR

## Troubleshooting

### Application won't start
- Ensure Python 3.7+ is installed
- Verify port 8000 is available
- Run `pip install mysql-connector-python pandas` to install dependencies

### Can't connect to database
- Verify MySQL is running
- Check credentials (host, username, password, database name)
- Ensure your MySQL user has table access permissions

### No tables appear after connecting
- Verify your MySQL user has view permissions on tables
- Check database name is spelled correctly
- Contact your database administrator

For more detailed troubleshooting, see `USER_MANUAL.md`.

## Documentation

- **USER_MANUAL.md** - Complete user guide with step-by-step instructions, use cases, and detailed troubleshooting

## Version

**v1.0** - February 2026

## License

This project is provided as-is for use with MySQL databases.

## Support

For issues or questions:
1. Check `USER_MANUAL.md` for detailed documentation
2. Review the Troubleshooting section above
3. Verify your MySQL database structure and credentials

## Features for Future Versions

- Export results to CSV/Excel
- Custom date range filtering
- Scheduled automated reports
- Custom segment definitions
- API endpoints for programmatic access

---

Made with care for data analysis
