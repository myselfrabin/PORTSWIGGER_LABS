
# 🛡️ XSS Analysis of JavaScript Code Using `innerHTML`

This document analyzes a real-world potential XSS vulnerability in JavaScript and provides insights from a seasoned web security expert.

---

## 📜 The Code Under Review

```js
function doSearchQuery(query) {
    document.getElementById('searchMessage').innerHTML = query;
}

var query = (new URLSearchParams(window.location.search)).get('search');
if (query) {
    doSearchQuery(query);
}
```

---

## ✅ What’s Happening?

1. **Extracts `search` from the URL:**
   ```js
   (new URLSearchParams(window.location.search)).get('search')
   ```
   Example URL:
   ```
   https://victim.com/?search=hello
   ```

2. **Passes it to `doSearchQuery`:**
   ```js
   doSearchQuery(query);
   ```

3. **Directly injects it into the page using `innerHTML`:**
   ```js
   document.getElementById('searchMessage').innerHTML = query;
   ```

---

## ❗ The Problem: `innerHTML` Injection

Using `innerHTML` with unsanitized user input is **dangerous**.

### 🔥 Exploitable Example

```html
https://victim.com/?search=<script>alert(document.cookie)</script>
```

Rendered HTML:

```html
<span id="searchMessage"><script>alert(document.cookie)</script></span>
```

💣 **This is a classic Reflected XSS vulnerability.**

---

## 🧠 Security Analysis

| Component                         | Risk Level | Explanation                                                  |
|----------------------------------|------------|--------------------------------------------------------------|
| `window.location.search`         | 🟢 Safe     | Just retrieves the query string                              |
| `URLSearchParams().get()`        | 🟢 Safe     | Parses query parameters safely                               |
| `innerHTML = query`              | 🔴 **Danger** | Injects unsanitized HTML/JavaScript directly                 |

---

## 🔐 Secure Code Recommendation

Replace:
```js
innerHTML = query;
```

With:
```js
textContent = query;
```

✅ `textContent` safely escapes any HTML or JS content.

---

## 🧪 Exploit Examples

Test these payloads in the `search` parameter:

- `<img src=x onerror=alert(1)>`
- `%3Cscript%3Ealert(document.domain)%3C/script%3E`
- `<svg/onload=alert('XSS')>`
- `"><script>alert(1)</script>`

---

## 🛠️ Pro Pentester Tips

- **Check CSP Headers:**
  Are they using `Content-Security-Policy` to block inline scripts?

- **Try HTML-Breaking Payloads:**
  ```html
  "><script>alert(1)</script>
  ```

- **Event Handler Injection:**
  ```html
  <a href="#" onclick=alert(1)>Click me</a>
  ```

- **Bypass Filters:**
  - `<scr<script>ipt>`
  - `<iframe srcdoc="<script>alert(1)</script>">`
  - Unicode/Obfuscation Tricks

---

## 🧨 Final Verdict

The following line is the **vulnerability root**:

```js
innerHTML = query;
```

If user input isn't sanitized, this leads to **Reflected XSS**.

---

## ✅ Recommendation Summary

- **Do NOT use `innerHTML` with user input.**
- Use `textContent` or properly sanitize the input.
- Test with payloads to confirm vulnerability.
- Always audit any DOM manipulation involving user-controlled data.
