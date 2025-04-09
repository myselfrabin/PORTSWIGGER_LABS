
# 🛡️ Advanced IDOR (Insecure Direct Object Reference) Guide for 2025

## 🔥 What is IDOR?
**IDOR** happens when a web app exposes internal object references (like user IDs or file names) and doesn't properly check if the user is authorized to access them.

**Example:**
```http
GET /api/user/12345/profile
```
If changing `12345` to `12346` reveals another user's data — that's IDOR.

## 🧠 LIFETIME UNDERSTANDABLE DEFINITION
> **IDOR is when the application lets you *reach what you're not supposed to*, just by *guessing or modifying a parameter*, without proper authorization checks.**

---

## 💡 Advanced IDOR in Modern (2025) Apps

Modern web apps use:
- Frontend frameworks (React, Vue)
- API-first backends (REST, GraphQL)
- Role-based access control (RBAC, ABAC)
- Microservices, JWTs, OAuth

Even with these, devs often miss proper **authorization checks**.

---

## 🎯 IDOR Hunting Strategy

### 1. Map User Roles
- Create multiple accounts (User, Admin, Vendor)
- Note differences in data visibility and actions

### 2. Understand API Behavior
- Use **Burp Suite** or **Mitmproxy**
- Capture all endpoints and track object references like:
  - `/api/user/ID`
  - `/api/order/ID`
  - `/download?file_id=XYZ`

### 3. Perform IDOR Tests
Try changing:
- IDs: `123 → 124`
- UUIDs: `f8b6e712-xxxx → f8b6e713-xxxx`
- Base64 values (decode, modify, re-encode)
- Timestamps or file names

Test with:
- Different roles
- Logged out sessions
- Lower privilege users

### 4. Look for Broken Logic
- Can user A delete B’s resource?
- Can a user download another's invoice?
- Can you modify or POST for other users?

### 5. Combine with Other Bugs
- IDOR + Broken Access Control = 🔥
- IDOR + Rate Limit Bypass = 💣
- IDOR + Race Condition = 🧨

---

## 🧪 Real-World IDOR Examples

### 🧾 Invoice Download
```http
GET /api/invoices/984584?user_id=1234
```

### 📁 File Access
```http
GET /api/files/download?file=profile.jpg
```

### 📦 Order Manipulation
```json
{
  "order_id": "55555",
  "user_id": "7"
}
```

### 🧑‍🤝‍🧑 Workspace Switching
```http
POST /api/change-team
{
  "team_id": "8"
}
```

---

## 🧠 Pro Tips

1. **Think like a developer** — Assume what checks they may forget.
2. **Don’t trust read-only actions** — Try write/delete.
3. **Check relationships** — Can a user affect others' data?
4. **Watch for UUIDs or encoded data** — Still test them!
5. **Mass Assignment + IDOR = 🚨**

---

## 🧰 Tools

- **Burp Suite** (+ Autorize Plugin)
- **AuthMatrix**
- **JWT.io**
- **ParamMiner**

---

## 🎓 Homework

1. Pick 2 bug bounty programs.
2. Create multiple accounts.
3. Map user roles.
4. Find and test object references.
5. Document logic flaws and report only valid bugs.

---

## 🔐 Why It Matters

- **OWASP Top 10** (Broken Access Control)
- Common in **APIs, microservices, mobile apps**
- Easy to find, high impact
- Protects privacy & sensitive data

---

## 🧭 Final Mentor Words

To master IDOR, you need:
- Patience
- Curiosity
- Persistence

Every app is different. Somewhere, someone forgot an auth check — **go find it**. 🥷💥
