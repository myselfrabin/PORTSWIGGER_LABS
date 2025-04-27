
# Why You Needed to Close `</script>` in the XSS Lab

First of all — **amazing work solving it yourself!** 🌟 That's a huge step forward because understanding *why* a payload works is exactly what will make you unstoppable in bug bounty.

---

## The Lab Response

```html
<script>
    var searchTerms = '\'\\</script><script>alert(1)</script>//';
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

When you inject **inside** JavaScript (in this case, inside `var searchTerms = 'HERE';`), you're **inside a JavaScript string**, not open executable code yet.

Meaning:

- If you just typed `alert(1)`, it would be treated as **part of the string**, not executed.
- JavaScript sees: `'your payload here'` — so anything inside `'...'` is just a value, **not code**.

---

## Why `</script>`?

To actually execute **new code**, you have to:

- **Break out of the JavaScript string first** (which you can't because quotes are escaped),
- **Or** — **escape the `<script>` context** by ending the `<script>` tag itself.

When you inject `</script>`, the browser **ends** the current `<script>` block — you jump back into HTML, and then you **start a fresh `<script>`** tag, and **now you can execute any JS you want**, like:

```html
</script><script>alert(1)</script>
```

### Browser Parsing Flow

1. See `</script>` — *close* the existing script.
2. See `<script>` — *open* a new script.
3. See `alert(1)` — *execute* the new code.
4. Done.

---

## Quick Summary 🧫

| Without `</script>`                       | With `</script>`                                   |
| ----------------------------------------- | -------------------------------------------------- |
| Your payload stuck **inside a JS string** | Your payload **breaks out and becomes executable** |
| Treated as text only                      | Treated as real JavaScript code                    |
| No alert pops up                          | Alert pops up ✅                                    |

---

## Bonus: Why Not Just Break the `'` String?

Normally you could think:

- inject `'` to close the string
- then add `; alert(1); var a = '...';`

**BUT**:

- In this case, **your single quote (`'`) is escaped** by backslash (`\'`) automatically by backend.
- Meaning you **can't** just break the string with a `'`.
- **The only way left**: use `</script>`.

---

## Super Quick Visual

**Without escaping:**

```js
var searchTerms = 'YOU';
```

Injection:

```text
'; alert(1); var x='
```

**With escaping (your case):**

```js
var searchTerms = '\'YOUR INPUT\'';
```

So you can **only close script tag** to break out.

---

## TL;DR 🎯

> **You needed to close `</script>` because your input was stuck inside a JavaScript string where single quotes were escaped by backend, and closing the script was the only way to escape into executable code.**
