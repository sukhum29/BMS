import mysql.connector
import random
import datetime
import smtplib
from email.mime.text import MIMEText as text

conn = mysql.connector.connect(host = 'localhost', user = 'root', password = 'sukhum29',auth_plugin='mysql_native_password')
mycur = conn.cursor(buffered = True)


mycur.execute("USE project;")
columns_list = ["accID","name","username","password","balance","gender","email"]

def createAccount(list1):
    command = f"INSERT into accounts values({list1[0]},'{list1[1]}','{list1[2]}','{list1[3]}',{list1[4]},'{list1[5]}','{list1[6]}');"
    mycur.execute(command)
    conn.commit()
    print("Account has been created!")
    print("your account details are: ")
    mycur.execute(f"select * from accounts where username = '{list1[2]}';")
    for i in mycur:
        print(i)

def login():
    while True:
        global username
        global pw
        username = input("Enter your username: ")
        
        pw = input("enter your password: ")
        
        mycur.execute(f"select * from accounts where username = '{username}' and password = '{pw}';")
        records = mycur.fetchall()
        if len(records) != 0:
            rec_email=str(records[0][6])
            
            sender_email='bmanagementsys123@outlook.com'
            pas='abcd@54321'
            otp=random.randint(100000,999999)
            msg=text(str(otp))
            msg['Subject'] = 'OTP FOR LOGIN'
            msg['From'] = "bmanagementsys123@outlook.com"
            msg['To'] = str(records[0][6])

        try:
            server=smtplib.SMTP("smtp.outlook.com",587)
            server.starttls()
            server.login(sender_email,pas)
            print("LOGIN SUCCESS")
            server.sendmail(sender_email,rec_email,msg.as_string())
            print("otp has been sent to ",rec_email)
            print("email  sent")
            server.quit()
            break
        except:
            print('Something went wrong...')
            

    n=int(input("enter otp: "))
    if n==otp:
        mycur.execute(f"select * from accounts where username = '{username}' and password = '{pw}';")
        records = mycur.fetchall()
        print(records)
        
        return True
    else:
        print("Login unsuccessful!")
        print("Incorrect Username or Password")
        login()
        

def check_funds(accID,amount):
    command = f"select balance from accounts where accID = {accID};"
    mycur.execute(command)
    for i in mycur:
        balance = i[0]
    if balance < amount:
        print("Insufficient funds!")
        return False
    else:
        return True
    

def withdraw(accID,amount):
    command = f"update accounts set balance = balance - {amount} where accID = {accID};"
    mycur.execute(command)
    conn.commit()
    print("Balance updated!")
    print("New balance is: ")
    mycur.execute(f"select balance from accounts where accID = '{accID}';")
    for i in mycur:
        print(i[0])

def deposit(accID,amount):
    command = f"update accounts set balance = balance + {amount} where accID = {accID};"
    mycur.execute(command)
    conn.commit()
    print("Balance updated!")
    print("New balance is: ")
    mycur.execute(f"select balance from accounts where accID = '{accID}';")
    for i in mycur:
        print(i[0])

def emi_calc(loan_type):
    global p,n,interest
    p = int(input("Enter loan amount requested: "))
    n = int(input("Enter the loan term in years: "))
    if loan_type == 1:
        interest = 9.6
    elif loan_type == 2:
        interest = 7.5
    elif loan_type == 3:
        interest = 10.5
    r = (interest / 12) / 100
    emi = ((p*r) * (((1+r) ** (n*12)))) // (((1+r) ** (n*12)) - 1)
    return emi


while True:
    userinput = int(input("Press 1 to do online banking, 2 to create a new bank account: "))
    if userinput == 1:
        login()
        mycur.execute(f"select accID from accounts where username = '{username}';")
        accID = mycur.fetchone()[0]
        while True:
            choice = int(input("Press 1 to manage balance, 2 to transfer money, 3 for loan requests: "))
            if choice == 1:
                ch2 = input("Would you like to withdraw or deposit or exit[w/d/b]: ").lower()
                if ch2 == 'w':
                    while True:
                        amount = int(input("Please enter amount to be withdrawn: "))
                        if check_funds(accID,amount):
                            withdraw(accID,amount)
                            break
                        else:
                            continue                                          
                elif ch2 == 'd':
                    amount = input("Please enter amount to be deposited: ")
                    deposit(accID,amount)
                elif ch2 == 'b':
                    break
            elif choice == 2:
                receiver = int(input("Enter recipient's account ID: "))
                while True:
                    amount = int(input("Enter amount to be transferred: "))
                    if check_funds(accID,amount):
                        withdraw(accID,amount)
                        break
                    else:
                        continue
                    goback = int(input("Try again or go back [1/0]: "))
                    if goback == 1:
                        continue
                    elif goback == 0:
                        break
            
                
                
                receiver_update = f"update accounts set balance = balance + {amount} where accID = {receiver};"
                
                mycur.execute(receiver_update)
                conn.commit()
                print("Transfer successful")
             
                
            elif choice == 3:  
                print("What type of loan would you like to request?")
                ch = int(input("Enter 1 for home loan, 2 for educational loan, 3 for vehicle loan: "))
                if ch == 1:
                    print("The bank charges an interest rate of 9.6% on home loans")
                    emi = emi_calc(1)
                    category = "Home"
                    print("Amount to be paid per month is",emi)
                elif ch == 2:
                    print("The bank charges an interest rate of 7.5% on student loans")
                    emi = emi_calc(2)
                    category = "Student"
                    print("Amount to be paid per month is",emi)
                elif ch == 3:
                    print("The bank charges an interest rate of 10.5% on vehicle loans")
                    emi = emi_calc(3)
                    category = "Vehicle"
                    print("Amount to be paid per month is",emi)
                else:
                    print("Invalid choice")
                proceed = input("Do you wish to proceed with the loan [y/n]: ").lower()
                if proceed == 'y':         
                    loanID = random.randint(10000,99999)
                    issueDate = datetime.date.today()
                    mycur.execute("select loanID from loans;")
                    IDlist = mycur.fetchall()
                    i = 0
                    while i < len(IDlist):
                        if IDlist[i][0] == loanID:
                            loanID = random.randint(10000,99999)
                            i = 0
                        else:
                            i += 1
                    mycur.execute(f"insert into loans values({loanID},{p},'{category}',{n},{accID},{emi},'{issueDate}');")
                    conn.commit()
                    print("Loan Issued!")
                    print("Loan details are:")
                    mycur.execute(f"select * from loans where loanID = {loanID};")
                    print(mycur.fetchall())
            repeat = input("Any further changes [y/n]: ").lower()
            if repeat == 'y':
                continue
            elif repeat == 'n':
                break
    elif userinput == 2:
        list1 = [input(f"Please enter {columns_list[i]}: ") for i in range(len(columns_list))]
        createAccount(list1)
    elif userinput == 0:
        break
#print(datetime.date.today())
