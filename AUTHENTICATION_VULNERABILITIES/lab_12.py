import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080','http':'http://127.0.0.1:8080'}

def change_carlos_pass(s,url):
    print("########We will be get success####################")
    #open the file
    
   
    
    change_passwd_url=url+"/my-account/change-password"
    data={'username':'carlos','current-password':'bruteforce it', 'new-password-1':'12345','new-password-2':'12345'}
    


def main():
    if len(sys.argv)!=2:
        print("Usage %s <url>" % sys.argv[0])
        print("Example %s www.example.com" % sys.argv[0])
    else:
        s=requests.Session()
        url=sys.argv[1]
        print("The url is: ",url)    
        change_carlos_pass(s,url)
    


if __name__ == '__main__':
    main()