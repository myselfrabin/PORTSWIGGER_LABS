import requests
import urllib3
import jwt
import sys
from bs4 import BeautifulSoup
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# setting up the proxy

proxies = {'http':'http://127.0.0.1:8080',
           'https':'http://127.0.0.1:8080'
            }

def get_csrf(url,s):
    print(url)
    request = s.get(url,verify=False,proxies=proxies)
    soup=BeautifulSoup(request.text,'html.parser')
    csrf=soup.find("input",{'name':'csrf'})['value']
    return csrf


def default_login(url,s,username,password):
    print(username)
    # what I need to do here is: 
    # WE HAVE TO GET AN CSRF TOKEN HAI
    login_url=url+'/login'
    csrf_token=get_csrf(login_url,s)
    print(csrf_token) 
    data={'csrf':csrf_token,'username':username,'password':password}
    request = s.post(login_url,data=data,verify=False,proxies=proxies,allow_redirects=False)
    res=request.text
    
    if res.status_code==302:
        print("SUccessfully loggedin")
        jwt = s.cookies['session']
        print(jwt)
    


def main():
    # give user a instruction
    if len(sys.argv)!=2:
        print("[+] Usage is %s <url>" % sys.argv[0])
        print("[+] Example is %s <www.example.com>" % sys.argv[0])
    else:
        url = sys.argv[1]
        s=requests.Session()
        username="wiener"
        password="peter"
        default_login(url,s,username,password)



if __name__=="__main__":
    main()