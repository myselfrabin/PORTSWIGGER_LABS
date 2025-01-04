print("############## The followings are the usernames###################")

for i in range(150):
    if i % 3: #if the remaider is not zero then the codintion is true
        print("carlos")
    else:
        print("wiener")
        
print("############### The followings are the passwords###################")

with open('lab_06_passwords.txt','r') as f:
    lines=f.readlines()
    
i=0
for pwd in lines:
    if i % 3:
        print(pwd.strip("\n"))
            
    else:
        print("peter")
        print(pwd.strip("\n"))
        i=i+1
    i=i+1        
            