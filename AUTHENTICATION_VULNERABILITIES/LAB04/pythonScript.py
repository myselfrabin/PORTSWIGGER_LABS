print('########The usernames are############')
for i in range(100):
    if i % 3:
        print('carlos')
    else:
        print('wiener')

print("######The passwords are#######################")
with open("passwords.txt","r") as file:
    pwd =file.readlines()
    

i=0
for passwords in pwd:
     if i % 3:
         print(passwords.strip('\n'))
     else:
         print('peter')
         print(passwords.strip('\n'))
         i=i+1
     i=i+1

