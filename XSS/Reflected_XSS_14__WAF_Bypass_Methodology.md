# Reflected XSS into HTML Context with Most Tags and Attributes Blocked – Methodology

## Objective:
Exploit a reflected XSS vulnerability bypassing WAF to successfully execute the `print()` function.

---

## Step-by-Step Methodology

### 1. Initial Input Reflection Check
- Input a random string such as `123456` into the search field.
- Confirm it's reflected back into the page (HTML context).

### 2. Test Common XSS Payloads
- Try standard payloads like `<script>alert(1)</script>`.
- Confirm if tags are being blocked by the WAF (likely returns a 403 or 400 error).

### 3. Tag Enumeration (Brute-force)
- Use Burp Suite Intruder to fuzz different HTML tags based on PortSwigger's XSS cheatsheet.
  - Payload format: `<$TAG$>`.
- Observe which tags do **not** trigger the WAF.
- Common outcome: Most tags blocked, but some like `<body>` or `<custom>` may be allowed.

### 4. Event Handler Discovery
- Use Burp Intruder again to fuzz for working JavaScript event handlers.
  - Example format: `<body $EVENT$=1>`.
- From response codes and reflection behavior, identify accepted handlers (e.g. `onresize`).

### 5. Final Payload Crafting
- Combine valid tag and valid event handler:
  ```html
  <body onresize=print()>
  ```
- Resize the page manually or automate it to trigger the `print()` function.

### 6. Automation using Iframes (Bonus)
- To make it auto-trigger, use an iframe that causes the parent page to resize:
  ```html
  <iframe src="/?search=<body onresize=print()>" onload="this.style.width='100px'"></iframe>
  ```

---

## Pro Tips (From 10+ Years Web Hacking Experience)

- 🔍 **Always fuzz WAF-filtered endpoints** using Burp Intruder and a good tag/event handler list.
- 🧠 **Think creatively** – if script tags are blocked, use event-driven tags (`<body>`, `<iframe>`, etc).
- 📜 **Use indirect execution methods** like resizing, auto-focusing inputs, or CSS-based triggers.
- ⚙️ **Don't ignore reflection quirks** – sometimes just `"`, `>` or broken tag contexts can open the door.
- 🛠️ **Tools to Use**:
  - Burp Intruder (tag/event bruteforce)
  - PortSwigger Cheatsheets (for tags and event handlers)
  - DevTools to inspect reflection and behavior

---

## Conclusion
Always test **both** tags and event handlers when facing WAFs. Some unusual vectors may still bypass them if carefully crafted. Automating execution using iframes or passive behaviors can help trigger functions without user interaction.

**Happy Hacking, Rabin!** 🚀