
# ❓ User Question

**Does if the web is made on AngularJS we should try for `{{}}` always?**

---

# ✅ Answer: Lifetime-Understandable Explanation

If a website is built with **AngularJS**, trying `{{}}` (expression injection) is **definitely a smart move**, **but not always guaranteed** to work. Here's a **lifetime-understandable breakdown** 🧠✨:

---

## ✅ Why try `{{}}` first?

- AngularJS uses `{{ }}` for **data binding** — it evaluates whatever is inside and renders it.
- If user input is reflected **inside `{{ }}` without sanitization**, it can lead to **template injection** and sometimes full-blown **XSS** 💥.

---

## 🕵️‍♂️ So should we always try `{{}}`?

### 👉 Yes, **try it** when:

- You **suspect or confirm** AngularJS is being used.
- You see reflection of your input directly on the page.
- You are testing search, comments, forms, query parameters, etc.
- You can spot `ng-` attributes like `ng-app`, `ng-bind-html`, etc.

> ✅ Example quick test:
> ```
> ?q={{7*7}}
> ```

If it renders `49` — 🎯 *AngularJS template injection confirmed.*

---

### ❌ But it's not always exploitable!

Even if a site uses AngularJS:
- The input might be **escaped or sanitized**.
- It might be using **Angular 2+** (which doesn’t support `{{ }}` in the same way).
- The injection might be happening **outside Angular context**.

---

## 🔍 Pro tips for AngularJS recon:

1. **Check for AngularJS version** in browser dev tools (Sources tab or console):
   ```js
   angular.version.full
   ```

2. Look for attributes like:
   - `ng-app`
   - `ng-controller`
   - `ng-bind`, `ng-bind-html`
   - `ng-repeat`, etc.

3. Use tools like:
   - `Wappalyzer` or `BuiltWith` to confirm AngularJS is in use
   - Burp Intruder with payloads like `{{7*7}}`, `{{$eval('1+1')}}`

---

## 🧨 Final Thought:

**Yes — try `{{}}` early**, but always combine it with context checking. If you find AngularJS + unsanitized input + expression rendering, you're sitting on a potential **XSS jackpot** 🏆💰

---

💬 Want help crafting payloads for a specific case? Drop me the context and I got you 👨‍💻🔥
