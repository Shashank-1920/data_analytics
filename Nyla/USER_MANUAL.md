# Data Analytics Application — User Manual

## Introduction

This document provides professional, task-oriented instructions for installing, configuring, and operating the Data Analytics Application. The application connects to a MySQL database and delivers customer-focused analytics, including order frequency forecasting, recency measurement, churn risk assessment, and customer segmentation.

Contents:
- Quick Start
- Requirements
- Installation
- Operation (4-step workflow)
- Analysis descriptions
- Common use cases
- Troubleshooting

---

## Quick Start

1. Install Python dependencies:
```bash
pip install mysql-connector-python pandas
```
2. Start the backend service:
```bash
python backend/app.py
```
3. Open the application in a browser at:
```text
http://localhost:8000
```

Refer to the Operation section for detailed usage instructions.

---

## System Requirements

- Python 3.7 or later
- MySQL server accessible from the host running the application
- A modern web browser (Chrome, Edge, Firefox, Safari)
- Network access to the MySQL host (if remote)

---

## Installation

1. Extract the application files to a working directory.
2. Open a terminal (Command Prompt or PowerShell on Windows).
3. Change to the application directory:
```bash
cd [your-application-folder-path]
```
4. Install required packages:
```bash
pip install mysql-connector-python pandas
```

---

## Operation — 4-Step Workflow

Step 1 — Connect to MySQL
- Provide Host, Username, Password, and Database name.
- Click Connect and confirm a successful connection before proceeding.

Step 2 — Select Table
- Choose the table containing customer transaction history.
- The application attempts to auto-detect: a customer identifier column, a date column, and an optional customer name column. If auto-detection fails, select a table that includes these fields.

Step 3 — Select Analysis Type
- Available analyses: Order Frequency, Recency, Churn Risk, Customer Segmentation.

Step 4 — View and Filter Results
- Results are presented in a table with the following columns: Customer Name, Customer ID, Last Order Date, and the analysis-specific metric.
- Use the search box and filters to narrow results.

---

## Analysis Descriptions

Order Frequency Analysis
- Purpose: Estimate each customer's likely next order date based on historical purchase intervals.
- Columns: Customer Name | Customer ID | Last Order Date | Predicted Next Order

Recency Analysis
- Purpose: Measure the number of days since each customer's most recent transaction.
- Columns: Customer Name | Customer ID | Last Order Date | Days Since Last Order

Churn Risk Analysis
- Purpose: Identify customers exhibiting patterns indicative of potential churn.
- Columns: Customer Name | Customer ID | Last Order Date | Churn Risk Status

Customer Segmentation
- Purpose: Classify customers into segments (e.g., Loyal, At Risk, Lost, New, High Value, One-time Buyers) for targeted actions.
- Columns: Customer Name | Customer ID | Last Order Date | Segment

---

## Common Use Cases

- Customer retention: Use Churn Risk to prioritize outreach.
- Inventory planning: Use Order Frequency to anticipate demand peaks.
- Marketing segmentation: Use Customer Segmentation to tailor offers.
- Customer lifecycle monitoring: Use Recency to identify inactive customers.

---

## Tips for Best Results

- Ensure the selected table contains accurate transactional dates and a stable customer identifier.
- For large tables (100,000+ rows), initial analysis may require additional processing time.
- Use the search and filter functions to work with manageable subsets of results.
- Re-run analyses on a regular cadence to monitor trends.

---

## Troubleshooting

Problem: The application will not start
- Verify Python 3.7+ is installed and available on the PATH:
```bash
python --version
```
- Install required packages:
```bash
pip install mysql-connector-python pandas
```
- Start the application and review any error messages printed to the terminal.

Problem: Database connection fails
- Confirm the MySQL server is running and reachable from the host executing the application.
- Verify Host, Username, Password, and Database values.
- If the server is remote, ensure network and firewall rules permit access to the MySQL port (default 3306).

Problem: ModuleNotFoundError for mysql or pandas
- Install missing dependencies using pip as shown above.

---

## Operational Notes

- The application runs locally by default on port 8000. Modify the backend code if a different port is required.
- For production deployment, host the backend behind a process manager and configure secure access to the MySQL server.

---

## Support and Contributions

For issues, improvements, or contributions, create an issue or pull request in the project's Git repository. Include details on the environment, steps to reproduce, and any relevant logs.

---

End of manual.
1. Type in the search field at the top of the results table
2. Search works instantly as you type
3. Searches are **case-insensitive** (uppercase and lowercase both work)
4. Leave empty to see all customers

**What it searches:**
- Customer names
- Customer IDs

**Examples:**
- Type "John" to find all customers named John
- Type "CUST123" to find that specific customer ID
- Type "acme" to find customers with "acme" in their name

#### **Filter Feature**
Use the **filter dropdown** to narrow results by category:

**Available filters depend on your analysis:**

| Analysis Type | Filter Options |
|---|---|
| Order Frequency | All Customers |
| Recency | All Customers |
| Churn Risk | All Customers, At Risk, Safe |
| Segmentation | All Customers, Loyal, At Risk, Lost, New, High Value, One-time Buyers |

**How to filter:**
1. Click the filter dropdown menu
2. Select a category
3. Results automatically update to show only matching customers
4. Select "All Customers" to remove the filter

**Combining Search + Filter:**
For powerful results, use both together:
- Example: Search for "John" AND filter to show only "At Risk" customers
- This shows only at-risk customers named John

#### **Navigation Options**
At the bottom of results:
- **Back to Analysis Selection** - Run a different analysis on the same table
- **New Analysis** - Start over with a different table or database

---

## Common Use Cases

These examples show how to accomplish specific business goals using the application.

### Scenario 1: Finding Inactive Customers for Re-engagement Campaign
**Goal:** Identify customers who haven't ordered in a long time

**Steps:**
1. Start the application and connect to your database
2. Select the table containing your customer orders
3. Choose **Recency Analysis**
4. Look at the "Days Since Last Order" column
5. Sort mentally or search for customers with high day counts
6. Export this list for your marketing team to create a "We miss you!" campaign

**What you'll find:** Customers ranked by inactivity - helps you prioritize who to reach out to

---

### Scenario 2: Preventing Customer Loss
**Goal:** Identify which customers are most likely to stop buying

**Steps:**
1. Connect to your database with your order history
2. Select the appropriate transactions table
3. Choose **Churn Risk Analysis**
4. Use the filter dropdown to show only **At Risk** customers
5. Review the list of customers showing churn warning signs
6. Create a retention plan (discounts, outreach, special offers)

**What you'll find:** Customers labeled as "At Risk" - focus your retention efforts here

---

### Scenario 3: Targeting Premium Customers
**Goal:** Create a special VIP program for high-value customers

**Steps:**
1. Connect and select your customer table
2. Choose **Customer Segmentation**
3. Use the filter dropdown to show only **High Value** customers
4. Copy this list for your VIP program enrollment
5. Use these customers for exclusive offers or loyalty rewards

**What you'll find:** Your most valuable customers by spending and activity patterns

---

### Scenario 4: Planning Inventory Based on Demand Patterns
**Goal:** Know when to stock items based on customer ordering patterns

**Steps:**
1. Connect and select your order history table
2. Choose **Order Frequency Analysis**
3. Review the "Predicted Next Order" column
4. Look for clusters of dates where many customers are predicted to order
5. Increase inventory before those dates
6. Plan promotions and shipping capacity accordingly

**What you'll find:** Forecast of when customers will likely place their next orders

---

### Scenario 5: Understanding Your Customer Mix
**Goal:** Get a complete picture of who your customers are

**Steps:**
1. Connect and run **Customer Segmentation** on your customer table
2. View the distribution across segments:
   - How many Loyal customers do you have?
   - How many are At Risk?
   - Who are your High Value customers?
3. Use this to inform business strategy and resource allocation

**What you'll find:** Breakdown of customer composition - shows where to focus efforts

---

## Tips for Best Results

### ✅ Before You Start
- Have your MySQL credentials ready (host, username, password, database name)
- Make sure you know which table contains your customer transaction data
- If unsure, ask your database administrator or IT support

### ✅ During Analysis
- Run multiple analyses on the same table to get different perspectives
- Use search to find specific customers you're interested in
- Combine search and filters for precise result sets
- Take screenshots of important findings

### ✅ After Analysis
- Share results with your team
- Use segmentation insights to inform business decisions
- Re-run analyses periodically (weekly, monthly) to track changes
- Monitor how your customer composition changes over time

### ⚡ Performance Notes
- Initial analysis on large tables (100,000+ records) may take 10-30 seconds - this is normal
- Once loaded, search and filtering are instant
- If results are very large, use search/filter to work with smaller subsets

---

## Troubleshooting

### I Can't Start the Application

**Error:** "python: command not found" or "Python is not recognized"
- **Fix:** Python is not installed or not in your system PATH
- **Solution:** 
  1. Install Python from [python.org](https://www.python.org)
  2. During installation, check "Add Python to PATH"
  3. Restart Command Prompt/PowerShell
  4. Try again

**Error:** "ModuleNotFoundError: No module named 'mysql'"
- **Fix:** Dependencies not installed
- **Solution:**
  1. Run: `pip install mysql-connector-python pandas`
  2. Wait for installation to complete
  3. Start the application again

---

### I Can't Connect to the Database

**Error:** "Connection refused" or "Connection failed"
- **Causes:** 
  - MySQL server is not running
  - Wrong hostname/IP address
  - Wrong username or password
  - Database doesn't exist
- **Fix:**
  1. Verify MySQL is running on your system
  2. Double-check all credentials:
     - Host (try `localhost` first)
     - Username (case-sensitive)
     - Password (case-sensitive)
     - Database name (case-sensitive)
  3. Ask your database administrator if unsure

**Error:** "Access denied for user"
- **Fix:** Incorrect username or password
- **Solution:** Verify credentials, or contact your database administrator

**Error:** "Unknown database"
- **Fix:** Database name is incorrect or doesn't exist
- **Solution:** Ask your database administrator for the correct database name

---

### No Tables or Data Appears

**Problem:** After connecting, Step 2 shows no tables
- **Cause:** Your user account doesn't have permission to see tables
- **Fix:** Contact your database administrator to grant table access

**Problem:** Tables appear but no data in results
- **Cause:** 
  - Table structure doesn't match requirements (missing date or customer ID column)
  - No data in the selected table
  - Wrong table selected
- **Fix:**
  1. Go back to Step 2
  2. Try selecting a different table
  3. Verify the table has customer IDs and dates

---

### Filters Don't Work or Results Look Wrong

**Problem:** Search returns no results
- **Fix:** 
  - Check spelling (search is case-insensitive, but spelling matters)
  - Try a shorter search term
  - Clear the search box and try again

**Problem:** Filter dropdown shows no useful options
- **Fix:** This is normal - some analyses only have "All Customers" option
  - Only Churn Risk and Segmentation have additional filter options

**Problem:** Results seem incorrect or unexpected
- **Fix:**
  1. Re-run the analysis
  2. Try a different analysis type
  3. Verify your data in the source database

---

### Application is Running Slowly

**Problem:** Results take a long time to load
- **Normal behavior:** First-time analysis on large datasets (10,000+ records) can take 10-30 seconds
- **Fix:** This is expected. Wait for results to fully load.

**Problem:** Search/filters are slow
- **Fix:** Unlikely, but try:
  1. Refresh the page (F5)
  2. Clear all filters
  3. Try with fewer results

---

### Browser Won't Connect to Application

**Error:** "Cannot reach localhost:8000" or "This site can't be reached"
- **Cause:** Application server isn't running
- **Fix:**
  1. Check your Command Prompt/PowerShell window
  2. Verify you see a message saying the server is running
  3. If not, start the server again: `python backend/app.py`

**Error:** "Connection refused"
- **Fix:**
  1. Verify you started the application in the correct folder
  2. Verify port 8000 is available (nothing else using it)
  3. Try restarting the application

---

## Getting Help

If you encounter an issue not covered here:

1. **Check your credentials** - Most issues are incorrect username/password
2. **Verify MySQL is running** - Database server must be accessible
3. **Contact your IT support** - For database access questions
4. **Restart the application** - Close and restart often fixes temporary issues
5. **Try a different browser** - Clear browser cache and try Chrome, Firefox, or Safari

---

## Advanced Information

### Supported MySQL Versions
- MySQL 5.7 and higher
- MariaDB 10.3 and higher
- Any MySQL-compatible database

### Supported Data Types
- **Date columns:** DATE, DATETIME, TIMESTAMP, or similar
- **ID columns:** INT, BIGINT, VARCHAR, UUID, or any unique identifier
- **Name columns:** VARCHAR, TEXT, CHAR, or text-based fields

### How Calculations Work

**Recency:** 
- Calculated as: Today's date minus the customer's most recent order date
- Result shown in days

**Churn Risk:**
- Based on: How long since last order + how often they normally order
- Shows "At Risk" if activity pattern matches churn indicators

**Customer Segments:**
- Loyal: Regular customer with recent activity
- At Risk: Previously active but activity declining
- Lost: No activity for extended period
- New: Very recent customer, few orders
- High Value: Top percentage by spending/activity
- One-time: Only one order ever placed

**Predicted Next Order:**
- Based on historical ordering patterns and average order gaps
- Used to forecast inventory and marketing needs
