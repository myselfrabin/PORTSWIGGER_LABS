
# 🔍 Reflected DOM XSS Finding Methodology (eval-based)

This methodology is based on a real-world lab scenario to help you consistently find and exploit Reflected DOM XSS vulnerabilities, especially those involving `eval()` in JavaScript.

---

## 🧠 Phase 1: Recon & Reflection Check
1. Input any string (e.g., `123456`) into any input field (like search).
2. Observe the page source and dev tools (Elements tab).
3. If the input is reflected into the DOM (e.g., inside a tag like `<h1>`), note it.

---

## 🔥 Phase 2: Find JS Files Processing the Input
4. Look for suspicious JavaScript files being loaded — example:
   ```html
   <script src="/resources/js/searchResults.js"></script>
   ```
5. Open that JavaScript file directly in browser or via Burp to analyze.

---

## ⚠️ Phase 3: Dangerous JS Function Discovery
6. Look for dangerous JavaScript functions, like:
   - `eval()`
   - `document.write()`
   - `innerHTML`
   - `setTimeout(string)`
   - `setInterval(string)`
   - `Function()`
7. In this case, you saw:
   ```js
   eval('var searchResultsObj = ' + this.responseText);
   ```

---

## 🧪 Phase 4: Understand the JSON Response Flow
8. Send a Burp request to the endpoint, e.g.:
   ```
   /search-results?search=123456
   ```
9. Observe the JSON response:
   ```json
   {"results":[],"searchTerm":"123456"}
   ```

---

## 🧨 Phase 5: Attempt to Break the JS Context
10. Try payloads to escape the JSON string and break into real JS execution:
    - Inject payloads like:
      ```
      \"
      \"}
      \"};alert(1);//
      ```

11. Watch for results like:
    ```json
    {"results":[],"searchTerm":"123456\"};alert(1);//"}
    ```

---

## ✅ Phase 6: Final Payload & Success
12. Once the JS is broken successfully, alert gets executed:
    ```
    /search-results?search=123456\"};alert(1);//
    ```

13. Confirm the popup. 🎉 You’ve exploited Reflected DOM XSS via eval()!

---

## 🛠️ Final Payload Recap
```
/search-results?search=123456\"};alert(1);//
```

---

## 🧠 Pro Tips
- If `eval()` is used with user-controlled content, it’s almost always dangerous.
- Always look at how the JSON is handled inside JavaScript.
- Don’t just look for direct reflection — trace how your input moves from server to JS.

---

Want a printable cheatsheet or a visual flowchart version? Let me know! 💡
