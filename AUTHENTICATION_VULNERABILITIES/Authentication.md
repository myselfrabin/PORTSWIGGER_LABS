# Authentication vs. Authorization

## Overview
**Authentication** and **authorization** are two crucial concepts in cybersecurity, often used interchangeably but serving distinct purposes.

---

## Key Differences
| Aspect               | Authentication                                              | Authorization                                               |
|---------------------|--------------------------------------------------------------|-------------------------------------------------------------|
| **Definition**       | Verifying a user's identity.                                | Determining what actions a user is allowed to perform.      |
| **Question Answered**| "Who are you?"                                              | "What are you allowed to do?"                              |
| **Process**          | Requires credentials (e.g., password, biometrics).          | Based on roles, policies, or rules.                         |
| **Timing**           | Happens before authorization.                               | Happens after authentication.                               |
| **Examples**         | Logging in with a username and password.                    | Accessing admin-only features after login.                  |

---

## Example Scenario
| Step                        | Authentication                                             | Authorization                                                |
|----------------------------|------------------------------------------------------------|--------------------------------------------------------------|
| **Scenario**                | Carlos123 attempts to log into a website.                  | Carlos123 tries to access admin-only features.               |
| **Verification**            | Carlos123 provides a password or biometric.                | System checks if Carlos123 has admin privileges.             |
| **Outcome (Success)**       | Carlos123 is verified as the account holder.               | Carlos123 gains access to admin panel (if authorized).       |
| **Outcome (Failure)**       | Login is denied if credentials are incorrect.              | Access is denied if Carlos123 lacks admin permissions.       |
| **Actions Allowed/Denied**  | Carlos123 can log in and view personal profile.            | Carlos123 cannot delete other user accounts.                 |

---

## Visual Representation





---

## Why It Matters
- **Authentication** protects against unauthorized access by verifying identity.
- **Authorization** limits the scope of what authenticated users can do, adding layers of security.

Understanding and correctly implementing both ensures robust system security and protects sensitive data.

## HOW IT ARISES
  Most vulnerability in authentication mechanism occur in two of ways.
  - The authentication mechanism are of weak because they failed to protect agains bruteforce attack.
  - By logic flaw or poor coding mistake by the developer.

## What is the impact of vulnerable authentication?
- Lots of impact xa hai ta heram aba.
- Kunai euta attacker lay broken authentication bata aru kasaiko account ma login garna sakcha by doing bruteforcing, the attacker has access to all the data of comramized account.
- Also by accessing control of low-priveledge account kai sansitive na vaye pani some hidden page will be there, attacker can have those hidden page.

## Username enumeration
While doing the username enumeration we should have a closed look at this things.
- Status code: Suppose while trying everusername it's giving me 200 code but for the one username it's giving me another status code that means the username we guess might be correct. It is best practice for websites to always return the same status code regardless of the outcome, but this practice is not always followed.
- Error message: Look closly in the error message there you can get a hint, small typing mistake by developer can lead us into the account takeover.
- Response times: Let's suppose many wrong username and password where handing with the same response time but one username and password handling with the different response time then we should get the hint from there as well. For example: A website only check for the password filed if the username is valid, this extra step may increase in the response time. This may subtle but as a hacker we can put the more long password to delay the response time more.

# Flawed brute-force protection
It is highly likely that a brute-force attack will involve many failed guesses before the attacker successfully compromises an account. Logically, brute-force protection revolves around trying to make it as tricky as possible to automate the process and slow down the rate at which an attacker can attempt logins. The two most common ways of preventing brute-force attacks are:
- Locking the account that the remote user is trying to access if they make too many failed login attempts
- Blocking the remote user's IP address if they make too many login attempts in quick succession.
Both approaches offer varying degrees of protection, but neither is invulnerable, especially if implemented using flawed logic.

For example, you might sometimes find that your IP is blocked if you fail to log in too many times. In some implementations, the counter for the number of failed attempts resets if the IP owner logs in successfully. This means an attacker would simply have to log in to their own account every few attempts to prevent this limit from ever being reached.

In this case, merely including your own login credentials at regular intervals throughout the wordlist is enough to render this defense virtually useless.

- The explain of all this is below:


# Flawed Brute-Force Protection Explained  

| **Explanation for a 5-Year-Old** 🧸 | **Explanation for a Cybersecurity Student** 🛡️ |  
|-------------------------------|-------------------------------------------|  
| Imagine you have a toy box with a lock. If you try the wrong key too many times, you can't open it for a while. But if you use the right key in between, the box forgets how many wrong keys you tried. | Brute-force protection often involves blocking IPs after several failed login attempts. However, if successful logins reset the failed attempt counter, attackers can bypass the block by logging into their own account periodically. |  
| So, if a naughty kid tries to open the box with wrong keys, they can stop the box from locking by using the correct key sometimes. | Attackers can automate login attempts with their credentials interspersed in the attack payload, preventing the system from triggering IP bans. This logic flaw weakens the defense mechanism. |  
| The box keeps counting from zero again, making it easy to keep trying! | This flaw essentially nullifies rate-limiting defenses by exploiting the reset logic in brute-force protection mechanisms. |

# USER RATE LIMITING: 
1. Another way a website try to prevent the bruteforce attack is by implementing the user-rate limiting.
2. In this case logging too many login request within the short period of time cause IP address to be blocked.
- The IP can be only unblocked in one of the following ways: 
   1. Automatically after a certain period of time
   2. Manually by admin
   3. Manually by the user after completing the CAPTCHA. 

# NOTE: 
- As the limit is based on the rate of HTTP requests sent from the user's IP address, it is sometimes also possible to bypass this defense if you can work out how to guess multiple passwords with a single request.

# HTTP basic authentication: 
1. In HTTP basic authentication the client receives the Authentication token from the server, which is made by concatenating the **username** and __password__ and encoding it in **Base64**.
2. The authentication token is stored and managed by the browser, which automically adds in to **Authorization** header of every request.
     1. **Authorization: Basic base64(username:password)**
