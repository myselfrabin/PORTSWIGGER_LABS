
# 🕵️ JavaScript File Analysis for Bug Bounty Hunters (2025 Edition)

> A full-spectrum guide to analyzing JavaScript manually + exploiting AI-generated bugs most people miss.

---

## 🔍 Part 1: What Most Hackers Miss During Manual JS Analysis

### 🧠 1. Environment-specific Logic
```js
if (window.location.hostname.includes("staging")) {
  var apiUrl = "https://staging-api.target.com";
}
```
- Hidden staging/internal domains = gold for recon, IDOR, or logic flaws

---

### 🧱 2. Feature Flags & Role-based Logic
```js
if (user.role === 'admin') {
  showAdminDashboard();
}
```
- Force hidden features by manipulating roles or params

---

### 🔁 3. Dynamic Endpoint Construction
```js
const url = `/api/${username}/logs`
```
- Reconstruct endpoints manually; could hide sensitive access

---

### 🧬 4. Unusual Encodings or Obfuscation
```js
var endpoint = atob("L2FkbWluL2xvZ2lu");
```
- Base64/Hex encoding might hide secrets or URLs

---

### 🐞 5. Debug or Dev Console Logs
```js
console.log("API Token: ", token);
```
- Look for dev breadcrumbs leaking internals

---

### 🧪 6. Error Handlers or Catch Blocks
```js
.catch(error => {
  alert("Failed to call /api/deleteAccount: " + error);
})
```
- Find rare endpoints from error messages

---

### 🧠 7. Hidden Parameters and Feature Toggles
```js
if (params.debug === true) { showDebugInfo(); }
```
- Try ?debug=1, ?admin=true on endpoints

---

### 🧩 8. Third-party Services & Integrations
```js
const firebaseConfig = { apiKey: "AIz...." }
```
- Look for Firebase, Stripe, AWS keys

---

### 🧠 9. Abandoned Code / Legacy Functions
```js
function legacyLoginFlow() { ... }
```
- Old code = vulnerable logic

---

### 🚩 10. Hidden Event Listeners
```js
$('#hiddenDiv').on('click', unlockSecretFeature)
```
- Look for unlinked or CSS-hidden actions

---

## 🧵 BONUS: Mindmap the JS
Map functions, variables, endpoints, and listeners to visualize app logic.

---

## 🧠 Part 2: Exploiting Bugs in AI-Generated JavaScript Code

### 🔐 1. Insecure API Defaults
```js
fetch('/api/data').then(res => res.json());
```
- No auth, no headers → try unauthenticated

---

### 🍪 2. Cookie Issues
```js
document.cookie = "token=abc123";
```
- No `Secure`, `SameSite`, or `HttpOnly` → XSS/CSRF

---

### 🔑 3. Hardcoded Secrets
```js
const API_KEY = "sk_live_abc123";
```
- Found in dev/test files or demo scripts

---

### 🧍 4. No Role Checks
```js
if (isLoggedIn) { deleteAccount(); }
```
- Auth bypass / IDOR goldmine

---

### 🛡️ 5. Missing Input Validation
```js
changePassword(userInput);
```
- Try malicious inputs or bypass length checks

---

### 🔁 6. Async/Await Mistakes
```js
async function run() { const res = fetch(); const data = res.json(); }
```
- No `await` → logic errors

---

### ✅ 7. Client-side Only Validation
```js
if (password.length > 8) { ... }
```
- Bypass using Burp or custom payloads

---

### 🔓 8. JWT Role Escalation
```js
const payload = JSON.parse(atob(token.split('.')[1]));
```
- No signature check → forge JWT

---

### 💥 9. DOM XSS
```js
innerHTML = userInput;
```
- Classic reflected XSS

---

### 🧼 10. Over-trusting JSON
```js
const obj = JSON.parse(input);
```
- No try-catch → crash or pollution

---

### 🎯 Bonus: AI Rarely Sets CORS or CSP Headers
- No CSRF protection or content security policy

---

## ✅ Final TL;DR Cheatsheet

| What To Look For | Why It Matters |
|------------------|----------------|
| `+ "/" +` or template literals | Dynamic endpoint recon |
| `console.log` / `debug`        | Info leakage |
| `atob` / `split()` / `reverse` | Obfuscated URLs |
| `admin`, `debug` in logic      | Feature access |
| `innerHTML =`                  | XSS |
| JWT parsing without verify     | Role escalation |
| Dev-only toggles               | Bypass logic |
| Hardcoded `apiKey`, `secret`   | Recon jackpot |
| `.on('click', ...)`            | Hidden buttons |
| Staging URLs or configs        | Environment discovery |

---

Happy Hunting, Hacker 🧠💻🔥