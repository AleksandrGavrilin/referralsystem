import requests as r

while True:
    inp = input("""Choose an action:
1: Request registration code
2: Entering the registration code
3: Entering the invite code
Step 4: View Invited Users
0: Exit
[0-4]: """)
    if inp == '1':
        phone = input("Enter a phone number: ")    
        response = r.get('http://127.0.0.1:8000/api/phone_auth', params={'phonenumber': phone})
    elif inp == "2":
        phone = input("Enter a phone number: ")
        code =  input("Enter a phone code: ")   
        response = r.get('http://127.0.0.1:8000/api/phone_code', params={'phonenumber': phone,
                                                                        'phonecode': code})
    elif inp == "3":
        phone = input("Enter a phone number: ")
        usercode =  input("Enter a user code: ")
        invitecode =  input("Enter a invite code: ")
        response = r.get('http://127.0.0.1:8000/api/invite', params={'phonenumber': phone,
                                                                     'usercode': usercode,
                                                                     'invitecode': invitecode})  
    elif inp == "4":
        phone = input("Enter a phone number: ")
        usercode =  input("Enter a user code: ")
        response = r.get('http://127.0.0.1:8000/api/getreferrals', params={'phonenumber': phone,
                                                                 'usercode': usercode})
    elif inp == "0":
        break
    else:
        print("Invalid input!")
        continue
      
    print(f"Status code: {response.status_code}")
    print(f"Text body: {response.text}")
