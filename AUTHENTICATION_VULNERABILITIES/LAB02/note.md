## 2FA simple bypass
## HERE'S THE LAB LINK, YOU CAN TRY IT BY YOURSELF TOO: [2FA SIMPLE BYPASS](https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-simple-bypass)

## TO DO: 
- There's 2FA enable in the account we have to bypass it.

## GIVEN CREDS:
```
wiener:peter    --> our credentials
carlos:montoya  --> victims credentials
```

## LET'S DO THE LAB:
- At first we will be loggin as the given user i.e `wiener:peter` and see that process what's happening with the `2fa code`
- It gives the input box to enter the 2fa code
![2fa code place](./2facodePlace.png)
- There's a email clinet too, so the 2fa code must gone to the email right?? let's see
- And yeah we get the `2fa` code in the email for the normal user, let's give it and login
![email](./email.png)

- Ok, giving `2fa` code we successfully loggedin as wiener, let's view every request in burp and trying to find a loophole.

- Ok, after viewing the burp HTTP HISTORY I noticed one pattern i.e after POST login it's giving me another endpoint i.e login2 which gives 2fa input field as response and when we enter the 2fa code it have POST /login2 endpoint and after that it successfully loggedin to account as endpoint : `/my-account?id=wiener`
- Now what I thought here is: the code is of only 4 digit we can bruteforce it right? If the application doesnot prevent bruteforce mechanism.
- And another thought is: what if we skip the endpoint `/login2` after `/login` we go direct to `my-account?id=carlos` can we do this?? let's try
- Loggin with the victim account:
![victim account](./loginwithvictimAcc.png)
- Listening the proxy intercept while logging, we forward the `/login` endpoint but as soon as it reaches `/login2` we going to drop it and give the endpoint `/my-account`
![drop login2](./droplogin2.png)
- Ok after dropping that request we  go to the endpoint `/my-account` and we successfully logged in as carlos.
![logged in as carlos](./loggedinasCarlos.png)
- Here we successfully bypass the 2fa the application is weak on checking the 2fa code.

## Root Cause
The server grants a fully  right after the password check, before 2FA is completed. The /login2 step is enforced only by a redirect, with no server-side check ensuring 2FA was actually verified before granting access to protected page.

## Remediation
- All protected endpoints should verify server-side that 2FA is complete before serving content.
- Navigating directly to /my-account without completing 2FA should redirect back to /login2 or /login.

