# Data Analytics Application

A universal web-based data analytics application that works with any MySQL database. Built with Python backend and vanilla JavaScript frontend.

## Features

- 🔗 **Universal Database Connection**: Connect to any MySQL database with dynamic credentials
- 📊 **Dynamic Table Selection**: Analyze any table from your connected schema
- 📈 **Customer Analytics**: 
  - Calculate order frequency (average days between orders)
  - Predict next order date
  - Classify customers as Frequent, Moderate, or Infrequent
  - View comprehensive metrics per customer
- 🎨 **Modern UI**: Clean, responsive interface with step-based workflow
- 🔐 **No Hardcoded Credentials**: All connection details are user-provided
- 📱 **Fully Responsive**: Works on desktop and mobile devices

## Project Structure

```
Nyla/
├── backend/
│   ├── app.py              # Main HTTP server (uses Python std library)
│   ├── db_connector.py     # MySQL connection logic
│   └── analytics.py        # Analytics calculations
├── frontend/
│   ├── index.html          # Main UI
│   ├── styles.css          # Modern styling
│   └── script.js           # Client-side logic
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Prerequisites

- **Python 3.7+** installed on your system
- **MySQL** database server running and accessible
- A web browser (Chrome, Firefox, Safari, Edge, etc.)

## Setup Instructions

### 1. Install Python Dependencies

Open a terminal/command prompt and navigate to the project directory:

```bash
cd path/to/Nyla
```

Install required packages:

```bash
pip install -r requirements.txt
```

If you encounter issues with `mysql-connector-python`, try:

```bash
pip install mysql-connector-python --allow-external mysql-connector-python
```

### 2. Verify MySQL Connection Details

Before running the app, ensure you have:
- MySQL server running
- Database name
- Username and password
- Host (usually `localhost` for local development)
- Port (usually `3306`)

### 3. Run the Application

From the project directory, run:

```bash
python backend/app.py
```

You should see output like:
```
Server running at http://localhost:8000
Serving frontend from: C:\Users\...\Nyla\frontend
Press Ctrl+C to stop the server
```

### 4. Open in Browser

Open your web browser and navigate to:

```
http://localhost:8000
```

## How to Use

### Step 1: Connect to Database
1. Enter your MySQL connection details:
   - **Host**: Server address (e.g., `localhost`, `127.0.0.1`, or remote IP)
   - **Port**: MySQL port (default: `3306`)
   - **Username**: MySQL user
   - **Password**: MySQL password
   - **Schema**: Database name

2. Click "Connect" button

3. Wait for confirmation message

### Step 2: Select Table
1. Once connected, you'll see a list of all tables in your database
2. Click on any table to select it for analysis
3. The application will automatically perform analytics

### Step 3: View Analytics Results
The table shows:
- **Customer ID**: Unique customer identifier
- **Total Orders**: Number of orders placed by the customer
- **Avg Order Gap**: Average days between consecutive orders
- **Last Order Date**: Date of most recent order
- **Predicted Next Order**: Estimated date of next order based on historical frequency
- **Classification**: 
  - 🟢 **Frequent**: Orders every < 7 days
  - 🟡 **Moderate**: Orders every 7-30 days
  - 🔴 **Infrequent**: Orders every > 30 days

### Step 4: New Analysis
Click "New Analysis" to return to step 1 and analyze a different database or table.

## Supported Table Structures

The application automatically detects:
- **Customer identifier columns**: Any column with "customer" in the name
- **Date columns**: Any column with "date" in the name

Common supported column names:
- Customer: `customer_id`, `customer`, `cust_id`, `client_id`
- Date: `order_date`, `date`, `created_at`, `order_at`, `transaction_date`

## API Endpoints (Internal)

The backend exposes these endpoints:

### POST `/api/connect`
Establishes a connection to the MySQL database.

**Request:**
```json
{
  "host": "localhost",
  "port": 3306,
  "username": "root",
  "password": "password",
  "schema": "my_database"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Connected to the database successfully."
}
```

### GET `/api/tables`
Retrieves all table names from the connected database.

**Response:**
```json
{
  "status": "success",
  "tables": ["customers", "orders", "products"]
}
```

### POST `/api/analytics`
Performs analytics on the specified table.

**Request:**
```json
{
  "table": "orders"
}
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "customer_id": "CUST001",
      "total_orders": 15,
      "avg_order_gap": 10.5,
      "last_order_date": "2024-02-05",
      "predicted_next_order_date": "2024-02-15",
      "customer_classification": "Frequent"
    }
  ]
}
```

## Troubleshooting

### "Connection Failed" Error
- Verify MySQL server is running
- Check host, port, username, and password
- Ensure the user has permissions for the specified schema
- Try connecting with a GUI tool (MySQL Workbench) to verify credentials

### "No Tables Found"
- Ensure the database (schema) exists
- Verify the user has SELECT privileges on the database
- The database must have at least one table

### Analytics Returns No Results
- Check that the table has columns containing "customer" and "date" in their names
- Ensure the table has data
- Verify date column format is valid (ISO 8601 or MySQL date format)

### Port Already in Use
If port 8000 is already in use, edit `backend/app.py` and change:
```python
PORT = 8000  # Change to another port like 8080
```

## Architecture Notes

### Backend Design
- **Server-side rendering**: Uses Python's built-in `http.server` module
- **Stateful connections**: Connection stored in memory during session
- **Production-ready error handling**: All database errors are caught and returned as JSON

### Frontend Design
- **No build process**: Pure HTML, CSS, JavaScript
- **Responsive layout**: CSS Grid and Flexbox for modern layouts
- **Vanilla JavaScript**: No frameworks required
- **Extensible**: Easy to add new features

## Performance Considerations

- For tables with 100K+ rows, analytics calculation may take a few seconds
- Large result sets are rendered in the browser and may be slow with 10K+ customers
- Consider adding pagination for very large datasets

## Future Enhancements

- Export results to CSV/Excel
- Date range filtering
- Custom classification thresholds
- Multiple database connections
- REST API conversion
- Authentication and user management

## Technology Stack

- **Backend**: Python 3.7+ (standard library + mysql-connector-python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: MySQL 5.7+

## License

This project is provided as-is for educational and commercial use.

## Support

For issues or questions, verify:
1. Python version is 3.7+
2. All dependencies are installed: `pip install -r requirements.txt`
3. MySQL server is running and accessible
4. Firewall isn't blocking port 8000
