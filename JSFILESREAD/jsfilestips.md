
# 🛡️ JavaScript File Analysis for Bug Bounty (2025 Edition)

## 📜 Why Analyze JavaScript Files?

JavaScript files often contain:
- Hidden **API endpoints**
- Internal **admin paths**
- **Auth tokens** or secrets
- Debugging messages
- **URLs to internal services**
- Parameters that lead to **IDORs**, **RCE**, or **SSRF**

## ⚙️ Step 1: Where to Get JS Files

### 🔎 Manually:
1. Open browser dev tools → Network tab → Reload the page → Filter by “JS”
2. Right click → "Open in new tab"
3. Save the content / copy URL

### 🛠️ Automated Tools:
- `getJS`
- `katana`
- `subjs`

Example:
```bash
getJS -u https://target.com
```

## 👁️ Step 2: Manual JavaScript Analysis

### 🔥 What to Look for:

#### 1. XHR / fetch / axios calls
```javascript
fetch('/api/user?id=123', {
  method: 'GET',
  headers: { Authorization: 'Bearer ' + token }
});
```

#### 2. Regexes
```javascript
var emailRegex = /^[\w.-]+@target\.com$/
```

#### 3. Hardcoded keys / tokens
```javascript
const API_KEY = "sk_live_abc123"
```

#### 4. Internal Paths
```javascript
const adminPanel = "/admin/dashboard"
```

#### 5. Commented-Out Code
```javascript
// TODO: Enable this for admin login
// fetch('/admin/login') 
```

#### 6. Function Names
`getSecret()`, `resetPassword()`, `deleteUser()`, etc.

## ✂️ Deobfuscation Tips

### 🧹 Unminify:
- [https://beautifier.io/](https://beautifier.io/)
- VS Code + Prettier
- CLI:
```bash
js-beautify app.min.js -o clean.js
```

### 🔍 Rename Variables
Use Find + Replace to rename `_0x1a2b3` into meaningful names.

## 🤖 Automation Tools

| Tool | Description |
|------|-------------|
| LinkFinder | Finds URLs/endpoints in JS |
| JSParser | Legacy tool |
| SecretFinder | Finds secrets/tokens |
| gf patterns | Extracts sensitive patterns |
| DevTools Search | Cmd+F `token`, `api`, etc. |

Example:
```bash
python3 linkfinder.py -i app.js -o cli
```

## 🧠 Pro Tips

### Search Like a Pro:
Search these keywords:
```
token, apikey, Authorization, fetch, axios, base64, admin, secret, jwt
```

### Check for Encoded Secrets
```bash
echo 'YXBpX2tleT0xMjM0NQ==' | base64 -d
```

### Trace Function Execution
Simulate in browser console using `console.log()`.

## 📦 Common Sensitive Endpoints

| Path | Vulnerability |
|------|---------------|
| /api/deleteUser | IDOR |
| /admin/login | Admin access |
| /resetPassword?token= | Token leak |
| /getUserDetails?id= | IDOR |
| s3.amazonaws.com | Open S3 Bucket |

## 🧪 Practice Labs

- PentesterLab
- PortSwigger Labs
- Juice Shop (OWASP)

### Real Targets:
```bash
waybackurls target.com | grep '\.js'
```
```bash
cat jslist.txt | while read url; do curl -s $url | tee -a all-js.txt; done
```

## 🧠 Mindset

> “Don’t just read the code. Read the *intent* of the developer.”

## 🧙 Final Words

> **"JavaScript files are like a developer’s diary. You’re not just reading code—you’re reading secrets they hoped no one would notice."**