
# 🧠 Understanding jQuery Hashchange Scroll Code (For Bug Bounty Hunters)

## 📜 Original Code:
```javascript
<script>
  $(window).on('hashchange', function() {
    var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
    if (post) post.get(0).scrollIntoView();
  });
</script>
```

---

## 💡 What Does This Code Do?

This code listens for any **URL hash change**, like:
```
https://example.com#SomeBlogTitle
```

Then it tries to **find a `<h2>` element** inside `<section class="blog-list">` that contains the text `SomeBlogTitle`. If it finds it, it **scrolls to that heading**.

---

## 🔍 Step-by-Step Explanation:

1. `$(window).on('hashchange', function() {...})`  
   - Listens for hash changes in the URL.

2. `window.location.hash.slice(1)`  
   - Gets the part after `#`.

3. `decodeURIComponent(...)`  
   - Decodes any URL-encoded characters.

4. `$('section.blog-list h2:contains(...)')`  
   - Finds the matching `<h2>` in `.blog-list`.

5. `.scrollIntoView()`  
   - Scrolls the view to that element.

---

## 🚨 SECURITY THREATS — What Hackers Often Miss

### ⚠️ DOM-Based XSS (Client-Side)

This code uses user-controlled input (`window.location.hash`) directly in a jQuery selector:

```javascript
$('section.blog-list h2:contains(' + userInput + ')');
```

#### 💥 Exploitable Example:
```url
https://example.com#</h2><img/src=x onerror=alert(1)>
```

This can lead to DOM-based XSS if not handled properly.

---

## 🧪 Payloads to Test (Even in Hash Context):
```
<script>alert(1)</script>
"><img src=x onerror=alert(1)>
#<svg/onload=alert(1)>
```

---

## 🛡️ Safe Version (Fixing the Code)

```javascript
$(window).on('hashchange', function() {
  const safeText = decodeURIComponent(window.location.hash.slice(1)).replace(/[^\w\s\-]/g, '');
  const post = $('section.blog-list h2').filter(function() {
    return $(this).text().trim() === safeText;
  });
  if (post.length) post.get(0).scrollIntoView();
});
```

✅ This version:
- Cleans up input
- Doesn’t inject into a jQuery selector directly

---

## 🧠 HACKER’S CHECKLIST (Don’t Skip These!)

| 🔎 Test Area | Why It's Powerful |
|-------------|-------------------|
| `window.location.hash` | Often unsafely used |
| jQuery `:contains(...)` | Can be injectable |
| `.html()` / `.append()` usage | Risky with untrusted input |
| Hash-based payloads | Great for DOM XSS |
| Prototype pollution (`#constructor=alert(1)`) | Rare but real |

---

## 🔥 Bonus Hacker Tip

Some JavaScript-heavy apps use hashes in dynamic behavior or merge them with objects. Always test:
```
https://victim.com#constructor=alert(1)
https://victim.com#toString=alert(1)
```

---

## 🧠 Final Wisdom

> _"Every time you see user input used in a selector, URL, or inner HTML — ask yourself: What if I could control this completely?"_

This is where DOM bugs hide — and where elite hackers shine.

---

Happy hunting, legend 🏹💻

### HELLO