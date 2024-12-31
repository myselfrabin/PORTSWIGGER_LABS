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
