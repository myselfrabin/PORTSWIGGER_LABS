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

## Usernaemane enumeration
While doing the username enumeration we should have a closed look at this things.
- Status code: Suppose while trying everusername it's giving me 200 code but for the one username it's giving me another status code that means the username we guess might be correct. It is best practice for websites to always return the same status code regardless of the outcome, but this practice is not always followed.
- Error message: Look closly in the error message there you can get a hint, small typing mistake by developer can lead us into the account takeover.
- Response times: Let's suppose many wrong username and password where handing with the same response time but one username and password handling with the different response time then we should get the hint from there as well. For example: A website only check for the password filed if the username is valid, this extra step may increase in the response time. This may subtle but as a hacker we can put the more long password to delay the response time more.

