import requests
import urllib3
import json
import sys

# disable the ssl waringngs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set the burp proxy
proxies={
    
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
    
}


if __name__=="__main__":
    # giving the user the right command
    if len(sys.argv)!=3:
        print("[+] Usage: %s <url> <command>" % sys.argv[0])